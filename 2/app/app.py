from flask import Flask
from prometheus_client import Counter, generate_latest, REGISTRY

app = Flask(__name__)

REQUEST_COUNT = Counter('app_requests_total', 'Total number of requests')

@app.route('/')
def hello():
    REQUEST_COUNT.inc()  
    return "Work"

@app.route('/metrics')
def metrics():
    return generate_latest(REGISTRY), 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
