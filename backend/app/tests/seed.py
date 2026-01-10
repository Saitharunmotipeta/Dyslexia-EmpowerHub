import sys

TEST_USER = {
    "name": "abcd",
    "email": "abcd@gmail.com",
    "password": "1234"
}


def seed_system(client, cfg):
    """
    Prepare a deterministic baseline for all tests.
    Returns a shared context dictionary.
    """

    print("[SEED] Authenticating test user")
    token = _login_or_register(client)
    client.set_token(token)

    print("[SEED] Fetching learning levels")
    level_id = _get_first_level(client)

    print("[SEED] Fetching words for level")
    word_ids = _get_words_for_level(client, level_id)

    if not word_ids:
        print("❌ No words found for level — cannot continue tests")
        sys.exit(1)

    print("[SEED] Baseline ready")

    return {
        "level_id": level_id,
        "word_ids": word_ids,
        "user_email": TEST_USER["email"],
    }


# -------------------------------------------------------------------
# AUTH HELPERS
# -------------------------------------------------------------------

def _login_or_register(client) -> str:
    """
    Login using OAuth2PasswordRequestForm.
    Register user only if login fails.
    """

    # Try login first (FORM DATA)
    resp = client.post(
        "/auth/login",
        data={
            "username": TEST_USER["email"],  # backend expects email as username
            "password": TEST_USER["password"]
        }
    )

    if resp.status_code == 200:
        return resp.json()["access_token"]

    # Register user (JSON)
    resp = client.post(
        "/auth/register",
        json=TEST_USER
    )

    if resp.status_code not in (200, 201):
        print("❌ Failed to register test user")
        print(resp.text)
        sys.exit(1)

    # Login again
    resp = client.post(
        "/auth/login",
        data={
            "username": TEST_USER["email"],
            "password": TEST_USER["password"]
        }
    )

    if resp.status_code != 200:
        print("❌ Failed to login after registration")
        print(resp.text)
        sys.exit(1)

    return resp.json()["access_token"]


# -------------------------------------------------------------------
# LEARNING HELPERS
# -------------------------------------------------------------------

def _get_first_level(client) -> int:
    resp = client.get("/learning/levels")

    if resp.status_code != 200:
        print("❌ Failed to fetch levels")
        print(resp.text)
        sys.exit(1)

    levels = resp.json()

    if not levels:
        print("❌ No learning levels found")
        sys.exit(1)

    return levels[0]["id"]


def _get_words_for_level(client, level_id: int):
    resp = client.get(f"/learning/levels/{level_id}/words")

    if resp.status_code != 200:
        print("❌ Failed to fetch words for level")
        print(resp.text)
        sys.exit(1)

    words = resp.json()

    return [w["id"] for w in words]
