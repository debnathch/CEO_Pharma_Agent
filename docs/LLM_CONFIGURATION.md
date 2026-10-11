# Free Local LLM Strategy & Configuration Guide

## 1. Zero Paid API Fee Philosophy

The platform operates completely without paid commercial LLM APIs (OpenAI, Anthropic, Gemini, etc.).

We achieve this via a dual-provider abstraction:
1. **Ollama Local Inference**: Uses open-weights models running directly on the user's host machine.
2. **Deterministic Mock Provider**: A fully offline provider returning structured summaries for tests and lightweight development.

---

## 2. Environment Configuration

Configure the active provider via environment variables in `.env`:

### Option A: Fully Offline Development (Default / Testing)
```bash
LLM_PROVIDER=mock
```
- Requires zero background services or daemons.
- Runs entire test suite in 0.4s.
- Deterministic, reproducible evaluation baselines.

### Option B: Local Inference with Ollama
```bash
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3:4b
OLLAMA_TIMEOUT_SECONDS=30.0
```

---

## 3. Recommended Candidate Models

| Model | Size | Minimum RAM | Tool Calling | Structured Output | Recommended Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`qwen3:4b`** | 2.5 GB | 8 GB | High | Excellent | Recommended primary model for executive summarization |
| **`llama3.2:3b`** | 2.0 GB | 8 GB | Moderate | Good | Alternative lightweight option for constrained hardware |
| **`mistral:7b`** | 4.1 GB | 16 GB | Excellent | Excellent | Best performance if 16GB+ RAM available |

*Important*: Never assume any model is automatically the best across all hardware architectures. Latency, memory bandwidth, context window retention, and formatting consistency should be benchmarked on your target hardware.

---

## 4. Setting Up Ollama

### macOS Setup
```bash
brew install ollama
ollama serve
ollama pull qwen3:4b
```

### Linux Setup
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
ollama pull qwen3:4b
```

### Windows Setup
Download the installer from [ollama.com/download](https://ollama.com/download) and run:
```powershell
ollama pull qwen3:4b
```

---

## 5. Failure Handling & Transparent Reporting

1. **Honest Provider Health Reporting**: `GET /api/v1/health` checks Ollama reachability via `/api/tags` and reports whether the selected model is downloaded.
2. **Never Silently Fabricate**: If Ollama is unreachable, `OllamaLLMProvider` returns an explicit error message: `"Ollama server connection failed at http://localhost:11434"`.
3. **Graceful Deterministic Fallback**: The CEO orchestrator catches the provider error, attaches a warning to the response, and falls back to a deterministic bullet-point synthesis of the verified agent data so the user is never stranded with an unhandled exception.
4. **Provider Mode Visibility**: Every API response and UI screen displays whether `mock` or `ollama` generated the response.
