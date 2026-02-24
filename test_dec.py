from app import storage

# Retrieve decrypted
retrieved = storage.get_record("patient456")
print("Retrieved record:", retrieved)