# 3D Animated Christmas Tree

> This project was heavily inspired by this video made by Matt Parker at the Stand-up Maths youtube channel:
> [![Watch the video](https://img.youtube.com/vi/TvlpIojusBE/maxresdefault.jpg)](https://www.youtube.com/watch?v=TvlpIojusBE)

---

## Project Overview
Utilizing the power of a lot of crappy python code, I was able to hook up 550 individually addressible LED lights to my Raspberry Pi 3B and control the lights using the neo_pixel and Raspberry Pi's board libraries to display several different animations that I created and many animations from the Stand-up Maths video too. The hardest part of this project was finding accurate 3D coordinates of each light on the tree, which was needed to display true 3D animations on the tree. I accomplished this by following the great advice from the video which was to take a picture of each light from 4 different directions and finding the brightest pixel in each image in order to extrapolate the 3D coordinates.
