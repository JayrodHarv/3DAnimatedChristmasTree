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

## User Guide
First off, in order to use my code, you will have had to build your own tree. If you wish to do so, take the above video as a guide for how to do it. The video doesn't cover most of the wiring, but just know that I used pin 12 (GPIO 18) for the data wire and pin 6 (Ground) for the gound wire connections to the lights from the Raspberry Pi.

Once you have the tree built, you need to scan it. This is done by setting up a camera at a fixed position so that it contains all the lights in its frame. You then need to set up AutoHotKey and use my scan_tree.ahk macro in tandem with the ScanTree.py to take pictures of each light from 4 different directions which are all 90 degrees apart. Once you have done this, use the TriangulateCoordinates.py script and pass it the necessary arguements to have it output the coordinates to a text file.

Once you have the text file, try running any animation by running "sudo python PlaySingleAnimation.py" that requires the coordinates and see if it looks right. If it looks completely wrong, go through each step again. If only a handfull of lights appear to be incorrect, use the coordinate_correction.py script to correct those light coordinates.

### How to use once tree is built and scanned
Enter command "sudo python CycleAnimations.py" to cycle through every animation. By default, the ordering is shuffled and the duration of each animation is 60 seconds (1 minute). Enter command "sudo python CycleAnimations.py --help" for information on how to change these parameters

Enter command "sudo python PlaySingleAnimation.py" to select an animation from the list to play indefinitely.
