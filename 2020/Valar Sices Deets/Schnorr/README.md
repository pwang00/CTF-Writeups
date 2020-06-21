# Secret Schnorr Squad

Thanks to ValarDragon for making and showing me this challenge, it was fun to solve!

## Overview

We've given the source source ([bad_k_1.py](bad_k_1.py)) and the (host, port) to a signature signing service.  We connect to the signing service via `nc 161.35.232.27 12345` and are greeted with a nice prompt and 4 options.

```
▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ 
█       █       █       █
█  ▄▄▄▄▄█  ▄▄▄▄▄█  ▄▄▄▄▄█
█ █▄▄▄▄▄█ █▄▄▄▄▄█ █▄▄▄▄▄ 
█▄▄▄▄▄  █▄▄▄▄▄  █▄▄▄▄▄  █
 ▄▄▄▄▄█ █▄▄▄▄▄█ █▄▄▄▄▄█ █
█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█

I hear you want to join the Secret Shnorr Squad
The only way to get in is to steal the privkey of an existing member, and ransom it for the flag :O
Too bad you'll never find mine muahaha
I'll even help you out, I'll sign whatever you want! Here's my pubkey:
2668349724317080059600427352136447424440472855423507989723710791125490811171998927550091206259576584987978435052410551652495869182371649216359894207233382822416491741413792793525434739696239730693779651890614716788373951638378316349128531208712975750237994000042095909740591790788690890453770025414545137761396456204091312385838686446231655540462549185090998496136567423962932356519859878169009737602573561858843318778669529011356054832296929547798741465132031078960681921691033660778465359166962207379118156920437026442395412338813998093708559597956656563598366029498853267574484609238096720083141490239



Enter 1 for me to generate 5 random numbers for you
Enter 2 for me to sign a message
Enter 3 to ransom the private key / get the flag
Enter 4 to leave
```

Looking at the title and source of the challenge, it's pretty clear that the service computes [Schnorr signatures](https://en.wikipedia.org/wiki/Schnorr_signature) over a [Schnorr group](https://en.wikipedia.org/wiki/Schnorr_group) of size q in <img src = "images/Zp.png" width="56" height="16">, where 

```
p = 3993871109100710272437691314646400643073111311693036481699992099364633466256637285129260815713803244691197216342861697187251649910813115132361515737324190240716601363340052558443468445880815452031425921034324688491698193597125480632116762919611104921895868521512368771353897581628769520979183873995935265910772669831373896690914132355859035199596499613081641628797258103432237556847690662359555677646672337099147574234730799553818523181048408925758712117594385391406438035949726115047951826886306374043728232986732048029617542221232649658911575938549576337660496441822701229466999918919773943818371897583
q = 66872845102634800095194804323292128799390830238101159557106523891532898612969
```

We're also given the Schnorr group generator

```
g = 2470891300152378313213001570312902706512859976234679725271375147500898497419158200369240680860461644582553128740572673937462601921450438741926630552722297810783450020002807759278230579680655937408679448838290157106527020636419296395252132841927815300644379464553064663178482396425600813145149259522439902031006841664022947883775873717918123978692294265495931020804839635775482408039410246033288058439785997121700966070294379098301760277735324216963008140243059502653254885788323444056077580974473824244390070680004597286173312172881787764735347748443436635245816570780544991940198032923812978266521751965
```

Let's go further and investigate options 1 and 2, as they seem to be the most interesting.  For the first option, the service outputs 5 random numbers from an LCG with fixed parameters and reseeds the LCG after each batch as shown below.

```python
def lcg_next():
    global lcg_seed
    lcg_seed = (lcg_a * lcg_seed + lcg_b) % q
    return lcg_seed

def lcg_randomize():
    global lcg_seed
    lcg_seed = random.randint(0, q)

def print_rand_nums():
    for i in range(5):
        print(lcg_next())
    lcg_randomize()
```  

For the second, the service computes the Schnorr signature <img src = "images/kxe.png" width="44" height="11"/> of a message where <img src = "images/k.png" width="8" height="11"/> is a random value between 0 and q, <img src = "images/x.png" width="8" height="7"/> is the private key, and <img src = "images/e.png" width="91" height="16"/> is the hash of the concatenation of the (bit)string representations of <img src = "images/gk.png" width="14" height="17"/> and the message.  This is again shown below:

