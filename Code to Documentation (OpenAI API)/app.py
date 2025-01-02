from flask import Flask, render_template, request
import openai
from openai import OpenAI
import os


API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")
openai.api_key = API_KEY

client = OpenAI()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/response', methods=["POST"])
def response():
    # get code and action from the form
    code = request.form.get("code")
    action = request.form.get("action")
    
    # get detailed prompt
    if action == "document":
        prompt = f"Make detail documentation about this code:\n\n{code}"

    elif action == "comment":
        prompt = f"Add useful comments into this code:\n\n{code}"
    
    elif action == "optimize":
        prompt = f"Optimize this code, make it faster:\n\n{code}"
    
    # get response from GPT-4
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in code documentation and optimization"},
            {"role": "user", "content": prompt}
        ]
    )

    result = response.choices[0].message["content"]

    return render_template("result.html", action=action, result=result)
        

if __name__ == '__main__':
    app.run(debug=True)