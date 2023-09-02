#! /bin/bash

alembic upgrade head
uvicorn app:app --port 80 --host 0.0.0.0