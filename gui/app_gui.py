import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any
from models.camera_models import CameraConfig, CameraType
from controller.camera_controller import CameraController

MAX_CAMERAS = 8

class AppGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QR Reader Multi-Camera")
        self.geometry("980x640")
        self.controller = CameraController()
        self.cameras: Dict[str, Dict[str, Any]] = {}
        self._build_ui()
        self.after(100, self._poll_events)

    def _build_ui(self):
        frm = ttk.Frame(self)
        frm.pack(fill="x", padx=8, pady=8)

        self.cam_id_var = tk.StringVar(value="Cam1")
        self.type_var = tk.StringVar(value=CameraType.DUMMY.value)
        self.serial_var = tk.StringVar()
        self.ip_var = tk.StringVar()
        self.user_var = tk.StringVar()
        self.pass_var = tk.StringVar()
        self.rtsp_var = tk.StringVar()
        self.interval_var = tk.StringVar(value="200")

        ttk.Label(frm, text="Camera ID").grid(row=0, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.cam_id_var, width=12).grid(row=0, column=1, sticky="w")

        ttk.Label(frm, text="Type").grid(row=0, column=2, sticky="w")
        ttk.Combobox(frm, textvariable=self.type_var, values=[t.value for t in CameraType], width=10, state="readonly").grid(row=0, column=3, sticky="w")

        ttk.Label(frm, text="Serial (EOS)").grid(row=1, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.serial_var, width=20).grid(row=1, column=1, sticky="w")

        ttk.Label(frm, text="IP (ONVIF)").grid(row=1, column=2, sticky="w")
        ttk.Entry(frm, textvariable=self.ip_var, width=18).grid(row=1, column=3, sticky="w")

        ttk.Label(frm, text="User").grid(row=2, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.user_var, width=16).grid(row=2, column=1, sticky="w")

        ttk.Label(frm, text="Pass").grid(row=2, column=2, sticky="w")
        ttk.Entry(frm, textvariable=self.pass_var, width=16, show="*").grid(row=2, column=3, sticky="w")

        ttk.Label(frm, text="RTSP").grid(row=3, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.rtsp_var, width=46).grid(row=3, column=1, columnspan=3, sticky="we")

        ttk.Label(frm, text="Interval(ms)").grid(row=0, column=4, sticky="w")
        ttk.Entry(frm, textvariable=self.interval_var, width=8).grid(row=0, column=5, sticky="w")

        ttk.Button(frm, text="Add Camera", command=self.on_add_camera).grid(row=0, column=6, padx=5)
        ttk.Button(frm, text="Connect", command=self.on_connect).grid(row=1, column=6, padx=5)
        ttk.Button(frm, text="Disconnect", command=self.on_disconnect).grid(row=2, column=6, padx=5)
        ttk.Button(frm, text="Capture Once", command=self.on_capture_once).grid(row=3, column=6, padx=5)
        ttk.Button(frm, text="Start Stream", command=self.on_start_stream).grid(row=4, column=6, padx=5)
        ttk.Button(frm, text="Stop Stream", command=self.on_stop_stream).grid(row=5, column=6, padx=5)
        ttk.Button(frm, text="Remove Camera", command=self.on_remove_camera).grid(row=6, column=6, padx=5)

        columns = ("camera_id", "type", "status", "last_result")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=18)
        for c in columns:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=160 if c != "last_result" else 520, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel:
            return None
        values = self.tree.item(sel[0], "values")
        return values[0] if values else None

    def on_add_camera(self):
        if len(self.cameras) >= MAX_CAMERAS:
            messagebox.showwarning("Limit", f"最大{MAX_CAMERAS}台までです。")
            return
        cam_id = self.cam_id_var.get().strip()
        if not cam_id or cam_id in self.cameras:
            messagebox.showerror("Error", "Camera IDが空、または重複しています。")
            return
        cam_type = CameraType(self.type_var.get())
        try:
            interval = int(self.interval_var.get())
        except ValueError:
            interval = 200
        cfg = CameraConfig(
            camera_id=cam_id,
            camera_type=cam_type,
            serial_number=self.serial_var.get().strip(),
            ip_address=self.ip_var.get().strip(),
            username=self.user_var.get().strip(),
            password=self.pass_var.get().strip(),
            rtsp_url=self.rtsp_var.get().strip(),
            frame_interval_ms=interval,
        )
        self.controller.add_camera(cfg)
        self.cameras[cam_id] = {"cfg": cfg, "status": "starting", "last_result": ""}
        self.tree.insert("", "end", iid=cam_id, values=(cam_id, cam_type.value, "starting", ""))

    def on_remove_camera(self):
        cam_id = self._selected_id()
        if not cam_id:
            return
        self.controller.remove_camera(cam_id)
        if cam_id in self.cameras:
            del self.cameras[cam_id]
        try:
            self.tree.delete(cam_id)
        except Exception:
            pass

    def on_connect(self):
        cam_id = self._selected_id()
        if not cam_id:
            return
        self.controller.send(cam_id, {"type": "connect"})

    def on_disconnect(self):
        cam_id = self._selected_id()
        if not cam_id:
            return
        self.controller.send(cam_id, {"type": "disconnect"})

    def on_capture_once(self):
        cam_id = self._selected_id()
        if not cam_id:
            return
        self.controller.send(cam_id, {"type": "capture_once"})

    def on_start_stream(self):
        cam_id = self._selected_id()
        if not cam_id:
            return
        self.controller.send(cam_id, {"type": "start_stream"})

    def on_stop_stream(self):
        cam_id = self._selected_id()
        if not cam_id:
            return
        self.controller.send(cam_id, {"type": "stop_stream"})

    def _poll_events(self):
        evt = self.controller.poll_event(timeout_ms=50)
        while evt:
            cam_id = evt.get("camera_id")
            event = evt.get("event")
            payload = evt.get("payload", {})
            if cam_id in self.cameras:
                if event == "status":
                    state = payload.get("state", "")
                    self.cameras[cam_id]["status"] = state
                    self._update_row(cam_id)
                elif event == "frame_processed":
                    result = payload.get("result")
                    self.cameras[cam_id]["last_result"] = str(result)
                    self._update_row(cam_id)
            evt = self.controller.poll_event(timeout_ms=10)
        self.after(100, self._poll_events)

    def _update_row(self, cam_id: str):
        info = self.cameras[cam_id]
        values = (cam_id, info["cfg"].camera_type.value, info["status"], info["last_result"])
        self.tree.item(cam_id, values=values)

    def on_closing(self):
        self.controller.shutdown_all()
        self.destroy()
