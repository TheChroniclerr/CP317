# Configurations

## System archetecture
Frontend - React\
Backend - Python 

## Requirements
Docker

# Initialization Commands 

## Configure React-Vite client
```powershell
cd client
npm install
```

## Run Vite client
```powershell
cd client
npm run dev
```

## Configure Python-Flask server
```powershell
cd server
docker pull thechronicler/cp317_docker:latest
```

## Run Flask server
```powershell
cd server
docker run -v <your-project-dir>\CP317\server\src:/app/src -p 8080:8080 thechronicler/cp317_docker:latest
```

# Build Commands

## Update requirements.txt & requirement_readonly.txt
```powershell
cd server
pip install pipreqs
pipreqs ./src
```

```powershell
cd server
pip freeze > requirements.txt
```

## Rebuild docker image
```powershell
cd server
docker login
docker build -t <username>/cp317_docker .
```

## Push docker image to DockerHub
```powershell
cd server
docker login
docker push <username>/cp317_docker:latest
```