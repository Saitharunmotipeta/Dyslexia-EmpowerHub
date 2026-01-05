psql -U postgres
psql -U postgres -d dyslexia_learning
\c dyslexia_learning


TRUNCATE TABLE words RESTART IDENTITY CASCADE;