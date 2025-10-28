# crossref-django

This project provides a Django REST API to fetch article information from Crossref by DOI, store it in a SQLite database, and expose it via a REST endpoint. The project runs in Docker for easy setup.

Features

Fetch article metadata (title, authors, published date, peer review info) from Crossref

Store retrieved articles in a SQLite database

REST API endpoint for bulk DOI queries (up to 200 DOIs per request)

Dockerized for easy setup and deployment

Requirements

Docker

Docker Compose

Setup and Run

Clone the repository:

git clone https://github.com/<your-username>/crossref-django.git
cd crossref-django


Build and start the Docker container:

docker-compose up --build


This will:

Build the Docker image

Run database migrations

Start the Django application using Gunicorn on port 8080

API Usage

Endpoint:

POST http://localhost:8080/get-article-info-by-doi


Request Body:
A JSON array of DOIs (maximum 200 items), for example:

["10.1038/nphys1170", "10.1038/s41586-020-2649-2"]


Response:

{
  "fetched": {
    "10.1038/nphys1170": {
      "doi": "10.1038/nphys1170",
      "title": "Measured measurement",
      "authors": ["Author Name"],
      "published_date": "2008-06-01",
      "peer_review": null,
      "raw": { ... }
    }
  },
  "errors": {
    "10.1038/invalid-doi": "Not Found"
  }
}


fetched contains successfully retrieved articles.

errors contains DOIs that could not be fetched with the error messages.

Database

The project uses SQLite stored in a Docker volume (sqlite_data) so data persists across container restarts.

Access the database inside the container if needed:

docker exec -it crossref-django-web-1 bash
sqlite3 db_data/db.sqlite3

Environment

The Crossref API requires a valid User-Agent with a contact email. Update the email in articles/views.py:

CROSSREF_MAILTO = "your-email@example.com"

Notes

The API enforces a maximum of 200 DOIs per request to avoid overloading Crossref.

All fetched data is stored in the SQLite database, so repeated requests for the same DOI will update the existing record.

Docker ensures the project works the same way across different machines without additional installation of Python or SQLite.

License

MIT License
