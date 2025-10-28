from .abstract import WebCameraAbstract
from ochra.common.utils.mixins import RestProxyMixin
from ochra.common.equipment.device import HTMLForm
import logging
from pathlib import Path


logger = logging.getLogger(__name__)


class WebCamera(WebCameraAbstract, RestProxyMixin):
    def __init__(self, name, usb_port=""):
        super().__init__(
            name=name,
            usb_port=usb_port,
            module_path="devices.web_camera.device",
            collection="devices",
        )
        self._mixin_hook(self._endpoint, self.id)

    @HTMLForm(call="take_image", method="POST")
    def take_image(self) -> bool:
        logger.info(f"Taking image with {self.name}")
        image_path = Path(__file__).parent.joinpath("image.png")
        return str(image_path)

    def upload_image_folder(self) -> bool:
        logger.info(f"Uploading folder with {self.name}")
        photos_path = Path(__file__).parent.joinpath("photos")
        return str(photos_path)

    def error(self):
        raise Exception("The quick brown fox jumps over the lazy dog")
