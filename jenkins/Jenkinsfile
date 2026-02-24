pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Build') {
      steps {
        sh 'docker build -t health-api:local ./app'
      }
    }
    stage('Test') {
      steps {
        sh 'docker run --rm health-api:local python -m pytest -q'
      }
      post {
        always { junit 'pytest.xml' }
      }
    }
    stage('Security basics') {
      steps {
        sh 'echo "Placeholder: validate dependencies (offline)"'
      }
    }
    stage('Deploy') {
      steps {
        sh 'docker compose up -d app'
      }
    }
  }
}