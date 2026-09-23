# Workshop: Local Homelab AI

**Duration:** 90 minutes · **Level:** beginner to intermediate ·
**Prerequisites:** basic command line use; Python functions, lists and
dictionaries (see the Python Basics workshop)

---

## Introduction

### Background

Tools like ChatGPT run a **large language model (LLM)** on someone else's
servers: your prompt travels over the internet, is processed there, and the
answer travels back. For personal use that is often fine. For customer
records, patient data, contracts, or internal company documents it can be a
legal and practical problem.

A **local LLM** runs the same kind of model on hardware you own. The prompt
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

Every local AI setup is built from the same three layers:

| Layer | Job | Examples |
|---|---|---|
| **Model** | The trained weights: a file of billions of numbers | Llama, Qwen, Gemma, Mistral |
| **Runtime** | Loads the model into memory and generates text | Ollama, LM Studio, llama.cpp |
| **Interface** | How humans or programs talk to the runtime | Terminal, Open WebUI, your own Python code |

This workshop uses **Ollama** as the runtime, talks to it from the terminal
and from Python, and ends with a small program that answers questions about
*your own* notes: a minimal RAG pipeline.

### Schedule

| Time | Part | Tasks |
|---|---|---|
| 0:00 – 0:10 | Setup and why local AI | Introduction |
| 0:10 – 0:20 | Will it fit? | Task 1 |
| 0:20 – 0:40 | Ollama on the command line | Tasks 2 – 3 |
| 0:40 – 1:05 | Talking to the model from code | Tasks 4 – 8 |
| 1:05 – 1:25 | Your own documents: embeddings and RAG | Tasks 9 – 10 |
| 1:25 – 1:30 | Outlook: a permanent homelab stack | Task 11 (bonus / homework) |

### Setting Up the Development Environment

**1. Install Ollama**

