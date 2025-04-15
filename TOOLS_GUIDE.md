# Task Master Tools Implementation Guide

## 1. Understanding Task Master Structure

The Task Master repository (`claude-task-master`) is organized into several key directories:

```
├── mcp-server/          # MCP server implementation
├── tasks/              # Task-related tools
├── context/            # Context management
├── scripts/            # Utility scripts
└── docs/               # Documentation
```

## 2. Core Tool Categories

Based on the repository, we can create tools in these categories:

### 2.1 Task Management Tools

```python
@mcp.tool()
async def create_task(ctx: Context, title: str, description: str, priority: str = "medium") -> str:
    """Create a new task in the task management system.
    
    Args:
        title: The title of the task
        description: Detailed description of the task
        priority: Task priority (low, medium, high)
        
    Returns:
        Confirmation message with task ID
    """
    # Implementation
```

### 2.2 PRD (Product Requirements Document) Tools

```python
@mcp.tool()
async def parse_prd(ctx: Context, prd_content: str) -> str:
    """Parse a Product Requirements Document and extract tasks.
    
    Args:
        prd_content: The content of the PRD
        
    Returns:
        List of extracted tasks and requirements
    """
    # Implementation
```

### 2.3 Task Status Tools

```python
@mcp.tool()
async def update_task_status(ctx: Context, task_id: str, status: str) -> str:
    """Update the status of a task.
    
    Args:
        task_id: The ID of the task to update
        status: New status (todo, in_progress, done)
        
    Returns:
        Confirmation message
    """
    # Implementation
```

## 3. Implementation Guide

### 3.1 Basic Tool Structure

```python
from mcp.server.fastmcp import FastMCP, Context
from typing import Optional

mcp = FastMCP(
    "task-master",
    description="Task management system for AI-driven development",
    host=os.getenv("HOST", "0.0.0.0"),
    port=os.getenv("PORT", "8050")
)

@mcp.tool()
async def your_tool_name(ctx: Context, param1: str, param2: Optional[str] = None) -> str:
    """Tool description
    
    Args:
        param1: Description
        param2: Optional description
        
    Returns:
        Result description
    """
    try:
        # Implementation
        return "Result"
    except Exception as e:
        return f"Error: {str(e)}"
```

### 3.2 Required Dependencies

Add these to your `pyproject.toml`:

```toml
[project]
dependencies = [
    "mcp[cli]>=1.3.0",
    "python-dotenv>=1.0.0",
    "anthropic>=0.8.0",  # For Claude API
    "openai>=1.0.0"      # For Perplexity API (optional)
]
```

### 3.3 Environment Variables

Create a `.env` file with:

```env
ANTHROPIC_API_KEY=your_claude_api_key
PERPLEXITY_API_KEY=your_perplexity_api_key  # Optional
MODEL=claude-3-7-sonnet-20250219
PERPLEXITY_MODEL=sonar-pro
MAX_TOKENS=64000
TEMPERATURE=0.2
DEFAULT_SUBTASKS=5
DEFAULT_PRIORITY=medium
```

## 4. Example Tool Implementations

### 4.1 Task Creation Tool

```python
@mcp.tool()
async def create_task(ctx: Context, title: str, description: str, priority: str = "medium") -> str:
    """Create a new task in the task management system.
    
    Args:
        title: The title of the task
        description: Detailed description of the task
        priority: Task priority (low, medium, high)
        
    Returns:
        Confirmation message with task ID
    """
    try:
        # Generate unique task ID
        task_id = f"task_{int(time.time())}"
        
        # Create task object
        task = {
            "id": task_id,
            "title": title,
            "description": description,
            "priority": priority,
            "status": "todo",
            "created_at": datetime.now().isoformat()
        }
        
        # Store task (implement your storage logic)
        # store_task(task)
        
        return f"Task created successfully with ID: {task_id}"
    except Exception as e:
        return f"Error creating task: {str(e)}"
```

### 4.2 PRD Parser Tool

```python
@mcp.tool()
async def parse_prd(ctx: Context, prd_content: str) -> str:
    """Parse a Product Requirements Document and extract tasks.
    
    Args:
        prd_content: The content of the PRD
        
    Returns:
        List of extracted tasks and requirements
    """
    try:
        # Use Claude API to parse PRD
        # Implement PRD parsing logic
        
        return "Parsed tasks and requirements"
    except Exception as e:
        return f"Error parsing PRD: {str(e)}"
```

## 5. Testing Your Tools

1. Start your MCP server:
   ```bash
   uv run src/main.py
   ```

2. Test with an MCP client:
   ```json
   {
     "mcpServers": {
       "taskmaster": {
         "transport": "sse",
         "url": "http://localhost:8050/sse"
       }
     }
   }
   ```

## 6. Best Practices

1. **Error Handling**
   - Always use try-except blocks
   - Return meaningful error messages
   - Log errors appropriately

2. **Documentation**
   - Document all parameters
   - Include examples in docstrings
   - Keep documentation up to date

3. **Type Hints**
   - Use proper type hints
   - Include Optional types where appropriate
   - Document complex types

4. **Async Operations**
   - Use async/await properly
   - Handle concurrent operations safely
   - Use appropriate async libraries

## 7. Next Steps

1. Implement basic task management tools
2. Add PRD parsing capabilities
3. Create task status management
4. Add task prioritization
5. Implement task dependencies
6. Add task search and filtering 