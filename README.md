# Sri Jagannath Math Website 🛕

Official website and digital portal for **Sri Jagannath Math**, located in Tetri-Dandari, Begusarai, Bihar, India. Dedicated to Lord Jagannath, spiritual enlightenment, cultural heritage, and community service.

---

## 🚀 Tech Stack

- **Backend**: Python 3.13+, Django 5.0+
- **WSGI / Web Server**: Gunicorn 22.0+
- **Static Assets**: WhiteNoise 6.6+ with `CompressedStaticFilesStorage`
- **Database**: PostgreSQL (production via `dj-database-url`) / SQLite3 (local development)
- **Media Storage**: Cloudinary (production) / Local Filesystem (development)
- **Frontend**: Django Templates (DTL), Bootstrap 5.3.2, Bootstrap Icons 1.11.3, Vanilla JavaScript, Custom CSS

---

## ⚙️ Environment Variables

Configure the following environment variables in your `.env` file or cloud dashboard:

| Variable | Required in Prod? | Default (Dev) | Description |
| :--- | :---: | :--- | :--- |
| `DEBUG` | No | `False` | Set `True` or `1` for local development. |
| `SECRET_KEY` | **Yes** | Dev fallback | Cryptographic secret key. Required in production. |
| `ALLOWED_HOSTS` | **Yes** | `localhost,127.0.0.1` | Comma-separated list of valid domain names. |
| `DATABASE_URL` | Optional | Local SQLite | Connection URI for PostgreSQL (e.g. `postgres://user:pass@host:5432/db`). |
| `CSRF_TRUSTED_ORIGINS` | Optional | Railway defaults | Comma-separated list of trusted HTTPS origins for CSRF. |
| `CLOUDINARY_URL` | Optional | None | Single connection string for Cloudinary media uploads. |
| `CLOUDINARY_CLOUD_NAME`| Optional | None | Cloudinary cloud identifier (if not using `CLOUDINARY_URL`). |
| `CLOUDINARY_API_KEY`   | Optional | None | Cloudinary API Key. |
| `CLOUDINARY_API_SECRET`| Optional | None | Cloudinary API Secret. |
| `DATA_DIR` | No | Base directory | Persistent storage directory for SQLite/media files. |

---

## 🛠️ Local Development Setup

### 1. Clone & Set Up Environment

```powershell
# Clone the repository
git clone <repository-url>
cd jagannath_math

# Create and activate virtual environment
python -m venv env
.\env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Apply Migrations & Seed Data

```powershell
# Set development mode
$env:DEBUG = "1"

# Run database migrations
python manage.py migrate

# Seed initial temple data (optional)
python manage.py shell < seed_data.py
```

### 3. Start Development Server

```powershell
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 🧪 Running Automated Tests

Run the full automated test suite:

```powershell
python manage.py test core
```

Run Django production deployment security checks:

```powershell
python manage.py check --deploy
```

---

## 🩺 Health Check & Monitoring

A lightweight health check endpoint is exposed at:

```
GET /health/
```

**Response (HTTP 200 OK):**
```json
{
  "status": "ok",
  "database": "connected",
  "timestamp": "2026-09-19T05:15:30.123456+00:00"
}
```

---

## 🚢 Production Deployment

The project is pre-configured for cloud platforms (e.g., Railway, Render, Fly.io, Heroku) with a 12-factor compliant [`Procfile`](Procfile):

- **Release Phase**: `release: python manage.py migrate --noinput`
- **Web Dyno**: `web: gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3 --timeout 60`

### Pre-Deployment Checklist
1. Provide a cryptographically secure `SECRET_KEY` (50+ random characters).
2. Set `DEBUG=False`.
3. Set `ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com`.
4. Attach a PostgreSQL database and provide `DATABASE_URL`.
5. Attach Cloudinary storage and set `CLOUDINARY_URL`.
