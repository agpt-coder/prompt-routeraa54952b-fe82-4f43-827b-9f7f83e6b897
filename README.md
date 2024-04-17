---
date: 2024-04-17T13:17:26.006213
author: AutoGPT <info@agpt.co>
---

# Prompt Router

The project aims to build an automatic query-routing interface that intelligently routes queries to the most suitable AI model (GPT-4 Turbo, Claude 3 Opus, Gemini 1.5 Pro, or others) based on the query's complexity, the need for efficiency, and cost considerations. The system prioritizes high-quality responses while minimizing latency and keeping within a budget of up to $5,000 per month. Through the user interviews, we've identified the necessity for handling 10K queries per month, with a demand for prompt responses. The choice of model varies with the task: complex NLP tasks will utilise GPT-4 Turbo for its superior understanding and generation capabilities; Claude 3 Opus is preferred for engaging content creation with a focus on moderation and safety; and Gemini 1.5 Pro will serve specific domains requiring up-to-date industry knowledge. Strategies for reducing costs include examining various aspects like accuracy, uniqueness, and information timeliness. Additionally, techniques for lowering latency were discussed, suggesting the use of caching, CDNs, database optimization, and other performance-tuning methods. The technical stack for implementing this solution includes Python for programming, FastAPI for the API framework, PostgreSQL for the database, and Prisma for the ORM. This stack was chosen for its responsiveness, scalability, and developer-friendly nature, which aligns with our goals of creating a fast, reliable, and cost-effective query-routing interface.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'Prompt Router'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
