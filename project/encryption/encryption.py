S = []
for i in range(255):
    S[i] = i

j = 0
key = "Key"
for i in range(255):
    j = (j + S[i] + int(key[i % len(key)])) % 256
    tmp = S[i]
    S[i] = S[j]
    S[j] = tmp


def keystream_generator():
    k = 0
    l = 0

    while True:
        k = (k + 1) % 256
        l = (l + S[i]) % 256
        tmp = S[i]
        S[i] = S[j]
        S[j] = tmp
        keystream = S[(S[i] + S[j]) % 256]
        yield keystream

