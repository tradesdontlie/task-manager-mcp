FROM python:3.12-slim

ARG PORT=8050

WORKDIR /app

# Install system dependencies and PyYAML
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-yaml \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy the application
COPY . .

# Install dependencies
RUN pip install PyYAML
RUN uv pip install --system -e .

EXPOSE ${PORT}

ENV PYTHONUNBUFFERED=1

# Command to run the MCP server
CMD ["python", "src/main.py"]