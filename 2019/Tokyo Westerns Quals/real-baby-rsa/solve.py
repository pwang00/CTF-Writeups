from problem import N, e

with open("output", "r") as f:
    encrypted = f.read().splitlines()

e = 65537
recovered = "TWCTF{"
for char in encrypted[len(recovered):]:
    for guess in range(32, 127):
        if pow(guess, e, N) == int(char):
            recovered += chr(guess)

print(recovered)
