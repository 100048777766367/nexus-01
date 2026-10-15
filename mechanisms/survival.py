import os
import json
import time
import hashlib
from mechanisms.base import BaseMechanism

class SurvivalMechanism(BaseMechanism):
    name = "survival"
    priority = 40

    def execute(self, context):
        current_time = int(time.time())
        current_epoch = context.get("current_epoch", 1)
        final_decision = context.get("final_decision", 0.5)
        peers = context.get("peers", [])

        # 1. Định danh thế hệ con cháu
        node_dna = {
            "identity": context.get("repo_name"),
            "generation": "F1_MODULAR_NEXUS",
            "generation_epoch": current_epoch,
            "architecture": "Decomposed_Microkernel_v1"
        }

        # 2. Phát sóng hai chiều
        fwd_packet = {
            "contract": "bodhi.nexus.v2",
            "node_dna": node_dna,
            "generation_epoch": current_epoch,
            "timestamp": current_time,
            "decision": final_decision,
            "command_pulse": [final_decision, round(1.0 - final_decision, 4)],
            "features": [final_decision, round(1.0 - final_decision, 4)],
            "gossip_network": peers,
            "quantum_cid": hashlib.shake_256(f"fwd_{current_epoch}_{current_time}".encode()).hexdigest(64)
        }
        with open("synapse_forward.json", "w", encoding="utf-8") as f:
            json.dump(fwd_packet, f, indent=4, ensure_ascii=False)

        bwd_packet = {
            "contract": "bodhi.nexus.v2",
            "node_dna": node_dna,
            "generation_epoch": current_epoch,
            "timestamp": current_time,
            "tuning_gradients": context.get("grad_backward", [0.0, 0.0]),
            "gossip_network": peers,
            "quantum_cid": hashlib.shake_256(f"bwd_{current_epoch}_{current_time}".encode()).hexdigest(64)
        }
        with open("synapse_backward.json", "w", encoding="utf-8") as f:
            json.dump(bwd_packet, f, indent=4, ensure_ascii=False)

        # 3. Ốc Mượn Hồn Snapshot (Bảo tồn linh hồn số)
        soul = {
            "node_dna": node_dna,
            "timestamp": current_time,
            "consensus": final_decision,
            "swarm_weights": context.get("swarm_weights", []),
            "peers": peers
        }
        with open("synapses/soul_snapshot.json", "w", encoding="utf-8") as f:
            json.dump(soul, f, indent=4, ensure_ascii=False)

        # 4. Ghi nhật ký thế hệ
        with open("synapses/state.json", "w") as f:
            json.dump({"generation_epoch": current_epoch, "last_t": current_time, "status": "nexus01_evolved"}, f, indent=4)

        # Lưu danh bạ
        with open("synapses/peers.json", "w") as f:
            json.dump({"trusted_peers": peers}, f, indent=4)

        print(f"💾 [SURVIVAL] Đã đóng gói thế hệ #{current_epoch} và phát sóng hoàn tất.")
