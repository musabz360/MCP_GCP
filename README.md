# MCP Weather Server on Google Cloud Run

This project implements a weather data service using the **Model Context Protocol (MCP)**, designed to be consumed by intelligent agents (e.g., LLM agents). It's built with Python, containerized with Docker, and deployed to Google Cloud Run with continuous deployment configured from GitHub. It leverages the `https://open-meteo.com/` to fetch live weather data.

  * **Model Context Protocol (MCP) Server:** Exposes a dedicated MCP endpoint (`/sse`) for structured communication with AI agents.
  * **Containerized:** Packaged as a Docker image for consistent deployment across environments.
  * **Google Cloud Run Deployment:** Serverless deployment on GCP, scales automatically to zero when idle.
  * **Continuous Deployment (CD):** Automatically builds and deploys new versions from GitHub pushes using Google Cloud Build.
  * **Python 3.10+:** Built on a modern Python runtime.

## Architecture

The project's deployment architecture is as follows:

1.  **Python Application (`app.py`, `server.py`):**
      * `app.py` contains the core logic for fetching weather data.
      * `server.py` is the **FastMCP server** that defines and exposes the weather tool (`get_live_weather`) via the MCP protocol. It's configured to listen on `0.0.0.0` and the port provided by Cloud Run, using the `sse` transport.
2.  **`requirements.txt`:** Lists all Python dependencies, including `mcp`, `openmeteo-requests`, etc.
3.  **`Dockerfile`:** Defines how the Python application and its dependencies are bundled into a portable Docker image.
4.  **Google Cloud Build:** Triggered by pushes to the GitHub repository, it uses the `Dockerfile` to build the container image and pushes it to Google Cloud Artifact Registry.
5.  **Google Cloud Run:** Pulls the latest container image from Artifact Registry and deploys it as a serverless service. Cloud Run automatically handles scaling, load balancing, and health checks.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following:

  * A [Google Cloud Platform (GCP) Project](https://cloud.google.com/resource-manager/docs/creating-managing-projects).
  * [Git](https://git-scm.com/downloads) installed on your local machine.
  * (Optional, for local testing) [Docker Desktop](https://www.docker.com/products/docker-desktop) installed.
  * (Optional, for local development) [Python 3.10+](https://www.python.org/downloads/) and `pip`.

### 1\. Clone the Repository

First, clone your project's GitHub repository to your local machine:

```bash
git clone https://github.com/musabz360/MCP_GCP.git
cd MCP_GCP
```

### 2\. Project Structure

Here's a brief overview of the key files in your project:

```
MCP_GCP/
├── app.py                  # Core logic for fetching weather data (getliveTemp function)
├── server.py               # Model Context Protocol (MCP) server implementation
├── Dockerfile              # Instructions for building the Docker image
├── requirements.txt        # Python package dependencies
└── README.md               # This documentation file
```

## Deployment to Google Cloud Run

This project is set up for continuous deployment to Google Cloud Run directly from GitHub.

1.  **Enable GCP APIs:**

      * In your GCP project, enable the following APIs:
          * **Cloud Run API**
          * **Cloud Build API**
          * **Artifact Registry API**
      * You can do this via the GCP Console: `Navigation Menu > APIs & Services > Enabled APIs & services`. Search for and enable each one.

2.  **Configure Cloud Run Service:**

      * Go to the [Cloud Run page in the GCP Console](https://console.cloud.google.com/run).
      * Click **"CREATE SERVICE"**.
      * Select **"Continuously deploy from a repository"** and choose **"GitHub"**.
      * **Connect GitHub:** If this is your first time, **"Set up Cloud Build"** you'll be prompted to authorize Google Cloud Build to access your GitHub repositories. Grant the necessary permissions.
      * **Select Repository:** Choose your `./MCP_GCP` repository.
      * **Branch:** Select the branch you want to deploy from (e.g., `main` or `master`).
      * **Build Type:** Select **"Dockerfile"**. Ensure "Location" is "Repository root".
      * Click **"DONE"**.

3.  **Service Configuration:**

      * **Service name:** Choose a descriptive name, e.g., `mcp-weather-server`.
      * **Region:** Select a region close to your users or desired data center, e.g., `europe-west1` (as per your deployed URL).
      * **Auto-scaling:** Leave defaults (scales to zero instances when idle).
      * **Ingress:** Select **"Allow all traffic"**.
      * **Authentication:** Select **"Allow unauthenticated invocations"** (for public API access).
      * Click **"CREATE"**.

4.  **Automatic Deployment:**

      * Google Cloud Build will automatically build your Docker image and deploy it to Cloud Run.
      * Any subsequent `git push` to the configured branch in your GitHub repository will trigger a new build and deploy a new revision of your service.

## MCP Endpoint Usage

Your Cloud Run service now provides an MCP endpoint, designed to be consumed by an MCP client, typically within an AI agent.

### Endpoint

The MCP endpoint for the `sse` transport is located at the `/sse` path of your Cloud Run service URL.

**Example Cloud Run URL:** `https://mcp-weather-server-422554102903.europe-west1.run.app`

### Consuming with `langchain-mcp-adapters`

You would integrate this service into your LangChain/LangGraph agent using the `MultiServerMCPClient` as you've shown in your agent code. **Crucially, the `url` must include the `/sse` path.**

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

async def get_mcp_tools():
    client = MultiServerMCPClient({
        "weather": {
            # IMPORTANT: The '/sse' path is required for the 'sse' transport.
            # Replace with YOUR Cloud Run URL + '/sse'
            "url": "https://mcp-weather-server-422554102903.europe-west1.run.app/sse",
            "transport": "sse", # Matches your server.py configuration
        },
    })
    return await client.get_tools()

# Fetch tools for your agent (e.g., during agent initialization)
mcp_tools = asyncio.run(get_mcp_tools())
```

Your LLM agent would then use these `mcp_tools` to understand how to invoke `get_live_weather` by sending MCP-compliant requests to your Cloud Run service.

**Note:** Direct browser access to the Cloud Run service URL or other paths (like `/weather?latitude=...`) will result in a "Not Found" error. This service is not a conventional REST API for individual tools, but an MCP protocol server specifically at the `/sse` endpoint.

**MusabLatifi@Z360**
