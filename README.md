# VPN-Optimized Local AI Package

This repository is modified from the original to remove Let's Encrypt, Caddy, and Ollama. It binds all service ports directly to the host for easy access over a local network or VPN. Just clone, copy `.env.example` to `.env`, and run `python3 start_services.py`.

---

**Self-hosted AI Package** is an open, docker compose template that
quickly bootstraps a fully featured Local AI and Low Code development
environment. This is a slimmed-down version of Cole's repository, optimized specifically for VPN or local Proxmox deployments without the overhead of local LLMs or reverse proxies.

**February 26th, 2026 Update**: The latest Supabase storage container (`storage-api v1.37.8`) requires several new environment variables. These are included in the `.env.example`.

## Important Links
- [Local AI community](https://thinktank.ottomator.ai/c/local-ai/18) forum over in the oTTomator Think Tank
- [Original Local AI Starter Kit](https://github.com/n8n-io/self-hosted-ai-starter-kit) by the n8n team
- Download the N8N + OpenWebUI integration [directly on the Open WebUI site.](https://openwebui.com/f/coleam/n8n_pipe/) 

### What’s included

✅ [**Self-hosted n8n**](https://n8n.io/) - Low-code platform with over 400 integrations and advanced AI components
✅ [**Supabase**](https://supabase.com/) - Open source database as a service - most widely used database for AI agents
✅ [**Open WebUI**](https://openwebui.com/) - ChatGPT-like interface to privately interact with your API models and N8N agents
✅ [**Flowise**](https://flowiseai.com/) - No/low code AI agent builder that pairs very well with n8n
✅ [**Qdrant**](https://qdrant.tech/) - Open source, high performance vector store with an comprehensive API. 
✅ [**Neo4j**](https://neo4j.com/) - Knowledge graph engine that powers tools like GraphRAG, LightRAG, and Graphiti 
✅ [**SearXNG**](https://searxng.org/) - Open source, free internet metasearch engine.
✅ [**Langfuse**](https://langfuse.com/) - Open source LLM engineering platform for agent observability

## Prerequisites

Before you begin, make sure you have the following software installed:
- [Python](https://www.python.org/downloads/) - Required to run the setup script
- [Git/GitHub Desktop](https://desktop.github.com/) - For easy repository management
- [Docker/Docker Desktop](https://www.docker.com/products/docker-desktop/) - Required to run all services

> [!TIP]
> **For Proxmox Users:** We highly recommend configuring your Docker LXC environment using the community scripts available at [community-scripts.org](https://community-scripts.org/scripts?q=docker). It will configure the LXC container optimally for Docker workloads out of the box.

## Installation

Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/thomasmaerz/local-ai-packaged.git
cd local-ai-packaged
```

1. Make a copy of `.env.example` and rename it to `.env` in the root directory of the project
2. Set the following required environment variables (make sure to generate secure random values!):
   ```bash
   ############
   # N8N Configuration
   ############
   N8N_ENCRYPTION_KEY=
   N8N_USER_MANAGEMENT_JWT_SECRET=

   ############
   # Supabase Secrets
   ############
   POSTGRES_PASSWORD=
   JWT_SECRET=
   ANON_KEY=
   SERVICE_ROLE_KEY=
   DASHBOARD_USERNAME=
   DASHBOARD_PASSWORD=
   POOLER_TENANT_ID=

   ############
   # Neo4j Secrets
   ############   
   NEO4J_AUTH=

   ############
   # Langfuse credentials
   ############
   CLICKHOUSE_PASSWORD=
   MINIO_ROOT_PASSWORD=
   LANGFUSE_SALT=
   NEXTAUTH_SECRET=
   ENCRYPTION_KEY=  
   ```

---

The project includes a `start_services.py` script that handles starting both the Supabase and local AI services. 

To start the environment, run:

```bash
python3 start_services.py
```

This will run everything in the "private" mode by default, meaning all service ports are bound directly to your host's IP address (0.0.0.0). You can access them securely over your local LAN or VPN connection.

## Deploying

This package is optimized specifically for **local environments and VPNs**. It strips out Caddy and Let's Encrypt to simplify deployment when public IPs or domains are not necessary. 

**WARNING:** Do not deploy this repository as-is on a public cloud instance without configuring a reverse proxy (like Nginx, Traefik, or Caddy) to secure the traffic. Exposing these ports directly to the open internet is a major security risk.

## Importing Starter Workflows

This package includes pre-built n8n workflows in the `n8n/backup/workflows/` folder. To import them:

1. Open n8n at `http://<your-server-ip>:5678/` 
2. Go to your workflow list and click the three-dot menu or use **Import from File**
3. Select the JSON files from the `n8n/backup/workflows/` folder on your local machine

> [!NOTE]
> You'll need to create credentials for each workflow after importing. See step 3 in Quick Start below.

## ⚡️ Quick start and usage

1. Open `http://<your-server-ip>:5678/` in your browser to set up n8n. You’ll only have to do this once. You are NOT creating an account with n8n in the setup here, it is only a local account for your instance!
2. Import a workflow from `n8n/backup/workflows/`, then open it from your workflow list.
3. Create credentials for every service:
   
   Postgres (through Supabase): use DB, username, and password from .env. IMPORTANT: Host is 'db' Since that is the name of the service running Supabase

   Qdrant URL: `http://qdrant:6333` (API key can be whatever since this is running locally)

4. Select **Test workflow** to start running the workflow.
5. Make sure to toggle the workflow as active and copy the "Production" webhook URL!
6. Open `http://<your-server-ip>:8080/` in your browser to set up Open WebUI. You’ll only have to do this once.
7. Go to Workspace -> Functions -> Add Function -> Give name + description then paste in the code from `n8n_pipe.py`
8. Click on the gear icon and set the n8n_url to the production URL for the webhook you copied in a previous step.
9. Toggle the function on and now it will be available in your model dropdown in the top left! 

To keep everything local/API-driven, remember to configure your favorite API keys (e.g., OpenAI, Anthropic, Google Gemini) in Open WebUI, Flowise, or n8n natively! Local LLM inference (Ollama) has been stripped out of this VPN-optimized package to keep hardware requirements lightweight.

## Upgrading

To update all containers to their latest versions (n8n, Open WebUI, etc.), run these commands:

```bash
# Stop all services
python3 start_services.py

# Note: The easiest way to pull fresh containers is to manually run:
docker compose -p localai -f docker-compose.yml pull

# Start services again
python3 start_services.py
```

## Troubleshooting

### Supabase Issues
- **Supabase Pooler Restarting**: If the supabase-pooler container keeps restarting itself, follow the instructions in [this GitHub issue](https://github.com/supabase/supabase/issues/30210#issuecomment-2456955578).
- **Supabase Analytics Startup Failure**: If the supabase-analytics container fails to start after changing your Postgres password, delete the folder `supabase/docker/volumes/db/data`.
- **Supabase Service Unavailable** - Make sure you don't have an "@" character in your Postgres password! 
- **Files not Found in Supabase Folder** - If you get any errors around files missing in the supabase/ folder like .env, docker/docker-compose.yml, etc. this most likely means you had a "bad" pull of the Supabase GitHub repository. Delete the supabase/ folder within the Local AI Package folder entirely and try again.

### SearXNG Issues
- **SearXNG Restarting**: If the SearXNG container keeps restarting, run the command `chmod 755 searxng` within the local-ai-packaged folder so SearXNG has the permissions it needs to create the uwsgi.ini file.

## Tips & tricks

### Accessing local files

The self-hosted AI starter kit will create a shared folder (by default, located in the same directory) which is mounted to the n8n container and allows n8n to access files on disk. This folder within the n8n container is located at `/data/shared` -- this is the path you’ll need to use in nodes that interact with the local filesystem.

## 📜 License

This project (originally created by the n8n team and Cole) is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
