# Chatbot Agent Module — Dyslexia EmpowerHub

## Overview

This module implements a database-grounded intelligent chatbot agent.

It does NOT allow the LLM to access the database directly.
All analytics are computed deterministically in backend engines.

The LLM is used only for explanation and guidance.

---

## Architecture

Request Flow:

Route → Orchestrator → Engine → Response Router → (Deterministic OR LLM)

---

## Key Components

### agent/
- intent_detector.py → Classifies user intent
- intent_registry.py → Maps intent to engine + prompt
- response_router.py → Decides deterministic vs LLM
- orchestrator.py → Core execution controller

### analysis/
Deterministic analytics engines:
- resume_engine
- progress_engine
- similarity_engine
- mock_engine
- practice_engine
- aggregate_engine

### services/
- prompt_loader.py → Loads external prompt templates
- llm_client.py → Handles OpenRouter calls + token tracking

### schemas/
- chat_request.py
- chat_response.py

---

## Cost Control Strategy

- Numeric queries bypass LLM
- Minimal structured context sent to LLM
- Response limited to 8 lines
- Token usage printed in console
- Configurable via .env

---

## Environment Variables

Defined in `.env`:

CHATBOT_USE_LLM_FOR_NUMERIC  
CHATBOT_MAX_RESPONSE_LINES  
CHATBOT_MAX_PROMPT_CHAR_LENGTH  
CHATBOT_ENABLE_TOKEN_PRINT  
CHATBOT_MODEL_NAME  
CHATBOT_TEMPERATURE  
CHATBOT_MAX_TOKENS  

---

## Production Safety

- No raw DB access by LLM
- Deterministic analytics
- Fallback response on LLM failure
- Strict response schema
- Token estimation monitoring

---

## Future Enhancements

- LLM-based intent classification
- Tool-based multi-step reasoning
- LangGraph experimentation branch
- Chat logging for analytics
