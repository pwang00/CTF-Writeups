import requests
from base64 import b64decode as d, b64encode as e
import hlextend

def sice():
    new = "http://crypto.chal.csaw.io:5003/new"
    view = "http://crypto.chal.csaw.io:5003/view"

    data = {"author": "a", "note" : "a"}

    r = requests.post(new, data = data)
    print(r.text)

    hashes = []
    for k in range(1, 200):
        sha = hlextend.new("sha1")

        data = sha.extend('&admin=True&access_sensitive=True&entrynum=7', 'admin=False&access_sensitive=False&author=a&note=a&entrynum=783', k, 
            '9cd6a40678d84d3c407ef7f23ee21e8c65c8d4b2')

        forged = sha.hexdigest()
        sice = {"id": e(data), "integrity": forged}
        r2 = requests.post(view, data = sice)
        print(r2.text)


if __name__ == "__main__":
    sice()
        
