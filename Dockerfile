FROM python:3.9-slim-buster

ARG GITHUB_TOKEN

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    curl \
    gnupg \
    libicu-dev && \
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | tee /usr/share/keyrings/githubcli-archive-keyring.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee -a /etc/apt/sources.list.d/github-cli.list && \
    apt-get update && \
    apt-get install gh -y && \
    rm -rf /var/lib/apt/lists/* && \
    # Add Docker's official repository
    apt-get update && \
    apt-get install -y apt-transport-https ca-certificates lsb-release && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian buster stable" | tee /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y docker-ce docker-ce-cli containerd.io # Install Docker

COPY actions-script.py /app/actions-script.py

RUN pip install --upgrade pip
RUN pip install requests PyGithub python-gitlab python-dotenv

# Install the actions-importer extension
RUN GH_TOKEN=$GITHUB_TOKEN gh extension install github/gh-actions-importer
