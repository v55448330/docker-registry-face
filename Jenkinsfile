pipeline {
  agent any
  stages {
    stage('') {
      steps {
        parallel(
          "testa": {
            checkout scm
            echo "current branch: $BRANCH_NAME"
          }
        )
      }
    }
  }
}
