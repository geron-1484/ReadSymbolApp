import logging
from multiprocessing import get_context
from typing import Dict
from models.camera_models import CameraConfig
from utils.logging_setup import setup_logging
from controller.camera_worker import worker_main

class CameraController:
    def __init__(self):
        setup_logging()
        self.log = logging.getLogger("Controller")
        self.ctx = get_context("spawn")
        self.procs: Dict[str, any] = {}
        self.cmd_qs: Dict[str, any] = {}
        self.evt_q = self.ctx.Queue()

    def add_camera(self, cfg: CameraConfig):
        if cfg.camera_id in self.procs:
            raise ValueError(f"camera_id重複: {cfg.camera_id}")
        cmd_q = self.ctx.Queue()
        p = self.ctx.Process(
            target=worker_main,
            args=(cfg, cmd_q, self.evt_q),
            name=f"Cam-{cfg.camera_id}",
            daemon=True,
        )
        p.start()
        self.procs[cfg.camera_id] = p
        self.cmd_qs[cfg.camera_id] = cmd_q
        self.log.info(f"Started worker for {cfg.camera_id}")

    def remove_camera(self, camera_id: str):
        if camera_id in self.procs:
            self.cmd_qs[camera_id].put({"type": "shutdown"})
            self.procs[camera_id].join(timeout=3)
            if self.procs[camera_id].is_alive():
                self.procs[camera_id].terminate()
            del self.procs[camera_id]
            del self.cmd_qs[camera_id]
            self.log.info(f"Stopped worker for {camera_id}")

    def send(self, camera_id: str, cmd: dict):
        if camera_id not in self.cmd_qs:
            raise ValueError(f"Unknown camera_id: {camera_id}")
        self.cmd_qs[camera_id].put(cmd)

    def poll_event(self, timeout_ms=50):
        try:
            return self.evt_q.get(timeout=timeout_ms/1000.0)
        except Exception:
            return None

    def shutdown_all(self):
        for cam_id in list(self.procs.keys()):
            self.remove_camera(cam_id)
