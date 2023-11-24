'''2. Create a Flask app that consumes data from external APIs and displays it to users.
Try to find an public API which will give you a data and based on that call it and deploy it on cloud platform'''

import requests
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template("index1.html")


@app.route('/weatherapp', methods=['POST', "GET"])
def get_weatherdata():
    url = "https://api.openweathermap.org/data/2.5/weather"

    param = {
        'q': request.form.get("city"),
        # 'appid': request.form.get('appid'),
        'appid':'411483bfc5bc843550fec681b795adc9',
        'units': request.form.get('inits')
    }
    response = requests.get(url, params=param)

    data = response.json()
    city = data['name']
    return f"data : {data}, city : {city}"


if __name__ == "__main__":
    app.run(debug=True)