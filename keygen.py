from cryptography.fernet import Fernet
open('keys/data.key','wb').write(Fernet.generate_key())
print('Key generated')