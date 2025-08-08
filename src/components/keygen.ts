export function generateRSAKeys(p: number, q: number) {
  const n = p * q;
  const phi = (p - 1) * (q - 1);
  const e = 65537; // standard public exponent

  const d = modInverse(e, phi);

  return {
    p, q, n, phi, e, d,
    publicKey: [e, n],
    privateKey: [d, n],
  };
}

// Extended Euclidean Algorithm to compute modular inverse
function modInverse(a: number, m: number): number {
  let m0 = m, x0 = 0, x1 = 1;
  while (a > 1) {
    const q = Math.floor(a / m);
    [a, m] = [m, a % m];
    [x0, x1] = [x1 - q * x0, x0];
  }
  return x1 < 0 ? x1 + m0 : x1;
}