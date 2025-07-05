import os

import numpy as np
import default_constants as k

def testPrint(obj):
    print(obj)

def numpify_3vector(arr) -> np.ndarray:
    if isinstance(arr, np.ndarray):
        if arr.shape != (3,):
            raise ValueError("Expected 3D array")
        if not np.issubdtype(arr.dtype, np.number):
            raise TypeError("Input array must be numeric")
        return arr
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
        return arr
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
        return arr / norm
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
        for theta in theta_vals:
            x = np.sin(phi) * np.cos(theta)
            y = np.sin(phi) * np.sin(theta)
            z = np.cos(phi)
            vectors.append(np.array([x, y, z]))
    return vectors

def inverse_square_multiplier(vector: np.ndarray) -> float:
    vector = numpify_3vector(vector)
    length = np.linalg.norm(vector)
    return 1 / (length ** 2)

def bucketize(x: float, n: int) -> int:
    idx = int(x * n)
    return min(idx, n - 1)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')