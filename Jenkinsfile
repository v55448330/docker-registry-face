pipeline {
  agent any
  stages {
    stage('') {
      steps {
        parallel(
          "testa": {
            dir ('master') {
              checkout([
                $class: 'GitSCM', branches: [[name: '*/master']],
                doGenerateSubmoduleConfigurations: false,
                extensions: [],
                submoduleCfg: [],
                userRemoteConfigs: [[url: 'https://github.com/v55448330/docker-registry-face.git']]])
            }

            dir ('test') {
              checkout([
                $class: 'GitSCM', branches: [[name: '*/test']],
                doGenerateSubmoduleConfigurations: false,
                extensions: [],
                submoduleCfg: [],
                userRemoteConfigs: [[url: 'https://github.com/v55448330/docker-registry-face.git']]])
            }

          }
        )
      }
    }
  }
}
