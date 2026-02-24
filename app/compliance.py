import time, json, os
from flask import g

AUDIT_FILE = 'audit.log'
RETENTION_DAYS = int(os.environ.get('RETENTION_DAYS','30'))

def audit_log(action, pid):
    user = getattr(g, 'user', {})
    log_entry = {
        'user': user.get('preferred_username', 'unknown'),
        'action': action,
        'patient_id': pid
    }
    print(log_entry)
    """ entry = {
        'ts': int(time.time()),
        'user': request.user.get('preferred_username','unknown'),
        'action': action,
        'resource': pid,
        'ip': request.remote_addr
    }
    with open(AUDIT_FILE,'a') as f:
        f.write(json.dumps(entry)+'\n')
 """
def data_minimize(payload):
    #allowed = {k: payload[k] for k in ['id','name','dob','consent'] if k in payload}
    allowed = {k: payloads[k] for k in ['id','name','dob','consent'] if k in payload}
    return allowed

def enforce_consent(payload):
    if not payload.get('consent', False):
        raise ValueError('Consent required')

def retention_cleanup():
    cutoff = time.time() - RETENTION_DAYS*24*3600
    # stub: you’d scan files with timestamps and remove older than cutoff
    return cutoff