import os
import re
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from mcp.server.fastmcp import FastMCP, Context

def create_mcp() -> FastMCP:
    """Create a new MCP instance with task management tools."""
    mcp = FastMCP(
        "TASK MANAGER",
        description="Markdown-based task management system with PRD parsing",
        host=os.getenv("HOST", "0.0.0.0"),
        port=os.getenv("PORT", "8050")
    )

    class TaskManager:
        def __init__(self, tasks_dir: str = "tasks"):
            self.tasks_dir = Path(tasks_dir)
            self.tasks_dir.mkdir(exist_ok=True)
            
        def _get_task_file(self, project_name: str) -> Path:
            return self.tasks_dir / f"{project_name}.md"
            
        def _parse_markdown_tasks(self, content: str) -> List[dict]:
            tasks = []
            current_task = None
            
            for line in content.split('\n'):
                # Match task headers (## Task: Title)
                task_match = re.match(r'^##\s+Task:\s+(.+)$', line)
                if task_match:
                    if current_task:
                        tasks.append(current_task)
                    current_task = {
                        'title': task_match.group(1),
                        'description': '',
                        'subtasks': [],
                        'status': 'todo'
                    }
                    continue
                    
                # Match subtasks (- [ ] Subtask)
                subtask_match = re.match(r'^-\s+\[(.)\]\s+(.+)$', line)
                if subtask_match and current_task:
                    status = 'done' if subtask_match.group(1) == 'x' else 'todo'
                    current_task['subtasks'].append({
                        'title': subtask_match.group(2),
                        'status': status
                    })
                    continue
                    
                # Match description lines
                if current_task and line.strip() and not line.startswith('-'):
                    current_task['description'] += line + '\n'
                    
            if current_task:
                tasks.append(current_task)
                
            return tasks
            
        def _generate_markdown(self, tasks: List[dict]) -> str:
            """Generate markdown content from tasks list."""
            content = "# Project Tasks\n\n"
            
            # Add task categories explanation
            content += "## Categories\n"
            content += "- [MVP] Core functionality tasks\n"
            content += "- [AI] AI-related features\n"
            content += "- [UX] User experience improvements\n"
            content += "- [INFRA] Infrastructure and setup\n\n"
            
            # Add priority levels explanation
            content += "## Priority Levels\n"
            content += "- P0: Blocker/Critical\n"
            content += "- P1: High Priority\n"
            content += "- P2: Medium Priority\n"
            content += "- P3: Low Priority\n\n"
            
            for idx, task in enumerate(tasks, 1):
                # Add task header with number, category, and priority
                category = task.get('category', '')
                priority = task.get('priority', 'P2')
                content += f"## Task {idx}: {category} {task['title']} ({priority})\n\n"
                
                # Add task description
                if task.get('description', '').strip():
                    content += f"{task['description'].strip()}\n\n"
                
                # Add dependencies if they exist
                if task.get('dependencies'):
                    content += "### Dependencies:\n"
                    for dep in task['dependencies']:
                        content += f"- Task {dep}\n"
                    content += "\n"
                
                # Add estimated complexity and time
                if task.get('complexity'):
                    content += f"### Complexity: {task['complexity']}\n"
                    content += f"Estimated hours: {task['estimated_hours']}\n\n"
                
                # Add subtasks with proper formatting and indentation
                if task.get('subtasks'):
                    content += "### Subtasks:\n\n"
                    for subtask in task['subtasks']:
                        status = 'x' if subtask.get('status') == 'done' else ' '
                        content += f"- [{status}] {subtask['title']}\n"
                    content += "\n"
                
                # Add separator between tasks
                content += "---\n\n"
            
            return content

    # Create a TaskManager instance
    manager = TaskManager()

    @mcp.tool()
    async def create_task_file(ctx: Context, project_name: str) -> str:
        """Create a new markdown task file for a project.
        
        Args:
            project_name: Name of the project
            
        Returns:
            Confirmation message with file path
        """
        try:
            task_file = manager._get_task_file(project_name)
            
            if task_file.exists():
                return f"Task file already exists at {task_file}"
                
            with open(task_file, 'w') as f:
                f.write("# Project Tasks\n\n")
                
            return f"Created new task file at {task_file}"
        except Exception as e:
            return f"Error creating task file: {str(e)}"

    @mcp.tool()
    async def add_task(ctx: Context, project_name: str, title: str, description: str, subtasks: Optional[List[str]] = None, batch_mode: bool = False) -> str:
        """Add a new task to a project's task file.
        
        Args:
            project_name: Name of the project
            title: Task title
            description: Task description
            subtasks: Optional list of subtasks
            batch_mode: If True, don't read existing tasks (for bulk additions)
            
        Returns:
            Confirmation message
        """
        try:
            task_file = manager._get_task_file(project_name)
            
            if not task_file.exists() and not batch_mode:
                return f"Task file not found for project {project_name}"
            
            # Read existing content if file exists
            existing_content = ""
            if task_file.exists():
                with open(task_file, 'r') as f:
                    existing_content = f.read().strip()
            
            # If this is the first task, add the header
            if not existing_content:
                existing_content = "# Project Tasks\n\n"
            
            # Create the new task content
            new_task = {
                'title': title,
                'description': description,
                'subtasks': [{'title': st, 'status': 'todo'} for st in (subtasks or [])],
                'status': 'todo'
            }
            
            # Generate markdown for just this task
            task_content = f"\n## Task: {new_task['title']}\n\n"
            if new_task['description'].strip():
                task_content += f"{new_task['description'].strip()}\n\n"
            
            if new_task['subtasks']:
                task_content += "### Subtasks:\n\n"
                for subtask in new_task['subtasks']:
                    status = 'x' if subtask.get('status') == 'done' else ' '
                    task_content += f"- [{status}] {subtask['title']}\n"
                task_content += "\n"
            
            task_content += "---\n\n"
            
            # Append the new task to existing content
            with open(task_file, 'w') as f:
                f.write(existing_content.rstrip() + "\n\n" + task_content)
            
            return f"Added new task '{title}' to {project_name}"
        except Exception as e:
            return f"Error adding task: {str(e)}"

    @mcp.tool()
    async def parse_prd(ctx: Context, project_name: str, prd_content: str) -> str:
        """Parse a PRD and create tasks from it."""
        try:
            # Parse sections from PRD
            sections = {}
            current_section = None
            current_content = []
            
            for line in prd_content.split('\n'):
                if line.startswith('# '):
                    if current_section:
                        sections[current_section] = '\n'.join(current_content)
                    current_section = line[2:].strip()
                    current_content = []
                elif line.startswith('## '):
                    if current_section:
                        sections[current_section] = '\n'.join(current_content)
                    current_section = line[3:].strip()
                    current_content = []
                else:
                    current_content.append(line)
                    
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            
            # Create tasks based on sections
            tasks = []
            
            # Project Setup (First task)
            tasks.append({
                'title': 'Project Setup',
                'description': 'Set up the Next.js project with TypeScript and Tailwind CSS',
                'category': '[INFRA]',
                'priority': 'P0',
                'complexity': 'low',
                'estimated_hours': 4,
                'dependencies': [],
                'subtasks': [{'title': st, 'status': 'todo'} for st in [
                    'Initialize Next.js project',
                    'Configure TypeScript',
                    'Set up Tailwind CSS',
                    'Configure development environment',
                    'Set up testing framework'
                ]]
            })
            
            # Core Features from Key Features section (MVP Phase)
            if 'Key Features' in sections:
                features = extract_bullet_points(sections['Key Features'])
                mvp_features = [f for f in features if 'AI' not in f and 'cloud' not in f.lower()]
                tasks.append({
                    'title': 'Implement Core Features',
                    'description': 'Implement the core MVP features of the journaling app',
                    'category': '[MVP]',
                    'priority': 'P0',
                    'complexity': 'medium',
                    'estimated_hours': 8,
                    'dependencies': [1],  # Depends on Project Setup
                    'subtasks': [{'title': st, 'status': 'todo'} for st in mvp_features]
                })
            
            # Authentication & Storage (MVP Phase)
            tasks.append({
                'title': 'Authentication & Local Storage',
                'description': 'Implement user authentication and local storage features',
                'category': '[MVP]',
                'priority': 'P1',
                'complexity': 'medium',
                'estimated_hours': 8,
                'dependencies': [1],  # Depends on Project Setup
                'subtasks': [{'title': st, 'status': 'todo'} for st in [
                    'Implement email authentication',
                    'Set up local storage with IndexedDB',
                    'Add user session management',
                    'Implement data persistence'
                ]]
            })
            
            # AI Features (Phase 2)
            if 'Key Features' in sections:
                ai_features = [f for f in features if 'AI' in f or 'summarize' in f.lower() or 'pattern' in f.lower()]
                if ai_features:
                    tasks.append({
                        'title': 'Implement AI Features',
                        'description': 'Add AI-powered features for insights and analysis',
                        'category': '[AI]',
                        'priority': 'P2',
                        'complexity': 'high',
                        'estimated_hours': 16,
                        'dependencies': [2, 3],  # Depends on Core Features and Auth
                        'subtasks': [{'title': st, 'status': 'todo'} for st in ai_features]
                    })
            
            # UI/UX Features
            tasks.append({
                'title': 'Enhance UI/UX',
                'description': 'Implement UI/UX improvements and polish',
                'category': '[UX]',
                'priority': 'P2',
                'complexity': 'medium',
                'estimated_hours': 8,
                'dependencies': [2],  # Depends on Core Features
                'subtasks': [{'title': st, 'status': 'todo'} for st in [
                    'Implement dark/light mode',
                    'Add responsive design',
                    'Create minimalist editor',
                    'Add keyboard shortcuts'
                ]]
            })
            
            # Cloud Features (Phase 3)
            tasks.append({
                'title': 'Implement Cloud Features',
                'description': 'Add cloud sync and advanced storage features',
                'category': '[INFRA]',
                'priority': 'P3',
                'complexity': 'high',
                'estimated_hours': 16,
                'dependencies': [2, 3],  # Depends on Core Features and Auth
                'subtasks': [{'title': st, 'status': 'todo'} for st in [
                    'Set up cloud sync',
                    'Implement end-to-end encryption',
                    'Add offline support',
                    'Create backup/restore functionality'
                ]]
            })
            
            # Create task file with the structured content
            task_file = manager._get_task_file(project_name)
            with open(task_file, 'w', encoding='utf-8') as f:
                f.write(manager._generate_markdown(tasks))
            
            return f"Successfully created tasks from PRD in {task_file}"
            
        except Exception as e:
            return f"Error parsing PRD: {str(e)}"

    @mcp.tool()
    async def update_task_status(ctx: Context, project_name: str, task_title: str, subtask_title: Optional[str] = None, status: str = "done") -> str:
        """Update the status of a task or subtask.
        
        Args:
            project_name: Name of the project
            task_title: Title of the task
            subtask_title: Optional title of the subtask
            status: New status (todo/done)
            
        Returns:
            Confirmation message
        """
        try:
            task_file = manager._get_task_file(project_name)
            
            if not task_file.exists():
                return f"Task file not found for project {project_name}"
                
            with open(task_file, 'r') as f:
                content = f.read()
                
            tasks = manager._parse_markdown_tasks(content)
            
            for task in tasks:
                if task['title'] == task_title:
                    if subtask_title:
                        for subtask in task['subtasks']:
                            if subtask['title'] == subtask_title:
                                subtask['status'] = status
                                break
                    else:
                        task['status'] = status
                    break
                    
            with open(task_file, 'w') as f:
                f.write(manager._generate_markdown(tasks))
                
            return f"Updated status of {'subtask' if subtask_title else 'task'} to {status}"
        except Exception as e:
            return f"Error updating status: {str(e)}"

    @mcp.tool()
    async def get_next_task(ctx: Context, project_name: str) -> str:
        """Get the next uncompleted task from a project.
        
        Args:
            project_name: Name of the project
            
        Returns:
            Next task information or completion message
        """
        try:
            task_file = manager._get_task_file(project_name)
            
            if not task_file.exists():
                return f"Task file not found for project {project_name}"
                
            with open(task_file, 'r') as f:
                content = f.read()
                
            tasks = manager._parse_markdown_tasks(content)
            
            for task in tasks:
                if task['status'] == 'todo':
                    # Check if all subtasks are done
                    if all(st['status'] == 'done' for st in task['subtasks']):
                        continue
                        
                    # Find first incomplete subtask
                    for subtask in task['subtasks']:
                        if subtask['status'] == 'todo':
                            return json.dumps({
                                'task': task['title'],
                                'subtask': subtask['title'],
                                'description': task['description']
                            })
                            
            return "All tasks are completed!"
        except Exception as e:
            return f"Error getting next task: {str(e)}"

    @mcp.tool()
    async def expand_task(ctx: Context, project_name: str, task_title: str) -> str:
        """Break down a task into smaller, more manageable subtasks using AI.
        
        Args:
            project_name: Name of the project
            task_title: Title of the task to expand
            
        Returns:
            Confirmation message with new subtasks
        """
        try:
            task_file = manager._get_task_file(project_name)
            
            if not task_file.exists():
                return f"Task file not found for project {project_name}"
                
            with open(task_file, 'r') as f:
                content = f.read()
                
            tasks = manager._parse_markdown_tasks(content)
            
            for task in tasks:
                if task['title'] == task_title:
                    # Use AI to generate subtasks
                    prompt = f"Break down this task into smaller, actionable subtasks: {task['description']}"
                    # Here we would use Cursor's AI to generate subtasks
                    # For now, we'll use a placeholder
                    new_subtasks = [
                        "Research existing solutions",
                        "Design implementation approach",
                        "Write initial code",
                        "Test functionality",
                        "Review and refine"
                    ]
                    
                    task['subtasks'].extend([{'title': st, 'status': 'todo'} for st in new_subtasks])
                    
                    with open(task_file, 'w') as f:
                        f.write(manager._generate_markdown(tasks))
                        
                    return f"Expanded task '{task_title}' with new subtasks"
                    
            return f"Task '{task_title}' not found"
        except Exception as e:
            return f"Error expanding task: {str(e)}"

    @mcp.tool()
    async def generate_task_file(ctx: Context, project_name: str, task_title: str) -> str:
        """Generate a file template based on a task's description.
        
        Args:
            project_name: Name of the project
            task_title: Title of the task to generate file for
            
        Returns:
            Confirmation message with file path
        """
        try:
            task_file = manager._get_task_file(project_name)
            
            if not task_file.exists():
                return f"Task file not found for project {project_name}"
                
            with open(task_file, 'r') as f:
                content = f.read()
                
            tasks = manager._parse_markdown_tasks(content)
            
            for task in tasks:
                if task['title'] == task_title:
                    # Use AI to generate file content
                    prompt = f"Generate a file template for implementing: {task['description']}"
                    # Here we would use Cursor's AI to generate file content
                    # For now, we'll use a placeholder
                    file_content = """# File generated from task: {task_title}

def main():
    # TODO: Implement functionality
    pass

if __name__ == "__main__":
    main()
"""
                    
                    # Create file in project directory
                    file_path = Path(project_name) / f"{task_title.lower().replace(' ', '_')}.py"
                    file_path.parent.mkdir(exist_ok=True)
                    
                    with open(file_path, 'w') as f:
                        f.write(file_content)
                        
                    return f"Generated file template at {file_path}"
                    
            return f"Task '{task_title}' not found"
        except Exception as e:
            return f"Error generating file: {str(e)}"

    @mcp.tool()
    async def get_task_dependencies(ctx: Context, project_name: str, task_title: str) -> str:
        """Get all tasks that depend on the given task.
        
        Args:
            project_name: Name of the project
            task_title: Title of the task to check dependencies for
            
        Returns:
            JSON string of dependent tasks
        """
        try:
            task_file = manager._get_task_file(project_name)
            
            if not task_file.exists():
                return f"Task file not found for project {project_name}"
                
            with open(task_file, 'r') as f:
                content = f.read()
                
            tasks = manager._parse_markdown_tasks(content)
            dependent_tasks = []
            
            for task in tasks:
                if task['title'] != task_title and task_title.lower() in task['description'].lower():
                    dependent_tasks.append({
                        'title': task['title'],
                        'status': task['status']
                    })
                    
            return json.dumps(dependent_tasks)
        except Exception as e:
            return f"Error getting dependencies: {str(e)}"

    @mcp.tool()
    async def estimate_task_complexity(ctx: Context, project_name: str, task_title: str) -> str:
        """Estimate the complexity of a task using AI.
        
        Args:
            project_name: Name of the project
            task_title: Title of the task to estimate
            
        Returns:
            Complexity estimate (low/medium/high)
        """
        try:
            task_file = manager._get_task_file(project_name)
            
            if not task_file.exists():
                return f"Task file not found for project {project_name}"
                
            with open(task_file, 'r') as f:
                content = f.read()
                
            tasks = manager._parse_markdown_tasks(content)
            
            for task in tasks:
                if task['title'] == task_title:
                    # Use AI to estimate complexity
                    prompt = f"Estimate the complexity of this task (low/medium/high): {task['description']}"
                    # Here we would use Cursor's AI to estimate complexity
                    # For now, we'll use a placeholder
                    complexity = "medium"
                    
                    return json.dumps({
                        'task': task_title,
                        'complexity': complexity,
                        'estimated_hours': 4 if complexity == 'low' else 8 if complexity == 'medium' else 16
                    })
                    
            return f"Task '{task_title}' not found"
        except Exception as e:
            return f"Error estimating complexity: {str(e)}"

    @mcp.tool()
    async def suggest_next_actions(ctx: Context, project_name: str, task_title: str) -> str:
        """Suggest next actions for a task using AI.
        
        Args:
            project_name: Name of the project
            task_title: Title of the task to get suggestions for
            
        Returns:
            JSON string of suggested actions
        """
        try:
            task_file = manager._get_task_file(project_name)
            
            if not task_file.exists():
                return f"Task file not found for project {project_name}"
                
            with open(task_file, 'r') as f:
                content = f.read()
                
            tasks = manager._parse_markdown_tasks(content)
            
            for task in tasks:
                if task['title'] == task_title:
                    # Use AI to suggest next actions
                    prompt = f"Suggest next actions for this task: {task['description']}"
                    # Here we would use Cursor's AI to suggest actions
                    # For now, we'll use a placeholder
                    suggestions = [
                        "Review existing codebase",
                        "Set up development environment",
                        "Create initial test cases",
                        "Implement core functionality",
                        "Write documentation"
                    ]
                    
                    return json.dumps({
                        'task': task_title,
                        'suggestions': suggestions
                    })
                    
            return f"Task '{task_title}' not found"
        except Exception as e:
            return f"Error suggesting actions: {str(e)}"

    return mcp

def extract_bullet_points(content: str) -> List[str]:
    """Extract bullet points from text content."""
    points = []
    for line in content.split('\n'):
        line = line.strip()
        if line and (line.startswith('-') or line.startswith('*') or line.startswith('•')):
            # Remove bullet point marker and any markdown formatting
            cleaned = re.sub(r'^[-*•]\s*', '', line)
            cleaned = re.sub(r'`[^`]*`', '', cleaned)
            cleaned = re.sub(r'\*\*([^*]*)\*\*', r'\1', cleaned)
            cleaned = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', cleaned)
            if cleaned:
                points.append(cleaned)
    return points

# Create the default MCP instance for backward compatibility
mcp = create_mcp() 