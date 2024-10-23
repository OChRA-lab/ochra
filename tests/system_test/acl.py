from ochra_manager.lab.lab_server import LabServer
import uvicorn
from pathlib import Path

# start lab
myLab = LabServer("0.0.0.0", 8001)
if __name__ == "__main__":
    # myLab.run()
    uvicorn.run("acl:myLab.app", host="0.0.0.0", port=8001, workers=8)
