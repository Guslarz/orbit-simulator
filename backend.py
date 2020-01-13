from orbit_simulator.object import Object
from orbit_simulator.orbit import Orbit
from orbit_simulator.simulation import Simulation
from orbit_simulator.vector import Vector

from matplotlib import pyplot
from matplotlib.backends.backend_agg import FigureCanvasAgg
from io import BytesIO
from base64 import b64encode


def get_response(sun_mass: float, planet_mass: float, planet_x: float, planet_y: float,
                 planet_vx: float, planet_vy: float):
    sun = Object(mass=sun_mass)
    planet = Object(
        mass=planet_mass,
        position=(planet_x, planet_y),
        velocity=(planet_vx, planet_vy)
    )
    orbit = Orbit(sun, planet)
    simulation = Simulation(orbit, delta_phi=0.01)

    x, y = [], []
    for vector in simulation:
        x.append(vector.x)
        y.append(vector.y)

    fig = pyplot.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect(aspect='equal', adjustable='datalim')
    ax.set_title('Wyznaczona orbita')
    ax.ticklabel_format(axis='both', style='sci', useMathText=True)
    ax.grid(b=True, linewidth=0.5)
    ax.set_xlabel('x[m]');
    ax.set_ylabel('y[m]')
    fig.patch.set_facecolor('#eeeeee')

    ax.plot(x, y)

    ax.plot(0, 0, 'ro')
    ax.plot(planet_x, planet_y, 'bo')

    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim();
    if orbit.e >= 1:
        ax.set_xlim(.9 * x_min, .9 * x_max)
        ax.set_ylim(.9 * y_min, .9 * y_max)
    plot_unit = (x_max - x_min) / 10

    velocity_arrow = Vector(
        planet_vx, planet_vy
    ).unit_vector() * plot_unit
    ax.arrow(
        planet_x, planet_y,
        velocity_arrow.x, velocity_arrow.y,
        width=0.01 * plot_unit,
        head_width=0.1 * plot_unit, head_length=0.1 * plot_unit
    )

    output = BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    img = 'data:image/png;base64,' + b64encode(output.getvalue()).decode('utf8')

    return {
        'img': img,
        'data': {
            'shape': {
                'value': 'elipsa' if orbit.e < 1 else 'hiperbola' if orbit.e > 1 else 'parabola'
            },
            'angular-momentum': {
                'value': orbit.L,
                'unit': '<sup>kg&middot;m<sup>2</sup></sup>&frasl;<sub>s</sub>'
            },
            'energy': {
                'value': orbit.E,
                'unit': "J"
            },
            'eccentricity': {
                'value': orbit.e
            }
        }
    }

