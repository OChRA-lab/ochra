from fastapi import FastAPI

from pydantic import BaseModel
import uvicorn
import rospy
from comunicator import Comunicator
from pylabware import RCTDigitalHotplate, XCalibur
import time
from handlers.ika_handler import IkaPlateHandler
from handlers.web_cam_handler import web_cam
from handlers.XCalibur import XCaliburHandler
from handlers.yumi_handler import YuMiHandler



class myStation(Comunicator):
    def __init__(self) -> None:
        super().__init__()
        self.ikaPlate = IkaPlateHandler("amyIka","serial","/dev/ttyACM0")
        self.devices.append(self.ikaPlate)
        self.webCam = web_cam("amyscam",0,"test.png")
        self.devices.append(self.webCam)
        self.pump = XCaliburHandler("amyPump","serial","/dev/ttyUSB0","2.5mL","6-port-dist-valve")
        self.devices.append(self.pump)
        self.yumi = YuMiHandler("amyYuMi")
        self.devices.append(self.yumi)


if __name__ == "__main__":   
    station = myStation()
    station.run()
