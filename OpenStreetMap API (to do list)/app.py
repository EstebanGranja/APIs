from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder="templates")

tasks = [{"task": "Do dishes", "done": False}]

@app.route('/')
def home():
	return render_template("index.html", to_do=tasks)



@app.route("/add", methods=["POST"])
def add_task():
    task = request.form['to_do_form']
    tasks.append({"task": task, "done": False}) # Set task not done by default
    return redirect(url_for("home"))  



@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit_task(index):
    edited_task = tasks[index]
    if request.method == "GET":
        return render_template("edit.html", edited_task=edited_task, index=index) # Edit template
    else:
        edited_task["task"] = request.form["to_do_form"] # Update task
        return redirect(url_for("home"))



@app.route("/check/<int:index>")
def check_task(index):
    tasks[index]['done'] = not tasks[index]['done'] # Changes if task is done or not
    return redirect(url_for("home"))



@app.route("/delete/<int:index>")
def delete_task(index):
    del tasks[index]
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
