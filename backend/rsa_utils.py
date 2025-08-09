# backend/rsa_utils.py
"""
Educational RSA utilities for key generation, encryption, and decryption.

Implements:
- Fast modular exponentiation (square-and-multiply)
- Extended Euclidean Algorithm (iterative) + math.gcd check
- Miller–Rabin probabilistic primality test
- Random prime generation
- Textbook RSA key generation (no padding)
- Simple text <-> integer blocks (1 byte per block; for demo only)

References (algorithms/public domain math):
- RSA: https://en.wikipedia.org/wiki/RSA_(cryptosystem)
- Miller–Rabin: https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
- Extended Euclid: https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
"""

from __future__ import annotations
import math
import secrets
from typing import List, Optional, Tuple


# ----------------- Core number theory -----------------

def modexp(base: int, exp: int, mod: int) -> int:
    """Fast modular exponentiation: (base ** exp) % mod."""
    if mod <= 0:
        raise ValueError("mod must be positive")
    base %= mod
    result = 1
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return result


def egcd(a: int, b: int) -> Tuple[int, int, int]:
    """Extended Euclid (iterative).
    Returns (g, x, y) such that a*x + b*y = g = gcd(a, b)."""
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


def modinv(a: int, m: int) -> int:
    """Return x such that (a * x) % m == 1. Raises if gcd(a, m) != 1."""
    if m <= 0:
        raise ValueError("Modulus must be positive")
    if math.gcd(a, m) != 1:
        raise ValueError("No modular inverse: a and m are not coprime")
    g, x, _ = egcd(a, m)
    # By the gcd check above, g should be 1
    return x % m

# ----------------- Primality & prime generation -----------------
def is_probable_prime(n: int, rounds: int = 12) -> bool:
    """Miller–Rabin probable prime test."""
    if n < 2:
        return False
    # Quick checks for small primes
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    if n in small_primes:
        return True
    if any(n % p == 0 for p in small_primes):
        return False

    # Write n-1 = d * 2^r
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Random bases
    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2  # a in [2, n-2]
        x = modexp(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def random_prime(bits: int) -> int:
    """Return a random probable prime with the given bit-length."""
    if bits < 2:
        raise ValueError("bits must be >= 2")
    while True:
        # Ensure top bit and oddness
        candidate = secrets.randbits(bits) | (1 << (bits - 1)) | 1
        if is_probable_prime(candidate):
            return candidate

# ------------------ RSA core ------------------

def generate_keypair(bits_per_prime: int = 32) -> dict:
    """
    Generate a tiny RSA keypair.
    bits_per_prime controls the size of p and q individually (e.g., 32 or 64).
    """
    # 1) pick two distinct primes
    p = random_prime_bits(bits_per_prime)
    q = random_prime_bits(bits_per_prime)
    while q == p:
        q = random_prime_bits(bits_per_prime)

    # 2) compute n and phi
    n = p * q
    phi = (p - 1) * (q - 1)

    # 3) choose public exponent e (small and coprime with phi)
    #    65537 is standard but for small demos you can also use 3 or 17.
    for e in (65537, 17, 3, 5):
        if math.gcd(e, phi) == 1:
            break
    else:
        # fallback: search for an odd e that works
        e = 3
        while e < 1 << 20 and math.gcd(e, phi) != 1:
            e += 2
        if math.gcd(e, phi) != 1:
            raise RuntimeError("Could not find a valid public exponent e.")

    # 4) find private exponent d (modular inverse of e mod phi)
    d = modinv(e, phi)

    return {
        "p": p, "q": q,
        "n": n, "phi": phi,
        "e": e, "d": d,
        "bits_per_prime": bits_per_prime
    }

def encrypt_int(m: int, e: int, n: int) -> int:
    """Encrypt a single integer m (< n)."""
    if not (0 <= m < n):
        raise ValueError("Message integer must be 0 <= m < n")
    return modexp(m, e, n)

def decrypt_int(c: int, d: int, n: int) -> int:
    """Decrypt a single integer c (< n)."""
    if not (0 <= c < n):
        raise ValueError("Cipher integer must be 0 <= c < n")
    return modexp(c, d, n)
    
# ------------------ Text helpers (1 byte per block) ------------------

def text_to_ints(s: str, n: int) -> List[int]:
    """Encode string to list of small integers (bytes)."""
    data = s.encode("utf-8")
    # Ensure each byte < n (true for normal n)
    return [b for b in data if b < n]

def ints_to_text(vals: List[int]) -> str:
    """Decode list of small integers back to string."""
    return bytes(vals).decode("utf-8", errors="replace")