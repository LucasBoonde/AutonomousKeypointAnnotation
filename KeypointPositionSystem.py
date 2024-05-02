import bpy, bmesh
import math
from math import pi
import numpy as np
from mathutils import Vector
import bpy_extras.object_utils
import bpy_extras



#   function should return the points as a .txt file with 3 coordinates for each point [x, y, visible(1/2)]

#Giver 8 punkter som er bounding box af aircraft. - Kan blive brugt til at regne bbox i hvert frame.  VIRKER IKKE I SCRIPT, MEN GØR I TERMINAL??
#bbox_corners = [aircraft.matrix_world @ Vector(corner) for corner in aircraft.bound_box]

#Calculate the [minX, maxX, minY, maxY] coordinates, relative to the camera.
def BBoxFromCamera(camera, scene, object):
    matrix = object.matrix_world
    
    mesh = object.data
    
    #Collumns of the world coordinates?
    col0 = matrix.col[0]
    col1 = matrix.col[1]
    col2 = matrix.col[2]
    col3 = matrix.col[3]
    
    minX = 1
    maxX = 0
    minY = 1
    maxY = 0
    
    numVerticies = len(object.data.vertices)
    
    #Calculate looks at the relative corners to the camera:
    for t in range(0, numVerticies):
        co = mesh.vertices[t].co
        pos = (col0 * co[0]) + (col1 * co[1]) + (col2 * co[2]) + col3
        pos = bpy_extras.object_utils.world_to_camera_view(scene, camera, pos)
        
        if (pos.x < minX):
            minX = pos.x     
        if (pos.y < minY):
            minY = pos.y    
        if (pos.x > maxX):
            maxX = pos.x
        if (pos.y > maxY):
            maxY = pos.y   

    #--- Changing the coordinates to COCO format (centerX, centerY, width, height) ---
    centerX, centerY = ((minX+maxX)/2, (minY+maxY)/2)
    w, h = (np.linalg.norm(maxX-minX), np.linalg.norm(maxY-minY))
    
    render = scene.render
    pCenterX = str((centerX*render.resolution_x)/render.resolution_x)
    pCenterY = str(((render.resolution_y)-centerY*render.resolution_y)/render.resolution_y)
    pW = str((w*render.resolution_x)/render.resolution_x)
    pH = str((h*render.resolution_y)/render.resolution_y)
    #print("COCO Bounding Box:  (centerX: "+pCenterX+", centerY: "+pCenterY+") - (width: "+pW+", height: "+pH+")")
    
    #render.border_min_x = minX
    #render.border_min_y = minY
    #render.border_max_x = maxX
    #render.border_max_y = maxY
    
    return pCenterX, pCenterY, pW, pH
    
    
#Function to update the BBox each frame
def UpdateFrame(scene):
    if bpy.ops.render.render.poll():
        
        camera = bpy.data.objects['Camera']
        object = bpy.data.objects['Component#20']
        
        cX, cY, w, h = BBoxFromCamera(camera, scene, object)
        
        frame_number = scene.frame_current
        
        image_file_name = f"{frame_number:04d}"
        
        file_path = r"C:\Users\Lucas Bonde\OneDrive - Aalborg Universitet\Skrivebord\Uni\6. Semester\Project\data\labels\aircraft_" + image_file_name + ".txt"
        
        with open(file_path, "w") as file_object:
            file_object.write(f"{class_id} {cX} {cY} {w} {h} ")


        bpy.app.handlers.frame_change_post.clear()
        bpy.app.handlers.frame_change_post.append(UpdateFrame)
        
        
        kpCollection = bpy.data.collections['Keypoints']
        kp_coords = Keypoints2D(camera, scene ,kpCollection)
        
        with open(file_path, "a") as file_object:
            file_object.write(str(kp_coords))
        file_object.close()
    else:
        print("Not Currently Rendering")
    

# --- Outputting Keypoint ---

#This function uses the camera that the keypoints should be projected to, the current scene, and what collection the keypoints are in. 
def Keypoints2D(camera, scene, collection):
    
    keypoints_2d = []
    
    for obj in collection.objects:
        if obj and obj.parent:
            #Getting the parent of the keypoint
            parent = obj.parent
            local_location = obj.location
            
            #Converting to world location
            world_location = parent.matrix_world @ local_location
            kp_2d = bpy_extras.object_utils.world_to_camera_view(scene, camera, world_location)
            
            render_scale = scene.render.resolution_percentage / 100
            render_size = (
                int(scene.render.resolution_x * render_scale),
                int(scene.render.resolution_y * render_scale),
            )
            
            pixel_coordinates = (
                ((kp_2d.x * render_size[0]) / render_size[0]),
                ((render_size[1] - (kp_2d.y * render_size[1])) / render_size[1]), 
            )
            
            
            #Adding the coordinates to the keypoints2d array
            keypoints_2d.append(pixel_coordinates)
            
            keypoints_2d_str = " ".join("{:.16f} {:.16f}".format(coord[0], coord[1]) for coord in keypoints_2d)
            
    return keypoints_2d_str

#Initializing
class_id = 0
#bpy.app.handlers.frame_change_post.clear()
#bpy.app.handlers.frame_change_post.append(UpdateFrame)

UpdateFrame(bpy.context.scene)

#rendered image should be exported to a folder called images, the images should be split into train, val and test images. This might be easier to split afterwards. The article below shows that process.

# https://aravinda-gn.medium.com/how-to-split-image-dataset-into-train-validation-and-test-set-5a41c48af332

# coordinates should be split the same way. 
