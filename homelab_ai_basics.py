# Local Homelab AI Tutorial
#
# This tutorial talks to a large language model running on your own machine
# through Ollama's HTTP API. Nothing leaves your computer.
# Run this file to see the output of each section, then experiment
# by changing the prompts, models, and options and re-running.
#
# SETUP
# -----
# 1. Install Ollama from https://ollama.com and make sure it is running.
# 2. Download a chat model and an embedding model:
#      ollama pull llama3.2:3b
#      ollama pull nomic-embed-text
# 3. Run with:
#      python homelab_ai_basics.py
#
# No Python packages are required — only the standard library is used.

import json
import math
import time
import urllib.error
import urllib.request

OLLAMA_URL = "http://localhost:11434"   # Default address of a local Ollama server
CHAT_MODEL = "llama3.2:3b"              # Change this to any model from `ollama list`
EMBED_MODEL = "nomic-embed-text"        # A small model that turns text into vectors

print("=" * 40)
print("  Local Homelab AI Tutorial")
print("=" * 40)


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------
# Every Ollama endpoint takes JSON in and gives JSON back. These two small
# functions hide the urllib boilerplate so the sections below stay readable.

def get_json(path):
    """Send a GET request to Ollama and return the decoded JSON."""
    with urllib.request.urlopen(OLLAMA_URL + path) as response:
        return json.loads(response.read())


def post_json(path, payload):
    """Send a POST request with a JSON body and return the decoded JSON."""
    request = urllib.request.Request(
        OLLAMA_URL + path,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read())


# ---------------------------------------------------------------------------
# 1. SIZING YOUR HARDWARE
# ---------------------------------------------------------------------------
# A model is mostly a huge list of numbers (parameters). How much memory it
# needs depends on how many there are and how many bits each one is stored in.
# Quantisation stores each parameter in fewer bits, e.g. 4 instead of 16.

print("\n--- 1. Sizing Your Hardware ---")


def estimate_memory_gb(params_billion, bits_per_param, overhead=1.2):
    """Rough memory needed to run a model: weights plus ~20 % for context and runtime."""
    weights_gb = params_billion * bits_per_param / 8   # 1 billion params at 8 bit = 1 GB
    return weights_gb * overhead


for size in [3, 8, 14, 32, 70]:
    fp16 = estimate_memory_gb(size, 16)
    q4 = estimate_memory_gb(size, 4.5)                  # Q4_K_M averages ~4.5 bits per weight
    print(f"{size:>3}B model:  FP16 ≈ {fp16:6.1f} GB   Q4 ≈ {q4:5.1f} GB")


# ---------------------------------------------------------------------------
# 2. IS THE SERVER RUNNING?
# ---------------------------------------------------------------------------
# Ollama runs as a background server on port 11434. The CLI (`ollama run`)
# and every other tool are just clients of this server.

print("\n--- 2. Is the Server Running? ---")

try:
    version = get_json("/api/version")["version"]
except urllib.error.URLError:
    print("Cannot reach Ollama at", OLLAMA_URL)
    print("Start it (open the Ollama app or run `ollama serve`) and try again.")
    raise SystemExit(1)

print(f"Ollama {version} is running.")

installed = get_json("/api/tags")["models"]           # Same list as `ollama list`
for model in installed:
    print(f"  {model['name']:<28} {model['size'] / 1e9:5.1f} GB")


# ---------------------------------------------------------------------------
# 3. YOUR FIRST API CALL
# ---------------------------------------------------------------------------
# /api/generate takes a single prompt and returns a single answer.
# "stream": False waits for the full answer instead of sending it word by word.

print("\n--- 3. Your First API Call ---")

result = post_json("/api/generate", {
    "model": CHAT_MODEL,
    "prompt": "In one sentence: why would someone run an AI model at home?",
    "stream": False,
})
print(result["response"])


# ---------------------------------------------------------------------------
# 4. TOKENS AND SPEED
# ---------------------------------------------------------------------------
# Models read and write tokens — word pieces — not words. Every response
# reports how many tokens went in and came out, and how long it took.
# Durations are given in nanoseconds.

print("\n--- 4. Tokens and Speed ---")

prompt_tokens = result["prompt_eval_count"]
answer_tokens = result["eval_count"]
seconds = result["eval_duration"] / 1e9
print(f"Prompt tokens:  {prompt_tokens}")
print(f"Answer tokens:  {answer_tokens}")
print(f"Speed:          {answer_tokens / seconds:.1f} tokens/second")


# ---------------------------------------------------------------------------
# 5. CHAT WITH MEMORY
# ---------------------------------------------------------------------------
# The model itself remembers nothing between calls. /api/chat takes the whole
# conversation as a list of messages, and your code must keep that list.

