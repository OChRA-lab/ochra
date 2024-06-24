from ochra_lab.labBase import LabBase
from ochra_catalogue.devices.ika_plate import IKAPlate_, IKAPlate
from ochra_catalogue.devices.web_camera import WebCamera_ as webCam
from ochra_catalogue.robots.yumi import Yumi_ as Yumi
from ochra_catalogue.devices.Xcalibur import Xcalibur_ as Xcalibur
from ochra_lab.StationConnection import StationConnection


aa = LabBase()

mystation = StationConnection("10.24.58.208:8000")
myika = IKAPlate_(mystation, "amyIka", "serial", "/dev/ttyACM0")
web_cam = webCam(mystation, "amyscam", "this doesnt", "matter")
yumi = Yumi(mystation, "amyYuMi", "yup")
pump = Xcalibur(mystation, "amyPump", "serial",
                "/dev/ttyACM1", 6, 1, "2.5mL", "syringe")

aa.add_device(myika)
aa.add_device(web_cam)
aa.add_device(yumi)
aa.add_device(pump)
aa.run()
