import hashlib
import bisect

class ConsistentHashRing:
    def __init__(self, v_nodes):
        self.v_nodes = v_nodes
        self.ring = {}
        self.sorted_server_hashes = []
        self.MAX_HASH = 100
    
    def _hash(self, key):
        return int(hashlib.sha256(key.encode()).hexdigest(), 16)%self.MAX_HASH
    
    def add_server(self, server):
        for i in range(self.v_nodes):
            hash = self._hash(f"{server}:{i}")
            self.ring[hash] = server
            bisect.insort(self.sorted_server_hashes, hash)
    
    def remove_server(self, server):
        for i in range(self.v_nodes):
            hash = self._hash(f"{server}:{i}")
            del self.ring[hash]
            self.sorted_server_hashes.remove(hash)

    def get_server(self, key):
        if not self.ring:
            return
        key_hash = self._hash(key)
        idx = bisect.bisect(self.sorted_server_hashes, key_hash) % len(self.sorted_server_hashes)
        return self.ring[self.sorted_server_hashes[idx]]    
    
ring = ConsistentHashRing(3)
# Example usage
ring.add_server("server1")
ring.add_server("server2")
ring.add_server("server3")
ring.add_server("server4")

# Get the server for a specific key
server = ring.get_server("my_key")
print(f"Key 'my_key' is mapped to server: {server}")
# Remove a server
ring.remove_server("server2")

server = ring.get_server("my_key")
print(f"Key 'my_key' is mapped to server: {server}")
