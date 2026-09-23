# Workshop: Local Homelab AI

**Duration:** 90 minutes · **Level:** beginner ·
**Prerequisites:** none. You should be able to install programs on your
computer. Every terminal command is given in full, and no programming is
needed. The Python part at the end is optional.

---

## Introduction

### Background

Tools like ChatGPT run a **large language model (LLM)** on someone else's
servers: your question travels over the internet, is processed there, and the
answer travels back. For personal use that is often fine. For customer
records, patient data, contracts, or internal company documents it can be a
legal and practical problem.

A **local LLM** runs the same kind of model on hardware you own. The question
never leaves your machine. There are no per-request fees, it works offline,
and nobody can change or switch off the model behind your back. The price is
that your hardware has to be strong enough, and you are the one running it.

| | Cloud AI | Local AI |
|---|---|---|
| **Privacy** | Prompts go to the provider | Prompts stay on your machine |
| **Cost** | Subscription or pay per request | Hardware you already own or buy once |
| **Offline** | Needs internet | Works without a network |
| **Control** | Provider picks model and updates | You pick, pin and update the model |
| **Quality ceiling** | Largest frontier models | Limited by your memory |

Every local AI setup is built from the same three layers. You will set up
all three today:

| Layer | Job | Today |
|---|---|---|
| **Model** | The trained "brain": a file of billions of numbers | `llama3.2:3b` |
| **Runtime** | Loads the model into memory and generates text | **Ollama** |
| **Interface** | How people talk to the runtime | Terminal, then **Open WebUI** in the browser |

### Schedule

| Time | Part | Tasks |
|---|---|---|
| 0:00 – 0:10 | Why local AI, check the setup | Introduction |
| 0:10 – 0:20 | Will a model fit on my computer? | Task 1 |
| 0:20 – 0:35 | Ollama: first model, first conversation | Task 2 |
| 0:35 – 0:45 | How models behave | Task 3 |
| 0:45 – 0:55 | Your own assistant with a Modelfile | Task 4 |
| 0:55 – 1:05 | Docker in five minutes, start Open WebUI | Task 5 |
| 1:05 – 1:15 | Open WebUI for everyday use | Task 6 |
| 1:15 – 1:25 | Ask questions about your own documents (RAG) | Task 7 |
| 1:25 – 1:30 | Keeping it safe | Task 8 |
| Homework | Optional: talk to your model from Python | Tasks 9 – 10 |

### Before the Workshop

Downloads are big. Please do these steps **at home, before the workshop**.

**1. Install Ollama** from [ollama.com](https://ollama.com) (macOS, Windows,
Linux). On macOS and Windows, run the installer and open the app once.

**2. Open a terminal**

- **macOS:** press `Cmd + Space`, type `Terminal`, press Enter.
- **Windows:** press the Windows key, type `PowerShell`, press Enter.
- **Linux:** usually `Ctrl + Alt + T`.

**3. Download a model** (about 2 GB). Type this and press Enter:

```bash
ollama pull llama3.2:3b
```

