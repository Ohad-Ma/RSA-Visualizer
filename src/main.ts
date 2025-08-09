import './style.css';
import { apiGenerateKeys, apiEncrypt, apiDecrypt } from './api';

const pInput = document.getElementById("pInput") as HTMLInputElement | null;
const qInput = document.getElementById("qInput") as HTMLInputElement | null;
const generateBtn = document.getElementById("generateBtn") as HTMLButtonElement | null;
const output = document.getElementById("output") as HTMLDivElement | null;

function render(msg: string) {
  if (!output) return;
  output.innerHTML = msg;
}

window.addEventListener('DOMContentLoaded', () => {
  if (!generateBtn) return;

  generateBtn.addEventListener('click', async () => {
    try {
      render(`<span class="text-xs text-gray-500">Generating keys…</span>`);
      // For the simple RSA core, use small primes while learning:
      const keys = await apiGenerateKeys(32); // later: 256/512 with the faster utils
      const { p, q, n, phi, e, d } = keys;

      render(`
        <span class="text-xs">
          p=${p} | q=${q} | n=${n} | φ(n)=${phi} | e=${e} | d=${d}
        </span><br>
        <span class="font-bold">
          <span class="text-yellow-600">🔓</span> Public: (${e}, ${n}) |
          <span class="text-green-600">🔐</span> Private: (${d}, ${n})
        </span>
      `);

      // (Optional quick crypto smoke test)
      const enc = await apiEncrypt("HELLO", e, n);
      const dec = await apiDecrypt(enc.cipher, d, n);
      console.log('Cipher:', enc.cipher);
      console.log('Decrypted:', dec.message);

    } catch (err: any) {
      render(`<span class="text-red-600 text-sm">Error: ${err?.message || err}</span>`);
    }
  });
});
