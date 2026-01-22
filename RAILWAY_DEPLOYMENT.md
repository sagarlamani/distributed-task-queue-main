# Railway Deployment Guide

This guide will help you deploy the Distributed Task Queue System on Railway for a live demo.

## Prerequisites

1. A [Railway](https://railway.app) account (free tier available)
2. GitHub account (for connecting your repository)
3. Your project pushed to GitHub

## Step-by-Step Deployment

### 1. Prepare Your Repository

Ensure all files are committed and pushed to GitHub:
```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### 2. Create a New Railway Project

1. Go to [railway.app](https://railway.app) and sign in
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository: `sagarlamani/distributed-task-queue-main`
5. Railway will automatically detect it's a Python project

### 3. Add Redis Service

1. In your Railway project dashboard, click **"+ New"**
2. Select **"Database"** → **"Add Redis"**
3. Railway will automatically create a Redis instance
4. The `REDIS_URL` environment variable will be automatically set

### 4. Configure Environment Variables

Railway will automatically detect:
- `REDIS_URL` (from the Redis service you added)
- `PORT` (automatically set by Railway)

No additional configuration needed! The app will automatically use the Redis service.

### 5. Deploy

1. Railway will automatically start building and deploying your application
2. You can watch the build logs in real-time
3. Once deployed, Railway will provide you with a public URL (e.g., `https://your-app.railway.app`)

### 6. Verify Deployment

1. Visit your Railway URL
2. Check the health endpoint: `https://your-app.railway.app/health`
3. You should see:
   ```json
   {
     "status": "healthy",
     "redis": "connected",
     "timestamp": "..."
   }
   ```

## Testing the API

### 1. Submit a Task

```bash
curl -X POST https://your-app.railway.app/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "example_task",
    "task_data": {"message": "Hello from Railway!"},
    "priority": "high",
    "max_retries": 3
  }'
```

Response:
```json
{
  "task_id": "uuid-here",
  "status": "pending",
  "message": "Task submitted successfully"
}
```

### 2. Check Queue Statistics

```bash
curl https://your-app.railway.app/api/queues/stats
```

Response:
```json
{
  "high": 1,
  "medium": 0,
  "low": 0,
  "total": 1
}
```

### 3. Check Task Status

```bash
curl https://your-app.railway.app/api/tasks/{task_id}
```

## API Endpoints

Once deployed, your API will be available at:
- `GET /` - API information
- `GET /health` - Health check with Redis status
- `POST /api/tasks` - Submit a new task
- `GET /api/tasks/{task_id}` - Get task status
- `GET /api/queues/stats` - Get queue statistics

## Railway Features Used

- **Automatic Build Detection**: Railway detects Python projects automatically
- **Redis Service**: Managed Redis instance with automatic connection
- **Environment Variables**: Automatic `REDIS_URL` injection
- **Public URL**: Automatic HTTPS endpoint
- **Build Logs**: Real-time deployment logs
- **Metrics**: CPU, memory, and network usage

## Custom Domain (Optional)

1. In Railway project settings, go to **"Settings"** → **"Networking"**
2. Click **"Generate Domain"** or add a custom domain
3. Your API will be available at your custom domain

## Monitoring

Railway provides:
- **Deployment logs**: View in the Railway dashboard
- **Metrics**: CPU, memory usage in the dashboard
- **Build history**: Track all deployments

## Troubleshooting

### Redis Connection Issues

If you see `"redis": "disconnected"` in the health check:

1. Verify Redis service is added to your project
2. Check that `REDIS_URL` environment variable is set
3. View logs in Railway dashboard for connection errors

### Build Failures

1. Check `requirements.txt` is correct
2. Verify Python version in `runtime.txt` (if specified)
3. Check build logs in Railway dashboard

### Port Issues

Railway automatically sets the `PORT` environment variable. The app uses this via:
```python
port = int(os.getenv('PORT', 8000))
```

## Cost

Railway offers:
- **Free tier**: $5 credit per month
- **Hobby plan**: $5/month for additional resources
- **Pro plan**: $20/month for production workloads

For a demo, the free tier should be sufficient.

## Next Steps

1. **Add Worker Service** (Optional): You can deploy the worker as a separate service
2. **Set up CI/CD**: Railway automatically deploys on git push
3. **Add Monitoring**: Integrate with external monitoring tools
4. **Scale Workers**: Add multiple worker services for higher throughput

## Worker Deployment (Optional)

To deploy workers separately:

1. Create a new service in Railway
2. Use the same repository
3. Set the start command to: `python app/worker.py`
4. Connect to the same Redis service
5. Scale horizontally by adding more worker services

## Support

- [Railway Documentation](https://docs.railway.app)
- [Railway Discord](https://discord.gg/railway)
- Check Railway dashboard logs for detailed error messages

---

**Your deployed API will be live at**: `https://your-app.railway.app`

Enjoy your live demo! 🚀

