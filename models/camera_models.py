from dataclasses import dataclass
from enum import Enum

class CameraType(str, Enum):
    EOS = "EOS"
    ONVIF = "ONVIF"
    DUMMY = "DUMMY"

@dataclass
class CameraConfig:
    camera_id: str
    camera_type: CameraType
    serial_number: str = ""      # EOS向け
    ip_address: str = ""         # ONVIF向け
    username: str = ""           # ONVIF向け
    password: str = ""           # ONVIF向け
    rtsp_url: str = ""           # 直接RTSP指定
    frame_interval_ms: int = 200
