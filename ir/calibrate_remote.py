import time
import json
import lirc
from collections import Counter
from pathlib import Path

OUTPUT_FILE = Path("ir_buttons.json")
SAMPLE_TIME = 1.5
MIN_SAMPLES = 3


def learn_button(action_name):
    print(f"\nPress and HOLD the button for '{action_name}'...")
    print("Listening...")

    sockid = lirc.init("calibrate", blocking=False)
    start = time.time()
    codes = []

    while time.time() - start < SAMPLE_TIME:
        received = lirc.nextcode()
        if received:
            codes.append(received[0])
        time.sleep(0.01)

    lirc.deinit()

    if not codes:
        print("❌ No signal detected")
        return None

    counts = Counter(codes)

    # Remove obvious noise values
    counts.pop("0x0", None)
    counts.pop("0x80000000", None)

    if not counts:
        print("❌ Only noise detected")
        return None

    code, count = counts.most_common(1)[0]

    if count < MIN_SAMPLES:
        print("❌ Signal too unstable")
        return None

    print(f"✅ Learned code {code} ({count} hits)")
    return code


def main():
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, "r") as f:
            mapping = json.load(f)
    else:
        mapping = {}

    print("IR Button Calibration")
    print("Press Ctrl+C to finish\n")

    try:
        while True:
            action = input("Enter action name (e.g. next, shuffle, shutdown): ").strip()
            if not action:
                continue

            code = learn_button(action)
            if code:
                mapping[code] = action

                with open(OUTPUT_FILE, "w") as f:
                    json.dump(mapping, f, indent=2)

                print(f"Saved: {code} → {action}")

    except KeyboardInterrupt:
        print("\nCalibration complete")


if __name__ == "__main__":
    main()
