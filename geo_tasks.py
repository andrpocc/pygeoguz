import math
from sympy import Segment, Point
import numpy as np
import pprint


def to_degrees(degrees: int, minutes: float, seconds: float = 0):
    return degrees + minutes / 60 + seconds / 3600


def to_d_m_s(degrees: float):
    d = math.trunc(degrees)
    m = math.trunc((degrees - d) * 60)
    s = round(((degrees - d) - m / 60) * 60 * 60)
    return [d, m, s]


def ogz_points(xa, ya, xb, yb):
    """Обратная геодезическая задача"""
    delx = xb - xa
    dely = yb - ya
    S = math.sqrt(delx ** 2 + dely ** 2)
    if dely == 0 and delx > 0:
        alf = 0
    elif dely == 0 and delx < 0:
        alf = 180
    elif delx == 0 and dely > 0:
        alf = 90
    elif delx == 0 and dely < 0:
        alf = 270
    else:
        rumb = math.fabs(math.degrees(math.atan(dely / delx)))

        if delx > 0 and dely > 0:
            alf = rumb

        elif delx < 0 and dely > 0:
            alf = 180 - rumb

        elif delx < 0 and dely < 0:
            alf = 180 + rumb

        elif delx > 0 and dely < 0:
            alf = 360 - rumb

    G = math.trunc(alf)
    M = math.trunc((alf - G) * 60)
    C = round(((alf - G) - M/60) * 60 * 60)
    return G, M, C, S


def ogz_delta(dx, dy):
    """Обратная геодезическая задача"""
    delx = dx
    dely = dy
    S = math.sqrt(delx ** 2 + dely ** 2)
    if dely == 0 and delx > 0:
        alf = 0
    elif dely == 0 and delx < 0:
        alf = 180
    elif delx == 0 and dely > 0:
        alf = 90
    elif delx == 0 and dely < 0:
        alf = 270
    else:
        rumb = math.fabs(math.degrees(math.atan(dely / delx)))

        if delx > 0 and dely > 0:
            alf = rumb

        elif delx < 0 and dely > 0:
            alf = 180 - rumb

        elif delx < 0 and dely < 0:
            alf = 180 + rumb

        elif delx > 0 and dely < 0:
            alf = 360 - rumb
    return alf


def pgz(X1, Y1, G, M, C, S):
    """Прямая геодезическая задача"""
    angle = G + M/60 + C/(60*60)
    angle = math.radians(angle)
    X2 = X1 + S * math.cos(angle)
    Y2 = Y1 + S * math.sin(angle)
    return X2, Y2


def polygon_square(points):
    """Площадь полигона по координатам точек"""
    sx = 0
    sy = 0
    n = len(points)

    for i in range(n):
        if i != n-1:
            sx += points[i][0] * points[i+1][1]
        elif i == n-1:
            sx += points[i][0] * points[0][1]

    for i in range(n):
        if i != n-1:
            sy -= points[i][1] * points[i+1][0]
        elif i == n-1:
            sy -= points[i][1] * points[0][0]

    s = math.fabs(sx + sy) / 2
    return s


def midpoint(x1, y1, x2, y2):
    """Координаты середины отрезка"""
    xm = (x1 + x2)/2
    ym = (y1 + y2)/2
    return xm, ym


def intersection_of_segments(p1_x, p1_y, p2_x, p2_y):
    """Координаты точки пересечения двух отрезков"""
    s1 = Segment(p1_y, p1_x)
    s2 = Segment(p2_y, p2_x)
    intersection = s1.intersection(s2)
    if len(intersection) != 0:
        intersection = intersection[0]
        return float(intersection.y), float(intersection.x)
    else:
        return 0, 0


def adjustment_theodolite_course(first_directional_angle: float, last_directional_angle: float, angles: list, horizontal_layings: list, first_point: list, last_point: list, left_angle=True):
    angles_array = np.array(angles)
    horizontal_layings_array = np.array(horizontal_layings)
    number_of_angles = len(angles)
    practical_sum_of_angles = np.sum(angles)
    if left_angle:
        theoretical_sum_of_angles = last_directional_angle - first_directional_angle + 180 * number_of_angles
    else:
        theoretical_sum_of_angles = first_directional_angle - last_directional_angle + 180 * number_of_angles
    angular_residual = practical_sum_of_angles - theoretical_sum_of_angles
    correction = -angular_residual / number_of_angles
    corrected_angles = angles_array + correction
    if left_angle:
        directional_angles = []
        directional_angles.append(first_directional_angle + corrected_angles[0] - 180)
        for i in range(len(corrected_angles) - 2):
            directional_angles.append(directional_angles[i] + corrected_angles[i + 1] - 180)
    else:
        directional_angles = []
        directional_angles.append(first_directional_angle - corrected_angles[0] + 180)
        for i in range(len(corrected_angles) - 2):
            directional_angles.append(directional_angles[i] - corrected_angles[i + 1] + 180)
    directional_angles_array = np.array(directional_angles)
    delta_x_array = horizontal_layings_array * np.cos(np.radians(directional_angles_array))
    delta_y_array = horizontal_layings_array * np.sin(np.radians(directional_angles_array))
    theoretical_sum_of_delta_x = last_point[0] - first_point[0]
    theoretical_sum_of_delta_y = last_point[1] - first_point[1]
    practical_sum_of_delta_x = sum(delta_x_array)
    practical_sum_of_delta_y = sum(delta_y_array)
    delta_x_residual = practical_sum_of_delta_x - theoretical_sum_of_delta_x
    delta_y_residual = practical_sum_of_delta_y - theoretical_sum_of_delta_y
    sum_of_layings = sum(horizontal_layings)
    correction_delta_x = -delta_x_residual * horizontal_layings_array / sum_of_layings
    correction_delta_y = -delta_y_residual * horizontal_layings_array / sum_of_layings
    corrected_delta_x = delta_x_array + correction_delta_x
    corrected_delta_y = delta_y_array + correction_delta_y
    x_coordinates = []
    x_coordinates.append(first_point[0] + corrected_delta_x[0])
    for i in range(len(corrected_delta_x) - 2):
        x_coordinates.append(x_coordinates[i] + corrected_delta_x[i + 1])
    y_coordinates = []
    y_coordinates.append(first_point[1] + corrected_delta_y[0])
    for i in range(len(corrected_delta_y) - 2):
        y_coordinates.append(y_coordinates[i] + corrected_delta_y[i + 1])
    return [x_coordinates, y_coordinates]

right_angles = [to_degrees(302, 40), to_degrees(159, 25.5), to_degrees(189, 52.5,),
                to_degrees(268, 30.5)]
layings = [235.84, 415, 236]
first_point = [6093.62, 1984.51]
last_point = [5562.24, 2682.9]
answer = adjustment_theodolite_course(to_degrees(237, 26.1), to_degrees(36, 58.3), right_angles, layings, first_point, last_point, left_angle=False)
pprint.pprint(answer)

