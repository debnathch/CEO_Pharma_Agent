# Zero-Cost Free Deployment Guide

> **Bengal Remedies** • Enterprise Pharmaceutical Agentic AI Ecosystem • 100% Free Deployment Architectures

This guide details step-by-step instructions for deploying this full-stack application (FastAPI backend + React executive dashboard + SQLite/PostgreSQL) **completely free of charge with zero paid API keys or cloud subscriptions**.

---

## Architecture Summary

| Layer | Component | Free Cloud Option |
| :--- | :--- | :--- |
| **All-in-One Container** | Multi-stage Docker (FastAPI + React SPA) | **Render.com** (Free Web Service) or **Hugging Face Spaces** |
| **Frontend UI Only** | React 19 + TypeScript + Vite | **Vercel** / **Netlify** / **Cloudflare Pages** (Free forever) |
| **Backend API Only** | Python 3.12 + FastAPI + LangGraph | **Render.com** / **Koyeb** / **Fly.io** |
| **Database** | Synthetic pharmaceutical schema | **SQLite** (file-based, \$0) or **Neon.tech** (PostgreSQL, \$0) |
| **LLM Provider** | Agent synthesis & responses | **MockLLMProvider** (deterministic, \$0) or **Ollama** via free Cloudflare Tunnel |

---

## Option 1: 1-Click All-in-One Deployment on Render.com (Recommended)

Render provides a **free web service tier** (750 free hours/month). With the multi-stage [Dockerfile](file:///Users/debz/Documents/BR/Project/Ben_Rem/CEO_MultiAgent_Ecosystem/Dockerfile), Render builds the React frontend and runs FastAPI in a single container.

### Step 1: Push your code to GitHub
Make sure your changes are pushed to your GitHub repository:
```bash
git add .
git commit -m "feat: configure zero-cost free deployment"
git push origin main
```

### Step 2: Create Web Service on Render
1. Visit [dashboard.render.com](https://dashboard.render.com/) and sign up/in with GitHub.
2. Click **New +** > **Web Service** (or **Blueprint** to use `render.yaml`).
3. Connect your GitHub repository.
4. Set the following configuration:
   - **Name**: `bengal-remedies-ceo`
   - **Region**: Closest to you (e.g. Frankfurt, Oregon, Singapore)
   - **Branch**: `main`
   - **Runtime**: **Docker**
   - **Instance Type**: **Free**
5. Add Environment Variables:
   - `ENVIRONMENT` = `production`
   - `DATA_MODE` = `synthetic`
   - `LLM_PROVIDER` = `mock`
   - `DATABASE_URL` = `sqlite:///./data/pharma.db`
   - `LOG_LEVEL` = `INFO`
6. Click **Deploy Web Service**.

> [!NOTE]
> Render free services spin down after 15 minutes of inactivity. When a new visitor accesses your URL, it takes ~40-50 seconds to warm up and wake up.

---

## Option 2: Hugging Face Spaces (100% Free, 16GB RAM, 2 vCPUs)

Hugging Face Spaces offers free Docker hosting with generous CPU and 16 GB of memory with **no credit card required**.

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces) and click **Create new Space**.
2. Set:
   - **Space SDK**: **Docker** (Blank)
   - **License**: Apache 2.0 or MIT
   - **Space Hardware**: Free (2 vCPU, 16 GB RAM)
3. Clone the Space repo or link it to your GitHub repository:
   Add this metadata header to the top of the repository `README.md` if pushing directly to HF:
   ```yaml
   ---
   title: Bengal Remedies CEO Agent
   emoji: 💊
   colorFrom: blue
   colorTo: indigo
   sdk: docker
   app_port: 8000
   ---
   ```
4. Push your code. The space will automatically build and start both the API and the React UI.

---

## Option 3: Split Deployment (Backend on Render + Frontend on Vercel)

For ultra-fast global edge frontend delivery:

### Step 1: Deploy Backend to Render
1. Follow Option 1 above.
2. Note your public backend URL: `https://<your-render-subdomain>.onrender.com`.

### Step 2: Deploy Frontend to Vercel
1. Go to [vercel.com](https://vercel.com) and sign in.
2. Click **Add New...** > **Project** and select your GitHub repository.
3. Configure project settings:
   - **Framework Preset**: Vite
   - **Root Directory**: `apps/web`
4. Expand **Environment Variables** and add:
   - `VITE_API_URL` = `https://<your-render-subdomain>.onrender.com/api/v1`
5. Click **Deploy**. Vercel will build and deploy the React command center onto its global CDN.

---

## Option 4: Local Ollama + Free Public HTTPS (Cloudflare Tunnel)

If you want to use **real local Ollama LLMs** (`qwen3:4b`, `llama3.2:3b`) without paying for expensive cloud GPU instances:

1. Start your local Ollama instance:
   ```bash
   ollama serve
   ollama run qwen3:4b
   ```
2. Start the FastAPI backend and React frontend locally:
   ```bash
   # Terminal 1: Backend
   source .venv/bin/activate
   LLM_PROVIDER=ollama uvicorn apps.api.main:app --host 0.0.0.0 --port 8000

   # Terminal 2: Frontend
   cd apps/web && npm run dev
   ```
3. Expose the application via **Cloudflare Tunnel** (free, no port forwarding or credit card needed):
   ```bash
   brew install cloudflare/cloudflare/cloudflared
   cloudflared tunnel --url http://localhost:8000
   ```
4. Cloudflare provides a free HTTPS URL (e.g. `https://random-subdomain.trycloudflare.com`) accessible from any browser anywhere in the world, completely free while powered by your local machine's Ollama model!
