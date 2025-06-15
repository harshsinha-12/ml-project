# Student Performance Predictor - End to End ML Project

This project uses machine learning to predict a student's math score based on various attributes including gender, race/ethnicity, parental education level, lunch type, test preparation course, reading score, and writing score.

## Features

- Flask web application for predictions
- Streamlit interactive dashboard
- ML pipeline with data preprocessing and model training
- Docker support for easy deployment

## Getting Started

### Prerequisites

- Python 3.9+
- pip
- Docker (optional, for containerized deployment)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ML Project
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Applications Locally

#### Flask Web App
```bash
python application.py
```
Access the web interface at http://localhost:5001

#### Streamlit Dashboard
```bash
streamlit run streamlitapp.py
```
The Streamlit app should open automatically in your browser.

### Docker Deployment

#### Using Docker Compose (Recommended)

To start both Flask and Streamlit apps:
```bash
docker-compose up
```

Access:
- Flask app: http://localhost:5001
- Streamlit app: http://localhost:8501

To run in the background:
```bash
docker-compose up -d
```

To stop the services:
```bash
docker-compose down
```

#### Using Individual Dockerfiles

For Flask app only:
```bash
docker build -t student-performance-flask .
docker run -p 5001:5001 student-performance-flask
```

For Streamlit app only:
```bash
docker build -t student-performance-streamlit -f Dockerfile.streamlit .
docker run -p 8501:8501 student-performance-streamlit
```

#### Using Your Docker Hub Images

Once published, others can use your images with:
```bash
# Pull images
docker pull harshsinha12/student-performance-flask:latest
docker pull harshsinha12/student-performance-streamlit:latest

# Run containers
docker run -p 5001:5001 harshsinha12/student-performance-flask:latest
docker run -p 8501:8501 harshsinha12/student-performance-streamlit:latest
```

#### Automating Builds with GitHub Actions

To automatically build and push Docker images when you push to GitHub:

1. Create `.github/workflows/docker-build.yml`:
```yaml
name: Build and Push Docker images

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push Flask app
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ secrets.DOCKERHUB_USERNAME }}/student-performance-flask:latest

      - name: Build and push Streamlit app
        uses: docker/build-push-action@v4
        with:
          context: .
          file: ./Dockerfile.streamlit
          push: true
          tags: ${{ secrets.DOCKERHUB_USERNAME }}/student-performance-streamlit:latest
```

2. Add repository secrets in GitHub:
   - `DOCKERHUB_USERNAME`: Your Docker Hub username
   - `DOCKERHUB_TOKEN`: Your Docker Hub access token (create in Docker Hub account settings)

### Deploying Docker Images to Cloud Platforms

Once your images are published on Docker Hub, you can easily deploy them to various cloud platforms:

#### AWS Elastic Beanstalk

1. Create a `Dockerrun.aws.json` file:
```json
{
  "AWSEBDockerrunVersion": 2,
  "containerDefinitions": [
    {
      "name": "flask-app",
      "image": "yourusername/student-performance-flask:latest",
      "essential": true,
      "memory": 512,
      "portMappings": [
        {
          "hostPort": 80,
          "containerPort": 5001
        }
      ]
    },
    {
      "name": "streamlit-app",
      "image": "yourusername/student-performance-streamlit:latest",
      "essential": false,
      "memory": 512,
      "portMappings": [
        {
          "hostPort": 8501,
          "containerPort": 8501
        }
      ]
    }
  ]
}
```

2. Deploy to Elastic Beanstalk using the AWS Management Console or AWS CLI

#### Google Cloud Run

```bash
# Deploy Flask app
gcloud run deploy student-performance-flask \
  --image docker.io/yourusername/student-performance-flask:latest \
  --platform managed \
  --port 5001

# Deploy Streamlit app
gcloud run deploy student-performance-streamlit \
  --image docker.io/yourusername/student-performance-streamlit:latest \
  --platform managed \
  --port 8501
```

#### Microsoft Azure Container Instances

```bash
# Create a resource group
az group create --name student-performance-group --location eastus

# Deploy Flask app
az container create \
  --resource-group student-performance-group \
  --name flask-app \
  --image yourusername/student-performance-flask:latest \
  --dns-name-label student-flask-app \
  --ports 5001

# Deploy Streamlit app
az container create \
  --resource-group student-performance-group \
  --name streamlit-app \
  --image yourusername/student-performance-streamlit:latest \
  --dns-name-label student-streamlit-app \
  --ports 8501
```

#### DigitalOcean App Platform

1. Go to DigitalOcean App Platform
2. Create a new app
3. Select "Docker Hub" as the source
4. Enter your Docker Hub image name (e.g., `yourusername/student-performance-flask:latest`)
5. Configure the port mappings and resources
6. Deploy the app

## Project Structure

```
ML Project/
├─ artifacts/ - Model artifacts
├─ src/ - Source code
│  ├─ components/ - ML pipeline components
│  ├─ pipeline/ - Training and prediction pipelines
├─ templates/ - Flask HTML templates
├─ application.py - Flask application
├─ streamlitapp.py - Streamlit dashboard
├─ Dockerfile - Docker configuration for Flask app
├─ Dockerfile.streamlit - Docker configuration for Streamlit app
├─ docker-compose.yml - Docker Compose configuration
```

## Model Information

The model is trained on a dataset of student performance metrics and includes:

1. Data Preprocessing: Handling categorical variables and scaling numerical features
2. Model Training: Using various regression algorithms
3. Model Selection: Selecting the best performing model based on evaluation metrics
