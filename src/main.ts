import "./style.css";
import { apiGenerateKeys, apiEncrypt, apiDecrypt } from "./api";

const generateBtn = document.getElementById("generateBtn") as HTMLButtonElement | null;
const output = document.getElementById("output") as HTMLDivElement | null;

function render(html: string) {
  if (output) output.innerHTML = html;
}

window.addEventListener("DOMContentLoaded", () => {
  if (!generateBtn) return;

  generateBtn.addEventListener("click", async () => {
    try {
      render(`<span class="text-xs text-gray-500">Generating keys…</span>`);

      // Use small primes while developing (fast). Later try 64, 128.
      const keys = await apiGenerateKeys(32);
      const { p, q, n, phi, e, d } = keys; // all strings (safe for big ints)

      render(`
        <span class="text-xs">
          p=${p} | q=${q} | n=${n} | φ(n)=${phi} | e=${e} | d=${d}
        </span><br>
        <span class="font-bold">
          <span class="text-yellow-600">🔓</span> Public: (${e}, ${n}) |
          <span class="text-green-600">🔐</span> Private: (${d}, ${n})
        </span>
      `);

      // Optional smoke test: round-trip "HELLO" via backend
      const enc = await apiEncrypt("HELLO", e, n);      // e,n as strings
      const dec = await apiDecrypt(enc.cipher, d, n);   // cipher,d,n as strings
      console.log("Cipher:", enc.cipher);
      console.log("Decrypted:", dec.message);

    } catch (err: any) {
      render(`<span class="text-red-600 text-sm">Error: ${err?.message || err}</span>`);
    }
  });
});
