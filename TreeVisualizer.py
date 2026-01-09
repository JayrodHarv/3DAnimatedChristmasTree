"""TreeVisualizer GUI

Displays a 3D scatter of tree coordinates and lets you run/simulate animations
from the `animations` package on a virtual tree (no physical LEDs required).

Usage:
    python TreeVisualizer.py [coords_file]

Features:
- Load coordinates from a file (plain text of Python lists per line)
- Select any installed Animation and run it in the GUI
- Play / Pause, Speed control, Next/Previous animation, Cycle all
- 3D interactive view (matplotlib) that updates colors per-frame

This is intentionally lightweight and uses Tkinter + matplotlib so it works
on a Raspberry Pi / desktop with minimal dependencies (already used in the
project).
"""

import sys
import time
import math
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from utils import my_utils
from animations import ANIMATIONS


class PixelBuffer:
    """A simple in-memory pixel buffer that mimics the neopixel API used by
    animations. Supports indexing, len(), fill() and show()."""
    def __init__(self, n):
        self.n = n
        self.colors = [(0, 0, 0)] * n

    def __len__(self):
        return self.n

    def __setitem__(self, idx, value):
        self.colors[idx] = tuple(value)

    def __getitem__(self, idx):
        return self.colors[idx]

    def fill(self, color):
        self.colors = [tuple(color)] * self.n

    def show(self):
        # No-op; visualizer will pull `colors` directly
        pass


