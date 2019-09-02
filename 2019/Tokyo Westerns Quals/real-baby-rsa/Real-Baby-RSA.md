# Real-Baby-RSA

Points: 40
Solves: 504

# Problem Gist

Unpadded RSA done on each character rather than on entire message

# Solution

This problem, as its name suggests, is pretty straightforward.  Since RSA encryption in this case is done character by character without padding, one can obtain the flag by simply brute forcing each encrypted character (i.e. ASCII values between ranges 32 - 127) until the full flag is recovered.

# Flag

`TWCTF{padding_is_important}`
