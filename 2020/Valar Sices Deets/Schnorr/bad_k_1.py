# privkey is a random number between [0, q]
# lcg_a, lcg_b are random numbers in [0, p-1]
# and flag is a string, which you are tasked with learning =)
# if you want to test this code locally, define a secret.py file with such variables
from secret import privkey, flag, lcg_a, lcg_b
from hashlib import sha256
import random

# hah no pohlig-hellman for you
# I've generated real (AFAIK) Shnorr parameters
p = 3993871109100710272437691314646400643073111311693036481699992099364633466256637285129260815713803244691197216342861697187251649910813115132361515737324190240716601363340052558443468445880815452031425921034324688491698193597125480632116762919611104921895868521512368771353897581628769520979183873995935265910772669831373896690914132355859035199596499613081641628797258103432237556847690662359555677646672337099147574234730799553818523181048408925758712117594385391406438035949726115047951826886306374043728232986732048029617542221232649658911575938549576337660496441822701229466999918919773943818371897583
q = 66872845102634800095194804323292128799390830238101159557106523891532898612969
assert ((p-1) % q == 0)
g = 2470891300152378313213001570312902706512859976234679725271375147500898497419158200369240680860461644582553128740572673937462601921450438741926630552722297810783450020002807759278230579680655937408679448838290157106527020636419296395252132841927815300644379464553064663178482396425600813145149259522439902031006841664022947883775873717918123978692294265495931020804839635775482408039410246033288058439785997121700966070294379098301760277735324216963008140243059502653254885788323444056077580974473824244390070680004597286173312172881787764735347748443436635245816570780544991940198032923812978266521751965
assert(pow(g, q, p) == 1)

pubkey = pow(g, privkey, p)
# assert pubkey == 

## Shnorr impl - meant to match wikipedia notation

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

## LCG impl

lcg_seed = random.randint(0, q)
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

## Core loop

def core_loop():
    print("Enter 1 for me to generate 5 random numbers for you")
    print("Enter 2 for me to sign a message")
    print("Enter 3 to ransom the private key / get the flag")
    print("Enter 4 to leave\n")
    choice = input()
    if choice == "1":
        print_rand_nums()
    if choice == "2":
        msg = input("Enter your message: ")
        s, e =  shnorr_sign(privkey, msg)
        assert(shnorr_verify(pubkey, msg, s, e))
        print(s, e)
    if choice == "3":
        privkey_guess = int(input("Enter private key: "))
        if privkey_guess == privkey:
            print("Oh no! You found my key. Well here's the flag, don't tell anyone my key plz")
            print(flag)
            return
        print("Wrong!!")
    if choice == "4":
        return
    else:
        "Invalid choice"
    core_loop()
        

def main():
    print(u""" 
▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ 
█       █       █       █
█  ▄▄▄▄▄█  ▄▄▄▄▄█  ▄▄▄▄▄█
█ █▄▄▄▄▄█ █▄▄▄▄▄█ █▄▄▄▄▄ 
█▄▄▄▄▄  █▄▄▄▄▄  █▄▄▄▄▄  █
 ▄▄▄▄▄█ █▄▄▄▄▄█ █▄▄▄▄▄█ █
█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█
""")
    print("I hear you want to join the Secret Shnorr Squad")
    print("The only way to get in is to steal the privkey of an existing member, and ransom it for the flag :O")
    print("Too bad you'll never find mine muahaha")
    print("I'll even help you out, I'll sign whatever you want! Here's my pubkey:")
    print(pubkey)
    print("\n\n")

    core_loop()

main()