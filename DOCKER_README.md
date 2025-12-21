# Docker Deployment Guide 🐳

Complete guide for deploying the AHP Questionnaire backend using Docker.

## 📋 Prerequisites

- Docker installed on your system
- Docker Compose (optional, but recommended)
- GitHub Personal Access Token (for Gist storage)

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Set environment variables:**
   ```bash
   # Create .env file
   cat > .env << EOF
   GITHUB_TOKEN=ghp_your_token_here
   GIST_ID=your_gist_id_here
   EOF
   ```

2. **Start the service:**
   ```bash
   docker-compose up -d
   ```

3. **Check logs:**
   ```bash
   docker-compose logs -f backend
   ```

4. **Test:**
   ```bash
   curl http://localhost:5000/api/health
   ```

5. **Stop:**
   ```bash
   docker-compose down
   ```

### Option 2: Using Docker CLI

1. **Build the image:**
   ```bash
   docker build -t ahp-backend .
   ```

2. **Run the container:**
   ```bash
   docker run -d \
     --name ahp-backend \
     -p 5000:5000 \
     -e GITHUB_TOKEN=ghp_your_token_here \
     -e GIST_ID=your_gist_id_here \
     -v $(pwd)/criteria.csv:/app/criteria.csv:ro \
     --restart unless-stopped \
     ahp-backend
   ```

3. **Check logs:**
   ```bash
   docker logs -f ahp-backend
   ```

4. **Test:**
   ```bash
   curl http://localhost:5000/api/health
   ```

5. **Stop:**
   ```bash
   docker stop ahp-backend
   docker rm ahp-backend
   ```

## 📁 Files Explained

### Dockerfile
Main Docker configuration file that:
- Uses Python 3.11 slim image
- Installs system dependencies (gcc for some Python packages)
- Installs Python dependencies from `requirements-backend.txt`
- Copies backend code and criteria.csv
- Exposes port 5000
- Includes health check
- Runs the backend server

### .dockerignore
Tells Docker which files to exclude from the build:
- Python cache files
- Virtual environments
- IDE files
- Documentation
- Frontend code
- Test files

This makes builds faster and images smaller!

### docker-compose.yml
Docker Compose configuration for easy deployment:
- Builds the image
- Maps port 5000
- Sets environment variables
- Mounts criteria.csv
- Auto-restart on failure
- Health checks

## 🔧 Configuration

### Environment Variables

Set these in `.env` file or pass to `docker run`:

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| GITHUB_TOKEN | Yes (for Gist) | GitHub personal access token | ghp_xxxxxxxxxxxx |
| GIST_ID | No | Existing Gist ID | abc123def456 |
| PORT | No | Port to run on (default: 5000) | 5000 |

### Custom Criteria

To use custom criteria, modify `criteria.csv` before building:

```csv
Criterion
Your Criterion 1
Your Criterion 2
Your Criterion 3
```

The file is copied into the image during build.

## 🏗️ Building

### Development Build
```bash
docker build -t ahp-backend:dev .
```

### Production Build
```bash
docker build -t ahp-backend:latest .
```

### Multi-platform Build (for deployment)
```bash
docker buildx build --platform linux/amd64,linux/arm64 -t ahp-backend:latest .
```

## 🚢 Deployment

### Deploy to Docker Hub

1. **Tag image:**
   ```bash
   docker tag ahp-backend:latest yourusername/ahp-backend:latest
   ```

2. **Push to Docker Hub:**
   ```bash
   docker login
   docker push yourusername/ahp-backend:latest
   ```

3. **Pull and run on server:**
   ```bash
   docker pull yourusername/ahp-backend:latest
   docker run -d -p 5000:5000 \
     -e GITHUB_TOKEN=ghp_xxx \
     -e GIST_ID=xxx \
     yourusername/ahp-backend:latest
   ```

### Deploy to Railway (with Docker)

Railway can also use the Dockerfile if you prefer:

1. In Railway project settings
2. Set "Builder" to "Dockerfile"
3. Railway will use the Dockerfile instead of Nixpacks
4. Add environment variables in Railway dashboard

