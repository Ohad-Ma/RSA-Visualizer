import "./style.css";
import { apiGenerateKeys, apiEncrypt, apiDecrypt, type KeyResp } from "./api";

const output = document.getElementById("output") as HTMLDivElement | null;
const generateBtn = document.getElementById("generateBtn") as HTMLButtonElement | null;

// New elements
const plaintextInput = document.getElementById("plaintextInput") as HTMLTextAreaElement | null;
const encryptBtn = document.getElementById("encryptBtn") as HTMLButtonElement | null;
const cipherOutput = document.getElementById("cipherOutput") as HTMLTextAreaElement | null;

const cipherInput = document.getElementById("cipherInput") as HTMLTextAreaElement | null;
const decryptBtn = document.getElementById("decryptBtn") as HTMLButtonElement | null;
const plaintextOutput = document.getElementById("plaintextOutput") as HTMLDivElement | null;

function render(html: string) { if (output) output.innerHTML = html; }

// Keep the latest keys in memory (as strings!)
let currentKeys: KeyResp | null = null;

window.addEventListener("DOMContentLoaded", () => {
  if (generateBtn) {
    generateBtn.addEventListener("click", async () => {
      try {
        render(`<span class="text-xs text-gray-500">Generating keys…</span>`);
        const keys = await apiGenerateKeys(32); // 32 for dev; try 64/128 later
        currentKeys = keys;
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
      } catch (err: any) {
        render(`<span class="text-red-600 text-sm">Error: ${err?.message || err}</span>`);
      }
    });
  }

  if (encryptBtn) {
    encryptBtn.addEventListener("click", async () => {
      if (!currentKeys) {
        alert("Generate keys first.");
        return;
      }
      if (!plaintextInput || !cipherOutput) return;
      const msg = plaintextInput.value ?? "";
      const { e, n } = currentKeys; // strings
      try {
        cipherOutput.value = "Encrypting…";
        const { cipher } = await apiEncrypt(msg, e, n); // cipher: string[]
        // Show as comma-separated list
        cipherOutput.value = cipher.join(", ");
      } catch (err: any) {
        cipherOutput.value = `Error: ${err?.message || err}`;
      }
    });
  }

  if (decryptBtn) {
    decryptBtn.addEventListener("click", async () => {
      if (!currentKeys) {
        alert("Generate keys first.");
        return;
      }
      if (!cipherInput || !plaintextOutput) return;

      // Parse cipher: split by comma or whitespace, filter empty, keep as strings
      const raw = cipherInput.value || "";
      const cipherStrings = raw.split(/[\s,]+/).map(s => s.trim()).filter(Boolean);
      if (cipherStrings.length === 0) {
        plaintextOutput.textContent = "No cipher provided.";
        return;
      }

      const { d, n } = currentKeys; // strings
      try {
        plaintextOutput.textContent = "Decrypting…";
        const { message } = await apiDecrypt(cipherStrings, d, n);
        plaintextOutput.textContent = message;
      } catch (err: any) {
        plaintextOutput.textContent = `Error: ${err?.message || err}`;
      }
    });
  }
});
