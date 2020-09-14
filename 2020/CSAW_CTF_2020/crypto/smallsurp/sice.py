import requests
import json
import hashlib
import re
from Crypto.Protocol.SecretSharing import Shamir
from Crypto.Cipher import AES

from binascii import unhexlify

pattern = r"\d?\d?:[a-z0-9]{30,32}"
def xor_data(binary_data_1, binary_data_2):
    return bytes([b1 ^ b2 for b1, b2 in zip(binary_data_1, binary_data_2)])

def hmac_sha256(key, message):
    if len(key) > 64:
        key = sha256(key).digest()
    if len(key) < 64:
        key += b'\x00' * (64 - len(key))

    o_key_pad = xor_data(b'\x5c' * 64, key)
    i_key_pad = xor_data(b'\x36' * 64, key)
    return hashlib.sha256(o_key_pad + hashlib.sha256(i_key_pad + message).digest()).hexdigest()

def compute_hmac():
    base = "http://crypto.chal.csaw.io:5005"

    usernames = ['Jere', 'Lakisha', 'Loraine', 'Ingrid', 'Orlando', 'Berry', 'Alton', 'Bryan', 'Kathryn', 'Brigitte', 'Dannie', 'Jo', 'Leslie', 'Adrian', 'Autumn', 'Kellie', 'Alphonso', 'Joel', 'Alissa', 'Rubin']
    secrets = []
    for username in usernames:
        user = "http://crypto.chal.csaw.io:5005/dash/" + username
        query = {"username": username,
                 "token1":"240813191444383683610874141529779860149197802230704769987870099100087528009907833040793311446806654962619628779479768893754046830059506665136223928945955844493985860589048372285183371960781762148318571728054479065130190173251314874819258678950694281789476446925580245284216649024815216185549537539602050443878"}

        decoded = None
        
        with requests.Session() as sess:
            r = sess.post(base, data=query)

            try:
                decoded = json.loads(r.text)

            except:
                pass
            
            if not decoded:
                raise

            salt = decoded["nacl"]
            #print(salt)
            K = hashlib.sha256(str(0).encode()).digest()
            hmac = hmac_sha256(K, salt.encode())
            #print(hmac)

            query = {"hmac": hmac}
            r = sess.get(user, params=query)
            idx, share = re.findall(pattern, r.text)[0].split(":")
            secrets.append((int(idx), unhexlify(share)))

    key = Shamir.combine(secrets)
    print(key)
    iv = unhexlify("254dc5ae7bb063ceaf3c2da953386948")
    ctext = unhexlify("08589c6b40ab64c434064ec4be41c9089eefc599603bc7441898c2e8511d03f6")
    
    c = AES.new(key, AES.MODE_CBC, iv)
    print(c.decrypt(ctext))
        


if __name__ == "__main__":
    compute_hmac()
