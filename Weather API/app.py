from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

API_KEY = open("API_KEY.txt").read().strip()

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
    
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&units=metric&appid={API_KEY}"

    response = requests.get(url)
    data = response.json()
    print(data)

    ciudad = data['name']
    temperatura = data['main']['temp']
    nubes = data['clouds']['all']
    humedad = data['main']['humidity']
    
    return render_template('clima.html', temp=temperatura, city=ciudad, clouds=nubes, hum=humedad)  


if __name__ == '__main__':
    app.run(debug=True)