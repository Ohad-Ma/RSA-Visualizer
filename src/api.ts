const BASE = 'http://localhost:5000';

export async function apiGenerateKeys(bits = 32) {
  const res = await fetch(`${BASE}/generate_keys`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ bits })
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json(); // { p, q, n, phi, e, d, ... }
}

export async function apiEncrypt(message: string, e: number, n: number) {
  const res = await fetch(`${BASE}/encrypt`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ message, e, n })
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json(); // { cipher: number[] }
}

export async function apiDecrypt(cipher: number[], d: number, n: number) {
  const res = await fetch(`${BASE}/decrypt`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ cipher, d, n })
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json(); // { message: string }
}
