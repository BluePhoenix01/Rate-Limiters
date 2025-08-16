import hashlib

def hash_value(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()

def build_merkle_tree(data):
    """Builds a Merkle tree and returns all levels + leaf mapping."""
    level = [hash_value(item) for item in data]
    tree = [level]  # store all levels
    while len(level) > 1:
        new_level = []
        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i+1] if i+1 < len(level) else left
            parent = hash_value(left + right)
            new_level.append(parent)
        level = new_level
        tree.append(level)
    return tree, [hash_value(item) for item in data]

def find_differing_leaves(data1, data2):
    """Compare two data lists using their leaf hashes."""
    leaves1 = [hash_value(item) for item in data1]
    leaves2 = [hash_value(item) for item in data2]
    diffs = []
    for i, (h1, h2) in enumerate(zip(leaves1, leaves2)):
        if h1 != h2:
            diffs.append(i)
    # handle different lengths
    if len(leaves1) != len(leaves2):
        diffs.extend(range(min(len(leaves1), len(leaves2)), max(len(leaves1), len(leaves2))))
    return diffs

# Example
node1_data = ["a:1", "b:2", "c:3", "d:4"]
node2_data = ["a:1", "b:2", "c:3", "d:5"]

tree1, leaf_hashes1 = build_merkle_tree(node1_data)
tree2, leaf_hashes2 = build_merkle_tree(node2_data)

diff_indices = find_differing_leaves(node1_data, node2_data)
if diff_indices:
    print(f"Differing leaves at indices: {diff_indices}")
    for idx in diff_indices:
        print(f"  node1: {node1_data[idx]} | node2: {node2_data[idx]}")
else:
    print("Trees match!")

print("Root1:", tree1[-1][0])
print("Root2:", tree2[-1][0])
