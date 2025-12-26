import board
import neopixel
import sys

args = sys.argv[1:] # first argument is the name of script

if (len(args) < 1):
    print("Usage: sudo python ScanTree.py <number of lights>")
    sys.exit(1)

try:
    NUM_LIGHTS = int(args[0])
except:
   print("Invalid number of lights. Please try again...")

pixels = neopixel.NeoPixel(board.D18, NUM_LIGHTS, auto_write=False, pixel_order=neopixel.RGB)

def main():
  stop = False
  while not stop:
    for i in range(NUM_LIGHTS):
      pixels.fill((0,0,0))
      pixels[i] = (255,255,255)
      pixels.show()
      print(f"showing pixel: {i}")
      usr_in = input("increment to next pixel? (enter to continue, anything else to exit):")

      if usr_in != "":
        stop = True
        break

main()
