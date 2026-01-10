def run_learning_flow(client, context, cfg):
    """
    Simulate learning exposure for a level.
    Progress-based, production-aligned.
    """

    word_ids = context["word_ids"]

    learned_words = []

    for word_id in word_ids:
        # Learning exposure via TTS
        resp = client.get(f"/learning/tts/{word_id}")
        if resp.status_code != 200:
            raise RuntimeError(f"TTS failed for word_id={word_id}")

        learned_words.append(word_id)

    # ✅ Progress signal = exposure completed
    # Learning evaluation happens later via practice/mock
    return {
        "learned_words": learned_words,
        "progress": True
    }
