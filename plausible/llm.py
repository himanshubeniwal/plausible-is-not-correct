"""One function, `ask()`, so the notebook works with or without an API key.

Backends (choose with the environment variable PLAUSIBLE_LLM):
  anthropic  call Claude through the official Anthropic Python SDK
             (needs `pip install anthropic` and ANTHROPIC_API_KEY)
  manual     print the prompt; you paste it into ANY chatbot (ChatGPT, Claude,
             Gemini, Le Chat, a local model...) and paste the answer back.
  off        skip LLM calls (ask() returns None); the verification parts still run.
Default: anthropic if ANTHROPIC_API_KEY is set, otherwise manual.
"""
from __future__ import annotations

import os
from collections import Counter

MODEL = os.environ.get("PLAUSIBLE_MODEL", "claude-opus-5-5")


def backend() -> str:
    return os.environ.get("PLAUSIBLE_LLM") or ("anthropic" if os.environ.get("ANTHROPIC_API_KEY") else "manual")


_client = None


def _anthropic(prompt: str, system: str | None, max_tokens: int) -> str:
    global _client
    import anthropic
    if _client is None:
        _client = anthropic.Anthropic()
    kwargs = dict(model=MODEL, max_tokens=max_tokens,
                  messages=[{"role": "user", "content": prompt}])
    if system:
        kwargs["system"] = system
    if MODEL.startswith(("claude-opus", "claude-fable", "claude-sonnet")):
        # If a safety classifier declines (biology questions occasionally trigger
        # false positives), the API retries on a fallback model server-side.
        resp = _client.beta.messages.create(
            betas=["server-side-fallback-2026-07-01"], fallbacks="default", **kwargs)
    else:
        resp = _client.messages.create(**kwargs)
    if resp.stop_reason == "refusal":
        return "[MODEL DECLINED THIS REQUEST]"
    return "".join(b.text for b in resp.content if b.type == "text").strip()


def _manual(prompt: str, system: str | None) -> str:
    print("=" * 70)
    print("Copy everything between the lines into your chatbot of choice:")
    print("-" * 70)
    if system:
        print(f"[Instructions] {system}\n")
    print(prompt)
    print("-" * 70)
    print("Paste the answer below. Finish with a line containing only END")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def ask(prompt: str, system: str | None = None, max_tokens: int = 16000) -> str | None:
    if backend() == "off":
        print("[LLM backend is 'off' — skipping this call]")
        return None
    if backend() == "anthropic":
        return _anthropic(prompt, system, max_tokens)
    return _manual(prompt, system)


def sample(prompt: str, n: int = 5, system: str | None = None, normalise=None) -> dict:
    """Ask the same question n times (independent calls) and measure agreement.

    Low agreement is a cheap, useful warning sign for hallucination
    (the idea behind self-consistency and SelfCheckGPT). High agreement is NOT
    proof of correctness: a model can be consistently wrong.
    """
    normalise = normalise or (lambda s: s.strip().lower().rstrip("."))
    answers = [ask(prompt, system) for _ in range(n)]
    if any(a is None for a in answers):
        return {"answers": answers, "counts": {}, "majority": None, "agreement": None}
    counts = Counter(normalise(a) for a in answers)
    top, freq = counts.most_common(1)[0]
    return {"answers": answers, "counts": dict(counts),
            "majority": top, "agreement": round(freq / n, 2)}
