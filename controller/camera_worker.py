import time
import queue
import logging
from utils.logging_setup import setup_logging
from models.camera_models import CameraConfig, CameraType
from cameras.eos_camera import EosCamera
from cameras.onvif_camera import OnvifRtspCamera
from cameras.dummy_camera import DummyCamera
import services.process_image_api as process_image_api

def create_camera(cfg: CameraConfig):
    if cfg.camera_type == CameraType.EOS:
        return EosCamera(serial_number=cfg.serial_number)
    elif cfg.camera_type == CameraType.ONVIF:
        rtsp = cfg.rtsp_url or f"rtsp://{cfg.username}:{cfg.password}@{cfg.ip_address}/"
        return OnvifRtspCamera(rtsp_url=rtsp)
    elif cfg.camera_type == CameraType.DUMMY:
        return DummyCamera(label=cfg.camera_id)
    else:
        raise ValueError(f"Unsupported camera_type: {cfg.camera_type}")

def worker_main(cfg: CameraConfig, commands_q, events_q):
    setup_logging()
    log = logging.getLogger(f"Worker[{cfg.camera_id}]")
    cam = create_camera(cfg)
    connected = False
    streaming = False
    last_capture = 0
    interval = max(30, cfg.frame_interval_ms) / 1000.0

    def emit(event: str, payload=None):
        events_q.put({"camera_id": cfg.camera_id, "event": event, "payload": payload or {}})

    emit("status", {"state": "starting"})
    try:
        while True:
            try:
                cmd = commands_q.get(timeout=0.05)
            except queue.Empty:
                cmd = None

            if cmd:
                ctype = cmd.get("type")
                if ctype == "connect":
                    try:
                        cam.connect()
                        connected = True
                        emit("status", {"state": "connected"})
                    except Exception as e:
                        emit("status", {"state": "error", "message": str(e)})
                elif ctype == "disconnect":
                    cam.disconnect()
                    connected = False
                    streaming = False
                    emit("status", {"state": "disconnected"})
                elif ctype == "capture_once":
                    if connected:
                        frame = cam.capture()
                        if frame:
                            img_bytes, meta = frame
                            result = process_image_api.process_image(img_bytes, meta)
                            emit("frame_processed", {"result": result})
                elif ctype == "start_stream":
                    streaming = True
                    emit("status", {"state": "streaming"})
                elif ctype == "stop_stream":
                    streaming = False
                    emit("status", {"state": "connected"})
                elif ctype == "shutdown":
                    break

            if streaming and connected:
                now = time.time()
                if now - last_capture >= interval:
                    last_capture = now
                    frame = cam.capture()
                    if frame:
                        img_bytes, meta = frame
                        result = process_image_api.process_image(img_bytes, meta)
                        emit("frame_processed", {"result": result})
    finally:
        try:
            cam.disconnect()
        except Exception:
            pass
        emit("status", {"state": "stopped"})
