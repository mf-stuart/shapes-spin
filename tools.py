import os

import numpy as np
import default_constants as k
from render.pixel_data import PixelData



def testPrint(obj):
    print(obj)

def numpify_3vector(arr) -> np.ndarray:
    if isinstance(arr, np.ndarray):
        if arr.shape != (3,):
            raise ValueError("Expected 3D array")
        if not np.issubdtype(arr.dtype, np.number):
            raise TypeError("Input array must be numeric")
        return arr.astype(float)
    else:
        if len(arr) != 3:
            raise ValueError("Expected 3D array")
        if not all(isinstance(x, (int, float)) for x in arr):
            raise TypeError("Input must be a numerical vector")
        return np.array(arr, dtype=float)

def numpify_2vector(arr) -> np.ndarray:
    if isinstance(arr, np.ndarray):
        if arr.shape != (2,):
            raise ValueError("Expected 2D array")
        if not np.issubdtype(arr.dtype, np.number):
            raise TypeError("Input array must be numeric")
        return arr.astype(float)
    else:
        if len(arr) != 2:
            raise ValueError("Expected 2D array")
        if not all(isinstance(x, (int, float)) for x in arr):
            raise TypeError("Input must be a numerical vector")
        return np.array(arr, dtype=float)

def normpify_3vector(arr) -> np.ndarray:
    if isinstance(arr, np.ndarray):
        if arr.shape != (3,):
            raise ValueError("Expected 3D array")
        if not np.issubdtype(arr.dtype, np.number):
            raise TypeError("Input array must be numeric")
        norm = np.linalg.norm(arr)
        if norm < k.EPSILON:
            raise ValueError("Zero-length vector cannot be normalized")
        return arr.astype(float) / norm
    else:
        if len(arr) != 3:
            raise ValueError("Expected 3D array")
        if not all(isinstance(x, (int, float)) for x in arr):
            raise TypeError("Input must be a numerical vector")
        arr_np = np.array(arr, dtype=float)
        norm = np.linalg.norm(arr_np)
        if norm < k.EPSILON:
            raise ValueError("Zero-length vector cannot be normalized")
        return arr_np / norm


def x_axis_rotation_matrix(t: float) -> np.ndarray:
    return np.array([
        [1, 0, 0],
        [0, np.cos(t), -np.sin(t)],
        [0, np.sin(t), np.cos(t)],
    ])

def y_axis_rotation_matrix(t: float) -> np.ndarray:
    return np.array([
        [np.cos(t), 0 , np.sin(t)],
        [0, 1, 0],
        [-np.sin(t), 0, np.cos(t)],
    ])

def z_axis_rotation_matrix(t: float) -> np.ndarray:
    return np.array([
        [np.cos(t), -np.sin(t), 0],
        [np.sin(t), np.cos(t), 0],
        [0, 0, 1],
    ])

def generate_ray_tracers() -> list[np.ndarray]:
    vectors = []
    phi_vals = np.arange(0, np.pi + k.ANGULAR_DELTA, k.ANGULAR_DELTA)
    theta_vals = np.arange(0, 2 * np.pi, k.ANGULAR_DELTA)

    for phi in phi_vals:
        if abs(phi) < k.EPSILON:
            vectors.append(numpify_3vector([0.0, 0.0, 1.0]))
            continue
        elif abs(phi - np.pi) < k.EPSILON:
            vectors.append(numpify_3vector([0.0, 0.0, -1.0]))
            continue

        for theta in theta_vals:
            x = np.sin(phi) * np.cos(theta)
            y = np.sin(phi) * np.sin(theta)
            z = np.cos(phi)
            vectors.append(numpify_3vector([x, y, z]))

    return vectors

def inverse_square_multiplier(vector: np.ndarray) -> float:
    vector = numpify_3vector(vector)
    length = np.linalg.norm(vector)
    return 1

def bucketize(x: float, n: int) -> int:
    idx = int(x * n)
    return min(idx, n - 1)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')



import matplotlib.pyplot as plt
import numpy as np

def plot_reflection_points(reflection_points):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    positions = np.array([r.get_pos() for r in reflection_points])
    xs, ys, zs = positions[:, 0], positions[:, 1], positions[:, 2]

    ax.scatter(xs, ys, zs, c='green', s=30)

    # Auto-scale
    max_range = (positions.max(axis=0) - positions.min(axis=0)).max() / 2
    mid = positions.mean(axis=0)
    ax.set_xlim(mid[0] - max_range, mid[0] + max_range)
    ax.set_ylim(mid[1] - max_range, mid[1] + max_range)
    ax.set_zlim(mid[2] - max_range, mid[2] + max_range)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Reflection Points in 3D")

    plt.show()


def plot_pixel_data(pixels: list[PixelData]):
    xs, ys, brightness = zip(*[
        (*pixel.get_indices(), pixel.get_brightness()) for pixel in pixels
    ])
    plt.figure(figsize=(8, 6))
    plt.scatter(xs, ys, c=brightness, cmap='gray', s=10)
    plt.gca().invert_yaxis()  # Match screen orientation if top-left origin
    plt.colorbar(label="Brightness")
    plt.title("Pixel Data Projection")
    plt.xlabel("X (screen column)")
    plt.ylabel("Y (screen row)")
    plt.show()