### Deploy to Render

1. Create new "Web Service"
2. Connect GitHub repository
3. Select "Docker" as environment
4. Add environment variables
5. Deploy!

## 🐛 Troubleshooting

### "pip: command not found"

**Cause:** Dockerfile issue

**Fix:** Use the provided Dockerfile which includes:
```dockerfile
FROM python:3.11-slim
```

This base image includes Python and pip.

### Build is slow

**Cause:** Installing dependencies every time

**Fix:** Use Docker layer caching:
```bash
# Copy only requirements first
COPY requirements-backend.txt .
RUN pip install -r requirements-backend.txt

# Then copy code (changes more often)
COPY backend/ ./backend/
```

Our Dockerfile already does this!

### Image is too large

**Check size:**
```bash
docker images ahp-backend
```

**Reduce size:**
- ✅ Using `python:3.11-slim` (not full Python)
- ✅ Using `.dockerignore` to exclude unnecessary files
- ✅ Using `--no-cache-dir` in pip install
- ✅ Cleaning apt cache

Current image: ~200-300 MB (quite small!)

### Container exits immediately

**Check logs:**
```bash
docker logs ahp-backend
```

**Common causes:**
- Missing environment variables
- Port already in use
- Syntax error in Python code

### Can't connect from host

**Issue:** Container running but can't access from host

**Fix:** Make sure port is mapped:
```bash
docker run -p 5000:5000 ...
```

**Test from inside container:**
```bash
docker exec -it ahp-backend curl http://localhost:5000/api/health
```

## 📊 Monitoring

### View logs
```bash
# Docker Compose
docker-compose logs -f backend

# Docker CLI
docker logs -f ahp-backend
```

### Check health
```bash
# Docker health status
docker ps

# Manual health check
curl http://localhost:5000/api/health
```

### Resource usage
```bash
docker stats ahp-backend
```

## 🔄 Updates

### Update and restart

**Docker Compose:**
```bash
git pull
docker-compose down
docker-compose build
docker-compose up -d
```

**Docker CLI:**
```bash
git pull
docker stop ahp-backend
docker rm ahp-backend
docker build -t ahp-backend .
docker run -d --name ahp-backend -p 5000:5000 ... ahp-backend
```

## 🎯 Best Practices

### Production Deployment

1. **Use specific Python version:**
   ```dockerfile
   FROM python:3.11.0-slim
   ```

2. **Don't run as root:**
   ```dockerfile
   RUN useradd -m appuser
   USER appuser
   ```

3. **Use multi-stage builds** (for even smaller images):
   ```dockerfile
   FROM python:3.11-slim as builder
   # Install dependencies

   FROM python:3.11-slim
   COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
   # Copy only what's needed
   ```

4. **Set resource limits:**
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '0.5'
         memory: 512M
   ```

### Security

- ✅ Don't include `.env` in image
- ✅ Use secrets management for tokens
- ✅ Scan images for vulnerabilities:
  ```bash
  docker scan ahp-backend
  ```
- ✅ Keep base image updated
- ✅ Don't run as root (add USER in Dockerfile)

## 📚 Learn More

- Docker Docs: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/
- Best Practices: https://docs.docker.com/develop/dev-best-practices/

## 🆚 Docker vs Railway/Vercel

| Aspect | Docker | Railway/Vercel |
|--------|--------|----------------|
| Control | Full control | Managed service |
| Setup | Manual | Automatic |
| Scaling | Manual | Automatic |
| Cost | Server costs | Free tier available |
| Best for | Self-hosting, on-prem | Quick deployment |

**Use Docker when:**
- You have your own server
- You need full control
- You're deploying on-premise
- You want containerization

**Use Railway/Vercel when:**
- You want easiest deployment
- You want automatic scaling
- You're fine with managed services
- You want free tier

Both work great! Choose based on your needs.

---

**Questions?** Check the main [DEPLOYMENT_GUIDE_BEGINNERS.md](DEPLOYMENT_GUIDE_BEGINNERS.md) for Railway/Vercel deployment.
