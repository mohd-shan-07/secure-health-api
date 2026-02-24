import sys
import jwt   # pip install pyjwt

def decode_token(token: str):
    # Decode without verifying signature (safe for debugging)
    decoded = jwt.decode(token, options={"verify_signature": False})

    print("=== Full Token Payload ===")
    for k, v in decoded.items():
        print(f"{k}: {v}")

    print("\n=== Realm Roles ===")
    print(decoded.get("realm_access", {}).get("roles", []))

    print("\n=== Client Roles ===")
    print(decoded.get("resource_access", {}))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python decode_token.py <JWT_ACCESS_TOKEN>")
        sys.exit(1)

    token = sys.argv[1]
    decode_token(token)