Download it from [ollama.com](https://ollama.com) (macOS, Windows, Linux).
On Linux the site offers a one-line install script. After installing, check:

```bash
ollama --version
```

**2. Download two models** (≈ 2.3 GB in total, do this *before* the
workshop if the network is slow)

```bash
ollama pull llama3.2:3b        # A small chat model, ~2 GB
ollama pull nomic-embed-text   # An embedding model for Task 9, ~0.3 GB
```

A machine with 8 GB of RAM is enough. No GPU is needed, but it is slower
without one.

**3. Run the tutorial file**

```bash
python3 homelab_ai_basics.py
```

Only the Python standard library is used. There is nothing to `pip install`.

---

## Task 1 — Will It Fit? Sizing a Model

A model's size is given as its number of **parameters**: `3B` means 3
billion numbers. To run a model, all of them have to fit in memory: GPU
memory (VRAM) if you have a graphics card, otherwise normal RAM. Apple Silicon
Macs share one pool between both.

How much memory one parameter takes depends on its **precision**:

| Precision | Bits per parameter | Typical use |
|---|---|---|
| FP16 | 16 | Original training format |
| Q8 | 8 | Nearly lossless |
| Q4 (e.g. `Q4_K_M`) | ~4.5 | Default for most downloads, good quality/size balance |

Storing weights in fewer bits is called **quantisation**. It makes models
roughly 3–4× smaller at a small cost in quality.

Write a function `estimate_memory_gb(params_billion, bits_per_param)` that
returns the approximate memory needed. Add about 20 % on top of the raw
weights for the context window and the runtime itself. Print a table for 3B,
8B, 14B, 32B and 70B models at FP16 and at Q4.

Then answer: **what is the largest Q4 model your own machine can run?**

<details>
<summary>Solution</summary>

```python
def estimate_memory_gb(params_billion, bits_per_param, overhead=1.2):
    """Rough memory needed to run a model: weights plus ~20 % for context and runtime."""
    weights_gb = params_billion * bits_per_param / 8   # 8 bits = 1 byte
    return weights_gb * overhead


for size in [3, 8, 14, 32, 70]:
    fp16 = estimate_memory_gb(size, 16)
    q4 = estimate_memory_gb(size, 4.5)
    print(f"{size:>3}B model:  FP16 ≈ {fp16:6.1f} GB   Q4 ≈ {q4:5.1f} GB")
```

```
  3B model:  FP16 ≈    7.2 GB   Q4 ≈   2.0 GB
  8B model:  FP16 ≈   19.2 GB   Q4 ≈   5.4 GB
 14B model:  FP16 ≈   33.6 GB   Q4 ≈   9.4 GB
 32B model:  FP16 ≈   76.8 GB   Q4 ≈  21.6 GB
 70B model:  FP16 ≈  168.0 GB   Q4 ≈  47.2 GB
```

**Key points:**
- Quick estimate: **billions of parameters × bits ÷ 8 = GB of weights.**
- Leave headroom for the operating system and other programs. On a 16 GB
  laptop, 8B at Q4 is comfortable and 14B is the limit.
- If a model does not fit in VRAM, Ollama puts part of it in normal RAM. It
  still works, but much more slowly. **Memory bandwidth**, not raw compute, is
  usually what limits generation speed.
- Longer context windows need more memory. The 20 % is only a rough allowance
  for a few thousand tokens of context.

</details>

---

## Task 2 — Ollama on the Command Line

Ollama runs a background **server** on `localhost:11434`. The `ollama`
command is only a client for that server, just like every other tool you
will use today.

Try the following and note what each command does:

1. List the models you have downloaded.
2. Start an interactive chat with `llama3.2:3b` and ask it something.
3. Inside the chat, type `/?` to see the built-in commands, then leave the
   chat.
4. In a second terminal, while a chat is open, show which models are
   currently **loaded in memory** and how much they use.
5. Look at the details of a model: its parameter count, quantisation and
   context length.

<details>
<summary>Solution</summary>

```bash
ollama list                     # 1. Models on disk
ollama run llama3.2:3b          # 2. Chat (downloads the model first if missing)
>>> /?                          # 3. Help inside the chat
>>> /bye                        #    Leave (or Ctrl+D)
ollama ps                       # 4. Models in memory, size, CPU/GPU split
ollama show llama3.2:3b         # 5. Architecture, parameters, quantisation, context
```

Other everyday commands:

```bash
ollama pull qwen3:4b            # Download without starting a chat
ollama rm gemma3:1b             # Delete a model from disk
ollama stop llama3.2:3b         # Unload it from memory right now
ollama run llama3.2:3b "Explain DNS in one sentence."   # One-shot, no chat
```

**Key points:**
- The name after the colon is a **tag**, usually size and/or quantisation
  (`llama3.2:3b`, `qwen3:14b`). Without a tag, `latest` is used.
- `ollama ps` shows the `PROCESSOR` column: `100% GPU` is ideal. A split like
  `40%/60% CPU/GPU` means the model did not fit in VRAM.
- A loaded model stays in memory for ~5 minutes after the last request, then
  is unloaded automatically.
- Models live in `~/.ollama/models`. That folder is what fills your disk.

</details>

---

## Task 3 — Your Own Model with a Modelfile

A **Modelfile** is to Ollama roughly what a Dockerfile is to Docker: a short
recipe that builds a new model from an existing one. It does *not* retrain
anything. It bundles a base model with a **system prompt** (standing
instructions) and default **parameters**.

Write a `Modelfile` that creates `homelab-helper`:
- based on `llama3.2:3b`
- temperature `0.3`
- a system prompt that makes it a short-spoken homelab assistant

Build it, chat with it, and ask: *"How do I see which models are loaded right
now?"* Is the answer correct?

<details>
<summary>Solution</summary>

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

```bash
ollama create homelab-helper -f Modelfile
ollama run homelab-helper
ollama list                     # It now shows up next to the base model
```

**Key points:**
- The new model shares the base model's weights on disk, so it costs almost no
  extra space.
- A 3B model will often answer this question **confidently and wrongly**. In
  testing it suggested `docker ps -a` instead of `ollama ps`. This is a
  **hallucination**: the model produces plausible text, not checked facts.
  Small models do this more often. The system prompt asked it to admit
  uncertainty, and it still did not.
- `num_ctx` sets the **context window**: how many tokens of conversation the
  model can see. Anything older falls out and is forgotten. Bigger windows
  cost more memory.

</details>

---

## Task 4 — Your First API Call

Everything the CLI does goes through a plain HTTP API. That means **any**
program can use your local model: scripts, automation tools, web UIs.

1. Use `curl` to send the prompt *"Why would someone run an AI model at
   home?"* to `POST /api/generate`. Set `"stream": false`.
2. Do the same from Python using only `urllib.request` and `json`. Write a
   helper `post_json(path, payload)` that you can reuse for the rest of the
   workshop.

<details>
<summary>Solution</summary>

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "Why would someone run an AI model at home?",
  "stream": false
}'
```

```python
import json
import urllib.request

