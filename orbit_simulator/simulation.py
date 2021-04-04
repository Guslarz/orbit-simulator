from .orbit import Orbit
from .polar import Polar

from scipy.constants import pi
from math import acos


class Simulation:
    def __init__(self, orbit: Orbit, **kwargs):
        self.orbit = orbit

        self.phi = 0
        self.delta_phi = (
            kwargs['delta_phi'] if 'delta_phi' in kwargs
            else 0.01
        )

        self.index = 0

        self.iterator = (
            Elliptic(orbit, self.delta_phi)
            if orbit.e < 1 else
            Hyperbolic(orbit, self.delta_phi)
            if orbit.e > 1 else
            Parabolic(orbit, self.delta_phi)
        )

    def __iter__(self):
        self.iterator.set_next()
        return self.iterator


class SimulationIterator:
    def __init__(self, orbit: Orbit, delta_phi: int):
        self.orbit = orbit
        self.delta_phi = delta_phi

        self.current = None
        self.next = None

    def set_next(self):
        pass

    def end(self) -> bool:
        pass

    def __next__(self):
        if self.end():
            raise StopIteration

        self.set_next()
        return self.current


class Elliptic(SimulationIterator):
    def __init__(self, orbit: Orbit, delta_phi: int):
        super().__init__(orbit, delta_phi)

        self.phi = 0

    def set_next(self):
        self.current = self.next
        self.next = Polar(
            self.orbit.r(self.phi),
            self.phi
        ).to_vector()
        self.phi += self.delta_phi

    def end(self):
        return self.phi > 2 * pi + self.delta_phi


class Hyperbolic(SimulationIterator):
    def __init__(self, orbit: Orbit, delta_phi: int):
        super().__init__(orbit, delta_phi)

        self.phi = self.orbit.phi0 + pi / 2 + pi / 4
        self.end_phi = self.orbit.phi0 + 3 * pi / 2 - pi / 4

    def set_next(self):
        self.current = self.next
        next_polar = Polar(
            self.orbit.r(self.phi),
            self.phi
        )
        
        self.next = next_polar.to_vector()
        self.phi += self.delta_phi

    def end(self):
        return self.phi >= self.end_phi


class Parabolic(Hyperbolic):
    def __init__(self, orbit: Orbit, delta_phi: int):
        super().__init__(orbit, delta_phi)
