from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

API_KEY = open("API_KEY.txt").read().strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/obtener_clima', methods=['GET'])
def obtener_clima():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({"error": "Latitud o longitud no proporcionadas"}), 400
    else:
        print(f"Latitud: {lat}, Longitud: {lon}")
        
    return render_template('index.html', lat=lat, lon=lon)  