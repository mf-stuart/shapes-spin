import numpy as np
import default_constants as k

def testPrint(obj):
    print(obj)

def numpify_3vector(arr) -> np.ndarray:
    if not all(isinstance(x, (int, float)) for x in arr):
        raise TypeError("Input must be a numerical vector")
    elif isinstance(arr, np.ndarray):
        if arr.shape != (3,):
            raise ValueError("Expected 3D array")
        return arr
    else:
        if len(arr) != 3:
            raise ValueError("Expected 3D array")
        return np.array(arr)

def numpify_2vector(arr) -> np.ndarray:
    if not all(isinstance(x, (int, float)) for x in arr):
        raise TypeError("Input must be a numerical vector")
    elif isinstance(arr, np.ndarray):
        if arr.shape != (2,):
            raise ValueError("Expected 2D array")
        return arr
    else:
        if len(arr) != 2:
            raise ValueError("Expected 2D array")
        return np.array(arr)

def normpify_3vector(arr) -> np.ndarray:
    if not all(isinstance(x, (int, float)) for x in arr):
        raise TypeError("Input must be a numerical vector")
    elif isinstance(arr, np.ndarray):
        if arr.shape != (3,):
            raise ValueError("Expected 3D array")
        if np.linalg.norm(arr, axis=0) < k.EPSILON:
            raise ValueError("Zero-length vector cannot be normalized")
        return arr / np.linalg.norm(arr, axis=0)
    else:
        if len(arr) != 3:
            raise ValueError("Expected 3D array")
        if np.linalg.norm(np.array(arr), axis=0) < k.EPSILON:
            raise ValueError("Zero-length vector cannot be normalized")
        return np.array(arr) / np.linalg.norm(np.array(arr), axis=0)
