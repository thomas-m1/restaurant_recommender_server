# Restaurant Recommender — API

A FastAPI backend for discovering Toronto restaurants by cuisine, occasion, price, and distance. It serves restaurant data and community recommendations to the [React client](https://github.com/thomas-m1/restaurant_recommender_client).

## Stack

Python, FastAPI, SQLAlchemy, PostgreSQL, and Alembic.

## Local development

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env.dev` file with your local settings:

```dotenv
ENV=development
APP_VERSION=1.0.0
DATABASE_URL=postgresql://restaurant_user:restaurant_password@localhost:5432/restaurant_db
ALLOWED_ORIGINS=["http://localhost:3000"]
OFFICE_LAT=43.6534
OFFICE_LNG=-79.3841
GOOGLE_MAPS_API_KEY=
```

The `OFFICE_LAT` and `OFFICE_LNG` setting names are retained for compatibility; the default origin is Toronto City Hall. Supply a Google Maps key to use integrations that require it. Keep credentials out of version control.

Start PostgreSQL using your own installation, or start the database service from the included Compose configuration:

```sh
docker compose up -d db
```

Initialize the `businesses` table using the [batch importer](https://github.com/thomas-m1/restaurant_recommender_batch) against the same database, then apply the recommendation migrations:

```sh
alembic upgrade head
uvicorn app.main:app --reload
```

The API runs on port 8000. Interactive documentation is available at `/docs` in development.

## Endpoints

- `GET /api/v1/health` — database connectivity
- `GET /api/v1/restaurants/` — paginated restaurant search and filters
- `POST /api/v1/recommendations/` — add a recommendation
- `GET /api/v1/recommendations/` — retrieve recommendations by restaurant or email

Restaurant distances are calculated during batch ingestion. Reingest existing data after changing the importer's reference coordinates.
