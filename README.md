# Local Homelab AI Workshop

A hands-on, 90-minute workshop on running large language models on your own
hardware. Your prompts and documents never leave your machine. Participants
size hardware for a model, drive Ollama from the terminal, build a custom
model, talk to it from Python, and finish with a small RAG pipeline that
answers questions about their own notes.

The workshop comes as a pair: a runnable `.py` file you can execute and
experiment with, and a `.md` workshop file with step-by-step tasks and
collapsible solutions.

---

## Getting Started

**Requirements:** [Ollama](https://ollama.com), Python 3.9 or newer, and about
8 GB of RAM. No GPU and no Python packages are needed. Docker is optional and
only used in the bonus task.

```bash
# Download the two models used in the workshop (~2.3 GB)
ollama pull llama3.2:3b
ollama pull nomic-embed-text

# Run the tutorial
python3 homelab_ai_basics.py
```

Work through the `.md` file alongside the code: read a section, try the task
yourself, then open the solution to compare.

---

## Workshop

### Local Homelab AI
**Files:** [homelab_ai_basics.py](homelab_ai_basics.py) ·
[HOMELAB_AI_BASICS.md](HOMELAB_AI_BASICS.md) · [Modelfile](Modelfile) ·
[docker-compose.yml](docker-compose.yml)

| Time | Part |
|---|---|
| 0:00 – 0:10 | Why local AI: privacy, cost, offline use, control. Model, runtime and interface |
| 0:10 – 0:20 | Will it fit? Parameters, quantisation and a memory estimator |
| 0:20 – 0:40 | Ollama CLI and a custom model built from a Modelfile |
| 0:40 – 1:05 | The HTTP API from `curl` and Python: tokens, chat history, temperature, streaming |
| 1:05 – 1:25 | Embeddings, cosine similarity and a minimal RAG pipeline |
| 1:25 – 1:30 | Bonus: a permanent Ollama + Open WebUI stack with Docker Compose |

The Python tasks assume you are comfortable with functions, lists and
dictionaries.
