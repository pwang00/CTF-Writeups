# Smol e (372)

## Problem Statement

Anshul has a message that he wants to send to Disha using RSA. He padded the message with a random padding and sent it to Disha, but she didn’t receive the message. However, she was able to receive the message after a second attempt from Anshul. You were able to intercept both of Anshul’s ciphertexts, and you are also given Anshul’s RSA public key. Can you recover the message?

## Solution

We can use the famous Coppersmith's short-pad and Franklin-Reiter related message attacks (too see how they work, head over to [the corresponding wikipedia article](https://en.wikipedia.org/wiki/Coppersmith%27s_attack)) to decrypt both messages.  In particular, we first recover the fixed difference (denoted as `r`) between m1 and m2 via coppersmith's method by guessing a bound for `r`, and then solve for the messages which are the roots of the polynomials `x^e - C1` and `(x + r)^e - C2` via Franklin-Reiter.  This can be done as shown:

```python
from sage.all import *
import binascii

def coppersmith(C1, C2, e, N, X = 2^60, b = 0.25):
    P.<x, y> = PolynomialRing(Zmod(N))
    P2.<y> = PolynomialRing(Zmod(N))
    
    g1 = (x^e - C1).change_ring(P2)
    g2 = ((x + y)^e - C2).change_ring(P2)

    res = g1.resultant(g2, variable=x)

    roots = res.univariate_polynomial().change_ring(Zmod(N))\
        .small_roots(X=X, beta=b)

    return diff[0]


def franklin_reiter(c_array, N, r, e=3):
    P.<x> = PolynomialRing(Zmod(N))
    c1, c2 = c_array
    equations = [x ^ e - c1, (x + r) ^ e - c2]
    g1, g2 = equations
    return -composite_gcd(g1,g2).coefficients()[0]

def composite_gcd(g1,g2):
    return g1.monic() if g2 == 0 else composite_gcd(g2, g1 % g2)

def test():
    N = 163741039289512913448211316444208415089696281156598707546239939060930005300801050041110593445808590019811244791595198691653105173667082682192119631702680644123546329907362913533410257711393278981293987091294252121612050351292239086354120710656815218407878832422193841935690159084860401941224426397820742950923
    C1 = 110524539798470366613834133888472781069399552085868942087632499354651575111511036068021885688092481936060366815322764760005015342876190750877958695168393505027738910101191528175868547818851667359542590042073677436170569507102025782872063324950368166532649021589734367946954269468844281238141036170008727208883
    C2 = 42406837735093367941682857892181550522346220427504754988544140886997339709785380303682471368168102002682892652577294324286913907635616629790484019421641636805493203989143298536257296680179745122126655008200829607192191208919525797616523271426092158734972067387818678258432674493723618035248340048171787246777
    e = 3

    diff = coppersmith(C1, C2, e, N)
    print("Diff: ", diff)
    m1 = franklin_reiter([C1, C2], N, diff)
    print(f"Recovered message: {m1} \n")

    assert pow(m1, e, N) == C1 and pow(m1 + diff, e, N) == C2, "Recovered values are incorrect!"

    for i in range(100):
        candidate = binascii.unhexlify(hex(m1 // 2^i)[2:])
        if b"flag" in candidate:
            print("Message found!\n", candidate)
            break

if __name__ == "__main__":
    test()
```

Running this yields

`b"Press Point F to pay respects. I'm writing this a day before HSCTF starts. flag{n0t_4_v3ry_sm0l_fl4g}\n\x00\x00\x00\x00\x00\x00\x00\x00\xfcKU$\xd9t"`, and so our flag is `flag{n0t_4_v3ry_sm0l_fl4g}`.

