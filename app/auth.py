import os
import requests
import jwt
from functools import wraps
from flask import request, jsonify, g

os.environ["OIDC_ISSUER"] = "http://localhost:8080/realms/health"
os.environ["OIDC_AUDIENCE"] = "account"

ISSUER = os.environ.get('OIDC_ISSUER')
AUD = os.environ.get('OIDC_AUDIENCE', 'health-api')

def _jwks():
    r = requests.get(f"{ISSUER}/.well-known/openid-configuration")
    jwks_uri = r.json()['jwks_uri']
    return requests.get(jwks_uri).json()

def verify_jwt(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return jsonify({'error': 'missing token'}), 401
        token = auth.split(' ', 1)[1]
        try:
            jwks = _jwks()
            # NOTE: For production, you should verify signature using jwks keys.
            decoded = jwt.decode(
                token,
                options={"verify_signature": False, "verify_aud": False},  # ⚠️ Simplified for demo
                audience=AUD
            )
            print("Decoded claims:", decoded)
            g.user = decoded   # ✅ store claims in flask.g
            print("Decoded claims:", g.user)
            return fn(*args, **kwargs)
        except Exception as e:
            print("JWT decode error:", e)
            return jsonify({'error': 'invalid token'}), 401
    return wrapper

def require_roles(roles):
    def deco(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = getattr(g, 'user', {})
            realm_roles = user.get('realm_access', {}).get('roles', [])
            client_roles = user.get('resource_access', {}).get(AUD, {}).get('roles', [])
            print("Roles in token:", realm_roles, client_roles)
            # Check if any of the required roles are present
            if any(role in realm_roles or role in client_roles for role in roles):
                return fn(*args, **kwargs)
            print("Roles in token:", realm_roles, client_roles)
            return jsonify({'error': 'forbidden'}), 403
        return wrapper
    return deco