print("\n--- 5. Chat with Memory ---")

messages = [
    {"role": "system", "content": "You are a concise homelab assistant. Answer in at most two sentences."},
    {"role": "user", "content": "My server is called 'atlas'. Remember that."},
]
reply = post_json("/api/chat", {"model": CHAT_MODEL, "messages": messages, "stream": False})
messages.append(reply["message"])                       # Store the assistant's answer
print("Assistant:", reply["message"]["content"])

messages.append({"role": "user", "content": "What is my server called?"})
reply = post_json("/api/chat", {"model": CHAT_MODEL, "messages": messages, "stream": False})
print("Assistant:", reply["message"]["content"])


# ---------------------------------------------------------------------------
# 6. TEMPERATURE
# ---------------------------------------------------------------------------
# Temperature controls randomness. At 0 the model always picks the most
# likely next token; higher values make answers more varied (and riskier).

print("\n--- 6. Temperature ---")

for temperature in [0.0, 0.0, 1.5, 1.5]:
    answer = post_json("/api/generate", {
        "model": CHAT_MODEL,
        "prompt": "Invent a name for a home server. Reply with the name only.",
        "stream": False,
        "options": {"temperature": temperature},
    })
    print(f"temperature={temperature}: {answer['response'].strip()}")


# ---------------------------------------------------------------------------
# 7. STREAMING
# ---------------------------------------------------------------------------
# With streaming, Ollama sends one JSON object per line as soon as each piece
# of text is ready. This is what makes chat UIs feel fast.

print("\n--- 7. Streaming ---")

request = urllib.request.Request(
    OLLAMA_URL + "/api/generate",
    data=json.dumps({"model": CHAT_MODEL, "prompt": "Count from 1 to 10, separated by spaces."}).encode(),
    headers={"Content-Type": "application/json"},
)
start = time.perf_counter()
first_token_at = None
with urllib.request.urlopen(request) as response:
    for line in response:                              # One JSON object per line
        chunk = json.loads(line)
        if first_token_at is None:
            first_token_at = time.perf_counter() - start
        print(chunk["response"], end="", flush=True)
        if chunk["done"]:
            break
print(f"\n(first text after {first_token_at:.2f} s)")


# ---------------------------------------------------------------------------
# 8. EMBEDDINGS
# ---------------------------------------------------------------------------
# An embedding model turns text into a list of numbers (a vector). Texts with
# similar meaning get vectors that point in similar directions, which we can
# measure with cosine similarity: 1.0 = same direction, 0 = unrelated.

print("\n--- 8. Embeddings ---")


def embed(texts):
    """Return one embedding vector per input text."""
    return post_json("/api/embed", {"model": EMBED_MODEL, "input": texts})["embeddings"]


def cosine_similarity(a, b):
    """Measure how similar two vectors are, from -1 to 1."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)


try:
    vectors = embed(["How do I back up my data?", "Saving a copy of my files", "My cat likes tuna"])
except urllib.error.HTTPError:
    print(f"Embedding model missing — run: ollama pull {EMBED_MODEL}")
    raise SystemExit(1)

print(f"Each vector has {len(vectors[0])} numbers.")
print(f"backup  vs  copy of files: {cosine_similarity(vectors[0], vectors[1]):.2f}")
print(f"backup  vs  cat and tuna:  {cosine_similarity(vectors[0], vectors[2]):.2f}")


# ---------------------------------------------------------------------------
# 9. A MINIMAL RAG PIPELINE
# ---------------------------------------------------------------------------
# Retrieval-Augmented Generation: find the notes most relevant to a question,
# paste them into the prompt, and let the model answer from them. The model
# never had to be trained on your private documents.

print("\n--- 9. A Minimal RAG Pipeline ---")

notes = [
    "The NAS is backed up every Sunday at 03:00 to an external USB drive labelled 'vault'.",
    "The Wi-Fi password for the guest network is printed on the router's underside.",
    "Ollama runs on the machine 'atlas' and listens only on localhost port 11434.",
    "The Raspberry Pi in the hallway runs Pi-hole for network-wide ad blocking.",
    "Open WebUI is reachable at http://atlas:3000 and requires an admin-approved account.",
]
note_vectors = embed(notes)                            # Index once, reuse for every question


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
    return context, answer["response"].strip()


for question in ["When does the NAS backup run?", "What is the capital of France?"]:
    context, answer = ask(question)
    print(f"\nQ: {question}")
    print(f"Retrieved:\n{context}")
    print(f"A: {answer}")

print("\nDone. Everything above ran entirely on your own machine.")
