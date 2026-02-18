-- ================================
-- USERS
-- ================================
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    role VARCHAR NOT NULL DEFAULT 'student',
    password_hash VARCHAR NOT NULL,

    created_at TIMESTAMP DEFAULT NOW(),
    last_login_at TIMESTAMP,
    last_active_at TIMESTAMP,

    tts_rate INTEGER DEFAULT 100,

    streak_days INTEGER DEFAULT 0,
    total_login_days INTEGER DEFAULT 0,

    points INTEGER DEFAULT 0,
    badges VARCHAR DEFAULT '',
    achievements VARCHAR DEFAULT '',

    total_time_spent INTEGER DEFAULT 0,
    courses_completed INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS ix_users_email ON users(email);

-- ================================
-- LEVELS
-- ================================
CREATE TABLE IF NOT EXISTS levels (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR,
    difficulty VARCHAR,
    "order" INTEGER
);

-- ================================
-- WORDS (STATIC LEARNING DATA)
-- ================================
CREATE TABLE IF NOT EXISTS words (
    id SERIAL PRIMARY KEY,
    text VARCHAR NOT NULL,
    phonetics VARCHAR,
    syllables VARCHAR,
    difficulty VARCHAR,
    image_url VARCHAR,
    level_id INTEGER NOT NULL REFERENCES levels(id)
);

CREATE INDEX IF NOT EXISTS ix_words_level_id ON words(level_id);

-- ================================
-- USER LEARNING PROGRESS
-- ================================
CREATE TABLE IF NOT EXISTS level_words (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    word_id INTEGER NOT NULL REFERENCES words(id),
    level_id INTEGER NOT NULL REFERENCES levels(id),

    image_url VARCHAR,

    attempts INTEGER DEFAULT 0,
    correct_attempts INTEGER DEFAULT 0,

    mastery_score DOUBLE PRECISION DEFAULT 0,
    highest_score DOUBLE PRECISION DEFAULT 0,

    is_mastered BOOLEAN DEFAULT FALSE,

    last_similarity DOUBLE PRECISION,
    last_practiced_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_level_words_user ON level_words(user_id);
CREATE INDEX IF NOT EXISTS ix_level_words_word ON level_words(word_id);

-- ================================
-- MOCK TEST ATTEMPTS (ANALYTICS HEAVY)
-- ================================
CREATE TABLE IF NOT EXISTS mock_attempts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    level_id INTEGER NOT NULL REFERENCES levels(id),

    status VARCHAR NOT NULL,
    results JSON NOT NULL DEFAULT '{"words": []}',

    total_score INTEGER,
    verdict VARCHAR,

    started_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    last_accessed_at TIMESTAMPTZ DEFAULT NOW(),

    public_attempt_id INTEGER UNIQUE NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_mock_attempts_user ON mock_attempts(user_id);
CREATE INDEX IF NOT EXISTS ix_mock_attempts_level ON mock_attempts(level_id);
