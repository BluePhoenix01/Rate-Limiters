import hashlib
import math

class BloomFilter:
    def __init__(self, n, p):
        # derive m (bits) and k (hashes)
        m = int(-n * math.log(p) / (math.log(2) ** 2))
        k = max(1, int(round((m / n) * math.log(2))))
        print("Calculated m (bits):", m, "k (hashes):", k)
        self.m = m
        self.k = k
        # bit array stored as Python int (arbitrary precision)
        self.bits = 0

    def _hashes(self, item: str):
        # derive k 64-bit hashes from SHA-256 by salting
        for i in range(self.k):
            h = hashlib.sha256(f"{i}:{item}".encode()).digest()
            # take 8 bytes → 64-bit int, mod m for bit index
            print("Hashing item:", item, "with salt:", i)
            yield int.from_bytes(h[:8], "big") % self.m

    def add(self, item: str):
        for pos in self._hashes(item):
            print("Setting bit at position:", pos)
            self.bits |= (1 << pos)

    def might_contain(self, item: str) -> bool:
        for pos in self._hashes(item):
            if (self.bits >> pos) & 1 == 0:
                return False  # definitely not present
        return True  # possibly present (may be FP)

# Demo
bf = BloomFilter(n=1_000_000, p=0.01)
bf.add("alice@example.com")
print(bf.might_contain("alice@example.com"))  # True
print(bf.might_contain("bob@example.com"))    # Likely False (or a rare FP)
