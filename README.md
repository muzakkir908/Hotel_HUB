# Hotel Hub

A hotel booking platform built with Django. Guests browse hotels on a map, book rooms, download a PDF invoice and leave reviews. A REST API exposes the same data to other clients.

## Features

- **Hotels and rooms**: listings with photos, prices, room types, capacity and availability
- **Map view**: hotel locations shown with the Google Maps JavaScript API
- **Bookings**: check-in and check-out dates, guest count, automatic total price and booking status
- **PDF invoices**: generated for each confirmed booking
- **Reviews**: guests can leave reviews on hotels
- **REST API** (Django REST Framework): `/api/hotels/`, `/api/rooms/`, `/api/bookings/`, `/api/reviews/`
- **Health check** at `/health/` for load balancer and container probes

## Stack

| Layer | Tech |
|---|---|
| Backend | Python, Django 4.2, Django REST Framework |
| Database | SQLite locally, PostgreSQL in production (`DATABASE_URL`) |
| Serving | Gunicorn, Docker |
| Deployment | AWS Elastic Beanstalk |

## Run locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # then fill in the values
python manage.py migrate
python manage.py runserver
```

## Run with Docker

```bash
docker build -t hotel-hub .
docker run -p 8000:8000 --env-file .env hotel-hub
```

## Configuration

All secrets are read from environment variables. See `.env.example` for the full list.

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for local development |
| `ALLOWED_HOSTS` | Comma-separated hostnames |
| `DATABASE_URL` | PostgreSQL connection string (optional; falls back to SQLite) |
| `GOOGLE_MAPS_API_KEY` | Google Maps JavaScript API key |

## Project layout

```
hotel_project/   settings, URLs, health check, middleware
hotels/          hotel and room models, views, API
bookings/        bookings, PDF invoices, reviews, API
templates/       HTML templates
```
