// Deterministic PRNG so demo/mock data looks the same on every reload
// instead of reshuffling and making the dashboard feel inconsistent.
export function createSeededRandom(seed) {
  let state = seed;
  return function random() {
    state = (state * 1664525 + 1013904223) % 4294967296;
    return state / 4294967296;
  };
}

export function pick(random, list) {
  return list[Math.floor(random() * list.length)];
}

export function pickWeighted(random, weightedList) {
  const total = weightedList.reduce((sum, entry) => sum + entry.weight, 0);
  let roll = random() * total;
  for (const entry of weightedList) {
    roll -= entry.weight;
    if (roll <= 0) return entry.value;
  }
  return weightedList[weightedList.length - 1].value;
}

export function randomInt(random, min, max) {
  return Math.floor(random() * (max - min + 1)) + min;
}

// Generates a short, URL-safe token, e.g. for the mock feedback link.
export function generateToken(random = Math.random) {
  return Math.floor(random() * 36 ** 8)
    .toString(36)
    .padStart(6, '0');
}
