"""AI text generation via Gemini, Groq, or mock fallback."""

import json
import re
from typing import Any

from django.conf import settings

from .prompts import (
    build_generation_prompt,
    build_grammar_prompt,
    build_image_prompt,
    build_seo_prompt,
)


class AIError(Exception):
    pass


def _mock_generate(prompt: str) -> str:
    return f"""# Generated Content (Demo Mode)

> Add `GEMINI_API_KEY` or `GROQ_API_KEY` to your `.env` file for real AI output.

## Sample Section

This is placeholder content generated because no AI API key is configured.

**Your prompt summary:** {prompt[:200]}...

### Next Steps
- Sign up at [Google AI Studio](https://aistudio.google.com/) for Gemini
- Or use [Groq](https://console.groq.com/) for fast inference
- Set `AI_PROVIDER=gemini` or `groq` in `.env`

---
*ContentForge — AI-powered content for creators*
"""


def _generate_gemini(prompt: str) -> str:
    import google.generativeai as genai

    api_key = settings.GEMINI_API_KEY
    if not api_key:
        raise AIError("GEMINI_API_KEY is not set")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text.strip()


def _generate_groq(prompt: str) -> str:
    import urllib.error
    import urllib.request

    api_key = settings.GROQ_API_KEY
    if not api_key:
        raise AIError("GROQ_API_KEY is not set")

    payload = json.dumps({
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are ContentForge, an expert content writer."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 4096,
    }).encode()

    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else str(e)
        raise AIError(f"Groq API error: {body}") from e

    return data["choices"][0]["message"]["content"].strip()


def generate_text(prompt: str) -> str:
    provider = settings.AI_PROVIDER.lower()

    if provider == "mock":
        return _mock_generate(prompt)

    try:
        if provider == "groq":
            return _generate_groq(prompt)
        return _generate_gemini(prompt)
    except AIError:
        raise
    except Exception as exc:
        if settings.GEMINI_API_KEY or settings.GROQ_API_KEY:
            raise AIError(str(exc)) from exc
        return _mock_generate(prompt)


def generate_content(
    content_type: str,
    topic: str,
    keywords: str,
    target_audience: str,
    word_count: int,
    tone: str,
) -> str:
    prompt = build_generation_prompt(
        content_type, topic, keywords, target_audience, word_count, tone
    )
    return generate_text(prompt)


def _parse_json_response(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    return json.loads(text)


def analyze_seo(content: str, topic: str, keywords: str) -> dict[str, Any]:
    prompt = build_seo_prompt(content, topic, keywords)
    if settings.AI_PROVIDER == "mock" and not settings.GEMINI_API_KEY:
        return {
            "seo_score": 72,
            "meta_title": f"{topic[:55]} | Guide",
            "meta_description": f"Learn about {topic}. Practical tips for {keywords or 'your audience'}.",
            "suggested_keywords": (keywords or topic).split(",")[:5],
            "heading_suggestions": ["Key Benefits", "How to Get Started"],
            "competitor_angles": ["Beginner guide", "Case study angle"],
            "improvements": [
                "Add more primary keywords in the first paragraph",
                "Include internal link placeholders",
                "Strengthen meta description CTA",
            ],
        }
    raw = generate_text(prompt)
    try:
        return _parse_json_response(raw)
    except json.JSONDecodeError:
        return {
            "seo_score": 65,
            "meta_title": topic[:60],
            "meta_description": content[:155],
            "suggested_keywords": [],
            "heading_suggestions": [],
            "competitor_angles": [],
            "improvements": ["Could not parse AI SEO response — try again."],
        }


def check_grammar(content: str) -> str:
    prompt = build_grammar_prompt(content)
    if settings.AI_PROVIDER == "mock" and not settings.GEMINI_API_KEY:
        return (
            "- Demo mode: configure an API key for real grammar suggestions.\n"
            "- Consider shorter sentences in the introduction.\n"
            "- Vary paragraph length for readability."
        )
    return generate_text(prompt)


def generate_image_url(topic: str, content_type: str, style: str = "illustration") -> str | None:
    """Returns a placeholder or external URL. Integrate Flux/Ideogram via IMAGE_API_KEY."""
    prompt = build_image_prompt(topic, content_type, style)
    if not settings.IMAGE_API_KEY:
        return None
    # Placeholder for Flux/Ideogram API integration
    _ = prompt
    return None
