# FastAPI WhatsApp AI Chatbot Starter Kit 🚀

[![CI](https://github.com/gendonholaholo/Python-starter-kit-FastAPI-WhatsApp-AI-Chatbot/actions/workflows/ci.yml/badge.svg)](https://github.com/gendonholaholo/Python-starter-kit-FastAPI-WhatsApp-AI-Chatbot/actions/workflows/ci.yml)

A production-ready starter kit to build efficient WhatsApp Chatbots powered by AI (OpenAI), built with **FastAPI**, **SQLModel**, and **Asyncio**.

## Features

- **FastAPI**: Modern, fast (high-performance) web framework.
- **OpenAI Integration**: Seamless integration with OpenAI GPT models.
- **WhatsApp Cloud API**: Native integration for receiving and sending messages.
- **SQLModel + AsyncSQLite**: Easy-to-use Async ORM with SQLite (extensible to PostgreSQL).
- **Structured Architecture**: Service-based architecture for scalability.
- **Best Practices**: Type-safe, linted with `ruff`, managed with `uv`.

## Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- WhatsApp Business Account (Meta Developers)
- OpenAI API Key

## Installation

1. **Clone the repository:**
   ```bash
   git clone git@github.com:gendonholaholo/Python-starter-kit-FastAPI-WhatsApp-AI-Chatbot.git
   cd Python-starter-kit-FastAPI-WhatsApp-AI-Chatbot
   ```

2. **Initialize with `uv`:**
   ```bash
   uv sync
   ```

3. **Configure Environment:**
   Copy `.env.example` to `.env` and fill in your credentials.
   ```bash
   cp .env.example .env
   ```
   
   - `OPENAI_API_KEY`: Your OpenAI key.
   - `WHATSAPP_TOKEN`: Permanent or temporary access token from Meta.
   - `WHATSAPP_PHONE_NUMBER_ID`: Found in your Meta App Dashboard.
   - `WHATSAPP_VERIFY_TOKEN`: A random string you define (used for webhook verification).

## Running the Application

Start the development server:

```bash
uv run fastapi dev src/app/main.py
```

The API will be available at `http://localhost:8000`.
API Docs: `http://localhost:8000/docs`.

## Setting up WhatsApp Webhook

1. Expose your localhost to the internet (using ngrok or similar):
   ```bash
   ngrok http 8000
   ```
2. Go to **Meta Developers Dashboard** > **WhatsApp** > **Configuration**.
3. Click **Edit** in the Callback URL section.
4. Enter your Callback URL: `https://<your-ngrok-url>/api/v1/webhook`.
5. Enter the `WHATSAPP_VERIFY_TOKEN` you set in `.env`.
6. Verify and Save.
7. Subscribe to `messages` webhook field.

## Project Structure

```
src/app/
├── api/             # API Endpoints (Routes)
├── core/            # Config, Database, Logging
├── models/          # Database Models (SQLModel)
├── schemas/         # Pydantic Schemas (DTOs)
├── services/        # Business Logic (AI, Chat, WhatsApp)
└── main.py          # Entry Point
```

## Contributing

1. Fork the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## License

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
