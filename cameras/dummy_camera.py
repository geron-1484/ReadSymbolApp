import time
import io
from typing import Optional, Tuple
from cameras.camera_base import CameraBase
from PIL import Image, ImageDraw

class DummyCamera(CameraBase):
    def __init__(self, label: str = "DUMMY"):
        self.label = label
        self._connected = False
        self._counter = 0

    def connect(self) -> None:
        self._connected = True

    def disconnect(self) -> None:
        self._connected = False

    def capture(self) -> Optional[Tuple[bytes, str]]:
        if not self._connected:
            return None
        self._counter += 1
        img = Image.new("RGB", (640, 360), (30, 30, 30))
        d = ImageDraw.Draw(img)
        d.text((10, 10), f"{self.label} #{self._counter}", fill=(200, 200, 0))
        b = io.BytesIO()
        img.save(b, format="JPEG", quality=85)
        meta = f"dummy-{self._counter}-{int(time.time()*1000)}"
        return b.getvalue(), meta

    def is_connected(self) -> bool:
        return self._connected
