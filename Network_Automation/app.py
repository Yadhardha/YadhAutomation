from flask import Flask, render_template, request, session, redirect, url_for
from runner import run_switch_commands
import webbrowser
import threading

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", output="")

@app.route("/store_creds", methods=["POST"])
def store_creds():
    session["username"] = request.form["username"]
    session["password"] = request.form["password"]
    return redirect(url_for("index"))

@app.route("/run_switches", methods=["POST"])
def run_switches():
    output = ""
    username = session.get("username")
    password = session.get("password")

    if not username or not password:
        return "SSH credentials missing! Please submit them first."

    num_switches = int(request.form["num_switches"])
    for i in range(1, num_switches + 1):
        host = request.form[f"host_{i}"]
        interface = request.form[f"interface_{i}"]
        output += run_switch_commands(host, username, password, interface)
        output += "\n\n"

    return render_template("index.html", output=output)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    # Open browser in a separate thread so Flask can start
    threading.Timer(1, open_browser).start()
    app.run(debug=True)