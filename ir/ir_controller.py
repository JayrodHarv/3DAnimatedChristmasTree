import pigpio
import time
import threading

class IRController:
    """
    Receives IR signals via GPIO and maps buttons to actions.
    """

    def __init__(self, gpio_pin, action_map, action_handler):
        """
        gpio_pin: GPIO pin connected to IR receiver
        action_map: dict {hex_code: action_name}
        action_handler: function(action_name)
        """
        self.gpio = gpio_pin
        self.action_map = action_map
        self.action_handler = action_handler

        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise RuntimeError("pigpio daemon not running")

        self.edges = []
        self.last_action_time = 0
        self.debounce = 0.4  # seconds

        self.callback = self.pi.callback(
            self.gpio,
            pigpio.EITHER_EDGE,
            self._edge_callback
        )

        self.running = True
        self.thread = threading.Thread(target=self._process_loop, daemon=True)
        self.thread.start()

    def _edge_callback(self, gpio, level, tick):
        self.edges.append((level, tick))

    def _decode_nec(self):
        """
        Decode NEC IR pulses from edge timings.
        Returns hex string or None.
        """
        if len(self.edges) < 66:
            return None

        pulses = []
        for i in range(1, len(self.edges)):
            dt = pigpio.tickDiff(self.edges[i - 1][1], self.edges[i][1])
            pulses.append(dt)

        bits = []
        for p in pulses:
            if 1000 < p < 2000:
                bits.append(0)
            elif 2000 < p < 3000:
                bits.append(1)

        if len(bits) < 32:
            return None

        code = 0
        for b in bits[:32]:
            code = (code << 1) | b

        return hex(code)

    def _process_loop(self):
        while self.running:
            time.sleep(0.05)

            code = self._decode_nec()
            if not code:
                continue

            self.edges.clear()

            now = time.time()
            if now - self.last_action_time < self.debounce:
                continue

            self.last_action_time = now

            action = self.action_map.get(code)
            if action:
                print(f"[IR] {code} → {action}")
                self.action_handler(action)
            else:
                print(f"[IR] Unknown code: {code}")

    def stop(self):
        self.running = False
        self.callback.cancel()
        self.pi.stop()