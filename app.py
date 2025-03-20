from flask import Flask, render_template, request
import socket

app = Flask(__name__)

def scan_ports(target, start, end):
    open_ports = []
    for port in range(start, end + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        if sock.connect_ex((target, port)) == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

def check_password(password):
    score = 0
    feedback = []
    if len(password) >= 8: score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in "!@#$%^&*" for c in password): score += 1
    strength = "Weak" if score < 2 else "Moderate" if score < 4 else "Strong"
    return strength, feedback

@app.route("/", methods=["GET", "POST"])
def dashboard():
    ports = []
    password_result = ""
    if request.method == "POST":
        if "scan" in request.form:
            ports = scan_ports("127.0.0.1", 1, 100)
        elif "check" in request.form:
            password = request.form["password"]
            strength, _ = check_password(password)
            password_result = f"Password Strength: {strength}"
    return render_template("index.html", ports=ports, password_result=password_result)

if __name__ == "__main__":
    app.run(debug=True)