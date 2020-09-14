# Smallsurp (300) - Solved 20 mins after contest end

## Description

Your APT group scr1pt\_k1tt13z breached into a popular enterprise service, but due to inexperience, you only got the usernames of the administrators of the service, and an encrypted password for the root admin. However, you learned that the company had a key agreement ceremony at some point in time, and the administrators keys are all somehow connected to the root admin's.

http://crypto.chal.csaw.io:5005


## Overview

Abuse poor parameter checking in the web application's SRP protocol implementation to calculate the server HMAC, then recover the flag using Shamir's secret sharing.

## Solution

We're given a database, encrypted root admin password file, and the implementation of an enterprise web service (in server\_handout.py), and we're told that the admins of the service used some key agreement protocol.  Furthermore, we're told that the admin keys are all somehow related to that of the root admin.  Let's dive into the application code.

```python
@app.route("/", methods=["GET", "POST"])
def home():
    if flask.request.method == "POST":
        # omitted
        if A is None:

            flask.flash("Error encountered on server-side.")
            return flask.redirect(flask.url_for("home"))

        if A in [0, N]:
            flask.flash("Error encountered on server-side. >:)")
            return flask.redirect(flask.url_for("home"))

        xH = hasher(salt + str(pwd))
        v = modular_pow(g, xH, N)
        B = (k * v + modular_pow(g, b, N)) % N
        u = hasher(str(A) + str(B))
        S = modular_pow(A * modular_pow(v, u, N), b, N)
        K = hashlib.sha256(str(S).encode()).digest()
        flask.session["server_hmac"] = hmac_sha256(K, salt.encode())
        return flask.jsonify(nacl=salt, token2=B)
    else:
        return flask.render_template("home.html")

@app.route("/dash/<user>", methods=["POST", "GET"])
def dashboard(user):
    hmac = flask.request.args["hmac"]
    servermac = flask.session.get("server_hmac", None)
    print(hmac, servermac)
    if hmac != servermac:
        flask.flash("Incorrect password.")
        return flask.redirect(flask.url_for("home"))

    pwd = DATABASE[user]
    return flask.render_template("dashboard.html", username=user, pwd=pwd)

```

We note that the main application pretty much performs a standard password authenticated key agreement using the Secure Remote Password Protocol (SRP).  You can read more about the protocol here: [sice](https://en.wikipedia.org/wiki/Secure_Remote_Password_protocol).  In essence, we generate an ephemeral key A = g^a where g is a generator, and a, b are (supposed to be randomly chosen) values in Z/pZ for some safe prime p.  In context of this challenge though, we can just choose some random value of A and send it, along with a username, to the server as a POST request.  The server then sends us back a salt value and its ephemeral key B.  

In a perfect world, the server should be checking to see that A is not a multiple of N (i.e. `A \equiv 0 (mod N)`), but in this scenario, it's only checking to see that A is not in the _set_ `{0, N}`.  That is very bad! (for the server, of course.)  We can just set A to be c * N for some integer c > 1, which causes `S = modular_pow(A * modular_pow(v, u, N), b, N)` to evaluate to 0.  

Thus, the server's session key K simplifies to `SHA256("0")`, and the server HMAC is fixed as `hmac_sha256(SHA256("0"), salt)`.  We can compute the HMAC using the above process for each user in the database, and we can make POST requests to the server dashboard at "http://crypto.chal.csaw.io:5005/dash/<user>" as follows:

```python
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

```

We will successfully authenticate with the HMAC we provide, and if we print out our response text as `r.text`, we'll see something like looks like 

```html
<p>Welcome to the dashboard, Ingrid! You are a priviledged administrator for the Company.</p>
      <br>
	  <table class="table">
        <thead>
          <tr>
            <th scope="col">Login Username</th>
            <th scope="col">Password</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Ingrid</td>
            <td>4:48359d52540614247337a5a1191034a7:128</td>
          </tr>
        </tbody>
      </table>
```

Now since we're told that all of the admin passwords are somehow connected to the root admin's, we can reasonably infer that some secret sharing scheme was used--most likely Shamir.  Thus, we try Shamir secret recovery on the 20 admins' secrets, which yields the key `'_z3r0_kn0wl3dg3_'`.  We can then decrypt the root admin's cbc-encrypted password with the `C = 0x08589c6b40ab64c434064ec4be41c9089eefc599603bc7441898c2e8511d03f6` and `IV = 0x254dc5ae7bb063ceaf3c2da953386948` as given in `encrypted.txt`.  The full code to do this is shown below.

```python

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
```

This yields 

```
flag: b'flag{n0t_s0_s3cur3_4ft3r_4ll}\n\x00\x00'
```

