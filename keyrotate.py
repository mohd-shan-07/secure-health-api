import os, glob, json
from cryptography.fernet import Fernet
old_key = open('keys/data.key','rb').read()
new_key = Fernet.generate_key()
open('keys/data.key.new','wb').write(new_key)
from cryptography.fernet import Fernet as F
old, new = F(old_key), F(new_key)
for f in glob.glob('data/*.bin'):
    enc = open(f,'rb').read()
    dec = old.decrypt(enc)
    re = new.encrypt(dec)
    open(f,'wb').write(re)
os.replace('keys/data.key.new','keys/data.key')
print('Rotation complete')