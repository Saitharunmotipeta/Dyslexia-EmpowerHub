# app/feedback/services/trend_service.py

from statistics import mean


def trend_analysis(score: float, attempts: int, recent_scores: list[float] | None = None):

    if attempts <= 1:
        return {
            "code": "first_try",
            "title": "First Attempt",
            "message": "Great — you’ve taken the first step.",
            "tip": "Try again and watch your progress build 📈",
            "confidence": "high"
        }

    if not recent_scores:
        recent_scores = [score]

    last = recent_scores[-1]
    avg = mean(recent_scores)
    gain = score - last
    consistency = max(recent_scores) - min(recent_scores)

    # MASTERED — stable confidence
    if score >= 90 and avg >= 85 and consistency <= 10:
        return {
            "code": "mastered_trend",
            "title": "Consistently Excellent",
            "message": "Your pronunciation is consistently strong.",
            "tip": "You’ve got this — keep the streak alive 💫",
            "confidence": "very_high"
        }

    # BREAKTHROUGH
    if gain >= 20 and score >= 75:
        return {
            "code": "breakthrough",
            "title": "Breakthrough Moment",
            "message": "Huge improvement since your last attempt!",
            "tip": "Lock this in — repeat it once more to build muscle memory 🔒",
            "confidence": "high"
        }

    # FAST IMPROVEMENT
    if score > avg + 10:
        return {
            "code": "improving_fast",
            "title": "Rapid Improvement",
            "message": "You’re improving really quickly.",
            "tip": "Stay consistent — you’re on a roll 🚀",
            "confidence": "high"
        }

    # SLOW IMPROVEMENT
    if 0 < gain < 10 and score >= avg:
        return {
            "code": "steady_growth",
            "title": "Steady Growth",
            "message": "Your pronunciation is improving step-by-step.",
            "tip": "Small gains compound — keep going 🌱",
            "confidence": "medium"
        }

    # PLATEAU
    if abs(gain) <= 3 and consistency <= 8:
        return {
            "code": "plateau",
            "title": "Progress Paused",
            "message": "You’re repeating at the same level.",
            "tip": "Try changing pace or slowing down 🐢",
            "confidence": "medium"
        }

    # FLUCTUATING
    if consistency >= 25:
        return {
            "code": "fluctuating",
            "title": "Inconsistent Performance",
            "message": "Your scores are jumping up and down.",
            "tip": "Try focusing on pronunciation rhythm 🎶",
            "confidence": "medium"
        }

    # REGRESSION
    if gain < -12 and score < avg:
        return {
            "code": "regressing",
            "title": "Small Dip",
            "message": "Today’s score is lower than usual.",
            "tip": "No stress — take a breath and try again 😊",
            "confidence": "medium_low"
        }

    # FATIGUE
    if attempts >= 6 and score < last and score < 60:
        return {
            "code": "fatigue_drop",
            "title": "Getting Tired",
            "message": "Your score is dropping — you might be fatigued.",
            "tip": "Take a short break ☕ and try later.",
            "confidence": "low"
        }

    # STRUGGLING
    if avg < 55 and attempts >= 5:
        return {
            "code": "stuck",
            "title": "Finding This Tricky",
            "message": "You’ve been trying hard — but scores are still low.",
            "tip": "Break the word into sounds. Slow. Calm. One step at a time 🧘",
            "confidence": "low"
        }

    # EARLY LEARNING
    if avg < 65:
        return {
            "code": "early_stage",
            "title": "Early Learning Phase",
            "message": "You are still getting familiar with the sound.",
            "tip": "Repetition helps — you’re building the foundation 🧱",
            "confidence": "medium"
        }

    return {
        "code": "learning",
        "title": "Active Learning",
        "message": "You’re making steady progress.",
        "tip": "Stay curious — you’re doing great 💙",
        "confidence": "medium_high"
    }