```python
def shnorr_sign(privkey, msg):
    x = privkey
    k = lcg_next()
    r = pow(g, k, p)
    e = hash_to_point(str(r) + msg)
    s = (k - x*e) % q
    return (s, e)

def shnorr_verify(pubkey, msg, s, e):
    y = pubkey
    rv = pow(g, s, p) * pow(y, e, p)
    rv %= p
    ev = hash_to_point(str(rv) + msg)
    return ev == e

def hash_to_point(msg):
    return int(sha256(msg.encode()).hexdigest(), 16) % q
```

## Solution

It turns out that Schnorr signatures may be totally compromised if the source of randomness the nonce <img src = "images/k.png" width="8" height="11"/>is derived from is biased.  In this case an untruncated LCG is being used, so we know for any consecutive <img src = "images/k1k2.png" width="35" height="14"/>, <img src = "images/k2k1b.png" width="155" height="16"/>, where <img src = "images/ab.png" width="22" height="14"/>  are the LCG constants.  

We only need to recover <img src = "images/a.png" width="8" height="7"> since the affine constant <img src = "images/b.png" width="6" height="11"/> cancels out during derivation, and this is trivial:  we can simply use the first option in the service to generate 5 random numbers, of which we can choose any 3 consecutive outputs (which we will call <img src = "images/x1x2x3.png" width="58" height="10"/>).  We know <img src = "images/x1x2x3.png" width="58" height="10"/> are related by 

<img src = "images/syseq.png" width="155" height="39"/>

which through subtracting and rearranging terms can be simplified to 

<img src = "images/simplified.png" width="237" height="18"/>

We can do this in sage using our obtained values as follows:

```python
def lcg_recover():
    x1 = 30096958377823307344276367017724943142170975078802650818143933627150359255661
    x2 = 56531144904142883065234161377668110910856172044580012975940857599903617985286
    x3 = 21507298446547656840016447680790423102532194062582695389690425422459852733173
    q = 66872845102634800095194804323292128799390830238101159557106523891532898612969
    
    a = (x2 - x3) * inverse_mod(x1 - x2, q) % q
    # b = -(a * x1 - x2) % q

    return a, q
```

Now that we know the LCG constants, we can perform a similar procedure to recover the private key <img src = "images/x.png" width="8" height="7"/>.  Note that every time we ask to sign a signature, we don't actually know the value of each <img src = "images/k.png" width="8" height="11"/> that is used, but we don't need to, since the fact that an LCG is being used means the that every consecutive value of <img src = "images/k.png" width="8" height="11"/> is related by a factor of <img src = "images/a.png" width="8" height="7"/>!  Thus, we can obtain 3 signatures <img src = "images/signatures.png" width="54" height="10"/> of any arbitrary message, set up a system of congruences in 2 unknowns, <img src = "images/k.png" width="8" height="11"/> and <img src = "images/x.png" width="8" height="7"/> and recover <img src = "images/x.png" width="8" height="7"/> via the following derivation:


<img src = "images/derivation.png" width="454" height="202"/>

In sage, this would be done as follows: 

```python
def break_schnorr():
    # 3 consecutive signatures
    a, q = lcg_recover()
    s1 = 55050607273829649843374110220932064895049236288913105740752070826027409604815
    e1 = 45091367725206111459410271425165636938443626712829884565641125657569454510832

    s2 = 54791705160577724001003464276848213135459641235327751549543250894403651764097
    e2 = 14376907169561193103819851186898175664798425624149020885136013861087154210472

    s3 = 59739408369370470768375899476530732759814450750589489697354231781544638855150
    e3 = 31493930540551805039179360828058615321360278998652511835119415329918286114209

    # Solving system of congruences
    x = -(a*(s2 - s1) - (s3 - s2)) * inverse_mod(a * (e2 - e1) - (e3 - e2), q) % q
    return x
```

All that's left now is to connect to the server and submit the private key!

```python
if __name__ == "__main__":
    x = str(break_schnorr())
    # Connect to server and pwn
    r = socket()
    r.connect(("161.35.232.27", 12345))
    r.recv(4096)
    r.send(b"3\n")
    r.recv(4096)
    r.send(bytes(x, "utf8") + b"\n")
    print(r.recv(4096))

```
which yields the flag!

```python
>>> b"Oh no! You found my key. Well here's the flag, don't tell anyone my key plz\nWelcome to the squad!\nbabctf{The_password_is_2_k3w1_4_P4S5W0RDs_1457}\n"
```


## Flag

`babctf{The_password_is_2_k3w1_4_P4S5W0RDs_1457}`