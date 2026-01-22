# Distributed Task Queue System

## Overview
A production-ready distributed task queue system similar to Celery, built with FastAPI, Redis, and PostgreSQL. Supports asynchronous background job processing with horizontal scaling.

## Features
- Distributed task queue with Redis
- Worker pool management
- Priority queues (high, medium, low)
- Task scheduling and cron-like jobs
- Automatic retry with exponential backoff
- Dead letter queue for failed tasks
- Real-time task monitoring
- Task dependencies and chaining
- Rate limiting per task type

## Tech Stack
- **Backend**: FastAPI
- **Message Queue**: Redis
- **Database**: PostgreSQL
- **Worker**: Python multiprocessing
- **Scheduler**: APScheduler

## Quick Start

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start Redis (using Docker):
```bash
docker run -d -p 6379:6379 redis:latest
```

3. Run the API:
```bash
uvicorn app.main:app --reload
```

4. Run a worker (in another terminal):
```bash
python app/worker.py
```

### Railway Deployment

Deploy to Railway for a live demo in minutes! See [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) for detailed instructions.**Quick Steps:**
1. Push your code to GitHub
2. Create a new Railway project
3. Add Redis service
4. Deploy! 🚀

Your API will be live at `https://your-app.railway.app`

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check with Redis status
- `POST /api/tasks` - Submit a new task
- `GET /api/tasks/{task_id}` - Get task status
- `GET /api/queues/stats` - Get queue statistics
