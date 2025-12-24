# Coloring Page Generator

Cross-platform Flutter + FastAPI application that produces printable 300 DPI A4 coloring pages for children. The backend synthesizes a safe prompt, renders placeholder art (ready to swap with a real image model), converts it to bold line art, and exports a PDF. The Flutter client provides a simple, parent-friendly interface to pick a theme and age group and download the PDF.

## Project structure

```
backend/            # FastAPI service
  app/
    main.py         # API surface
    config.py       # settings and prompt template
    models/         # Pydantic schemas
    services/       # image generation, processing, PDF, storage
  requirements.txt  # backend dependencies
frontend/           # Flutter client
  lib/main.dart     # UI and API integration
  pubspec.yaml      # Dart dependencies
```

## Backend setup

1. Configure environment (optional but recommended for real images):

   ```bash
   cd backend
   cp .env.example .env  # edit OPENAI_API_KEY if available
   ```

2. Install and run:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

- Endpoint: `POST /generate` with JSON payload `{ "theme": "animals", "age_group": "3-4" }`
- Returns: JSON including `status`, generated prompt, preview (base64), `pdf_url` (served from `/files/...`), and `pdf_base64` for direct download.
- PDFs are stored under `backend/output/` and served by FastAPI static files.
- Health check: `GET /health`

## Frontend setup

Requires Flutter 3.x.

```bash
cd frontend
flutter pub get
flutter run --dart-define=API_BASE_URL=http://<backend-host>:8000
```

- Simple UI with theme chips, age group chips, and a single action button.
- Shows a loading indicator during generation.
- Displays the processed preview and enables "Download PDF" to save/open locally.

## Notes
- All content is intentionally simple and generic to avoid copyrighted or unsafe material.
- Image processing uses Pillow + OpenCV; PDF export uses ReportLab at 300 DPI on A4.
- The image generator is a safe placeholder. Swap `ImageGenerator.generate_image` with real model calls when available.
