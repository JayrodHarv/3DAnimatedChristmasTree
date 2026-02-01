import time
import json
import lirc
from pathlib import Path


class IRController:
    def __init__(
        self,
        mapping_file="ir_buttons.json",
        debounce_time=0.35,
    ):
        self.debounce_time = debounce_time
        self.last_code = None
        self.last_time = 0

        self.mapping_file = Path(mapping_file)
        self.button_map = {}

        self._load_mapping()
        self.sockid = lirc.init("tree", blocking=False)

    # -------------------------
    # Mapping
    # -------------------------

    def _load_mapping(self):
        if self.mapping_file.exists():
            with open(self.mapping_file, "r") as f:
                self.button_map = json.load(f)
        else:
            self.button_map = {}

    def reload_mapping(self):
        self._load_mapping()

    # -------------------------
    # Main update loop
    # -------------------------

    def poll(self):
        """
        Call this frequently (e.g. every frame / tick).
        Returns the action name if a valid button was pressed.
        """
        codes = lirc.nextcode()
        now = time.time()

        if not codes:
            return None

        code = codes[0]

        # Ignore noise / repeat frames
        if code == self.last_code and (now - self.last_time) < self.debounce_time:
            return None

        self.last_code = code
        self.last_time = now

        return self.button_map.get(code)

    # -------------------------
    # Utility
    # -------------------------

    def close(self):
        lirc.deinit()
