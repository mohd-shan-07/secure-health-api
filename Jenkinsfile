pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Build') {
      steps {
        bat 'docker build -t health-api:local ./app'
      }
    }
    stage('Test') {
      steps {
        bat 'docker run --rm -v \"%cd%:/app\" health-api:local python -m pytest --junitxml=/app/pytest.xml -q'
      }
      post {
        always { junit 'pytest.xml' }
      }
    }
    stage('Security basics') {
      steps {
        bat 'echo "Placeholder: validate dependencies (offline)"'
      }
    }
    stage('Deploy') {
      steps {
        bat 'docker compose up -d app'
      }
    }
  }
}