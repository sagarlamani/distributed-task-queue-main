# Troubleshooting Guide

## API Not Responding / Timeout Issues

### 1. Check if Railway Service is Running

1. Go to your Railway dashboard
2. Check if the service shows "Active" status
3. View the logs to see if there are any errors

### 2. Check Redis Connection

The API should work even without Redis (using in-memory queue), but if Redis is configured incorrectly, it might cause issues.

**Check Railway Logs:**
- Look for "Connected to Redis" message
- Look for "Redis not available" warning

### 3. Verify Environment Variables

In Railway dashboard:
1. Go to your service → Variables
2. Check if `REDIS_URL` is set (if you added Redis service)
3. Check if `PORT` is set (Railway sets this automatically)

### 4. Test Basic Endpoints

Try these endpoints in order:

1. **Root endpoint** (should always work):
   ```
   GET https://task-queue-f171f.up.railway.app/
   ```

2. **Health endpoint**:
   ```
   GET https://task-queue-f171f.up.railway.app/health
   ```

3. **Queue stats**:
   ```
   GET https://task-queue-f171f.up.railway.app/api/queues/stats
   ```

### 5. Common Issues

#### Issue: Health endpoint times out
**Cause**: Redis connection hanging
**Solution**: The health endpoint now handles Redis errors gracefully. If it still times out, check Railway logs.

#### Issue: "Redis not available" in logs
**Cause**: Redis service not added or not connected
**Solution**: 
- Add Redis service in Railway
- Or the app will use in-memory queue (works for demo)

#### Issue: Build fails
**Cause**: Missing dependencies or Python version issue
**Solution**: Check `requirements.txt` and `runtime.txt`

#### Issue: Port binding error
**Cause**: PORT environment variable not set
**Solution**: Railway should set this automatically. Check service variables.

### 6. Check Railway Logs

1. Go to Railway dashboard
2. Click on your service
3. Click "Deployments" tab
4. Click on latest deployment
5. View "Logs" to see what's happening

Look for:
- Application startup messages
- Redis connection messages
- Any error messages

### 7. Test with curl (PowerShell)

```powershell
# Test root endpoint
Invoke-WebRequest -Uri "https://task-queue-f171f.up.railway.app/" -Method GET

# Test health endpoint
Invoke-WebRequest -Uri "https://task-queue-f171f.up.railway.app/health" -Method GET

# Submit a task
$body = @{
    task_type = "test"
    task_data = @{
        message = "Hello"
    }
    priority = "high"
} | ConvertTo-Json

Invoke-WebRequest -Uri "https://task-queue-f171f.up.railway.app/api/tasks" -Method POST -Body $body -ContentType "application/json"
```

### 8. Test with Browser

Simply open:
- `https://task-queue-f171f.up.railway.app/`
- `https://task-queue-f171f.up.railway.app/health`
- `https://task-queue-f171f.up.railway.app/api/queues/stats`

### 9. Railway Service Status

Check if:
- Service is deployed (not building)
- Service is active (green status)
- No error indicators

### 10. Redeploy

If nothing works:
1. Go to Railway dashboard
2. Click on your service
3. Click "Deploy" → "Redeploy"
4. Wait for deployment to complete
5. Check logs again

---

## Quick Diagnostic Commands

### Check if API is responding:
```bash
curl https://task-queue-f171f.up.railway.app/
```

### Check health:
```bash
curl https://task-queue-f171f.up.railway.app/health
```

### Submit a test task:
```bash
curl -X POST https://task-queue-f171f.up.railway.app/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"task_type": "test", "task_data": {"message": "Hello"}, "priority": "high"}'
```

### Check queue stats:
```bash
curl https://task-queue-f171f.up.railway.app/api/queues/stats
```

---

If you're still having issues, check the Railway logs for specific error messages.

