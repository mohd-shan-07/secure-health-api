from app import storage

# Example record
record = {
    "patient_id": "patient123",
    "name": "Alice",
    "diagnosis": "Hypertension",
    "treatment": "Lifestyle + medication"
}

# Save encrypted
pid = storage.save_record(record)
print("Saved record with ID:", pid)