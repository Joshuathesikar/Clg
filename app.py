from flask import Flask, send_from_directory
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('.', 'frontend.html')   # Serve the frontend.html

@app.route('/run-script')
def run_script():
    subprocess.Popen(["python", "main.py"], shell=True)  # This runs main.py
    return "Running main.py!"

if __name__ == "__main__":
    app.run(port=5000)
