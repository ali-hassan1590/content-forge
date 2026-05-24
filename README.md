# ContentForge

AI-powered content platform for bloggers, YouTubers, and marketers. Built with **Django**, **SQLite**, **HTMX**, **Tailwind CSS**, and **Alpine.js**.

## Features

- AI content generation (blog, YouTube, social, email, etc.)
- SEO analysis with meta title/description suggestions
- Flesch-Kincaid readability scoring
- Grammar check via AI
- Content calendar & history dashboard
- Export to Markdown / plain text
- Credit system for AI usage
- Django Allauth authentication

## Quick start

```bash
# Clone and enter project
cd ContentForeg

# Virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt

# Environment
copy .env.example .env         # Windows
# cp .env.example .env         # macOS/Linux
# Edit .env and add GEMINI_API_KEY from https://aistudio.google.com/

# Database (SQLite — created automatically)
python manage.py migrate
python manage.py createsuperuser

# Run
python manage.py runserver
```

Open http://127.0.0.1:8000/

## AI configuration

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Google Gemini (recommended free tier) |
| `GROQ_API_KEY` | Groq + Llama (very fast) |
| `AI_PROVIDER` | `gemini`, `groq`, or `mock` (demo without API key) |

Without API keys, `AI_PROVIDER=mock` returns demo content so you can explore the UI.

## Project structure

```
ContentForeg/
├── accounts/          # UserProfile, credits
├── generator/         # Models, AI services, views
├── core/              # Home, dashboard
├── templates/         # HTMX-ready templates
├── static/            # CSS
├── contentforge/      # Django settings (SQLite)
└── db.sqlite3         # Created after migrate
```

## Credit costs

| Action | Credits |
|--------|---------|
| Generate content | 5 |
| SEO analysis | 2 |
| Image generation | 10 |

New users start with **100 credits**.

## Roadmap

- [ ] Celery async generation
- [ ] Flux / Ideogram image API
- [ ] PDF/Word export
- [ ] Team workspaces
- [ ] REST API for integrations

## License

MIT — use freely for learning and portfolios.
