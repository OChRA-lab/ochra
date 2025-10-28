# to add the parent directory to the path so we can import devices/robots folder
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from ochra.discovery.equipment.operation import Operation
from devices.web_camera.device import WebCamera
from ochra.discovery.spaces.lab import Lab
from ochra.discovery.equipment.operation_result import OperationResult
from ochra.discovery.utils.lock import lock
from time import sleep
from uuid import UUID

# connect to lab
my_lab = Lab("0.0.0.0:8001","example_id")

# get camera station
camera_station = my_lab.get_station("camera_station")
print(f"current session id: {my_lab._lab_conn._session_id}")

# get camera
my_camera: WebCamera = camera_station.get_device("my_camera")

print(f"camera_station locked status: {camera_station.locked}")

with lock(camera_station):
    # take an image
    take_image_op: Operation = my_camera.take_image()
    print("take image operation requested")
    print(f"operation: {take_image_op}")

    # wait for the data to be uploaded
    print("waiting for the operation to be executed")
    while take_image_op.result == "":
        sleep(2)
    
    result = OperationResult(id=UUID(take_image_op.result))
    print(f"result uploaded with id: {take_image_op.result}")

    print("waiting for the result data")
    while result.result_data == None:
        sleep(2)
        
    op_result = take_image_op.get_result_object()

    print("result data received. Saving data...")

    result.save_data("new_image")

    upload_image_folder_op: Operation = my_camera.upload_image_folder()
    print("upload image folder operation requested")
    print(f"operation: {upload_image_folder_op}")

    # wait for the data to be uploaded
    print("waiting for the operation to be executed")
    while upload_image_folder_op.result == "":
        sleep(2)

    result = upload_image_folder_op.get_result_object()
    print(f"id: {upload_image_folder_op.result}")

    print("waiting for the result data")
    while result.result_data == None:
        sleep(2)

    print("result data received. Saving data...")

    # save retrieved data to disk
    result.save_data("temp")
    
    # get results data and save it to the disk
    upload_image_folder_op.get_result_data("asd123")
