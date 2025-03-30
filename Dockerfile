# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install Git, GitHub CLI (gh), and other required tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    curl \
    gnupg && \
    # Install GitHub CLI
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | tee /usr/share/keyrings/githubcli-archive-keyring.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list && \
    apt-get update && \
    apt-get install gh -y && \
    rm -rf /var/lib/apt/lists/*

# Copy the Python script and any other necessary files
COPY actions-script.py /app/actions-script.py

# Install any dependencies (if needed)
RUN pip install --upgrade pip
RUN pip install requests PyGithub python-gitlab python-dotenv

# Command to run the script (optional, if you want to run the script by default)
CMD ["python", "actions-script.py"]
