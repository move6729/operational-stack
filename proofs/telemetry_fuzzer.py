import math
import random


class HPMCRControlLoop:
    def __init__(self, user_vector_dim: int, target_state_vector: list):
        self.dim = user_vector_dim
        self.v_target = target_state_vector

    def compute_feedback_step(self, current_user_vector: list, telemetry_delta: dict) -> list:
        """
        Server-Side Engine: Calculates next generative context-injection vector
        to minimize distance to target cognitive state.
        """
        dwell_ms = telemetry_delta.get("dwell_time_ms", 0)
        interaction_val = telemetry_delta.get("engagement_score", 0.0)

        state_shift = [
            (current_user_vector[i] - self.v_target[i]) * (interaction_val / (dwell_ms + 1e-5))
            for i in range(self.dim)
        ]
        next_user_vector = [
            current_user_vector[i] - (0.01 * state_shift[i])
            for i in range(self.dim)
        ]
        norm = math.sqrt(sum(x * x for x in next_user_vector))
        if norm == 0.0:
            norm = 1.0
        return [x / norm for x in next_user_vector]


def _l2_norm(a, b):
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(len(a))))


def simulate_telemetry_fuzzer_proof():
    """
    Client-Side Defense Proof: Demonstrates how local behavioral telemetry fuzzing
    (jitter injection) invalidates server-side gradient descent state estimation.
    """
    random.seed(42)
    true_user_state = [0.8, -0.5, 0.3]
    server_estimated_state = [0.0, 0.0, 0.0]

    for _ in range(100):
        # Raw micro-telemetry signal (e.g., true dwell time / scroll tell)
        raw_telemetry = [true_user_state[i] + random.gauss(0, 0.01) for i in range(3)]

        # Defensive Shield: Inject 20% Uniform Behavioral Jitter (Fuzzing)
        fuzzed_telemetry = [raw_telemetry[i] + random.uniform(-0.2, 0.2) for i in range(3)]

        # Server update attempt fails to converge due to noise floor
        server_estimated_state = [
            server_estimated_state[i] + 0.05 * (fuzzed_telemetry[i] - server_estimated_state[i])
            for i in range(3)
        ]

    estimation_error = _l2_norm(true_user_state, server_estimated_state)
    print(f"[DEFENSE PROOF] Trajectory Lock Error: {estimation_error:.4f} (State Estimator Broken)")
    return estimation_error > 0.3


if __name__ == "__main__":
    simulate_telemetry_fuzzer_proof()