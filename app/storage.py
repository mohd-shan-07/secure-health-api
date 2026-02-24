import os, json, uuid
from cryptography.fernet import Fernet

KEY_FILE = os.environ.get('APP_DATA_KEY', 'keys/data.key')
DATA_DIR = 'data'

def _key():
    with open(KEY_FILE, 'rb') as f:
        return f.read()

def _cipher():
    return Fernet(_key())

def save_record(obj):
    os.makedirs(DATA_DIR, exist_ok=True)
    pid = obj.get('patient_id') or str(uuid.uuid4())
    data = json.dumps(obj).encode('utf-8')
    enc = _cipher().encrypt(data)
    with open(os.path.join(DATA_DIR, f'{pid}.bin'), 'wb') as f:
        f.write(enc)
    return pid

def get_record(pid):
    try:
        with open(os.path.join(DATA_DIR, f'{pid}.bin'), 'rb') as f:
            enc = f.read()
        dec = _cipher().decrypt(enc)
        return json.loads(dec.decode('utf-8'))
    except FileNotFoundError:
        return None