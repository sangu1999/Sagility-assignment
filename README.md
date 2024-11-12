# Calculator API  
A simple calculator API built with FastAPI.  
  
## Table of Contents  
  
1. [Installation](#installation)  
2. [Running the Application](#running-the-application)  
3. [Setting up GitHub Actions CI pipeline](#setting-up-github-actions-ci-pipeline) 
4. [Environment variables and secret management](#environment-variables-and-secret-management)
5. [Configuring ArgoCD for continuous deployment](#configuring-agrocd-for-continious-deployment)
  
## Installation  
  
### Clone the Repository  
  
First, you need to clone the repository to your local machine:  
  
```bash  
git clone https://github.com/sangu1999/Sagility-assignment.git
cd Sagility-assignment
```

## Running the Application
  
### Install the requirements 
  
Install the python package dependencies:  
  
```bash  
pip3 install -r requirements.txt
```

### Start the application
  
After installing the packages you can start the application:

```bash  
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Setting up GitHub Actions CI pipeline

To set up the GitHub Actions CI pipeline, create a `.github/workflows/ci.yaml` file in your repository with the following content:

```yaml
on: [push]  
jobs:  
  build:  
    runs-on: ubuntu-latest  
    steps:  
      - name: Checkout code  
        uses: actions/checkout@v2  
  
      - name: Set up Python  
        uses: actions/setup-python@v2  
        with:  
          python-version: '3.10'  
  
      - name: Install dependencies  
        run: |  
          python -m pip install --upgrade pip  
          pip install -r requirements.txt  
  
      - name: Build application  
        run: |  
          echo "Building the application..."  
  
      - name: Run tests with coverage  
        run: |  
          pip install pytest pytest-cov  
          pytest --cov=app --cov-report=term-missing > coverage_report.txt  
          coverage=$(grep -Po 'TOTAL.*\s+\K[0-9]+(?=%)' coverage_report.txt)  
          echo "Coverage: $coverage%"  
          if (( coverage < 100 )); then  
            echo "Test coverage is less than 100%. Failing the step."  
            exit 1  
          fi    
  
      - name: Lint code  
        run: |  
          pip install pylint  
          pylint **/*.py > pylint_report.txt || true  
          score=$(tail -n 2 pylint_report.txt | grep -Po 'Your code has been rated at \K[0-9.]+')  
          echo "Pylint score: $score"  
          if (( $(echo "$score < 5" | bc -l) )); then  
            echo "Pylint score is less than 5. Failing the step."  
            exit 1  
          fi  
  
      - name: Build Docker image  
        run: |  
          docker build -t simple-calculator:latest .  
  
      - name: Log in to Docker  
        run: |  
          docker login "${{ secrets.DOCKER_SERVER }}" -u "${{ secrets.DOCKER_USERNAME }}" -p "${{ secrets.DOCKER_PASSWORD }}"
  
      - name: Push Docker image  
        run: |  
          docker tag simple-calculator:latest ${{ secrets.DOCKER_SERVER }}/simple-calculator:latest  
          docker push ${{ secrets.DOCKER_SERVER }}/simple-calculator:latest  
  
      - name: Update Kubernetes manifests  
        run: |  
          sed -i 's|image: .*$|image: ${{ secrets.DOCKER_SERVER }}/simple-calculator:latest|' k8s/deployment.yaml  
  
      - name: Commit and push updated manifests  
        run: |  
          git config --global user.name 'github-actions'  
          git config --global user.email 'github-actions@github.com'  
          git add k8s/deployment.yaml  
          git commit -m "Update image to ${{ secrets.DOCKER_SERVER }}/simple-calculator:latest"  
          git push  
  
      - name: Sync Argo CD application  
        env:  
          ARGOCD_SERVER: ${{ secrets.ARGOCD_SERVER }}  
          ARGOCD_USERNAME: ${{ secrets.ARGOCD_USERNAME }}  
          ARGOCD_PASSWORD: ${{ secrets.ARGOCD_PASSWORD }}  
          ARGOCD_APP_NAME: SimpleCalculator 
        run: |  
          if ! command -v argocd &> /dev/null; then  
            curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/download/v2.0.4/argocd-linux-amd64  
            chmod +x /usr/local/bin/argocd  
          fi  
          argocd login $ARGOCD_SERVER --username $ARGOCD_USERNAME --password $ARGOCD_PASSWORD --insecure  
          argocd app sync $ARGOCD_APP_NAME
```

This pipeline will automatically run tests, lint code, build a Docker image, and deploy it to a Kubernetes cluster using Argo CD.

## Environment variables and secret management

To manage environment variables and secrets in GitHub Actions, follow these steps:

1. Go to your repository on GitHub.
2. Click on `Settings`.
3. In the left sidebar, click on `Secrets and variables` and then `Actions`.
4. Click on the `New repository secret` button and add the following secrets:
   - `DOCKER_SERVER`: Your Docker server URL.
   - `DOCKER_USERNAME`: Your Docker username.
   - `DOCKER_PASSWORD`: Your Docker password.
   - `ARGOCD_SERVER`: Your Argo CD server URL.
   - `ARGOCD_USERNAME`: Your Argo CD username.
   - `ARGOCD_PASSWORD`: Your Argo CD password.

These secrets will be used in the GitHub Actions pipeline to authenticate and perform necessary operations.


## Configuring ArgoCD for continuous deployment

This document assumes that the cluster is installed with Argo CD and it's configured on the cluster that the application has to be deployed. If not, follow [this documentation](https://argo-cd.readthedocs.io/en/stable/getting_started/) to install and set up.

once configured run the following command to register the application into agro CD

```bash  
argocd app create simple-calculator --repo https://github.com/sangu1999/Sagility-assignment.git --path k8s --dest-server https://kubernetes.default.svc --dest-namespace default
```

This deployes the simple calculator fast API into you registered cluster in the default namespace domain
