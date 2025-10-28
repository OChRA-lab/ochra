from ochra.manager.connections.db_connection import DbConnection
from ochra.manager.lab.servers.lab_server import LabServer
import uvicorn
from pathlib import Path

# clear the db if it exists
db = DbConnection()
db.db_adapter.delete_database()

# dynamically determine the folder path relative to this script
current_dir = Path(__file__).parent
lab_folder = current_dir / "lab_folder"  # replace "lab_folder" with your actual lab folder name

# construct lab server and start running
# using 0.0.0.0 to listen on all network interfaces, i.e., all IPs
# a specific address should be used but this allows us to connect to the server
# on any network that we know its IP
lab = LabServer(host="0.0.0.0", port=8001, folderpath=str(lab_folder))

if __name__ == "__main__":
    uvicorn.run("Example_lab:lab.app", host="0.0.0.0", port=8001, workers=8)
