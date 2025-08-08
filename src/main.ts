import './style.css'
import { generateRSAKeys } from './components/keygen.ts';

const pInput = document.getElementById("pInput") as HTMLInputElement;
const qInput = document.getElementById("qInput") as HTMLInputElement;
const generateBtn = document.getElementById("generateBtn") as HTMLButtonElement;
const output = document.getElementById("output") as HTMLDivElement;

function getRandomPrime(): number {
  const primes = [61,67,71,73,79,83,89,97];
  return primes[Math.floor(Math.random() * primes.length)];
}

generateBtn.addEventListener("click", () => {
  const p = parseInt(pInput.value) || getRandomPrime(); // We either add a prime number or leave it blank
  const q = parseInt(qInput.value) || getRandomPrime(); // Same as above

  const keys = generateRSAKeys(p,q);

  output.innerText = `
  p = ${keys.p}
  q = ${keys.q} 
  n = ${keys.n}
  φ(n) = ${keys.phi}
  e = ${keys.e}
  d = ${keys.d}
  
  🔓 Public Key: (${keys.e}, ${keys.n})
  🔐 Private Key: (${keys.d}, ${keys.n})
  `.trim();
});
