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

Looking at the title and source of the challenge, it's pretty clear that the service computes [Schnorr signatures](https://en.wikipedia.org/wiki/Schnorr_signature) over a [Schnorr group](https://en.wikipedia.org/wiki/Schnorr_group) of size q in ![images/Zp.png], where 

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

For the second, the service computes the Schnorr signature ![k - xe](images/kxe.png) of a message where ![k](images/k.png) is a random value ![k](images/k.png) between 0 and q, ![images/x.png] is the private key, and ![e](images/e.png) is the hash ![hash](images/gkm.png).  This is again shown below:

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

The vulnerability here is twofold: 

