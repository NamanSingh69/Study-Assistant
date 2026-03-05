# Render Deployment Guide — Study Assistant

## ⚠️ Cold Start Disclaimer

> **Render Free Tier services spin down after 15 minutes of inactivity.** The first request after idle will take **30–60 seconds**. Note generation with Gemini 2.5 Pro can take an additional **30–90 seconds** for large content.

---

## 🔑 Getting Your Free Gemini API Key

1. Visit **[Google AI Studio](https://aistudio.google.com/app/apikey)**
2. Sign in with any Google account
3. Click **"Create API Key"** → Copy it
4. **Free forever** — no credit card, no billing required

### Free Tier Limits

| Model | RPM | Best For |
|-------|-----|----------|
| `gemini-2.5-pro` | 2 | Comprehensive note generation |
| `gemini-flash-latest` | 15 | Quizzes, flashcards, quick Q&A |
| `gemini-flash-lite-latest` | 30 | Search query generation |

### Google Custom Search API (Optional)
- Get a [Programmable Search Engine](https://programmablesearchengine.google.com/) CX ID
- **100 free searches/day** for web-augmented notes

---

## 🔄 Model Fallback Routing

The app uses `gemini-2.5-pro` by default. Recommended fallback strategy:

```python
# Suggested model cascade — add to app.py
MODEL_CASCADE = [
    "gemini-2.5-pro",          # Best quality
    "gemini-2.5-flash",        # Good quality, faster
    "gemini-flash-latest",     # Fast fallback
]

def get_model_with_fallback():
    for model_name in MODEL_CASCADE:
        try:
            model = genai.GenerativeModel(model_name)
            # Quick test call
            model.generate_content("test", request_options={"timeout": 5})
            return model
        except Exception:
            continue
    return genai.GenerativeModel(MODEL_CASCADE[-1])
```

---

## Environment Variables (Render Dashboard)

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | ✅ Yes | From [AI Studio](https://aistudio.google.com/app/apikey) |
| `SEARCH_ENGINE_ID` | ✅ Yes | Google Programmable Search Engine CX ID |

---

## Deployment Steps

### 1. Create Render Web Service
1. [render.com/new](https://dashboard.render.com/new) → Connect GitHub
2. Set **Root Directory** to project folder
3. Environment: **Docker** → Instance Type: **Free**
4. Add environment variables

### 2. Files
```
Dockerfile → python:3.10-slim → pip install requirements
start.sh   → gunicorn app:app --workers 1 --bind 0.0.0.0:$PORT --timeout 120
```

### 3. Post-Deploy
- The `--timeout 120` flag is critical — Gemini 2.5 Pro can take >30s for large notes

---

## Resource Limits

| Resource | Render Free Tier | This Project |
|----------|-----------------|--------------|
| RAM | 512 MB | ~100 MB (Flask + Gemini SDK) |
| Storage | 1 GB | ~500 KB code + temp uploads |
| Bandwidth | 100 GB/month | Moderate |