**4. Install Docker Desktop** from
[docker.com](https://www.docker.com/products/docker-desktop/) and start it
once. Then download Open WebUI in advance (several GB):

```bash
docker pull ghcr.io/open-webui/open-webui:main
```

**5. Install a text editor for code.** You will write a few small text
files today. Word processors such as Word or TextEdit add hidden formatting
and break these files. The free [Visual Studio Code](https://code.visualstudio.com)
works on every system and is what the instructions assume.

**6. Create your project folder.** All files from this workshop go into one
folder called `homelab-ai` in your home folder. These commands work the same
on macOS, Windows (PowerShell) and Linux:

```bash
cd ~                 # Go to your home folder
mkdir homelab-ai     # Create the project folder
cd homelab-ai        # Go into it
code .               # Open the folder in Visual Studio Code
```

If `code .` is not found, open VS Code yourself and choose *File → Open
Folder…* → `homelab-ai`.

**Hardware:** 8 GB of RAM is enough for today. A graphics card is not needed.
It only makes answers faster.

### Creating a File in Your Project Folder

Several tasks ask you to create a file. It always works the same way:

1. In VS Code, click the *New File* icon next to `HOMELAB-AI` in the file
   list on the left (or *File → New File…*).
2. Type the **exact** file name given in the task, e.g. `Modelfile`, with no
   `.txt` at the end.
3. Copy the content from the workshop into the file and save it with
   `Cmd + S` (macOS) or `Ctrl + S` (Windows/Linux).

Terminal commands in the tasks must be run **inside the project folder**. If
you open a new terminal window, go back into it first with `cd ~/homelab-ai`.
In VS Code, *Terminal → New Terminal* opens a terminal that is already in the
right place.

---

## Task 1 — Will It Fit? Choosing a Model for Your Computer

A model's size is given as its number of **parameters**, which are the
numbers it learned during training. `3B` means 3 billion, `70B` means 70
billion. More parameters usually means more knowledge and better reasoning,
but also more memory.

To run a model, **all of it must fit in memory**:

- a graphics card's own memory (**VRAM**), which is fast, or else
- normal **RAM**, which is slower, but works.
- Apple Silicon Macs share one memory pool, so there all of it counts.

Downloaded models are usually **quantised**: each number is stored in about
4–5 bits instead of 16. That makes them 3–4 times smaller and only slightly
worse. This gives a simple rule of thumb:

> **Memory needed ≈ billions of parameters × 0.6 GB** (plus headroom for your
> operating system)

| Model size | Memory needed (quantised) | Typical hardware |
|---|---|---|
| 1 – 4B | 1 – 3 GB | Any laptop from the last 5 years |
| 7 – 9B | 5 – 6 GB | 16 GB laptop, entry-level gaming GPU |
| 12 – 14B | 8 – 10 GB | 16 GB Mac or 12 – 16 GB graphics card |
| 27 – 32B | 17 – 22 GB | 32 GB Mac, 24 GB graphics card |
| 70B | 40 – 48 GB | 64 GB Mac, two large graphics cards |

**Your task:** find out how much memory your computer has. Then decide:
**what is the largest model size you could run?**

<details>
<summary>Solution</summary>

**Where to look:**

| System | RAM | Graphics memory (VRAM) |
|---|---|---|
| **macOS** | Apple menu → *About This Mac* → *Memory* | Same as RAM on Apple Silicon |
| **Windows** | Task Manager (`Ctrl + Shift + Esc`) → *Performance* → *Memory* | Same window → *GPU* → *Dedicated GPU memory* |
| **Linux** | `free -h` in the terminal | `nvidia-smi` (NVIDIA cards) |

**Example answers:**
- 8 GB laptop without a graphics card: stay at **3 – 4B**. Everything else
  already uses half of your RAM.
- 16 GB MacBook: **7 – 9B** runs comfortably, 14B is the limit.
- Gaming PC with a 12 GB graphics card: **up to 14B** fully on the card,
  which is fast.

**Key points:**
- Do not plan to use all of your memory. The operating system, browser and
  the conversation itself need some too.
- If a model does not fit in VRAM, Ollama puts the rest in normal RAM. It
  still works, but can be several times slower.
- A bigger model is not automatically the right choice. A fast 8B model you
  enjoy using beats a 32B model that takes a minute per answer.

</details>

---

## Task 2 — Ollama: First Model, First Conversation

**Ollama** runs quietly in the background, like a small server on your own
computer. The `ollama` command in the terminal is how you give it
instructions.

Type these commands one at a time and write down what each one does:

1. `ollama list`
2. `ollama run llama3.2:3b`: now ask it something, for example *"Explain
   what a homelab is in two sentences."*
3. While the chat is open, type `/?` and press Enter.
4. Open a **second** terminal window and type `ollama ps`. Look at the
   `SIZE` and `PROCESSOR` columns.
5. Back in the chat, type `/bye`. Then try `ollama show llama3.2:3b`.

<details>
<summary>Solution</summary>

| Command | What it does |
|---|---|
| `ollama list` | Shows all models downloaded to your disk |
| `ollama run llama3.2:3b` | Loads the model and starts a chat (downloads it first if needed) |
| `/?` | Lists the commands available inside a chat |
| `ollama ps` | Shows models currently loaded **in memory**, and how much they use |
| `/bye` | Leaves the chat (so does `Ctrl + D`) |
| `ollama show llama3.2:3b` | Details: parameter count, quantisation, context length, licence |

Other useful commands:

```bash
ollama pull gemma3:4b        # Download another model without starting a chat
ollama rm gemma3:4b          # Delete a model to free disk space
ollama stop llama3.2:3b      # Unload it from memory right now
```

**Key points:**
- The part after the colon is a **tag**, usually the size: `llama3.2:3b`,
  `qwen3:8b`. Browse all available models at
  [ollama.com/library](https://ollama.com/library).
- `PROCESSOR: 100% GPU` in `ollama ps` is ideal. A split like `50%/50%
  CPU/GPU` means the model did not fit in graphics memory.
- A loaded model stays in memory for about 5 minutes after your last message,
  then is unloaded automatically.
- Try pulling the plug: switch off Wi-Fi and keep chatting. It still works.

</details>

---

## Task 3 — How Models Behave

Start a chat again with `ollama run llama3.2:3b` and try these four small
experiments:

1. **Speed:** type `/set verbose`, then ask a question. What do the numbers
   below the answer mean?
2. **Memory:** tell the model *"My name is Sam."* Then ask *"What is my
   name?"* Now type `/clear` and ask again.
3. **Temperature:** type `/set parameter temperature 0` and ask *"Invent a
   name for a home server. Reply with the name only."* Then type `/clear` and
   ask again. Repeat once more, so you have three answers. Then do the same
   with `/set parameter temperature 1.5`. (`/clear` wipes the conversation
   but keeps the temperature setting.)
4. **Confidence:** ask *"Which Ollama command shows the models loaded in
   memory right now?"* Is the answer right? (You know it from Task 2.)

<details>
<summary>Solution</summary>

**1. Speed.** The most important line is **eval rate**, the speed of the
answer in **tokens per second**. Models do not read or write whole words but
**tokens**, which are word pieces. An English word is about 1.3 tokens, and
German words need more. About 10 tokens/s feels like fast reading. Below 5 it
feels slow.

**2. Memory.** Before `/clear` the model knows your name. Afterwards it does
not. The model itself remembers **nothing**. The chat program resends the
whole conversation with every new message. The amount it can take in at once
is the **context window**. In very long conversations, the oldest parts fall
out and are "forgotten".

**3. Temperature.** At `0` you get the same answer every time. The model
always takes the most likely next word. At `1.5` you get a different, more
unusual name each time. Use low temperature for facts and summaries, and
higher temperature for brainstorming.

Why `/clear`? Without it, the second question arrives *together with* the
first question and answer, and the model avoids repeating a name it already
gave, even at temperature 0. Temperature 0 means "same input, same output",
and a longer conversation is a different input. In testing, three questions
in one chat gave *Domus, NovaSpire, Kairos*, and three cleared chats gave
*Domus, Domus, Domus*.

**4. Confidence.** Small models often answer this **wrongly but
confidently**. In testing, a 3B model suggested a Docker command instead of
`ollama ps`. This is called a **hallucination**: the model produces text that
*sounds* right, and has no built-in sense of whether it *is* right.

**Key points:**
- Always check important facts, especially with small models.
- Hallucinations get rarer with bigger models and with RAG (Task 7), but
  never disappear completely.

</details>

---

## Task 4 — Your Own Assistant with a Modelfile

A **Modelfile** is a short text file that creates a new model from an
existing one. It does **not** retrain anything. It packages the base model
together with:

- a **system prompt**: standing instructions the model follows in every
  conversation
- default **parameters**, such as temperature

**1.** In your `homelab-ai` folder, create a file named exactly `Modelfile`
(capital M, no file extension) with this content:

```dockerfile
FROM llama3.2:3b

PARAMETER temperature 0.3
PARAMETER num_ctx 4096

SYSTEM """
You are a friendly homelab assistant. You help people run services such as
Ollama, Docker, backups and home networks on their own hardware.
Keep answers short, prefer concrete commands, and say clearly when you are
not sure about something.
"""
```

**2.** In the terminal, inside `homelab-ai`, build and try your assistant:

```bash
ollama create homelab-helper -f Modelfile
ollama run homelab-helper
```

**3.** What does each line of the Modelfile do?

**4.** Change the `SYSTEM` text so the assistant does something different,
for example answering like a patient teacher, or always replying in German.
Save, run the same `ollama create` command again, and compare.

<details>
<summary>Solution</summary>

| Line | Meaning |
|---|---|
| `FROM` | The model to start from |
| `PARAMETER temperature 0.3` | Rather predictable answers |
| `PARAMETER num_ctx 4096` | Context window: how many tokens of conversation it can see |
| `SYSTEM` | The standing instructions |

A German-speaking variant only needs a different system prompt:

```dockerfile
SYSTEM """
Du bist ein geduldiger Homelab-Assistent. Antworte immer auf Deutsch,
kurz und mit konkreten Befehlen.
"""
```

**Key points:**
- `ollama list` now shows `homelab-helper`. It shares the base model's files
  on disk, so it takes up almost no extra space.
- A system prompt shapes **style and focus**. It does not add knowledge. If
  the base model does not know something, the assistant does not either.
- Remove it again with `ollama rm homelab-helper`.
- `open Modelfile: no such file or directory` means the terminal is not in
  the `homelab-ai` folder (run `cd ~/homelab-ai`), or the editor saved the
  file as `Modelfile.txt`. Rename it, or use `-f Modelfile.txt`.

</details>

---

## Task 5 — Docker in Five Minutes, Starting Open WebUI

The terminal is fine for you, but not for the rest of your family or team.
**Open WebUI** gives your local model a ChatGPT-like page in the browser.

We run it with **Docker**. Docker packages a program together with
everything it needs into a **container**, so it runs the same on every
computer and you don't need to install anything else.

| Term | Meaning |
|---|---|
| **Image** | The packaged program, downloaded once (like an installer) |
| **Container** | A running copy of an image (like the installed program) |
| **Volume** | A storage area that survives when the container is deleted: **your data lives here** |
| **docker-compose.yml** | A text file describing which containers to start, and how |

**1.** In your `homelab-ai` folder, create a file named `docker-compose.yml`
with this content. Lines starting with `#` are comments for you. Docker
ignores them.

```yaml
# Open WebUI in Docker, talking to the Ollama installed on this computer.

name: homelab-ai

services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    restart: unless-stopped
    ports:
      - "127.0.0.1:3000:8080"
    environment:
      - OLLAMA_BASE_URL=http://host.docker.internal:11434
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - open-webui-data:/app/backend/data

volumes:
  open-webui-data:
```

In YAML files, the **indentation matters**: use spaces, never tabs, and keep
the lines exactly as far indented as above.

**2.** Read the file and find the answers to:

1. On which address will Open WebUI be reachable in your browser?
2. How does Open WebUI find your Ollama?
3. Where are your accounts and chats stored?

**3.** In the terminal, inside `homelab-ai`, start it:

```bash
docker compose up -d
```

Wait about a minute and open <http://localhost:3000>.

> **Linux only:** Ollama on Linux listens only to programs on the same
> computer, and a container does not count. Run `sudo systemctl edit ollama`,
> add the two lines `[Service]` and `Environment="OLLAMA_HOST=0.0.0.0"`, save,
> and run `sudo systemctl restart ollama`. Make sure your firewall blocks port
> 11434 from other computers.

<details>
<summary>Solution</summary>

1. `127.0.0.1:3000:8080` means that port **3000 on your computer** leads to
   port 8080 inside the container, so the address is <http://localhost:3000>.
   `127.0.0.1` restricts it to your own computer.
2. Through `OLLAMA_BASE_URL=http://host.docker.internal:11434`.

   A container is like a **small separate computer inside your computer**.
   `localhost` always means "the computer I am on", so inside the container
   it means the container itself, and Ollama is not in there.
   `host.docker.internal` is Docker's name for *the real computer the
   container runs on* (its **host**). `:11434` is the **port**, the "door
   number" Ollama listens behind.

   ```
   ┌───────────── Your computer (the host) ─────────────┐
   │  Ollama, port 11434                                │
   │     ▲                                              │
   │     │ host.docker.internal:11434                   │
   │  ┌──┴────────── Container ──────────┐              │
   │  │ Open WebUI                       │              │
   │  │ "localhost" = only this box  ✗   │              │
   │  └──────────────────────────────────┘              │
   └────────────────────────────────────────────────────┘
   ```

3. In the volume `open-webui-data`. Docker puts the project name in front,
   so `docker volume ls` lists it as `homelab-ai_open-webui-data`. Deleting and
   recreating the container keeps it.

| Line | Meaning |
|---|---|
| `name: homelab-ai` | Name of this project, used in front of container and volume names |
| `image:` | Which packaged program to run |
| `restart: unless-stopped` | Start it again automatically after a reboot, unless you stopped it |
| `ports:` | Which port on your computer leads into the container |
| `environment:` | Settings passed to the program |
| `extra_hosts:` | Makes `host.docker.internal` work on Linux too |
| `volumes:` | Where data is stored so it survives the container |

**Everyday Docker commands:**

```bash
docker compose ps              # Is it running?
docker compose logs -f         # Show its log output (Ctrl + C to stop watching)
docker compose down            # Stop and remove the container (data is kept)
docker compose pull            # Download a newer version…
docker compose up -d           # …and start it
```

**If the page does not load:**
- Give it a minute. The first start takes a while. Check `docker compose
  logs -f`.
- "No models found" in Open WebUI means Ollama is not running, or (on Linux)
  not reachable from Docker. See the *Linux only* note in the task.
- `port is already allocated`: something else uses port 3000. Change the
  first `3000` in the file to e.g. `3001`.

</details>

---

## Task 6 — Open WebUI for Everyday Use

1. **Create the first account.** The first account created becomes the
   **administrator**. Do this straight away on a new installation.
2. **Chat.** Pick `llama3.2:3b` at the top and ask something. If you
   downloaded a second model, switch models in the middle of a conversation
   and ask the same question again.
3. **System prompt.** Find the chat settings (the controls icon at the top
   right) and give this chat a system prompt, like in Task 4, but without any
   files.
4. **Users.** As administrator, open the *Admin Panel*. Find the setting
   that decides what happens when someone new signs up.

<details>
<summary>Solution</summary>

1. The admin account can see and manage all users, models and settings.
   Use a strong password.
2. The model menu at the top switches models per chat. Because the whole
   conversation is resent with every message (Task 3), the new model sees
   everything said so far.
3. A system prompt set in the chat controls applies to that chat only. Under
   *Workspace → Models* you can save a permanent assistant with its own name,
   system prompt and settings. That is the browser version of a Modelfile.
4. *Admin Panel → Settings → General*: the **default user role**. Leave it
   at **pending**, so new accounts can do nothing until an admin approves them
   under *Admin Panel → Users*.

**Key points:**
- Menu names move around between Open WebUI versions. If something is not
  where described, look in the *Admin Panel* or your profile menu at the
  bottom left.
- In *Admin Panel → Settings*, check that features that contact the internet
  (web search, external model connections) are switched **off** unless you
  want them. They would send data outside your network.

</details>

---

## Task 7 — Ask Questions About Your Own Documents (RAG)

A model only knows what it saw during training. It knows nothing about *your*
contracts, manuals or notes. Pasting a long document into the chat quickly
hits the context window.

**Retrieval-Augmented Generation (RAG)** solves this:

1. Your documents are split into small pieces (**chunks**).
2. Each chunk is turned into a list of numbers that captures its *meaning*,
   called an **embedding**, and stored in a **vector database**.
3. When you ask a question, the chunks with the most similar meaning are
   looked up...
4. ...and handed to the model together with your question, so it can answer
   from them.

The model is not retrained. It simply gets the right page placed in front of
it at the right moment. Open WebUI does all of this for you.

As a stand-in for your own documents, we use the handbook of an invented
family that runs a small homelab. It contains details no model can know.

**Your task:**

1. First, without any document, ask the model: *"When are updates installed
   in the Meyer family homelab?"* What happens?
2. In your `homelab-ai` folder, create a file named `homelab_handbook.md` and
   copy the handbook below into it.
3. In Open WebUI go to *Workspace → Knowledge*, create a knowledge base
   called `Homelab`, and upload `homelab_handbook.md` from your `homelab-ai`
   folder.
4. Start a new chat, type `#`, select `Homelab`, and ask the same question
   again. Then try:
   - *"What should I do if no websites load?"*
   - *"What is the IP address of the NAS?"*
   - *"Can Anna store client files on atlas?"*
   - *"What is the capital of Australia?"*
5. Check the **sources** shown under each answer.

<details>
<summary>homelab_handbook.md: content to copy</summary>

````markdown
# Homelab Handbook — Family Meyer

*Internal notes. Last updated: March 2026. Maintained by Jonas.*

## Devices

| Name | Hardware | Location | Purpose |
|---|---|---|---|
| atlas | Mini PC, 32 GB RAM, 1 TB SSD | Study, shelf above desk | Ollama, Open WebUI, Docker services |
| vault | Synology NAS, 2 × 4 TB (mirrored) | Basement, next to the router | File storage and photo backup |
| beacon | Raspberry Pi 4 | Hallway cupboard | Pi-hole ad blocker, DNS for the whole network |
| router | Fibre router from the ISP | Basement | Internet, Wi-Fi |

## Network

- Home network: `192.168.40.0/24`. The router is `192.168.40.1`.
- `atlas` has the fixed address `192.168.40.10`, `vault` is `192.168.40.20`,
  `beacon` is `192.168.40.2`.
- Guest Wi-Fi is called **Meyer-Guest**. It cannot reach any of the devices above.
- If websites suddenly stop loading for everyone, restart `beacon` first — a
  hung Pi-hole takes DNS down with it. Pull the power cable, wait ten seconds,
  plug it back in.

## Backups

- `vault` backs up the family photo folder every **night at 02:30** to an
  encrypted cloud bucket.
- Once a month, on the **first Saturday**, Jonas copies the Open WebUI data
  volume from `atlas` to `vault` by hand.
- A second USB drive labelled **"offsite"** is kept at Grandma Hilde's flat and
  swapped every three months.
- Restoring has been tested twice; the last successful test was in January 2026.

## AI services

- Open WebUI runs on `atlas` and is reachable inside the house at
  `http://192.168.40.10:3000`. New accounts must be approved by Jonas.
- The default model is `llama3.2:3b`. For homework help the kids use
  `qwen3:4b`, which is better at maths.
- Ollama is **not** reachable from outside the house. Remote access only works
  through the Tailscale app, which is installed on Jonas's and Anna's phones.

## Rules

1. No work documents from Anna's employer on `atlas` — her company policy
   forbids storing client data on private hardware, even locally.
2. Updates are installed on the **last Sunday of every month**, after a backup.
3. Nobody opens router ports. If a service needs outside access, use Tailscale.

## Emergency contacts

- Internet outage: ISP hotline, the number is on the sticker on the router.
- Jonas is travelling: ask Anna; the admin password envelope is in the
  fireproof box in the study.
````

</details>

<details>
<summary>Solution</summary>

1. Without the document the model has no chance. It either says it doesn't
   know or, more likely, **invents** a plausible schedule.
2. – 4. With the knowledge base the answers come from the handbook:
   - updates on the **last Sunday of every month**, after a backup
   - restart `beacon` (the Pi-hole): unplug, wait ten seconds, plug back in
   - `vault` is `192.168.40.20`
   - no, because her employer's policy forbids it, even locally
   - the capital question is answered from general knowledge. Nothing in the
     handbook matches, and the sources show that.
5. Sources let you **check** where an answer came from. This is the most
   important habit when using RAG at work.

**Key points:**
- RAG is the right tool for *knowledge that changes*: a new document is
  searchable seconds after upload. Retraining a model would take hours.
- If answers are poor, the problem is usually the **retrieval**, not the
  model: the wrong chunks were found. Under *Admin Panel → Settings →
  Documents* you can change the chunk size and the embedding model.
- Scanned PDFs without a text layer contain only images, so there is nothing
  to search. They need OCR first.
- Everything, including the documents, embeddings and database, stays on your
  machine.

</details>

---

## Task 8 — Keeping It Safe

Your homelab now holds private documents and chats. Go through this checklist
together and decide, for each line, whether it applies to your setup.

| Area | Checklist item |
|---|---|
| **Access** | Ports are bound to `127.0.0.1`, or only reachable inside your home network |
| | Ollama's port 11434 is **never** reachable from the internet. It has no password at all |
| | New Open WebUI accounts must be approved (role *pending*) |
| | Remote access goes through a VPN (e.g. Tailscale, WireGuard), not through open router ports |
| **Backup** | Back up the Open WebUI **volume**, not the container. Models can be downloaded again |
| | Keep at least one copy on a different device, and one outside your home |
| | Test a restore at least once |
| **Updates** | Back up first, then update: `docker compose pull && docker compose up -d` |
| | Update Ollama through its app or installer |
| | Update on a fixed day, not the moment a new version appears |

<details>
<summary>Solution</summary>

**Backing up the Open WebUI volume.** Run this inside `homelab-ai`. The
container is stopped first so the database is not changed during the copy.
The middle command is one long line:

```bash
docker compose down
docker run --rm -v homelab-ai_open-webui-data:/data -v ${PWD}:/backup alpine tar czf /backup/open-webui-backup.tar.gz -C /data .
docker compose up -d
```

Afterwards `open-webui-backup.tar.gz` is in your `homelab-ai` folder. Copy it
to another device, such as a USB drive or NAS. Expect about 1 GB even for a
fresh installation: Open WebUI keeps its own small model for searching
documents (Task 7) in the same volume.

**Key points:**
- A local setup is only as private as its weakest point. An exposed port or
  an unapproved account undoes the whole advantage over the cloud.
- The sample handbook in Task 7 does exactly this: fixed update day, backup
  first, no open ports, VPN for remote access.
- For access from other devices in your home, put a reverse proxy with HTTPS
  (e.g. Caddy) in front of Open WebUI. On a dedicated server, the file
  [docker-compose.full-stack.yml](https://github.com/cluebbe/local-homelab-ai/blob/main/docker-compose.full-stack.yml) runs
  Ollama in Docker too.

</details>

---

## Optional Part — Talking to Your Model from Python

Everything Open WebUI does, it does through Ollama's HTTP interface (its
**API**). Any program can do the same. You don't need to be able to program
for these tasks. You only run and change existing code.

### Task 9 — One Request, Three Ways

Send one question to Ollama without any chat interface. Paste this into the
terminal (on macOS or Linux):

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "Why would someone run an AI model at home? One sentence.",
  "stream": false
}'
```

Find the answer text in the result. What else does the result contain?

<details>
<summary>Solution</summary>

The answer is in `"response"`. The rest is information about the request:
`prompt_eval_count` (tokens in your question), `eval_count` (tokens in the
answer), and durations in nanoseconds. This is where `/set verbose` in Task 3
got its numbers.

**Key points:**
- `curl` is a program that sends web requests. Your browser does the same
  thing when it opens a page.
- Ollama also offers an interface compatible with OpenAI's, at
  `http://localhost:11434/v1`. Many existing tools and apps can use your local
  model just by changing that address.
- Windows PowerShell handles quotes differently. Use the Python file in Task
  10 instead.

</details>

### Task 10 — Run and Change the Tutorial Script

The script `homelab_ai_basics.py` walks through everything from this
workshop in code: sizing, a first request, tokens and speed, chat memory,
temperature, streaming, and a small RAG pipeline built by hand. It only uses
Python's built-in modules.

**1.** Install Python 3 from [python.org](https://www.python.org/downloads/)
if you don't have it yet.

**2.** Open [homelab_ai_basics.py](https://github.com/cluebbe/local-homelab-ai/blob/main/homelab_ai_basics.py) in your
browser, click the **Download raw file** button (the arrow icon above the
code, on the right), and save the file into your `homelab-ai` folder.

**3.** In the terminal, inside `homelab-ai`:

```bash
ollama pull nomic-embed-text      # The small embedding model for sections 8 and 9
python3 homelab_ai_basics.py      # On Windows: python homelab_ai_basics.py
```

**4.** Open the file in VS Code and change it:

1. At the top, set `CHAT_MODEL` to another model from `ollama list`, and run
   it again. Which answers change?
2. In section 9, add a note of your own to the `notes` list and a question
   that only that note can answer.

<details>
<summary>Solution</summary>

1. Only the model name needs to change. Every other part of the script works
   with any chat model. Speed (section 4) and answer style differ most.
2. For example:

   ```python
   notes = [
       ...
       "The spare key for the server cupboard hangs on the hook behind the kitchen door.",
   ]
   ```

   and ask `"Where is the key for the server cupboard?"`. The `Retrieved:`
   lines show which notes were handed to the model. That is exactly what
   Open WebUI showed as **sources** in Task 7.

**Key points:**
- Section 8 shows what an embedding is: a list of 768 numbers. Texts with
  similar meaning have similar numbers, even without shared words.
- Section 9 is RAG in about 30 lines: embed the notes, find the closest ones,
  paste them into the prompt, ask the model.

</details>

---

## Where to Go Next

- **Try other models.** Compare a general model with a coding or reasoning
  model of the same size on your own everyday tasks. Check each model's
  **licence** before using it commercially.
- **LM Studio** is a desktop app that does the same job as Ollama with a
  graphical model browser, which is handy for getting started without a
  terminal.
- **Automation:** tools like n8n can use your local model inside workflows,
  for example summarising every incoming invoice email.
- **Fine-tuning** (e.g. with LoRA) changes a model's style or teaches it a
  fixed output format. It needs a good graphics card. Try good system prompts
  and RAG first: they solve most problems more cheaply.
