import json
from ir_controller import IRController
import time

BUTTON_MAP_FILE = "ir_buttons.json"

learned = {}

def handle_code(code):
    print(f"\nReceived IR code: {code}")
    name = input("Enter action name for this button (or blank to skip): ").strip()
    if name:
        learned[code] = name
        print(f"Mapped {code} → {name}")

def dummy_handler(action):
    pass

ir = IRController(
    gpio_pin=17,
    action_map={},
    action_handler=lambda action: None
)

print("IR calibration mode")
print("Press buttons on the remote (Ctrl+C to finish)")

try:
    while True:
        time.sleep(0.1)

        if ir.edges:
            code = ir._decode_nec()
            if code:
                ir.edges.clear()
                handle_code(code)

except KeyboardInterrupt:
    pass

finally:
    ir.stop()

    with open(BUTTON_MAP_FILE, "w") as f:
        json.dump(learned, f, indent=2)

    print("\nSaved button mappings to ir_buttons.json")
