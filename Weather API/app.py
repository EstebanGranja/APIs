from flask import Flask, request, jsonify, render_template
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/clima', methods=['GET'])
def obtener_clima():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({"error": "Latitud o longitud no proporcionadas"}), 400
    else:
        print(f"Latitud: {lat}, Longitud: {lon}")
    
    current_weather = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&units=metric&appid={API_KEY}"
    forecast = f"api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}"

    
    response = requests.get(current_weather)
    data = response.json()
    print(data)

    ciudad = data['name']
    temperatura = data['main']['temp']
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    nubes = data['clouds']['all']
    humedad = data['main']['humidity']
    desc = data['weather'][0]['description']
        

    
    return render_template('clima.html', temp=temperatura, temp_min=temp_min, temp_max=temp_max, city=ciudad, clouds=nubes, hum=humedad, desc=desc)  


if __name__ == '__main__':
    app.run(debug=True)