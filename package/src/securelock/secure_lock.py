import random, hashlib
def lock(t, p):
    s = ''.join(chr(random.randint(0, 255)) for _ in range(32)); k = [hashlib.sha256((p + s).encode()).digest()[i % 32] for i in range(len(t))]; return ''.join(f"{ord(c):02x}" for c in s + ''.join(chr(ord(c) ^ k[i % len(k)]) for i, c in enumerate(t)))

def unlock(l, p):
    s, e = ''.join(chr(int(l[i:i+2], 16)) for i in range(0, 64, 2)), ''.join(chr(int(l[i:i+2], 16)) for i in range(64, len(l), 2)); k = [hashlib.sha256((p + s).encode()).digest()[i % 32] for i in range(len(e))]; return ''.join(chr(ord(c) ^ k[i % len(k)]) for i, c in enumerate(e))