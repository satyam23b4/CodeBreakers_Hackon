from flask import Flask, request, jsonify, send_from_directory
import joblib
import numpy as np

app = Flask(__name__, static_folder='static', static_url_path='')

# Load your trained model
model = joblib.load('keystroke_fraud_model.pkl')

def extract_features(key_events, mouse_events):
    # Compute dwell & flight times
    down_times = {}
    dwell_times = []
    flight_times = []
    prev_keydown = None
    delete_count = 0
    total_keys = 0

    for ev in key_events:
        if ev['type']=='down':
            total_keys += 1
            if prev_keydown is not None:
                flight_times.append(ev['time'] - prev_keydown)
            prev_keydown = ev['time']
            down_times[ev['key']] = ev['time']
        elif ev['type']=='up' and ev['key'] in down_times:
            dwell_times.append(ev['time'] - down_times.pop(ev['key']))
        if ev['key'].lower() in ['backspace','delete']:
            delete_count += 1

    # Basic stats
    import statistics
    md = statistics.mean(dwell_times) if dwell_times else 0.0
    sd = statistics.pstdev(dwell_times) if dwell_times else 0.0
    mf = statistics.mean(flight_times) if flight_times else 0.0
    sf = statistics.pstdev(flight_times) if flight_times else 0.0
    dr = delete_count/(total_keys or 1)*100

    # Mouse dynamics
    speeds, accels = [], []
    prev = None
    for ev in mouse_events:
        if prev:
            dt = ev['time'] - prev['time']
            dist = ((ev['x']-prev['x'])**2 + (ev['y']-prev['y'])**2)**0.5
            if dt>0:
                sp = dist/dt
                speeds.append(sp)
                if len(speeds)>1:
                    accels.append(abs(sp - speeds[-2]))
        prev = ev
    avg_sp = sum(speeds)/len(speeds) if speeds else 0.0
    std_acc = statistics.pstdev(accels) if accels else 0.0

    return np.array([[md, mf, avg_sp, std_acc, dr]])

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    key_events = data.get('keyEvents', [])
    mouse_events = data.get('mouseEvents', [])
    features = extract_features(key_events, mouse_events)
    proba = model.predict_proba(features)[0][1]
    label = 'Fraudulent' if proba>0.8 else 'Genuine'
    return jsonify({'probability': round(proba,3), 'label': label})

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
