import time
from typing import Optional, Tuple
from cameras.camera_base import CameraBase

class EosCamera(CameraBase):
    def __init__(self, serial_number: str):
        self.serial_number = serial_number
        self._connected = False
        # TODO: ここでEDSDKのロードやハンドル準備（プロセス内限定）

    def connect(self) -> None:
        # TODO: EDSDKで対象シリアルのカメラに接続
        self._connected = True

    def disconnect(self) -> None:
        # TODO: EDSDKのリソース解放
        self._connected = False

    def capture(self) -> Optional[Tuple[bytes, str]]:
        if not self._connected:
            return None
        # TODO: 実際の撮像/ライブビュー取得→JPEG化
        fake_bytes = b"\xff\xd8\xff" + b"\x00" * 100 + b"\xff\xd9"
        meta = f"eos-{self.serial_number}-{int(time.time()*1000)}"
        return fake_bytes, meta

    def is_connected(self) -> bool:
        return self._connected