class TreeVisualizer(tk.Tk):
    def __init__(self, coords_file=None):
        super().__init__()
        self.title("Tree Visualizer")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.coords = []
        if coords_file:
            self.load_coords(coords_file)

        # GUI state
        self.anim_classes = ANIMATIONS
        self.anim_index = 0
        self.animation = None
        self.pixels = None
        self.playing = False
        self.speed = 1.0
        self.last_time = None
        self.update_interval_ms = 30  # roughly 33 FPS update tick
        self.cycle_mode = False
        self.cycle_interval = 8.0  # seconds per animation when cycling
        self.cycle_last = 0.0

        self._build_ui()
        self._init_plot()

        # If we have coordinates, initialize a default animation
        if self.coords:
            self._prepare_animation(self.anim_index)

        # Start the tk update loop
        self.after(self.update_interval_ms, self._tick)

    # ------------------------- GUI -------------------------
    def _build_ui(self):
        # Top controls frame
        ctrl = ttk.Frame(self)
        ctrl.pack(side=tk.TOP, fill=tk.X)

        load_btn = ttk.Button(ctrl, text="Load Coords", command=self._on_load_coords)
        load_btn.pack(side=tk.LEFT, padx=4, pady=4)

        ttk.Label(ctrl, text="Animation:").pack(side=tk.LEFT, padx=(8, 2))
        self.anim_var = tk.StringVar()
        anim_names = [cls.name for cls in self.anim_classes]
        self.anim_combo = ttk.Combobox(ctrl, values=anim_names, state="readonly", width=28)
        self.anim_combo.current(self.anim_index)
        self.anim_combo.pack(side=tk.LEFT, padx=2)
        self.anim_combo.bind("<<ComboboxSelected>>", self._on_anim_selected)

        play_btn = ttk.Button(ctrl, text="Play/Pause", command=self._toggle_play)
        play_btn.pack(side=tk.LEFT, padx=4)

        prev_btn = ttk.Button(ctrl, text="Prev", command=self._prev_anim)
        prev_btn.pack(side=tk.LEFT, padx=2)
        next_btn = ttk.Button(ctrl, text="Next", command=self._next_anim)
        next_btn.pack(side=tk.LEFT, padx=2)

        ttk.Label(ctrl, text="Speed:").pack(side=tk.LEFT, padx=(8, 2))
        self.speed_var = tk.DoubleVar(value=self.speed)
        speed_slider = ttk.Scale(ctrl, from_=0.1, to=3.0, variable=self.speed_var, command=self._on_speed)
        speed_slider.pack(side=tk.LEFT, padx=4, pady=4)

        cycle_btn = ttk.Button(ctrl, text="Cycle All", command=self._toggle_cycle)
        cycle_btn.pack(side=tk.LEFT, padx=6)

        # Status label
        self.status_var = tk.StringVar(value="No coords loaded")
        status = ttk.Label(self, textvariable=self.status_var)
        status.pack(side=tk.TOP, fill=tk.X)

        # Figure frame
        fig_frame = ttk.Frame(self)
        fig_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.fig = Figure(figsize=(6, 6))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_box_aspect((1, 1, 1))

        self.canvas = FigureCanvasTkAgg(self.fig, master=fig_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas, fig_frame)
        toolbar.update()

    def _init_plot(self):
        self.ax.cla()
        if not self.coords:
            self.canvas.draw()
            return

        arr = np.array(self.coords)
        xs, ys, zs = arr[:, 0], arr[:, 1], arr[:, 2]
        self.sc = self.ax.scatter(xs, ys, zs, c=[(0, 0, 0)] * len(xs), s=20)

        # Label axes
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        # Set a sensible view and limits
        self._set_axes_equal()
        self.canvas.draw()

    def _set_axes_equal(self):
        # From https://stackoverflow.com/a/50664367
        x_limits = self.ax.get_xlim3d()
        y_limits = self.ax.get_ylim3d()
        z_limits = self.ax.get_zlim3d()

        x_range = abs(x_limits[1] - x_limits[0])
        x_middle = np.mean(x_limits)
        y_range = abs(y_limits[1] - y_limits[0])
        y_middle = np.mean(y_limits)
        z_range = abs(z_limits[1] - z_limits[0])
        z_middle = np.mean(z_limits)

        plot_radius = 0.5 * max([x_range, y_range, z_range])

        self.ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
        self.ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
        self.ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

    # ------------------------- Data loading -------------------------
    def load_coords(self, filename):
        try:
            coords = my_utils.read_in_coords(filename)
            if not coords:
                raise ValueError("No coordinates found in file")

            self.coords = coords
            self.status_var.set(f"Loaded {len(coords)} coordinates from {filename}")
            self._init_plot()

            # Prepare animation with new coords
            self._prepare_animation(self.anim_index)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load coords: {e}")

    # ------------------------- Animation control -------------------------
    def _prepare_animation(self, index):
        if not self.coords:
            return

        AnimClass = self.anim_classes[index]
        self.pixels = PixelBuffer(len(self.coords))
        try:
            self.animation = AnimClass(self.coords, self.pixels)
            self.animation.setup()
            # Ensure initial draw
            self._apply_pixels_to_plot()
            self.status_var.set(f"Selected animation: {AnimClass.name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize animation: {e}")
            self.animation = None

    def _toggle_play(self):
        if not self.animation:
            messagebox.showinfo("Info", "Load coordinates and select an animation first")
            return
        self.playing = not self.playing
        if self.playing:
            self.last_time = time.time()
            self.status_var.set(f"Playing: {self.animation.name}")
        else:
            self.status_var.set(f"Paused: {self.animation.name}")

    def _on_anim_selected(self, event=None):
        name = self.anim_combo.get()
        for i, cls in enumerate(self.anim_classes):
            if cls.name == name:
                self.anim_index = i
                self._prepare_animation(i)
                break

    def _next_anim(self):
        self.anim_index = (self.anim_index + 1) % len(self.anim_classes)
        self.anim_combo.current(self.anim_index)
        self._prepare_animation(self.anim_index)

    def _prev_anim(self):
        self.anim_index = (self.anim_index - 1) % len(self.anim_classes)
        self.anim_combo.current(self.anim_index)
        self._prepare_animation(self.anim_index)

    def _on_speed(self, val):
        try:
            self.speed = float(val)
        except Exception:
            pass

    def _toggle_cycle(self):
        self.cycle_mode = not self.cycle_mode
        self.cycle_last = time.time()
        self.status_var.set("Cycle mode: ON" if self.cycle_mode else "Cycle mode: OFF")

    # ------------------------- Main loop -------------------------
    def _tick(self):
        now = time.time()
        if self.last_time is None:
            self.last_time = now

        dt = now - self.last_time
        self.last_time = now

        if self.playing and self.animation:
            scaled_dt = dt * self.speed
            try:
                # Keep animation.time_elapsed in sync (many animations reference it)
                self.animation.time_elapsed += scaled_dt
                self.animation.update(scaled_dt)
                self.pixels.show()
                self._apply_pixels_to_plot()
            except Exception as e:
                # If an animation raises, show error and pause
                self.playing = False
                messagebox.showerror("Animation Error", f"Animation raised an exception: {e}")

        # Handle cycling between animations
        if self.cycle_mode:
            if time.time() - self.cycle_last > self.cycle_interval:
                self.cycle_last = time.time()
                self._next_anim()

        # Schedule next tick
        self.after(self.update_interval_ms, self._tick)

    def _apply_pixels_to_plot(self):
        if not hasattr(self, 'sc'):
            return
        # Convert pixel colors (0-255) to matplotlib RGBA (0-1)
        cols = [tuple(c/255.0 for c in col) for col in self.pixels.colors]
        # Matplotlib 3D scatter uses facecolors / edgecolors
        try:
            self.sc.set_facecolors(cols)
            self.sc.set_edgecolors(cols)
        except Exception:
            # Fallback: recreate scatter if setting colors fails
            arr = np.array(self.coords)
            self.sc.remove()
            self.sc = self.ax.scatter(arr[:,0], arr[:,1], arr[:,2], c=cols, s=20)
            self._set_axes_equal()

        self.canvas.draw_idle()

    # ------------------------- UI actions -------------------------
    def _on_load_coords(self):
        filename = filedialog.askopenfilename(title="Load coordinates file", filetypes=[("Text files","*.txt"), ("All files","*")])
        if filename:
            self.load_coords(filename)

    def on_close(self):
        self.playing = False
        self.destroy()


def main():
    coords_file = sys.argv[1] if len(sys.argv) > 1 else None
    app = TreeVisualizer(coords_file)
    app.mainloop()


if __name__ == '__main__':
    main()
