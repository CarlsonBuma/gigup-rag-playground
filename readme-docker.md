# Setup Docker Environement
Let’s walk it step by step, end to end, assuming you now have a `docker-compose.yml` with:

- `pgvector` (Postgres + pgvector)
- `pgadmin`
- `ollama` (local LLM)

## 1. Preconditions on your Windows machine
- Check Version:
  - `docker -v`
- Make sure:
  - Docker Desktop is installed.
  - WSL2 backend is enabled.
  - Docker is running (whale icon in system tray).

## 2. Start your stack
Open a terminal where your `docker-compose.yml` lives:

1. **Start all services in the background**
   ```bash
   docker compose up -d
   ```
2. **Verify containers are running**
   ```bash
   docker ps
   ```
   You should see something like:
   - `pgvector_db`
   - `pgadmin_ui`
   - `ollama_local` (or whatever names you used)


## 3. Configure Ollama container (LLM & Embeddings)

1. **Enter the Ollama container**
   ```bash
   docker exec -it ollama_local bash
   ```
   (Replace `ollama_local` with your container_name if different.)

2. **Pull a model**
   Local Environment:

   ```bash
   ollama pull smollm:360m        # LLM
   ollama pull mxbai-embed-large  # Embedding, 1024 Dimension (680 MB)
   ```
   
   Live Environment:

   ```bash
   ollama pull llama3             # LLM
   ollama pull mxbai-embed-large  # Embedding, 1024 Dimension (680 MB)
   ```

3. Check Ollama Models
   ```bash
   ollama list
   ```

4. **Exit the container**
   ```bash
   exit
   ```


## 4. Stop and restart the whole stack

- **Stop all containers**
  ```bash
  docker compose down
  ```
- **Start again later**
  ```bash
  docker compose up -d
  ```

Volumes (`pgvector_data`, `pgadmin_data`, `OLLAMA_MODELS`) keep your data and models.