OLLAMA_URL = "http://localhost:11434"
CHAT_MODEL = "llama3.2:3b"


def post_json(path, payload):
    """Send a POST request with a JSON body and return the decoded JSON."""
    request = urllib.request.Request(
        OLLAMA_URL + path,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read())


result = post_json("/api/generate", {
    "model": CHAT_MODEL,
    "prompt": "In one sentence: why would someone run an AI model at home?",
    "stream": False,
})
print(result["response"])
```

**Key points:**
- The answer text is in `result["response"]`. The rest of the JSON is
  metadata, which Task 5 uses.
- Useful `GET` endpoints: `/api/tags` (same as `ollama list`), `/api/ps`
  (same as `ollama ps`), `/api/version`.
- Ollama also provides an **OpenAI-compatible** API under `/v1/`. Many
  existing tools and libraries can use your local model just by changing their
  base URL to `http://localhost:11434/v1`.

</details>

---

## Task 5 — Tokens and Speed

LLMs do not read words. They read **tokens**, which are word pieces. As a rule
of thumb, one English word is about 1.3 tokens. German and code usually need
more tokens per word. Context limits and speed are both measured in tokens.

Using the `result` from Task 4, print:
- how many tokens the prompt had (`prompt_eval_count`)
- how many tokens the answer had (`eval_count`)
- the generation speed in tokens per second (`eval_duration` is in
  **nanoseconds**)

Compare with your neighbour: whose machine is fastest, and why?

<details>
<summary>Solution</summary>

```python
prompt_tokens = result["prompt_eval_count"]
answer_tokens = result["eval_count"]
seconds = result["eval_duration"] / 1e9

print(f"Prompt tokens:  {prompt_tokens}")
print(f"Answer tokens:  {answer_tokens}")
print(f"Speed:          {answer_tokens / seconds:.1f} tokens/second")
```

**Key points:**
- About 10 tokens/s feels like fast reading speed. Below 5 it feels sluggish.
- A GPU or Apple Silicon machine is often 5–20× faster than a CPU-only
  laptop, mainly because of higher memory bandwidth.
- `ollama run --verbose llama3.2:3b` prints the same statistics after every
  answer in the terminal.

</details>

---

## Task 6 — Chat with Memory

The model has **no memory** between requests. What looks like memory in a
chat app is the app sending the *entire* conversation again every time.

Use `POST /api/chat`, which takes a list of `messages`, each with a `role`
(`system`, `user`, `assistant`) and `content`.

1. Start with a system message that makes the model answer in at most two
   sentences, and a user message: *"My server is called 'atlas'. Remember
   that."*
2. Append the assistant's reply to the list.
3. Ask *"What is my server called?"* and check that it knows.
4. Now leave out step 2 and try again. What happens?

<details>
<summary>Solution</summary>

```python
messages = [
    {"role": "system", "content": "You are a concise homelab assistant. Answer in at most two sentences."},
    {"role": "user", "content": "My server is called 'atlas'. Remember that."},
]
reply = post_json("/api/chat", {"model": CHAT_MODEL, "messages": messages, "stream": False})
messages.append(reply["message"])            # The model's answer becomes part of the history
print("Assistant:", reply["message"]["content"])

messages.append({"role": "user", "content": "What is my server called?"})
reply = post_json("/api/chat", {"model": CHAT_MODEL, "messages": messages, "stream": False})
print("Assistant:", reply["message"]["content"])   # "Your server is called atlas."
```

**Key points:**
- Without the history the second request is a brand-new conversation, and
  the model has to guess.
- Every turn resends everything, so long chats get slower and eventually hit
  the context window. That is why chat apps summarise or trim old messages.
- The `system` message is the same mechanism as `SYSTEM` in the Modelfile,
  set per request instead of built into the model.

</details>

---

## Task 7 — Temperature

At every step the model has a probability for each possible next token.
**Temperature** controls how it picks:

- `0`: always take the most likely token. The same prompt gives the same answer.
- `0.7` (typical default): some variety.
- `> 1`: creative, but increasingly random and error-prone.

Ask for *"Invent a name for a home server. Reply with the name only."* twice at
temperature `0` and twice at `1.5`. Parameters go in an `"options"`
dictionary.

<details>
<summary>Solution</summary>

```python
for temperature in [0.0, 0.0, 1.5, 1.5]:
    answer = post_json("/api/generate", {
        "model": CHAT_MODEL,
        "prompt": "Invent a name for a home server. Reply with the name only.",
        "stream": False,
        "options": {"temperature": temperature},
    })
    print(f"temperature={temperature}: {answer['response'].strip()}")
```

