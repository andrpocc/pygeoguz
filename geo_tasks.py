import math
from random import normalvariate

import numpy as np
import pandas as pd
from sympy import Segment, Point


def to_degrees(degrees: int, minutes: float, seconds: float = 0) -> float:
    """
    Преобразование dms -> d
    :param degrees: Градусы
    :param minutes: Минуты
    :param seconds: Секунды
    :return: Градусы
    """
    return degrees + minutes / 60 + seconds / 3600


def to_d_m_s(degrees: float) -> tuple:
    """
    Преобразвоание d -> dms
    :param degrees: Градусы
    :return: Кортеж (градусы, минуты, секунды)
    """
    d = math.trunc(degrees)
    m = math.trunc((degrees - d) * 60)
    s = round(((degrees - d) - m / 60) * 60 * 60)
    return d, m, s


def ogz_points(xa: float, ya: float, xb: float, yb: float) -> tuple:
    """
    Обратная геодезическая задача для координат пунктов
    :param xa: Координата х первого пункта линии
    :param ya: Координата у первого пункта линии
    :param xb: Координата х второго пункта линии
    :param yb: Координата у второго пункта линии
    :return: Кортеж (градусы, минуты, секунды, горизонтальное проложение)
    """
    delx = xb - xa
    dely = yb - ya
    s = math.sqrt(delx ** 2 + dely ** 2)

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

    g = math.trunc(alf)
    m = math.trunc((alf - g) * 60)
    c = round(((alf - g) - m / 60) * 60 * 60)
    return g, m, c, s


def ogz_delta(dx: float, dy: float) -> tuple:
    """
    Обратная геодезическая задача для приращений координат
    :param dx: Приращение по х
    :param dy: Приращенеи по у
    :return: Кортеж (дирекционный угол, горизонтальное приложение)
    """
    delx = dx
    dely = dy
    s = math.sqrt(delx ** 2 + dely ** 2)
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
    return alf, s


def pgz(x1: float, y1: float, g: int, m: int, c: float, s: float) -> tuple:
    """
    Прямая геодезическая задача
    :param x1: Координата х пункта
    :param y1: Координата у пункта
    :param g: Дирекционный угол (градусы)
    :param m: Дирекционный угол (минуты)
    :param c: Дирекционный угол (секунды)
    :param s: Горизонтальное проложение
    :return: Кортеж координат вычисляемого пункта
    """
    angle = g + m / 60 + c / (60 * 60)
    angle = math.radians(angle)
    x2 = x1 + s * math.cos(angle)
    y2 = y1 + s * math.sin(angle)
    return x2, y2


def polygon_square(points: list) -> float:
    """
    Площадь полигона по координатам его вершин
    Формула Гаусса
    :param points: Список координат вершин полигона
    :return: Значение площади
    """
    sx = 0
    sy = 0
    n = len(points)
    for i in range(n):
        if i != n - 1:
            sx += points[i][0] * points[i + 1][1]
        elif i == n - 1:
            sx += points[i][0] * points[0][1]
    for i in range(n):
        if i != n - 1:
            sy -= points[i][1] * points[i + 1][0]
        elif i == n - 1:
            sy -= points[i][1] * points[0][0]
    square = math.fabs(sx + sy) / 2
    return square


def midpoint(x1: float, y1: float, x2: float, y2: float) -> tuple:
    """
    Координаты середины отрезка
    :param x1: Координата х первого пункта
    :param y1: Координата у первого пункта
    :param x2: Координата х второго пункта
    :param y2: Координата у второго пункта
    :return: Кортеж координат середины отрезка
    """
    xm = (x1 + x2) / 2
    ym = (y1 + y2) / 2
    return xm, ym


def intersection_of_segments(p1_x: Point, p1_y: Point, p2_x: Point, p2_y: Point) -> tuple:
    """
    Координаты точки пересечения двух отрезков
    :param p1_x: Первая точка первого отрезка
    :param p1_y: Вторая точка первого отрезка
    :param p2_x: Первая точка второго отрезка
    :param p2_y: Вторая точка второго отрезка
    :return: Кортеж координат точки пересечения отрезков
    """
    s1 = Segment(p1_y, p1_x)
    s2 = Segment(p2_y, p2_x)
    intersection = s1.intersection(s2)
    if len(intersection) != 0:
        intersection = intersection[0]
        return float(intersection.y), float(intersection.x)
    else:
        return 0, 0


def adjustment_traverse(first_directional_angle: float, last_directional_angle: float, angles: list,
                        horizontal_layings: list, first_point: list, last_point: list, left_angle=True) -> pd.DataFrame:
    """
    Раздельный метод уравнивание теодолитного хода
    :param first_directional_angle: Дирекционный угол исходной линии хода
    :param last_directional_angle: Дирекционный угол замыкающей линии хода
    :param angles: Горизонтальные углы
    :param horizontal_layings: Горизонтальные проложения
    :param first_point: Начальный опорный пункт
    :param last_point: Замыкающий опорный пункт
    :param left_angle: По умолчанию горизонтальные углы приняты за левые
    :return: DataFrame уравненных координат пунктов хода
    """
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
        directional_angles = list()
        directional_angles.append(first_directional_angle + corrected_angles[0] - 180)
        for i in range(len(corrected_angles) - 2):
            dir_angle = directional_angles[i] + corrected_angles[i + 1] - 180
            if dir_angle > 360:
                directional_angles.append(dir_angle - 360)
            elif dir_angle < 0:
                directional_angles.append(dir_angle + 360)
            else:
                directional_angles.append(dir_angle)
    else:
        directional_angles = list()
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
    corrected_delta_x = np.round(delta_x_array + correction_delta_x, 3)
    corrected_delta_y = np.round(delta_y_array + correction_delta_y, 3)
    x_coordinates = list()
    x_coordinates.append(round(first_point[0] + corrected_delta_x[0], 3))
    for i in range(len(corrected_delta_x) - 2):
        x_coordinates.append(x_coordinates[i] + corrected_delta_x[i + 1])
    y_coordinates = list()
    y_coordinates.append(round(first_point[1] + corrected_delta_y[0], 3))
    for i in range(len(corrected_delta_y) - 2):
        y_coordinates.append(y_coordinates[i] + corrected_delta_y[i + 1])
    coordinates_of_traverse = pd.DataFrame()
    coordinates_of_traverse['x'] = x_coordinates
    coordinates_of_traverse['y'] = y_coordinates
    return coordinates_of_traverse


def generate_errors(mu: float, count: int) -> list:
    """
    Генерация списка псевдослучайных ошибок,
    подчиняющихся нормальному закону распределения
    :param mu: среднее квадартическое отклонение
    :param count: Количество ошибок для генерации
    :return: Список ошибок
    """
    errors = list()
    for i in range(count):
        errors.append(round(normalvariate(0, mu), 0))
    return errors
