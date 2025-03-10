from pathlib import Path
from ochra_manager.connections.db_connection import DbConnection
from ochra_manager.lab.lab_server import LabServer
import uvicorn

# clear the db if it exists
db = DbConnection()
db.db_adapter.delete_database()

MODULE_DIRECTORY = Path(__file__).resolve().parent
print(MODULE_DIRECTORY)

# construct lab server and start running
lab = LabServer("0.0.0.0", 8000, template_path=MODULE_DIRECTORY)

if __name__ == "__main__":
    uvicorn.run("zTESTz:lab.app", host="0.0.0.0", port=8000, workers=8, reload=True)
