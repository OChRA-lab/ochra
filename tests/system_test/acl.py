from ochra_manager.lab.lab import lab
from ochra_manager.lab.lab_communication import LabCommunication
import uvicorn
from pathlib import Path

# start lab
myLab = LabCommunication("0.0.0.0", 8001)
if __name__ == "__main__":
    myLab.run()
    # uvicorn.run("acl:myLab.app", host="0.0.0.0", port=8001, workers=8)
