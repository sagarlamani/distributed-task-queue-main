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

