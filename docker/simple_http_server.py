from flask import Flask
import random
import socket

app = Flask(__name__)

@app.route('/')
def index():
    hostname = socket.gethostname()
    return f"Под: {hostname}, Рандомное число: {random.randint(1, 100)}\n"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)