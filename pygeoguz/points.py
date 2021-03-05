from dataclasses import dataclass


@dataclass
class Point2D:
    x: float
    y: float


@dataclass
class Point3D(Point2D):
    z: float


@dataclass
class PointBL:
    b: float
    l: float
