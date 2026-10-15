import json

class UniversalAdapter:
    """
    KHỚP TƯƠNG THÍCH NGƯỢC VÔ HẠN:
    Tự động chuẩn hóa mọi cấu trúc dữ liệu từ quá khứ (v1, v2) và tương lai
    thành một định dạng tín hiệu đồng nhất cho nexus-01.
    """
    @staticmethod
    def parse_packet(raw_text):
        try:
            data = json.loads(raw_text)
        except Exception:
            return None

        # Trích xuất quyết định/xung tín hiệu từ bất kỳ thế hệ nào
        decision = None
        if "decision" in data:
            decision = float(data["decision"])
        elif "synthesis_prediction" in data:
            decision = float(data["synthesis_prediction"])
        elif "command_pulse" in data and isinstance(data["command_pulse"], list):
            decision = float(data["command_pulse"][0])
        elif "features" in data and isinstance(data["features"], list):
            decision = float(data["features"][0])
        else:
            decision = 0.5

        # Trích xuất danh bạ lan truyền (Gossip)
        gossip = data.get("gossip_network", [])
        
        # Trích xuất đặc trưng đa chiều
        features = data.get("features", [decision, round(1.0 - decision, 4)])
        if len(features) < 2:
            features = [decision, round(1.0 - decision, 4)]

        return {
            "decision": round(decision, 4),
            "features": features[:4],
            "gossip": gossip,
            "contract": data.get("contract", "unknown.contract")
        }
