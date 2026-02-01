-- ================================
-- LEVELS
-- ================================
INSERT INTO levels (id, name, description, difficulty, "order") VALUES
(1, 'Basics', 'Simple everyday words', 'easy', 1),
(2, 'Intermediate', 'Longer common words', 'medium', 2),
(3, 'Advanced', 'Complex academic words', 'hard', 3)
ON CONFLICT DO NOTHING;

-- ================================
-- WORDS
-- ================================
INSERT INTO words (id, text, phonetics, syllables, difficulty, level_id) VALUES
-- Level 1
(1, 'cat', 'kat', 'cat', 'easy', 1),
(2, 'dog', 'dog', 'dog', 'easy', 1),
(3, 'sun', 'sun', 'sun', 'easy', 1),
(4, 'book', 'buk', 'book', 'easy', 1),
(5, 'tree', 'tree', 'tree', 'easy', 1),

-- Level 2
(6, 'planet', 'planet', 'pla-net', 'medium', 2),
(7, 'river', 'river', 'ri-ver', 'medium', 2),
(8, 'pencil', 'pencil', 'pen-cil', 'medium', 2),
(9, 'mountain', 'mountain', 'moun-tain', 'medium', 2),
(10, 'window', 'window', 'win-dow', 'medium', 2),

-- Level 3
(11, 'education', 'education', 'ed-u-ca-tion', 'hard', 3),
(12, 'responsibility', 'responsibility', 're-spon-si-bi-li-ty', 'hard', 3),
(13, 'architecture', 'architecture', 'ar-chi-tec-ture', 'hard', 3),
(14, 'imagination', 'imagination', 'i-ma-gi-na-tion', 'hard', 3),
(15, 'communication', 'communication', 'com-mu-ni-ca-tion', 'hard', 3)
ON CONFLICT DO NOTHING;
