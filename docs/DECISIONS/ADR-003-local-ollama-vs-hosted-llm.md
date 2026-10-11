# ADR-003: Local Ollama vs Hosted Cloud LLM Strategy

## Status
Accepted

## Context
Deploying enterprise AI platforms often encounters prohibitive per-token API fees and strict data privacy compliance hurdles (e.g. internal patient and commercial pharma sales data leaving corporate perimeters). The platform must guarantee zero required paid API credentials during initial development, evaluation, and developer onboarding.

## Decision
We implement a **Local-First LLM Architecture** using **Ollama** (`http://localhost:11434`) as the default local inference runtime, supporting open-weights candidate models such as `qwen3:4b` and `llama3.2:3b`.
The model provider is decoupled via the `LLMProvider` interface, allowing hot-swapping via environment variable `LLM_PROVIDER=ollama` or `LLM_PROVIDER=mock`.

## Alternatives Considered
1. **Mandatory OpenAI / Anthropic Cloud APIs**:
   - *Rejected*: Violates zero-API-cost requirement; creates recurring cost friction and external network dependency.
2. **Self-hosted vLLM / TGI GPU cluster**:
   - *Rejected*: Premature hardware infrastructure requirement; excessive complexity for laptop/workstation developer environments.

## Consequences & Trade-offs
- **Positive**:
  - Zero token inference costs.
  - Complete data privacy: no corporate prompts leave local hardware.
  - Works fully offline.
- **Negative / Trade-offs**:
  - Local inference speed depends on host machine hardware (Apple Silicon unified memory vs CPU).
  - Smaller quantized models (3B-4B) require explicit prompt grounding and guardrails to maintain output consistency compared to frontier cloud models.
