from mechanisms.base import BaseMechanism
from cells.neuron import AtomNeuron, sigmoid_derivative

NUM_CELLS = 8

class XorLearningMechanism(BaseMechanism):
    name = "xor_learning"
    priority = 30

    def execute(self, context):
        swarm = [AtomNeuron(f"n01_h_{i}", n_inputs=4, n_super_xor=4) for i in range(NUM_CELLS)]
        out_cell = AtomNeuron("n01_out", n_inputs=NUM_CELLS, n_super_xor=4)

        # Xây dựng vector đầu vào
        v_wisdom = context.get("wisdom_vector", [0.5, 0.5, 0.5, 0.5])
        q_dec = context.get("quorum_decision", 0.5)
        
        super_vector = [v_wisdom[0], v_wisdom[1], q_dec, round(1.0 - q_dec, 4)]
        entangled, masks = swarm[0].super_xor_entangle(super_vector, "nexus01_context")

        # Lan truyền tiến
        h_outs = [cell.forward(entangled) for cell in swarm]
        internal_pred = out_cell.forward(h_outs)

        # Hợp nhất với Quorum
        final_decision = round((internal_pred + q_dec) / 2.0, 4)
        print(f"🔮 [XOR_LEARNING] Phán quyết nội bộ: {internal_pred:.4f} ──► Hợp nhất tối thượng: {final_decision}")

        # Lan truyền ngược
        target = 1.0 if super_vector[0] > super_vector[1] else 0.0
        delta_out = (target - final_decision) * sigmoid_derivative(final_decision)
        deltas_h = [delta_out * out_cell.weights[j] * sigmoid_derivative(h_outs[j]) for j in range(NUM_CELLS)]

        out_cell.backward(delta_out)
        for j, cell in enumerate(swarm): cell.backward(deltas_h[j])

        # Tính toán đạo hàm nén
        grad_backward = [
            round(sum(deltas_h[j] * swarm[j].weights[0] for j in range(NUM_CELLS)), 4),
            round(sum(deltas_h[j] * swarm[j].weights[1] for j in range(NUM_CELLS)), 4)
        ]

        context["final_decision"] = final_decision
        context["grad_backward"] = grad_backward
        context["super_xor_masks"] = masks
        context["swarm_weights"] = [c.weights for c in swarm]
        context["out_weights"] = out_cell.weights
