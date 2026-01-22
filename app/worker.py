"""
Worker process for executing tasks from the queue
"""

import redis
import json
import time
import logging
from multiprocessing import Process
from typing import Dict, Callable
import signal
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Worker:
    def __init__(self, redis_host='localhost', redis_port=6379, queue_name='queue:medium'):
        self.running = False
        self.queue_name = queue_name
        
        try:
            self.redis_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                db=0,
                decode_responses=True
            )
            self.redis_client.ping()
            logger.info(f"Worker connected to Redis, listening on {queue_name}")
        except:
            self.redis_client = None
            logger.warning("Redis not available. Worker cannot start.")
    
    def register_task_handler(self, task_type: str, handler: Callable):
        """Register a task handler"""
        if not hasattr(self, 'task_handlers'):
            self.task_handlers = {}
        self.task_handlers[task_type] = handler
        logger.info(f"Registered handler for task type: {task_type}")
    
    def process_task(self, task_data: Dict):
        """Process a single task"""
        task_id = task_data.get('task_id')
        task_type = task_data.get('task_type')
        task_payload = task_data.get('task_data', {})
        
        logger.info(f"Processing task {task_id} of type {task_type}")
        
        try:
            # Get handler
            handler = self.task_handlers.get(task_type)
            if not handler:
                logger.warning(f"No handler for task type: {task_type}")
                return False
            
            # Execute task
            result = handler(task_payload)
            logger.info(f"Task {task_id} completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error processing task {task_id}: {e}")
            return False
    
    def start(self):
        """Start the worker"""
        if not self.redis_client:
            logger.error("Cannot start worker: Redis not available")
            return
        
        self.running = True
        logger.info(f"Worker started, listening on {self.queue_name}")
        
        # Signal handler
        def signal_handler(sig, frame):
            logger.info("Stopping worker...")
            self.running = False
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        try:
            while self.running:
                # Blocking pop from queue
                task_json = self.redis_client.brpop(self.queue_name, timeout=1)
                
                if task_json:
                    _, task_data_json = task_json
                    task_data = json.loads(task_data_json)
                    self.process_task(task_data)
                else:
                    # Timeout, continue loop
                    continue
                    
        except KeyboardInterrupt:
            logger.info("Worker stopped by user")
        finally:
            self.running = False
            logger.info("Worker stopped")

# Example task handlers
def example_task_handler(data: Dict):
    """Example task handler"""
    logger.info(f"Executing example task with data: {data}")
    time.sleep(1)  # Simulate work
    return True

if __name__ == "__main__":
    # Example usage
    worker = Worker(queue_name='queue:medium')
    worker.register_task_handler('example_task', example_task_handler)
    worker.start()

