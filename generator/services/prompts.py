CONTENT_TYPE_INSTRUCTIONS = {
    "blog": (
        "Write a well-structured blog post with an engaging introduction, "
        "H2/H3 headings, bullet points where helpful, and a strong call-to-action."
    ),
    "youtube": (
        "Write a YouTube video script with hook, main sections, B-roll cues in [brackets], "
        "and an outro with subscribe CTA."
    ),
    "instagram": (
        "Write an Instagram caption with hook, value, emojis, and hashtags at the end."
    ),
    "linkedin": (
        "Write a LinkedIn article/post with a professional hook, insights, "
        "and engagement question at the end."
    ),
    "email": (
        "Write an email newsletter with subject line, preview text, body sections, and CTA."
    ),
    "twitter": (
        "Write a Twitter/X thread (numbered tweets, each under 280 chars)."
    ),
    "podcast": (
        "Write a podcast episode outline with intro, segments, talking points, and outro."
    ),
}


def build_generation_prompt(
    content_type: str,
    topic: str,
    keywords: str,
    target_audience: str,
    word_count: int,
    tone: str,
) -> str:
    type_instruction = CONTENT_TYPE_INSTRUCTIONS.get(
        content_type,
        "Write high-quality, engaging content.",
    )
    return f"""You are ContentForge, an expert AI content creator.

Task: {type_instruction}

Requirements:
- Topic: {topic}
- Keywords to include naturally: {keywords or "none specified"}
- Target audience: {target_audience or "general audience"}
- Approximate length: {word_count} words
- Tone: {tone}

Output rules:
- Use Markdown formatting (headings, lists, bold where appropriate).
- Do not include meta commentary — output only the content.
- Make it original, actionable, and ready to publish.
"""


def build_seo_prompt(content: str, topic: str, keywords: str) -> str:
    return f"""Analyze this content for SEO and return ONLY valid JSON (no markdown fences):

{{
  "seo_score": <integer 0-100>,
  "meta_title": "<max 60 chars>",
  "meta_description": "<max 155 chars>",
  "suggested_keywords": ["kw1", "kw2", "kw3", "kw4", "kw5"],
  "heading_suggestions": ["H2 idea 1", "H2 idea 2"],
  "competitor_angles": ["angle 1", "angle 2"],
  "improvements": ["tip 1", "tip 2", "tip 3"]
}}

Topic: {topic}
Target keywords: {keywords or "none"}

Content to analyze:
---
{content[:8000]}
---
"""


def build_grammar_prompt(content: str) -> str:
    return f"""Review this content for grammar, clarity, and tone. Return a concise bullet list
of the top 5 improvements (no full rewrite):

{content[:6000]}
"""


def build_image_prompt(topic: str, content_type: str, style: str) -> str:
    return (
        f"Create a {style} featured image for {content_type} content about: {topic}. "
        "Modern, vibrant, professional, no text overlay unless minimal title space."
    )
