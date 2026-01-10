import sys
import traceback

from config import load_config
from seed import seed_system

from cases.positive import run_positive_cases
from cases.negative import run_negative_cases
from cases.stress import run_stress_cases


class TestClient:
    """
    Minimal HTTP client wrapper.
    No business logic here.
    """

    def __init__(self, base_url: str, timeout: int, verbose: bool = False):
        import requests
        self.requests = requests
        self.base_url = base_url
        self.timeout = timeout
        self.verbose = verbose
        self.token = None

    def set_token(self, token: str):
        self.token = token

    def _headers(self):
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    def get(self, path: str):
        url = f"{self.base_url}{path}"
        if self.verbose:
            print(f"[GET] {url}")
        return self.requests.get(
            url,
            headers=self._headers(),
            timeout=self.timeout
        )

    def post(self, path: str, json=None, files=None, data=None):
        url = f"{self.base_url}{path}"
        if self.verbose:
            print(f"[POST] {url}")
        return self.requests.post(
            url,
            headers=self._headers(),
            json=json,
            files=files,
            data=data,
            timeout=self.timeout
        )


def main():
    cfg = load_config()

    print("\n==============================")
    print("🧪 SINGLE-CLICK TEST HARNESS")
    print("==============================")

    client = TestClient(
        base_url=cfg["BASE_URL"],
        timeout=cfg["REQUEST_TIMEOUT"],
        verbose=cfg["VERBOSE"]
    )

    context = {}

    try:
        # -------------------------------
        # SEED SYSTEM
        # -------------------------------
        print("\n[1] Seeding system")
        seed_context = seed_system(client, cfg)
        context.update(seed_context)
        print("✅ Seed completed")

        # -------------------------------
        # POSITIVE CASES
        # -------------------------------
        print("\n[2] Running POSITIVE cases")
        run_positive_cases(client, context, cfg)
        print("✅ Positive cases passed")

        # -------------------------------
        # NEGATIVE CASES
        # -------------------------------
        print("\n[3] Running NEGATIVE cases")
        run_negative_cases(client, context, cfg)
        print("✅ Negative cases passed")

        # -------------------------------
        # STRESS CASES (OPTIONAL)
        # -------------------------------
        if cfg["STRESS_MODE"]:
            print("\n[4] Running STRESS cases")
            run_stress_cases(client, context, cfg)
            print("✅ Stress cases passed")

        print("\n==============================")
        print("🎉 ALL TESTS PASSED")
        print("==============================\n")

    except Exception as e:
        print("\n==============================")
        print("❌ TEST HARNESS FAILED")
        print("==============================")
        print(f"Error: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
