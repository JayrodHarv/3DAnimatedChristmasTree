#!/usr/bin/env python3
"""
triangulate_from_pixels.py

Input CSV format (header required):
 LightID,u0,v0,u90,v90,u180,v180,u270,v270

Outputs:
 - CSV with X,Y,Z (tree-frame) and reprojection errors
 - 3D scatter plot for quick visual verification

Requires: numpy, opencv-python, pandas, matplotlib
"""

import argparse
import math
import json
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt

# ---------------------------
# Math helpers
# ---------------------------
def R_y_deg(angle_deg):
    th = math.radians(angle_deg)
    return np.array([
        [math.cos(th), 0.0, math.sin(th)],
        [0.0, 1.0, 0.0],
        [-math.sin(th), 0.0, math.cos(th)]
    ], dtype=float)

def estimate_intrinsics_from_fov(img_w, img_h, fov_deg=60.0):
    fx = (img_w / 2.0) / math.tan(math.radians(fov_deg / 2.0))
    fy = fx
    cx = img_w / 2.0
    cy = img_h / 2.0
    K = np.array([[fx, 0, cx], [0, fy, cy], [0,0,1]], dtype=float)
    return K

def undistort_and_normalize_points(pts_px, K, distCoeffs):
    pts = np.array(pts_px, dtype=np.float32).reshape(-1,1,2)
    und = cv2.undistortPoints(pts, K, distCoeffs, P=None)  # normalized coords x,y
    return und.reshape(-1,2)

def rays_from_normalized(norm_pts):
    rays = []
    for (x,y) in norm_pts:
        v = np.array([x, y, 1.0], dtype=float)
        v /= np.linalg.norm(v)
        rays.append(v)
    return rays

def camera_center_in_tree_frame(camera_to_tree_vec, R_view):
    # camera at origin in camera frame; tree center at camera_to_tree_vec (in camera/world coords)
    # camera position in tree frame = R_view.T @ (-camera_to_tree_vec)
    return R_view.T @ (-np.array(camera_to_tree_vec, dtype=float))

def solve_point_from_rays_treeframe(rays_tree, cams_tree):
    A = np.zeros((3,3), dtype=float)
    b = np.zeros(3, dtype=float)
    for d, C in zip(rays_tree, cams_tree):
        d = d.reshape(3,1)
        P = np.eye(3) - (d @ d.T)
        A += P
        b += (P @ C)
    try:
        X = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        X = np.linalg.lstsq(A + 1e-8*np.eye(3), b, rcond=None)[0]
    return X

# ---------------------------
# Pipeline
# ---------------------------

