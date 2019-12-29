from .vector import Vector


class Object:
    index = 0

    def __init__(self, **kwargs):
        if 'label' in kwargs:
            self.label = kwargs['label']
        else:
            self.label = f'Object {Object.index}'
            Object.index += 1

        self.mass = kwargs['mass']
        self.position = (
            Vector(kwargs['position'][0], kwargs['position'][1])
            if 'position' in kwargs else
            Vector(0, 0)
        )
        self.velocity = (
            Vector(kwargs['velocity'][0], kwargs['velocity'][1])
            if 'velocity' in kwargs else
            Vector(0, 0)
        )

    def __repr__(self):
        return (
            f'{self.label}\n'
            f'Mass: {self.mass}\n'
            f'Position: {self.position}\n'
            f'Velocity: {self.velocity}\n'
        )
