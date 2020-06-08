## Extremely Complex Challenge (381)

## Problem Statement 

Eric has an elliptic curve defined over a Galois field with order 404993569381. A generator point (391109997465, 167359562362) is given along with a public key (209038982304, 168517698208). We also know that the curve is defined as y^2 = x^3 + ax + b (mod p), and that b is equal to 54575449882. What is Eric’s private key? Express the key as an integer in base 10. Use the flag format `flag{+private_key+}`.

## Solution

Our goal is to find the discrete logarithm of 2 points P and G on an elliptic curve E, where G is the generator and P is some other point on the curve (in other words, find an integer `n` such that `P = nG`.  But before we can do this, we must first figure out the missing parameter `a` of E.  Thankfully, solving for it is not too hard:  Simply put the curve in Weierstrass form, rearrange the equation, and plug in one of the points.  


The code to do this in SageMath is as follows:

```python
F = GF(404993569381)
x, y = G = (391109997465, 167359562362)
b = 54575449882
a = ((y^2 - x^3 - b) * inverse_mod(x, F.order())) % F.order()
```

Once we figure out `a`, we can then plug our 2 points into the curve, and calculate the discrete logarithm of P and G (I believe Sage's implementation of this uses Pohlig-Hellman, which is bottlenecked by the largest prime factor of `#E(F_p)`).

```python
E = EllipticCurve(F, [a, b])
G = E(G)
P = E((209038982304, 168517698208))
print(G.discrete_log(P))
```

This yields 17683067357, and so our flag is `flag{17683067357}`.

