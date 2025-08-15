import random
import time

class Node:
    def __init__(self, name, all_nodes):
        self.name = name
        self.alive = True
        self.known_states = {n.name: True for n in all_nodes}
        self.last_seen = {n.name: 0 for n in all_nodes}

    def heartbeat(self, peers, round_number, loss_prob=0.2):
        if not self.alive:
            return
        self.known_states[self.name] = self.alive
        self.last_seen[self.name] = round_number

        # Pick 1–2 random peers
        targets = random.sample(peers, min(2, len(peers)))
        for peer in targets:
            # Simulate message loss
            if random.random() < loss_prob:
                continue
            peer.receive_state(self.name, self.alive, self.known_states, self.last_seen, round_number)

    def receive_state(self, node_name, alive, other_states, other_last_seen, round_number):
        for n, status in other_states.items():
            old_status = self.known_states.get(n, None)
            self.known_states[n] = status
            self.last_seen[n] = max(self.last_seen.get(n, 0), other_last_seen.get(n, 0))
            if n != self.name and old_status is not None and old_status and not status:
                print(f"*** {self.name} detected {n} is DOWN ***")

    def check_missed_heartbeats(self, round_number, threshold=1):
        for n, last in self.last_seen.items():
            if n != self.name and self.known_states.get(n, True) and (round_number - last) > threshold:
                self.known_states[n] = False
                print(f"*** {self.name} detected {n} is DOWN due to missed heartbeat ***")

    def __repr__(self):
        return f"{self.name}: {self.known_states}"


# --- Simulation ---
num_nodes = 5
nodes: list[Node] = []
for i in range(num_nodes):
    nodes.append(Node(f"Node{i}", nodes))

rounds = 8
message_loss_prob = 0.3  # 30% of heartbeats are dropped randomly

for round_number in range(1, rounds + 1):
    print(f"\n--- Round {round_number} ---")

    # Node2 goes down at round 3
    if round_number == 3:
        print(">>> Node2 is going down!")
        nodes[2].alive = False
        nodes[2].known_states[nodes[2].name] = False
        nodes[2].last_seen[nodes[2].name] = round_number

    # Heartbeats with message loss
    for node in nodes:
        other_peers = [n for n in nodes if n != node]
        node.heartbeat(other_peers, round_number, loss_prob=message_loss_prob)

    # Check for missed heartbeats
    for node in nodes:
        node.check_missed_heartbeats(round_number, threshold=1)

    # Print states
    for node in nodes:
        print(node)

    time.sleep(0.5)
