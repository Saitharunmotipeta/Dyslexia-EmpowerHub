import argparse


def load_config():
    """
    Central configuration for the single-click testing harness.
    This is the ONLY place where CLI flags are parsed.
    """

    parser = argparse.ArgumentParser(
        description="Single-click test harness for Dyslexia Learning Platform"
    )

    # -----------------------
    # CORE SETTINGS
    # -----------------------
    parser.add_argument(
        "--base-url",
        default="http://localhost:8000",
        help="Backend base URL"
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=15,
        help="Request timeout (seconds)"
    )

    # -----------------------
    # TEST MODES
    # -----------------------
    parser.add_argument(
        "--stress",
        action="store_true",
        help="Enable stress test cases"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed request / response logs"
    )

    # -----------------------
    # STT / AUDIO CONTROL
    # -----------------------
    parser.add_argument(
        "--real-audio",
        action="store_true",
        help="Use real audio files instead of mock STT outputs"
    )

    args = parser.parse_args()

    return {
        # Networking
        "BASE_URL": args.base_url,
        "REQUEST_TIMEOUT": args.timeout,

        # Modes
        "STRESS_MODE": args.stress,
        "VERBOSE": args.verbose,

        # STT
        "USE_REAL_AUDIO": args.real_audio,

        # Safety flags (future-proof, unused for now)
        "TEST_MODE": True,
    }
