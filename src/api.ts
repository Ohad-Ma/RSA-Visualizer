// src/api.ts
const BASE = "http://127.0.0.1:5000";

export type KeyResp = {
  p: string; q: string; n: string; phi: string; e: string; d: string;
  bits_per_prime: number;
};

export async function apiGenerateKeys(bits_per_prime = 32): Promise<KeyResp> {
  const res = await fetch(`${BASE}/generate_keys`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ bits_per_prime })
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function apiEncrypt(message: string, e: string, n: string) {
  const res = await fetch(`${BASE}/encrypt`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, e, n })
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<{ cipher: string[] }>;
}

export async function apiDecrypt(cipher: string[], d: string, n: string) {
  const res = await fetch(`${BASE}/decrypt`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ cipher, d, n })
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<{ message: string }>;
}
