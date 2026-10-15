import os
import sys
import json
import time
import importlib
import inspect
from mechanisms.base import BaseMechanism

class Nexus01Microkernel:
    def __init__(self):
        self.repo_name = os.environ.get("GITHUB_REPOSITORY", "100048777766367/nexus-01")
        self.owner = os.environ.get("REPO_OWNER", "100048777766367")
        self.ancestor = f"{self.owner}/nexus"
        
        # Ngữ cảnh dùng chung cho mọi cơ chế (Shared Context Bus)
        self.context = {
            "repo_name": self.repo_name,
            "owner": self.owner,
            "ancestor": self.ancestor,
            "peers": self.load_initial_peers(),
            "current_epoch": self.load_current_epoch()
        }

    def load_initial_peers(self):
        peers_file = "synapses/peers.json"
        if os.path.exists(peers_file):
            try:
                with open(peers_file, "r") as f: return json.load(f).get("trusted_peers", [])
            except Exception: pass
        return [
            f"{self.owner}/nexus", f"{self.owner}/genome",
            f"{self.owner}/seed", f"{self.owner}/seed-01", f"{self.owner}/seed-02",
            f"{self.owner}/monad", f"{self.owner}/monad-01", f"{self.owner}/monad-02",
            f"{self.owner}/retina", f"{self.owner}/motor"
        ]

    def load_current_epoch(self):
        state_file = "synapses/state.json"
        if os.path.exists(state_file):
            try:
                with open(state_file, "r") as f: return json.load(f).get("generation_epoch", 0) + 1
            except Exception: pass
        return 1

    # TỰ ĐỘNG QUÉT VÀ NẠP TẤT CẢ CƠ CHẾ TRONG THƯ MỤC mechanisms/
    def discover_and_load_mechanisms(self):
        mechanisms = []
        mech_dir = os.path.join(os.path.dirname(__file__), "mechanisms")
        
        for file in sorted(os.listdir(mech_dir)):
            if file.endswith(".py") and not file.startswith("__") and file != "base.py":
                module_name = f"mechanisms.{file[:-3]}"
                try:
                    mod = importlib.import_module(module_name)
                    for _, obj in inspect.getmembers(mod, inspect.isclass):
                        if issubclass(obj, BaseMechanism) and obj is not BaseMechanism:
                            mechanisms.append(obj())
                            print(f"🔌 [MICROKERNEL NẠP TỆP] Cơ chế: '{obj.name}' từ '{file}'")
                except Exception as e:
                    print(f"⚠️ [LỖI NẠP TỆP {file}]: {e}")

        # Sắp xếp theo mức độ ưu tiên thực thi
        mechanisms.sort(key=lambda m: getattr(m, 'priority', 100))
        return mechanisms

    def run(self):
        print("=" * 65)
        print(f"💎 [NEXUS-01 MICROKERNEL] KHỞI ĐỘNG THẾ HỆ #{self.context['current_epoch']}")
        print(f"🏛️ Kiến trúc: Khớp siêu lỏng phân rã (Decoupled Microkernel)")
        print("=" * 65)

        mechanisms = self.discover_and_load_mechanisms()
        
        # Thực thi tuần tự các cơ chế (cô lập lỗi độc lập)
        for mech in mechanisms:
            try:
                mech.execute(self.context)
            except Exception as e:
                print(f"🚨 [CẢNH BÁO CƠ CHẾ '{mech.name}']: {e} (Hệ thống tự thích ứng, bỏ qua lỗi)")

        print("=" * 65)
        print(f"✨ [NEXUS-01 HOÀN TẤT VÒNG ĐỜI] Thế hệ #{self.context['current_epoch']} đã hội tụ thành công!")
        print("=" * 65)

if __name__ == "__main__":
    node = Nexus01Microkernel()
    node.run()
