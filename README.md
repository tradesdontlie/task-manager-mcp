# Task Manager MCP Server

A template implementation of the [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for managing tasks and projects. This server provides a comprehensive task management system with support for project organization, task tracking, and PRD parsing.

## Overview

This project demonstrates how to build an MCP server that enables AI agents to manage tasks, track project progress, and break down Product Requirements Documents (PRDs) into actionable tasks. It serves as a practical template for creating your own MCP servers with task management capabilities.

The implementation follows the best practices laid out by Anthropic for building MCP servers, allowing seamless integration with any MCP-compatible client.

## Features

The server provides several essential task management tools:

1. **Task Management**
   - `create_task_file`: Create new project task files
   - `add_task`: Add tasks to projects with descriptions and subtasks
   - `update_task_status`: Update the status of tasks and subtasks
   - `get_next_task`: Get the next uncompleted task from a project

2. **Project Planning**
   - `parse_prd`: Convert PRDs into structured tasks automatically
   - `expand_task`: Break down tasks into smaller, manageable subtasks
   - `estimate_task_complexity`: Estimate task complexity and time requirements
   - `get_task_dependencies`: Track task dependencies

3. **Development Support**
   - `generate_task_file`: Generate file templates based on task descriptions
   - `suggest_next_actions`: Get AI-powered suggestions for next steps

## Prerequisites

- Python 3.12+
- API keys for your chosen LLM provider (OpenAI, OpenRouter, or Ollama)
- Docker if running the MCP server as a container (recommended)

## Installation

### Using uv

1. Install uv if you don't have it:
   ```bash
   pip install uv
   ```

2. Clone this repository:
   ```bash
   git clone https://github.com/coleam00/mcp-mem0.git
   cd mcp-mem0
   ```

3. Install dependencies:
   ```bash
   uv pip install -e .
   ```

4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

5. Configure your environment variables in the `.env` file (see Configuration section)

### Using Docker (Recommended)

1. Build the Docker image:
   ```bash
   docker build -t mcp/mem0 --build-arg PORT=8050 .
   ```

2. Create a `.env` file based on `.env.example` and configure your environment variables

## Configuration

The following environment variables can be configured in your `.env` file:

| Variable | Description | Example |
|----------|-------------|----------|
| `TRANSPORT` | Transport protocol (sse or stdio) | `sse` |
| `HOST` | Host to bind to when using SSE transport | `0.0.0.0` |
| `PORT` | Port to listen on when using SSE transport | `8050` |

## Running the Server

### Using Python 3

```bash
# Set TRANSPORT=sse in .env then:
python3 src/main.py
```

The server will start on the configured host and port (default: http://0.0.0.0:8050).

### Using Docker

```bash
docker build -t task-manager-mcp .
docker run --env-file .env -p 8050:8050 task-manager-mcp
```

## Using the Task Manager

### Creating a New Project

1. Create a task file for your project:
```python
await mcp.create_task_file(project_name="my-project")
```

2. Add tasks to your project:
```python
await mcp.add_task(
    project_name="my-project",
    title="Setup Development Environment",
    description="Configure the development environment with required tools",
    subtasks=[
        "Install dependencies",
        "Configure linters",
        "Set up testing framework"
    ]
)
```

3. Parse a PRD to create tasks automatically:
```python
await mcp.parse_prd(
    project_name="my-project",
    prd_content="# Your PRD content..."
)
```

### Managing Tasks

1. Update task status:
```python
await mcp.update_task_status(
    project_name="my-project",
    task_title="Setup Development Environment",
    subtask_title="Install dependencies",
    status="done"
)
```

2. Get the next task to work on:
```python
next_task = await mcp.get_next_task(project_name="my-project")
```

3. Expand a task into subtasks:
```python
await mcp.expand_task(
    project_name="my-project",
    task_title="Implement Authentication"
)
```

### Development Workflow

1. Generate a file template for a task:
```python
await mcp.generate_task_file(
    project_name="my-project",
    task_title="User Authentication"
)
```

2. Get task complexity estimate:
```python
complexity = await mcp.estimate_task_complexity(
    project_name="my-project",
    task_title="User Authentication"
)
```

3. Get suggestions for next actions:
```python
suggestions = await mcp.suggest_next_actions(
    project_name="my-project",
    task_title="User Authentication"
)
```

## Integration with MCP Clients

### SSE Configuration

To connect to the server using SSE transport, use this configuration:

```json
{
  "mcpServers": {
    "task-manager": {
      "transport": "sse",
      "url": "http://localhost:8050/sse"
    }
  }
}
```

### Stdio Configuration

For stdio transport, use this configuration:

```json
{
  "mcpServers": {
    "task-manager": {
      "command": "python3",
      "args": ["src/main.py"],
      "env": {
        "TRANSPORT": "stdio",
        "LLM_PROVIDER": "openai",
        "LLM_API_KEY": "YOUR-API-KEY",
        "LLM_CHOICE": "gpt-4"
      }
    }
  }
}
```

## Building Your Own Server

This template provides a foundation for building more complex task management MCP servers. To extend it:

1. Add new task management tools using the `@mcp.tool()` decorator
2. Implement custom task analysis and automation features
3. Add project-specific task templates and workflows
4. Integrate with your existing development tools and processes
