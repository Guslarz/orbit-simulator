from .object import Object
from .polar import Polar

from scipy.constants import gravitational_constant as G, pi
from math import cos, sqrt, acos


class Orbit:
    def __init__(self, sun: Object, planet: Object):
        self.sun = sun
        self.planet = planet

        self.L = (planet.position - sun.position) ** (planet.velocity * planet.mass)
        self.E = (
            (abs(planet.velocity) ** 2) * planet.mass / 2 -
            G * sun.mass * planet.mass / abs(planet.position - sun.position)
        )
        self.p = (
            self.L ** 2 /
            (G * sun.mass * (planet.mass ** 2))
        )
        self.e = sqrt(
            1 + 2.0 * self.E * (self.L ** 2) /
            (((G * sun.mass * planet.mass) ** 2) * planet.mass)
        )

        initial_position = Polar.from_vector(
            planet.position - sun.position
        )
        tmp_phi = (self.p / initial_position.r - 1.0) / self.e
        if tmp_phi > 1.0:
            tmp_phi = 1.0
        elif tmp_phi < -1.0:
            tmp_phi = -1.0
        self.phi0 = (
            acos(
                tmp_phi
            ) - initial_position.phi
        )

    def r(self, phi):
        return self.p / (1 + self.e * cos(phi + self.phi0))

    def __repr__(self):
        return (
            f'L = {self.L}\n'
            f'E = {self.E}\n'
            f'p = {self.p}\n'
            f'\u025B = {self.e}\n'
            f'\u03C6\u2080 = {self.phi0}'
        )
