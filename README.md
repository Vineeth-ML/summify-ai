# ⚡ Summify — Instant AI Summaries

Summify is a Streamlit web app that takes any **YouTube video** or **website URL** and returns a concise 300-word AI-generated summary — powered by **Groq's LLaMA 3.1** and **LangChain**.

---

## ✨ Features

- 🎬 Summarize **YouTube videos** via transcript extraction
- 🌐 Summarize **any webpage** via URL
- ⚡ Blazing-fast inference using **Groq's LLaMA-3.1-8b-instant**
- 🔗 LangChain `map_reduce` chain handles long content gracefully
- 🔒 API key entered securely via sidebar (never stored)

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web UI |
| `langchain-groq` | Groq LLM integration |
| `langchain-classic` | Prompt templates & summarization chains |
| `langchain-community` | YouTube & URL document loaders |
| `validators` | URL validation |


## 🗂️ Project Structure

```
summify-ai/
├── app.py            # Main Streamlit application
├── requirements.txt  # Python dependencies
└── README.md         # You are here
```

---

## ⚙️ How It Works

1. **User pastes a URL** (YouTube or any website)
2. The appropriate **LangChain loader** fetches the content
3. Content is **split into chunks** (2000 tokens, 100 overlap) to stay within context limits
4. A **map_reduce summarization chain** summarizes each chunk, then combines them
5. The final **300-word summary** is displayed in the app
