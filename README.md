# Local Homelab AI Workshop

A hands-on, 90-minute beginner workshop on running AI language models on your
own hardware. Your questions and documents never leave your machine.
Participants find out which models their computer can run, chat with a model
through Ollama, build their own assistant, start a ChatGPT-like browser
interface with Docker and Open WebUI, and let it answer questions about their
own documents. It ends with a checklist for keeping the setup safe.

**No programming experience needed.** Every command is given in full. An
optional final part shows the same ideas in Python for those who want to go
further.

---

## Getting Started

**Requirements:** a computer with at least 8 GB of RAM,
[Ollama](https://ollama.com) and
[Docker Desktop](https://www.docker.com/products/docker-desktop/). A graphics
card is not needed. Python 3.9+ is only needed for the optional part.

Participants **do not need this repository**. They create their own
`homelab-ai` project folder and copy each file from the workshop text into
it, as explained in the workshop's *Before the Workshop* section. The files in
this repository are the finished versions, for instructors and for checking.

Work through the `.md` file: read a section, try the task yourself, then open
the solution to compare.

---

## Workshop

### Local Homelab AI
**Workshop:** [HOMELAB_AI_BASICS.md](HOMELAB_AI_BASICS.md)

**Reference files** (participants create these themselves during the tasks):
[Modelfile](Modelfile) (Task 4) · [docker-compose.yml](docker-compose.yml)
(Task 5) · [sample_docs/homelab_handbook.md](sample_docs/homelab_handbook.md)
(Task 7) · [homelab_ai_basics.py](homelab_ai_basics.py) (optional part,
downloaded from GitHub)

| Time | Part |
|---|---|
| 0:00 – 0:10 | Why local AI: privacy, cost, offline use, control. Model, runtime and interface |
| 0:10 – 0:20 | Will it fit? Choosing a model size for your computer |
| 0:20 – 0:35 | Ollama: first model and first conversation |
| 0:35 – 0:45 | How models behave: tokens, memory, temperature, hallucinations |
| 0:45 – 0:55 | Your own assistant with a Modelfile |
| 0:55 – 1:05 | Docker in five minutes and starting Open WebUI |
| 1:05 – 1:15 | Open WebUI for everyday use: accounts, models, system prompts |
| 1:15 – 1:25 | RAG: asking questions about your own documents |
| 1:25 – 1:30 | Keeping it safe: access, backups, updates |
| Optional | Talking to the model from `curl` and Python |

`docker-compose.yml` runs only Open WebUI and uses the Ollama installed on
your computer. [docker-compose.full-stack.yml](docker-compose.full-stack.yml)
runs both in Docker, for a dedicated home server.
