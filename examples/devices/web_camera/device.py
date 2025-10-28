from .abstract import WebCameraAbstract
from ochra.common.utils.mixins import RestProxyMixinReadOnly


class WebCamera(WebCameraAbstract, RestProxyMixinReadOnly):
    def __init__(self, name):
        super().__init__()
        self._mixin_hook(self._endpoint, name)

    def take_image(self) -> bool:
        return self._lab_conn.call_on_object(self._endpoint, self.id, "take_image", {})
    
    def upload_image_folder(self) -> bool:
        return self._lab_conn.call_on_object(self._endpoint, self.id, "upload_image_folder", {})
    
    def error(self):
        return self._lab_conn.call_on_object(self._endpoint, self.id, "error", {})
    