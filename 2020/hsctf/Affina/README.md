# Affina and the Quadratics (480)

## Problem statement

Affina was struggling with her graphing quadratics homework. Bored, she decided to cheat by using Desmos to graph the given quadratic, and then realized that she could use it to send messages to her best friend without anyone noticing!

She sent the following message to her friend: `7rr4p6_4e_4ph6bo8hap2?`

Can you decrypt it using the image of the quadratic Affina used? Note: the flag should make relative sense.

Author: Plate\_of\_Sunshine

Note: Affina uses a 26 character charset and the numbers are encoded differently.

## Solution (unintended)

I first started out by looking at the given graph, which works out to be the polynomial `(x + 1)(x + 2)`, but I didn't really know what to do after this.  I thought at first that Affina encoded her message character by character by doing `c_i = (x_i + 1)(x_i + 2) mod 26` or mod 10 where `c_i` is a character of the ciphertext and `x_i` is a character of the plaintext, which I think is reasonable considering letters and numbers are encoded differently.  However, this produced no results (and as it turns out, in general an encryption scheme like this will not work since the discriminant of any `ax^2 + bx + c` is not necessarily a quadratic residue of n)! 

Alas, hard stuck and frustrated, I just guessed the flag.  The first 7 characters are likely the word "Affine" in leetspeak, so I guessed `4ff1n3`.  The next 2 characters are then likely the word "is", so I guessed "1s".  Finally, the last 11 characters are probably the word "interesting", (and some characters are already fixed by our previous guesses), so I guessed "1nt3re5tin9".  Putting this together yields the flag `4ff1n3_1s_1nt3re5tin9`.

## Solution (intended)

The graph represents `(x + 1)(x + 2) = x^2 + 3x + 2`, so discard the quadratic term.  The letters can be decoded via a regular affine cipher with a = 3 and b = 2, and the numbers can be decoded via rot-7 (modulo 10).

