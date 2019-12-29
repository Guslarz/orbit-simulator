from backend import get_response
from orbit_simulator.vector import Vector

from flask import Flask, make_response, request, render_template, jsonify
from scipy.constants import speed_of_light


app = Flask(__name__)


@app.route('/')
def frontend():
    return render_template('index.html')


@app.route('/backend', methods=['POST'])
def backend():
    star_mass_m = request.form.get('star_mass_m', type=float)
    star_mass_e = request.form.get('star_mass_e', type=float)

    planet_mass_m = request.form.get('planet_mass_m', type=float)
    planet_mass_e = request.form.get('planet_mass_e', type=float)

    planet_position_x_m = request.form.get('planet_position_x_m', type=float)
    planet_position_x_e = request.form.get('planet_position_x_e', type=float)

    planet_position_y_m = request.form.get('planet_position_y_m', type=float)
    planet_position_y_e = request.form.get('planet_position_y_e', type=float)

    planet_velocity_x_m = request.form.get('planet_velocity_x_m', type=float)
    planet_velocity_x_e = request.form.get('planet_velocity_x_e', type=float)

    planet_velocity_y_m = request.form.get('planet_velocity_y_m', type=float)
    planet_velocity_y_e = request.form.get('planet_velocity_y_e', type=float)

    try:
        star_mass = star_mass_m * 10 ** star_mass_e
        planet_mass = planet_mass_m * 10 ** planet_mass_e
        planet_position_x = planet_position_x_m * 10 ** planet_position_x_e
        planet_position_y = planet_position_y_m * 10 ** planet_position_y_e
        planet_velocity_x = planet_velocity_x_m * 10 ** planet_velocity_x_e
        planet_velocity_y = planet_velocity_y_m * 10 ** planet_velocity_y_e
    except TypeError:
        return make_response(jsonify({
            "error": "Błędna wartość"
        }))

    if star_mass < planet_mass * 10 ** 5:
        return make_response(jsonify({
            "error": "Masa gwiazdy powinna być znacząco większa od masy planety"
        }))

    if abs(Vector(planet_velocity_x, planet_velocity_y)) > speed_of_light:
        return make_response(jsonify({
            "error": "Planeta nie może poruszać się szybciej niż światło"
        }))

    data = get_response(star_mass, planet_mass, planet_position_x,
                        planet_position_y, planet_velocity_x, planet_velocity_y)

    return make_response(jsonify(data), 200)


if __name__ == '__main__':
    app.run()