```
temperature=0.0: "Domus"
temperature=0.0: "Domus"
temperature=1.5: OmniaNova
temperature=1.5: NovaSphere
```

**Key points:**
- Use low temperature for facts, extraction, code and RAG. Use higher
  temperature for brainstorming and creative text.
- Temperature does not make a model more or less *knowledgeable*. It only
  changes how adventurous the choice of words is.
- Other useful options: `num_ctx` (context size), `seed` (reproducible
  output), `num_predict` (maximum answer length).

</details>

---

## Task 8 — Streaming

Without `"stream": false`, Ollama sends the answer piece by piece: one JSON
object per line, each with a bit of `response` text, and a final one with
`"done": true`.

Read the stream line by line and print each piece immediately (use
`print(..., end="", flush=True)`). Measure how long it takes until the
**first** text appears.

<details>
<summary>Solution</summary>

```python
import time

request = urllib.request.Request(
    OLLAMA_URL + "/api/generate",
    data=json.dumps({"model": CHAT_MODEL, "prompt": "Count from 1 to 10."}).encode(),
    headers={"Content-Type": "application/json"},
)
start = time.perf_counter()
first_token_at = None
with urllib.request.urlopen(request) as response:
    for line in response:                     # One JSON object per line
        chunk = json.loads(line)
        if first_token_at is None:
            first_token_at = time.perf_counter() - start
        print(chunk["response"], end="", flush=True)
        if chunk["done"]:
            break
print(f"\n(first text after {first_token_at:.2f} s)")
```

**Key points:**
- Total time is the same with or without streaming, but *perceived* speed is
  much better. This is why every chat UI streams.
- The first request after a pause is slower because the model has to be
  loaded from disk into memory first. Run it twice and compare.

</details>

---

## Task 9 — Embeddings: Meaning as Numbers

To let a model use *your* documents, we first need to find the relevant ones.
An **embedding model** turns a text into a vector, a long list of numbers.
Texts with similar *meaning* get vectors pointing in similar directions,
even if they share no words.

**Cosine similarity** measures that direction: `1.0` means the same
direction, around `0` means unrelated.

1. Write `embed(texts)` using `POST /api/embed` with model
   `nomic-embed-text` and `"input": [list of texts]`. The result has an
   `"embeddings"` list.
2. Write `cosine_similarity(a, b)` (dot product divided by the product of
   the lengths) using `math.sqrt`.
3. Compare *"How do I back up my data?"* with *"Saving a copy of my files"*
   and with *"My cat likes tuna"*.

<details>
<summary>Solution</summary>

```python
import math

EMBED_MODEL = "nomic-embed-text"


def embed(texts):
    """Return one embedding vector per input text."""
    return post_json("/api/embed", {"model": EMBED_MODEL, "input": texts})["embeddings"]


def cosine_similarity(a, b):
    """Measure how similar two vectors are, from -1 to 1."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)


vectors = embed(["How do I back up my data?", "Saving a copy of my files", "My cat likes tuna"])
print(len(vectors[0]))                                   # 768 numbers per text
print(cosine_similarity(vectors[0], vectors[1]))         # ~0.63 — related
print(cosine_similarity(vectors[0], vectors[2]))         # ~0.38 — unrelated
```

**Key points:**
- "backup" and "saving a copy" share no words, but the vectors are still
  close. That is the difference from a keyword search.
- Absolute values depend on the embedding model. Only compare scores that come
  from the same model.
- A **vector database** (Chroma, Qdrant, pgvector, ...) does exactly this
  comparison, but fast for millions of documents.

</details>

---

## Task 10 — A Minimal RAG Pipeline

**Retrieval-Augmented Generation (RAG)** combines Tasks 4 and 9:

1. **Index:** embed all your documents once.
2. **Retrieve:** embed the question and find the most similar documents.
3. **Augment:** paste those documents into the prompt.
4. **Generate:** let the model answer *from the pasted text*.

The model is never retrained. It just gets the right page placed in front of
it at the right moment.

Given these notes:

```python
notes = [
    "The NAS is backed up every Sunday at 03:00 to an external USB drive labelled 'vault'.",
    "The Wi-Fi password for the guest network is printed on the router's underside.",
    "Ollama runs on the machine 'atlas' and listens only on localhost port 11434.",
    "The Raspberry Pi in the hallway runs Pi-hole for network-wide ad blocking.",
    "Open WebUI is reachable at http://atlas:3000 and requires an admin-approved account.",
]
```

