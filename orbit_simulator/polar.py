from .vector import Vector

from math import atan2, sin, cos


class Polar:
    def __init__(self, r, phi):
        self.r = r
        self.phi = phi

    @staticmethod
    def from_vector(vector: Vector):
        return Polar(abs(vector), atan2(vector.y, vector.x))

    def to_vector(self):
        """X Y"""
        return Vector(self.r * cos(self.phi), self.r * sin(self.phi))

    def __repr__(self):
        return f'({self.r}, {self.phi} rad)'
