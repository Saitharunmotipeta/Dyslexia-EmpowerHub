# Database Infrastructure

This folder contains database infrastructure artifacts.

## Files
- schema.sql       → Database schema (tables, indexes, constraints)
- seed_static.sql  → Static learning content (levels + words)

## Rules
- These files are NOT executed automatically by the backend
- They are run manually or via CI in the future
- Backend runtime must NOT depend on this folder

## Environments
- Development: Local PostgreSQL
- Production: Supabase PostgreSQL

## Static Content Contract
If a word exists in `seed_static.sql`, corresponding static assets
(images + TTS) must exist in the static-assets repository.
