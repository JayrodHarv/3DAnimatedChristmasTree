# 3D Animated Christmas Tree

> This project was heavily inspired by this video made by Matt Parker at the Stand-up Maths youtube channel:
> [![Watch the video](https://img.youtube.com/vi/TvlpIojusBE/maxresdefault.jpg)](https://www.youtube.com/watch?v=TvlpIojusBE)

---

## Project Overview
Utilizing the power of a lot of crappy python code, I was able to hook up 550 individually addressible LED lights to my Raspberry Pi 3B and control the lights using the neo_pixel and Raspberry Pi's board libraries to display several different animations that I created and many animations from the Stand-up Maths video too. The hardest part of this project was finding accurate 3D coordinates of each light on the tree, which was needed to display true 3D animations on the tree. I accomplished this by following the great advice from the video which was to take a picture of each light from 4 different directions and finding the brightest pixel in each image in order to extrapolate the 3D coordinates.

## Youtube Video
### This video describes the process I went through to make it all work
[![Watch the video](https://img.youtube.com/vi/L4ZAIFt4BIo/maxresdefault.jpg)](https://youtu.be/L4ZAIFt4BIo)

### [3D Animated Christmas Tree](https://youtu.be/L4ZAIFt4BIo)

## External Python Libraries Used (Must be installed to use this program)
board, neopixel, argparse, numpy, matplotlib, cv2, tkinter

*To install dependencies, enter the command* `pip install board neopixel argparse numpy matplotlib cv2 tkinter`

## User Guide
First off, in order to use my code, you will have had to build your own tree. If you wish to do so, take the above video as a guide for how to do it. The video doesn't cover most of the wiring, but just know that I used pin 12 (GPIO 18) for the data wire and pin 6 (Ground) for the gound wire connections to the lights from the Raspberry Pi.

You also need to be able to connect to the Raspberrypi. This is most conveniently done via ssh. This requires your pi to be connected to your local network and for ssh to be enabled on your pi. You do this by entering the command `sudo raspi-config`, navigating to the Interfacing Options, and select SSH. Do this step when first setting up the raspberrypi using a keyboard/mouse and monitor plugged into pi.

Once you have the tree built, you need to scan it. This is done by setting up a camera at a fixed position so that it contains all the lights in its frame. You then need to set up AutoHotKey and use my `scan_tree.ahk` macro in tandem with the `ScanTree.py` to take pictures of each light from 4 different directions which are all 90 degrees apart. Once you have done this, use the `TriangulateCoordinates.py` script and pass it the necessary arguements to have it output the coordinates to a text file.

Once you have the text file, try running any animation by running `sudo python PlaySingleAnimation.py` that requires the coordinates and see if it looks right. If it looks completely wrong, go through each step again. If only a handfull of lights appear to be incorrect, use the CoordinateCorrectionGUI.py script to correct those light coordinates.

### How to use once tree is built and scanned
Enter command `sudo python CycleAnimations.py` to cycle through every animation. By default, the ordering is shuffled and the duration of each animation is 60 seconds (1 minute). Enter command `sudo python CycleAnimations.py --help` for information on how to change these parameters

Enter command `sudo python PlaySingleAnimation.py` to select an animation from the list to play indefinitely.

### How to simulate the tree
Run the `TreeVisualizer.py` script to simulate the tree and the animations I have created for it. For the coordinates, use either the `tree_d_coords.txt` or the `test_coords.txt` files and you should be able to have a virtual version of my tree play the animations.

### How to use a phone as a remote control
Start up the raspberrypi and run `sudo python -m uvicorn main:app --host 0.0.0.0 --port 80 --reload`. This will start up a small web server that facilitates calls to the api endpoints that controll the tree. Go to the address `http:<insert-raspberrypi-hostname-here>` to access the web interface.

#### Remote Control Functionality on Startup of Raspberrypi
If you want the remote control to work on startup of the raspberrypi, you need to create a background service for the api and to enable it to startup with the raspberrypi.
To do this, create a systemd service file using `sudo nano /etc/systemd/system/tree-api.service`
```bash
[Unit]
Description=Christmas Tree Animation API
After=network.target

[Service]
Type=simple
User=<insert-linux-username>
WorkingDirectory=<insert-path-to-project>

# Activate venv and start FastAPI
ExecStart=sudo python \
          -m uvicorn main:app \
          --host 0.0.0.0 \
          --port 80

Restart=always
RestartSec=3

# Clean shutdown
KillSignal=SIGINT
TimeoutStopSec=10

# Environment safety
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```
After making this file, run `sudo systemctl daemon-reload` then `sudo systemctl enable tree-api` to enable the api to startup with the raspberrypi. To start it initially, run the command `sudo systemctl start tree-api`. After doing this, you should be able to visit the web interface at the address: `http:<insert-raspberrypi-hostname-here>` in a browser and should see the gui to interface with the tree.

Also, to make it possible to shut off the raspberry pi from the web interface, you need to edit some config files on your pi. Normally this would be a bad idea but it's only hosted on the LAN and it's the only thing that still requires you to connect to the pi via ssh so it makes it more user friendly to do it this way. To edit the config, enter the command `sudo visudo` and add this line at the end of the file `<insert-your-linux-username> ALL=(ALL) NOPASSWD: /sbin/shutdown`. This allows for the user to run only the shutdown command without needing to enter the sudo password.

After all of this, you should have it so when you start up the raspberrypi, after a few seconds it starts shuffling through the animations. You can then connect to the web interface by visiting the site `raspberrypi.local` on a browser to be able to control the tree. You should also be able to shutdown the raspberry pi via the web too.