def run(input_csv, output_csv, calib_file, img_w, img_h, fov_deg, camera_to_tree_dist):
    # load CSV
    df = pd.read_csv(input_csv)
    req = ['LightID','u0','v0','u90','v90','u180','v180','u270','v270']
    if not all(c in df.columns for c in req):
        raise RuntimeError(f"Input CSV must contain columns: {req}")

    # load / estimate intrinsics
    if calib_file:
        with open(calib_file,'r') as f:
            c = json.load(f)
            K = np.array(c['K'], dtype=float)
            dist = np.array(c.get('distCoeffs', [0,0,0,0,0]), dtype=float)
        print("Loaded calibration from:", calib_file)
    else:
        K = estimate_intrinsics_from_fov(img_w, img_h, fov_deg)
        dist = np.zeros(5, dtype=float)
        print("Using estimated intrinsics (no calibration).")

    print("K:\n", K)
    print("distCoeffs:", dist)

    angles = [0, 90, 180, 270]
    Rs = {a: R_y_deg(a) for a in angles}

    # camera_to_tree vector (camera coords): camera at origin, tree center at (0,0,-D)
    camera_to_tree = np.array([0.0, 0.0, -camera_to_tree_dist], dtype=float)
    print("camera_to_tree (units same as distance):", camera_to_tree)

    results = []
    for idx, row in df.iterrows():
        lid = int(row['LightID'])
        pts_px = [
            (float(row['u0']), float(row['v0'])),
            (float(row['u90']), float(row['v90'])),
            (float(row['u180']), float(row['v180'])),
            (float(row['u270']), float(row['v270']))
        ]

        # undistort & normalize
        norm = undistort_and_normalize_points(pts_px, K, dist)  # 4x2
        rays_cam = rays_from_normalized(norm)  # 4 unit vectors in camera frame

        # transform rays and camera centers to tree frame
        rays_tree = []
        cams_tree = []
        for i, angle in enumerate(angles):
            R = Rs[angle]
            d_tree = (R.T @ rays_cam[i])
            d_tree /= np.linalg.norm(d_tree)
            rays_tree.append(d_tree)
            C_tree = camera_center_in_tree_frame(camera_to_tree, R)
            cams_tree.append(C_tree)

        # solve for X in tree frame
        X_tree = solve_point_from_rays_treeframe(rays_tree, cams_tree)

        # reprojection diagnostics
        reproj_errors = []
        for i, angle in enumerate(angles):
            X_cam_i = Rs[angle] @ X_tree + camera_to_tree
            if X_cam_i[2] == 0:
                reproj_errors.append(float('nan'))
            else:
                uv_proj = (K @ (X_cam_i / X_cam_i[2]))[:2]
                measured_uv = np.array(pts_px[i])
                reproj_errors.append(float(np.linalg.norm(uv_proj - measured_uv)))

        results.append({
            'LightID': lid,
            'X': float(X_tree[0]),
            'Y': float(X_tree[1]),
            'Z': float(X_tree[2]),
            'reproj_mean_px': float(np.nanmean(reproj_errors)),
            'reproj_0_px': reproj_errors[0],
            'reproj_90_px': reproj_errors[1],
            'reproj_180_px': reproj_errors[2],
            'reproj_270_px': reproj_errors[3]
        })

    out_df = pd.DataFrame(results).sort_values('LightID')
    out_df.to_csv(output_csv, index=False)
    print(f"Saved {len(out_df)} points to {output_csv}")
    print("Mean reprojection error (px):", out_df['reproj_mean_px'].mean())

    # quick 3D plot
    coords = out_df[['X','Y','Z']].to_numpy()
    if coords.shape[0] > 0:
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(coords[:,0], coords[:,1], coords[:,2], s=6)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Reconstructed lights (tree frame)')
        # approx equal aspect
        max_range = np.ptp(coords, axis=0).max() / 2.0
        midx, midy, midz = coords[:,0].mean(), coords[:,1].mean(), coords[:,2].mean()
        ax.set_xlim(midx - max_range, midx + max_range)
        ax.set_ylim(midy - max_range, midy + max_range)
        ax.set_zlim(midz - max_range, midz + max_range)
        plt.show()


if __name__ == '__main__':
    p = argparse.ArgumentParser(description="Triangulate lights from four rotated views.")
    p.add_argument('--input_csv', required=True, help="Input CSV with LightID,u0,v0,u90,v90,u180,v180,u270,v270")
    p.add_argument('--output_csv', default='lights_3d.csv', help="Output CSV filename")
    p.add_argument('--calib_file', default=None, help="Optional JSON with {'K':[[...]], 'distCoeffs':[...]} (if absent, a guessed K is used)")
    p.add_argument('--img_w', type=int, default=1080, help="Image width in px")
    p.add_argument('--img_h', type=int, default=920, help="Image height in px")
    p.add_argument('--fov_deg', type=float, default=60.0, help="Approx FOV if no calibration (deg)")
    p.add_argument('--camera_to_tree', type=float, default=75.0, help="Distance from camera to tree center (same units for output)")
    args = p.parse_args()

    run(args.input_csv, args.output_csv, args.calib_file, args.img_w, args.img_h, args.fov_deg, args.camera_to_tree)
