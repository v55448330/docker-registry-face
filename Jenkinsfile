pipeline {
  agent any
  stages {
    stage('') {
      steps {
        parallel(
          "testa": {
            sh 'echo "test"'

          },
          "testb": {
            sleep 10

          }
        )
      }
    }
  }
}
