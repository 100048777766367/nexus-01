import os
import json
import subprocess
from mechanisms.base import BaseMechanism
from adapters.universal_adapter import UniversalAdapter

class ConsensusMechanism(BaseMechanism):
    name = "consensus"
    priority = 20

    def execute(self, context):
        peers = context.get("peers", [])
        harvested = {}
        new_gossip = []

        os.makedirs("synapses/harvested_memory", exist_ok=True)

        for peer in peers:
            if peer == context.get("repo_name"): continue
            target_file = f"synapse_in_{peer.replace('/', '_')}.json"
            url = f"https://raw.githubusercontent.com/{peer}/main/synapse_forward.json"
            res = subprocess.run(["curl", "-s", "-f", url, "-o", target_file], capture_output=True)
            
            if res.returncode == 0 and os.path.exists(target_file):
                try:
                    with open(target_file, "r") as f:
                        raw = f.read()
                    parsed = UniversalAdapter.parse_packet(raw)
                    if parsed:
                        harvested[peer] = parsed["decision"]
                        new_gossip.extend(parsed["gossip"])
                        # Lưu bộ nhớ tạm
                        with open(f"synapses/harvested_memory/{peer.replace('/', '_')}.json", "w") as bf:
                            bf.write(raw)
                except Exception: pass

        # Cập nhật danh bạ
        for p in new_gossip:
            if p not in peers: peers.append(p)
        context["peers"] = list(dict.fromkeys(peers))[-50:]
        context["harvested"] = harvested

        # Đồng thuận đa số (Quorum Consensus)
        votes = list(harvested.values())
        context["quorum_decision"] = round(sum(votes) / len(votes), 4) if votes else 0.5
        print(f"⚖️ [CONSENSUS] Thu nhận {len(harvested)} phản hồi. Quorum trung bình: {context['quorum_decision']}")
