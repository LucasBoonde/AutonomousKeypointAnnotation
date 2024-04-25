import bpy

# Global flag to control the execution of the handler
execute_handler = True

def UpdateFrame(scene):
    global execute_handler
    
    # Check if Blender is currently rendering
    if bpy.ops.render.render.poll() and execute_handler:
        camera = bpy.data.objects['Camera']
        object = bpy.data.objects['Component#20']
        
        cX, cY, w, h = BBoxFromCamera(camera, scene, object)
        
        frame_number = scene.frame_current
        
        image_file_name = f"{frame_number:04d}"
        
        file_path = r"C:\Users\Lucas Bonde\OneDrive - Aalborg Universitet\Skrivebord\Uni\6. Semester\Project\Keypoints\aircraft_" + image_file_name + ".txt"
        
        with open(file_path, "w") as file_object:
            file_object.write(f"{class_id} {cX} {cY} {w} {h} ")

        kpCollection = bpy.data.collections['Keypoints']
        kp_coords = Keypoints2D(camera, scene, kpCollection)
        
        with open(file_path, "a") as file_object:
            file_object.write(str(kp_coords))

# Add frame change handler
bpy.app.handlers.frame_change_post.clear()
bpy.app.handlers.frame_change_post.append(UpdateFrame)

# Function to toggle handler execution
def toggle_handler_execution():
    global execute_handler
    execute_handler = not execute_handler

# Example usage to toggle handler execution
#toggle_handler_execution()