# app/api/core/logging_utils.py
import os
import json
import time
from typing import Dict, Any

from .config import settings

class Logger:
    def __init__(self, job_id: str, config: Dict[str, Any]):
        self.job_id = job_id
        self.config = config
        self.start_time = None
        self.log_path = os.path.join(settings.LOG_DIR, f"log_{job_id}.json")
        self.logs = {}

    def start(self):
        self.start_time = time.time()
        self.logs["job_id"] = self.job_id
        self.logs["config"] = self.config
        self.logs["start_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
        self.logs["events"] = []
        self._write_log()

    def log_event(self, message: str, extra: Dict[str, Any] = None):
        event = {"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "message": message}
        if extra:
            event.update(extra)
        self.logs["events"].append(event)
        self._write_log()

    def end(self, metrics: Dict[str, Any]):
        self.logs["end_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
        self.logs["duration_seconds"] = round(time.time() - self.start_time, 2)
        self.logs["metrics"] = metrics
        self._write_log()

    def _write_log(self):
        with open(self.log_path, "w", encoding="utf-8") as f:
            json.dump(self.logs, f, indent=4, ensure_ascii=False)
