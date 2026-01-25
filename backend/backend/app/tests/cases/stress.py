from flows.mock import run_mock_flow
from asserts.mock import assert_mock_success


def run_stress_cases(client, context, cfg):
    """
    Lightweight stress tests.
    """

    ATTEMPTS = 5  # keep dev-friendly

    for i in range(ATTEMPTS):
        result = run_mock_flow(client, context, cfg)
        assert_mock_success(result)

    print(f"Stress test completed: {ATTEMPTS} mock attempts successful.")