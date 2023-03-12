import math

import numpy as np


def get_translation_matrix(dx, dy, dz):
    return np.array([[1, 0, 0, dx],
                     [0, 1, 0, dy],
                     [0, 0, 1, dz],
                     [0, 0, 0, 1], ])


def get_scaleY_matrix(pt1, pt2):
    vect = np.array(pt2) - np.array(pt1)
    scale_factor = np.linalg.norm(vect)
    return np.array([[1, 0, 0, 0],
                     [0, scale_factor, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1], ])


def get_rot_from_vert(pt1, pt2):
    vect = np.array(pt2) - np.array(pt1)
    vect = 1 / np.linalg.norm(vect) * vect

    vertical = np.array([0, 1, 0])

    vector = np.cross(vect, vertical)
    if np.linalg.norm(vector - np.array([0, 0, 0])) <= 1e-9:
        return 0, np.array([0, 1, 0])
    angle = np.arccos(np.dot(vect, vertical))

    return angle, vector


def get_rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac), 0],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab), 0],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc, 0],
                     [0, 0, 0, 1]])


def main():
    get_rot_from_vert([1, 0, 0], [1, 1, 1])


if __name__ == '__main__':
    main()
