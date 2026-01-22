"""
FastAPI Backend for Distributed Task Queue System
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime
import redis
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Distributed Task Queue API",
    description="Celery-like distributed task queue system",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis connection
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_client.ping()
    logger.info("Connected to Redis")
except:
    redis_client = None
    logger.warning("Redis not available. Using in-memory queue.")

# In-memory queue (fallback)
in_memory_queue: Dict[str, List] = {
    "high": [],
    "medium": [],
    "low": []
}

# Request models
class TaskRequest(BaseModel):
    task_type: str
    task_data: Dict
    priority: str = "medium"  # high, medium, low
    delay: Optional[int] = None  # seconds
    max_retries: int = 3

class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str

# Routes
@app.get("/")
async def root():
    return {"message": "Distributed Task Queue API", "version": "1.0.0"}

@app.get("/health")
async def health():
    redis_status = "connected" if redis_client and redis_client.ping() else "disconnected"
    return {
        "status": "healthy",
        "redis": redis_status,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/tasks", response_model=TaskResponse)
async def submit_task(task: TaskRequest):
    """Submit a new task to the queue"""
    import uuid
    task_id = str(uuid.uuid4())
    
    task_data = {
        "task_id": task_id,
        "task_type": task.task_type,
        "task_data": task.task_data,
        "priority": task.priority,
        "max_retries": task.max_retries,
        "created_at": datetime.now().isoformat(),
        "status": "pending",
        "retry_count": 0
    }
    
    try:
        if redis_client:
            # Use Redis
            queue_name = f"queue:{task.priority}"
            redis_client.lpush(queue_name, json.dumps(task_data))
            logger.info(f"Task {task_id} added to Redis queue: {queue_name}")
        else:
            # Use in-memory queue
            in_memory_queue[task.priority].append(task_data)
            logger.info(f"Task {task_id} added to in-memory queue: {task.priority}")
        
        return TaskResponse(
            task_id=task_id,
            status="pending",
            message="Task submitted successfully"
        )
    except Exception as e:
        logger.error(f"Error submitting task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tasks/{task_id}")
async def get_task_status(task_id: str):
    """Get task status"""
    # In a real implementation, this would query the database
    return {
        "task_id": task_id,
        "status": "pending",
        "message": "Task status endpoint - would query database in full implementation"
    }

@app.get("/api/queues/stats")
async def get_queue_stats():
    """Get queue statistics"""
    if redis_client:
        try:
            high_count = redis_client.llen("queue:high")
            medium_count = redis_client.llen("queue:medium")
            low_count = redis_client.llen("queue:low")
            
            return {
                "high": high_count,
                "medium": medium_count,
                "low": low_count,
                "total": high_count + medium_count + low_count
            }
        except:
            pass
    
    # In-memory stats
    return {
        "high": len(in_memory_queue["high"]),
        "medium": len(in_memory_queue["medium"]),
        "low": len(in_memory_queue["low"]),
        "total": sum(len(q) for q in in_memory_queue.values())
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

