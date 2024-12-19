from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder="templates")

tasks = [{"task1": "Go shopping", "done": False}]

@app.route('/')
def home():
	return render_template("index.html", to_do=tasks)

if __name__ == '__main__':
    app.run(debug=True)