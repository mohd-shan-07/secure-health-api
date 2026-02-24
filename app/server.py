from flask import Flask, request, jsonify
from auth import verify_jwt, require_roles
from compliance import audit_log
from storage import save_record, get_record
from prometheus_client import Counter, Histogram, generate_latest

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('api_requests_total', 'Total API requests', ['endpoint', 'method', 'status'])
REQ_LATENCY = Histogram('api_request_latency_seconds', 'Latency', ['endpoint'])

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'}

print("before calling GET require_role")
@app.route('/records/<pid>', methods=['GET'])
@verify_jwt
@require_roles(['viewer', 'editor'])
def get_patient(pid):
    with REQ_LATENCY.labels('/records').time():
        data = get_record(pid)
    audit_log('READ', pid)
    status = 200 if data else 404
    REQUEST_COUNT.labels('/records', 'GET', str(status)).inc()
    return (jsonify(data), status) if data else (jsonify({'error': 'not found'}), 404)

print("before calling POST require_role")
@app.route('/records', methods=['POST'])
@verify_jwt
@require_roles(['editor'])
def create_patient():
    payload = request.get_json()
    pid = save_record(payload)
    audit_log('CREATE', pid)
    REQUEST_COUNT.labels('/records', 'POST', '201').inc()
    return jsonify({'id': pid}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8443, ssl_context=('certs/server.crt', 'certs/server.key'))