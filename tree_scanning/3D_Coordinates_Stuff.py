import numpy as np
import cv2
import math
import my_utils

# -----------------------------
# 1. Known parameters
# -----------------------------
img_w, img_h = 1920 - 1000, 1080    # pixels
tree_distance = 75.0               # inches from camera to tree center
fov = 60.0                         # horizontal FOV in degrees (adjust if known)
f = (img_w / 2) / math.tan(math.radians(fov / 2))  # focal length in pixels

# Intrinsic matrix
cx, cy = img_w / 2, img_h / 2
K = np.array([[f, 0, cx],
              [0, f, cy],
              [0, 0, 1]])

# Rotation helper
def R_y(deg):
    th = math.radians(deg)
    return np.array([[ math.cos(th), 0, math.sin(th)],
                     [ 0, 1, 0],
                     [-math.sin(th), 0, math.cos(th)]])

# Projection matrices (camera fixed, tree rotated)
def make_projection(angle_deg):
    R = R_y(angle_deg)
    t = np.array([[0], [0], [tree_distance]])   # tree center offset in inches
    # camera sees tree rotated, so translation is negative in camera frame
    Rt = np.hstack((R, -R @ t))
    return K @ Rt, R

P0,  R0  = make_projection(0)
P90, R90 = make_projection(90)
P180,R180= make_projection(180)
P270,R270= make_projection(270)

# -----------------------------
# 2. Function to triangulate one light
# -----------------------------
def triangulate_light(input):
    # points as 2x1 arrays (u,v)
    p0   = np.array(input[0], dtype=float).reshape(2,1)
    p90  = np.array(input[1], dtype=float).reshape(2,1)
    p180 = np.array(input[2], dtype=float).reshape(2,1)
    p270 = np.array(input[3], dtype=float).reshape(2,1)

    # Triangulate pairs with the 0° view
    pts = []
    for P, p in [(P90,p90), (P180,p180), (P270,p270)]:
        X = cv2.triangulatePoints(P0, P, p0, p)
        X = (X / X[3])[:3].ravel()  # homogeneous → 3D
        pts.append(X)

    X_avg = np.mean(pts, axis=0)        # average of all pair results
    # Convert to tree coordinates (rotate back to tree's frame)
    X_tree = np.linalg.inv(R0) @ X_avg
    return X_tree  # (x, y, z) in inches, tree-centered frame

# -----------------------------
# 3. Example usage
# -----------------------------
# Replace with your actual detected pixel coordinates:
# allDirectionCoords = my_utils.read_in_coords("All_Direction_Coords.txt")

# print(allDirectionCoords)

# pos = triangulate_light(allDirectionCoords[0])
# print("Light position (inches):", pos)


import csv
import json

# --- Configuration ---
input_file = "lights_raw.json"   # The file containing your [[u0,v0],[u90,v90],[u180,v180],[u270,v270]] data
output_file = "lights_formatted.csv"

# --- Load data ---
# It can be either a JSON array or Python list literal
with open(input_file, "r") as f:
    text = f.read().strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # fallback if it's not strict JSON (e.g., single quotes)
        data = eval(text)

# --- Convert & save ---
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["LightID","u0","v0","u90","v90","u180","v180","u270","v270"])
    for i, coords in enumerate(data, start=1):
        flat = [c for pair in coords for c in pair]  # flatten [[a,b],[c,d]...] → [a,b,c,d,...]
        writer.writerow([i] + flat)

print(f"✅ Wrote {len(data)} lights to {output_file}")