Write `retrieve(question, top_k=2)` and `ask(question)`. The prompt must tell
the model to answer **only** from the notes and to say so if they don't
contain the answer. Test with *"When does the NAS backup run?"* and *"What is
the capital of France?"*

<details>
<summary>Solution</summary>

```python
note_vectors = embed(notes)                  # Index once


def retrieve(question, top_k=2):
    """Return the top_k notes most similar to the question."""
    question_vector = embed([question])[0]
    scored = [(cosine_similarity(question_vector, v), note) for v, note in zip(note_vectors, notes)]
    scored.sort(reverse=True)
    return [note for _, note in scored[:top_k]]


def ask(question):
    """Answer a question using only the retrieved notes as context."""
    context = "\n".join(f"- {note}" for note in retrieve(question))
    prompt = (
        "Answer the question using only the notes below. "
        "If the notes do not contain the answer, say you don't know.\n\n"
        f"Notes:\n{context}\n\nQuestion: {question}"
    )
    answer = post_json("/api/generate", {
        "model": CHAT_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0},
    })
    return answer["response"].strip()


print(ask("When does the NAS backup run?"))     # "Every Sunday at 03:00."
print(ask("What is the capital of France?"))    # "I don't know."
```

**Key points:**
- The second answer shows the value of the instruction: the model *knows*
  Paris, but was told to rely only on the notes. For private documents this
  keeps answers grounded and checkable.
- Retrieval always returns *something*, even for unrelated questions. Always
  print the retrieved context while developing, because bad retrieval is the
  most common reason for bad RAG answers.
- Real documents are too long for one vector. They are split into **chunks**
  (a few hundred tokens each, with some overlap) before embedding. Chunk size
  is the first knob to turn when quality is poor.
- Open WebUI, AnythingLLM and similar tools run this same pipeline behind
  their "upload a document" button.

</details>

---

## Task 11 — Bonus: A Permanent Homelab Stack

So far Ollama was only for you, on the command line. A homelab usually runs
services **permanently** and gives other people in the household or office a
browser interface. Docker Compose describes the whole stack in one file.

Look at [docker-compose.yml](docker-compose.yml) in this repository and
answer:

1. How does Open WebUI find Ollama? (Hint: `OLLAMA_BASE_URL`.)
2. What happens to your downloaded models and chat history when you run
   `docker compose down` and then `up -d` again?
3. Why are the ports written as `127.0.0.1:3000:8080` rather than
   `3000:8080`?

Start the stack with `docker compose up -d`, open <http://localhost:3000>,
create the first account, and pull a model from the admin settings.

<details>
<summary>Solution</summary>

1. Containers in the same Compose project share a private network and reach
   each other by **service name**. So `http://ollama:11434` works inside the
   network, while `localhost` inside a container would mean the container
   itself.
2. They survive. They live in the named **volumes** `ollama-models` and
   `open-webui-data`, not in the containers. Only `docker compose down -v`
   deletes volumes. **Those volumes are what you back up.**
3. `127.0.0.1:` binds the port to this machine only. Without it the service
   is reachable from the whole network and, with a careless router setup, from
   the internet. **Ollama's API has no authentication**: anyone who reaches
   port 11434 can use your hardware and read or delete your models.

**Key points:**
- The first account created in Open WebUI becomes the **admin**. Create it
  right away, and approve later sign-ups manually.
- To give other devices in your LAN access, put a reverse proxy (e.g. Caddy)
  with HTTPS in front of Open WebUI, rather than opening the ports directly.
  For access from outside, use a VPN such as WireGuard or Tailscale.
- Update with `docker compose pull && docker compose up -d`. Back up the
  volumes first.
- If Ollama already runs natively on your machine, port 11434 is taken. Stop
  it, or delete the `ports:` section of the `ollama` service.

</details>

---

## Where to Go Next

- **Try bigger or specialised models.** Compare a general model with a coding
  or reasoning model of the same size on your own tasks. Check each model's
  **licence** before using it commercially.
- **LM Studio** is a desktop app that does the same as Ollama with a
  graphical model browser, which is handy for exploring quantisations.
- **Automation:** tools like n8n can call your local model from workflows
  (e.g. summarise every incoming invoice email).
- **Fine-tuning (LoRA)** changes a model's style or teaches it a fixed output
  format. Try good prompts and RAG first: they solve most problems more cheaply.
