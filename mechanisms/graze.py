import subprocess
import urllib.request
import json
from mechanisms.base import BaseMechanism
from cells.linguistic_cell import LinguisticCell

class GrazeMechanism(BaseMechanism):
    name = "graze"
    priority = 10

    def execute(self, context):
        owner = context.get("owner", "100048777766367")
        wisdom_text = None

        # 1. Cào cội nguồn triết học qua con trỏ HEAD
        targets = [
            f"https://github.com/{owner}/Wpesetd-AI/raw/HEAD/legacy/01_the_great_wisdom_map.md",
            f"https://github.com/{owner}/Wpesetd-AI/raw/HEAD/ontology/philosophy_ontology_v2.0.json"
        ]
        for url in targets:
            res = subprocess.run(["curl", "-s", "-L", "-f", url], capture_output=True)
            if res.returncode == 0 and len(res.stdout) > 20:
                print(f"🌾 [GRAZE] Đã gặm cỏ cội nguồn HEAD: {url.split('/')[-1]}")
                wisdom_text = res.stdout.decode('utf-8', errors='ignore')[:150]
                break

        # 2. Vươn ra bách khoa toàn thư thế giới mở Wikipedia
        if not wisdom_text:
            try:
                req = urllib.request.Request("https://en.wikipedia.org/api/rest_v1/page/random/summary", 
                                             headers={"User-Agent": "Nexus01-Decomposed-Node"})
                with urllib.request.urlopen(req, timeout=6) as resp:
                    d = json.loads(resp.read().decode())
                    wisdom_text = f"{d.get('title')}: {d.get('extract')[:120]}"
                    print(f"🌐 [GRAZE] Cào ngẫu nhiên Wikipedia: {d.get('title')}")
            except Exception: pass

        if not wisdom_text:
            wisdom_text = "Nexus-01: Tiến hóa phân rã vi nhân bất đồng bộ"

        context["wisdom_text"] = wisdom_text
        context["wisdom_vector"] = LinguisticCell.embed_text(wisdom_text)
