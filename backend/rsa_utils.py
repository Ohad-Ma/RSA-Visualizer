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