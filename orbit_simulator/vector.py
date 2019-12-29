from math import sqrt
from numpy import isscalar


class InvalidVectorOperation(Exception):
    pass


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        """ operator + """
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        """ operator += """
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        """ operator - """
        return Vector(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        """ operator -= """
        self.x += other.x
        self.y += other.y
        return self

    def __mul__(self, other):
        """ operator * (Vector, other)"""
        if isscalar(other):
            return Vector(other * self.x, other * self.y)
        elif isinstance(other, Vector):
            # iloczyn skalarny
            return self.x * other.x + self.y * other.y
        else:
            raise InvalidVectorOperation

    def __imul__(self, other):
        """ operator *= """
        if isscalar(other):
            self.x *= other
            self.y *= other
            return self
        else:
            raise InvalidVectorOperation

    def __truediv__(self, other):
        """ operator / """
        if isscalar(other):
            return Vector(self.x / other, self.y / other)
        else:
            raise InvalidVectorOperation

    def __itruediv__(self, other):
        """ operator /= """
        if isscalar(other):
            self.x /= other
            self.y /= other
        else:
            raise InvalidVectorOperation

    def __pow__(self, other):
        """Moduł iloczynu wektorowego"""
        return self.x * other.y - self.y * other.x

    def __abs__(self):
        """Długość wektora"""
        return sqrt(self.x * self.x + self.y * self.y)

    def unit_vector(self):
        """Wektor jednostkowy"""
        length = self.__abs__()
        return Vector(self.x / length, self.y / length)

    def perpendicular_vector(self, left=True):
        """Wektor prostopadły"""
        if left:
            return Vector(-self.y, self.x)
        else:
            return Vector(self.y, -self.x)

    def project_onto(self, other):
        """Rzut na other"""
        unit_vector = other.unit_vector()
        return unit_vector * (self * unit_vector)

    def __repr__(self):
        return f'({self.x}, {self.y})'

