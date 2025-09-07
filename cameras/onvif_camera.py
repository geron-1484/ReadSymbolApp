import time
from typing import Optional, Tuple
from cameras.camera_base import CameraBase
import cv2

class OnvifRtspCamera(CameraBase):
    def __init__(self, rtsp_url: str):
        self.rtsp_url = rtsp_url
        self._connected = False
        self._cap = None

    def connect(self) -> None:
        self._cap = cv2.VideoCapture(self.rtsp_url)
        if not self._cap.isOpened():
            raise RuntimeError(f"RTSP接続に失敗: {self.rtsp_url}")
        self._connected = True

    def disconnect(self) -> None:
        if self._cap:
            self._cap.release()
        self._connected = False

    def capture(self) -> Optional[Tuple[bytes, str]]:
        if not self._connected or self._cap is None:
            return None
        ok, frame = self._cap.read()
        if not ok or frame is None:
            return None
        ok, buf = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        if not ok:
            return None
        meta = f"rtsp-{int(time.time()*1000)}"
        return buf.tobytes(), meta

    def is_connected(self) -> bool:
        return self._connected
