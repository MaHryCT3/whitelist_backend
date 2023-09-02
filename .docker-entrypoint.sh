#! /bin/bash

alembic upgrade head
uvicorn app:app --port 8080 --host 0.0.0.0