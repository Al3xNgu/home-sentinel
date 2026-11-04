# Home Sentinel

A smart-home facial recognition backend. You enroll the people who live in or visit your home by uploading photos; Home Sentinel checks each photo for exactly one face, turns it into an embedding, and stores it in PostgreSQL so new faces can be matched by vector similarity.

> **Status:** in progress. Enrollment (people + photos + embeddings) works. Live recognition and the frontend are next.

## How it works

1. **Add a person** with `POST /people`
2. **Upload photos** of them with `POST /people/{id}/photos` (JPEG or PNG)
3. Each photo is validated: it's rejected if no face, or more than one face, is detected with ≥90% confidence
4. A 512-dimension **ArcFace** embedding is generated with DeepFace and stored in a `pgvector` column
5. *(in progress)* Recognition finds the closest stored embedding by L2 distance and accepts it under a match threshold

## Tech stack

- **API:** Python, FastAPI, SQLAlchemy, Pydantic
- **Face detection and embeddings:** DeepFace (ArcFace model, OpenCV detector)
- **Database:** PostgreSQL with the pgvector extension

## API

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/people` | Create a person |
| `GET` | `/people` | List people |
| `GET` | `/people/{id}` | Get a person |
| `PUT` | `/people/{id}` | Rename a person |
| `DELETE` | `/people/{id}` | Delete a person |
| `POST` | `/people/{id}/photos` | Upload a photo (validated and embedded) |
| `GET` | `/people/{id}/photos` | List a person's photos |
| `DELETE` | `/people/{id}/photos/{photo_id}` | Delete a photo |

Interactive docs are at `http://localhost:8000/docs` once the server is running.

## Getting started

Requirements: Python 3.11+, PostgreSQL with [pgvector](https://github.com/pgvector/pgvector) installed.

```bash
git clone https://github.com/Al3xNgu/home-sentinel.git
cd home-sentinel/backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

Create the database and enable the extension:

```sql
CREATE DATABASE home_sentinel;
\c home_sentinel
CREATE EXTENSION vector;
```

Create `backend/.env`:

```
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@localhost:5432/home_sentinel
```

Run the API (tables are created on startup):

```bash
uvicorn app.main:app --reload
```

## Project structure

```
backend/app/
  main.py         FastAPI app
  database.py     engine, session, table creation
  models/         Person, PersonPhoto, FaceEmbedding
  schemas/        Pydantic request/response models
  routes/         people and photo endpoints
  services/       face detection, embeddings, matching
frontend/         (planned)
```

## Roadmap

- [x] People CRUD
- [x] Photo upload with single-face validation
- [x] ArcFace embeddings stored in pgvector
- [ ] Recognition endpoint (match an incoming image against enrolled people)
- [ ] Camera / doorbell feed integration
- [ ] Web dashboard
