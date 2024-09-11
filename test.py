import pymel.core as pm




pm.polySphere()







# import maya.cmds as cmds
# import threading
# import os
# import time
# file_path = '/home/laio/Documents/rigTools/test.py'
# # Function to check if a file was saved in a separate thread
# def check_file_saved():
    
#     # Get the initial modification time
#     initial_mtime = os.path.getmtime(file_path)

#     while True:
#         time.sleep(1)  # Pause for one second

#         # Check if the file was saved by comparing the modification time
#         current_mtime = os.path.getmtime(file_path)

#         if initial_mtime != current_mtime:
#             with open(file_path, 'r') as script_file:
#                 script_code = script_file.read()
#                 exec(script_code, globals())
#             break

#     check_file_saved()

# # Create a new thread and start it
# thread = threading.Thread(target=check_file_saved)
# thread.start()
