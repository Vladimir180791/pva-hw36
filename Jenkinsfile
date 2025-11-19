pipeline {
    agent any
    
    parameters {
        string(name: 'SELENOID_URL', defaultValue: 'http://localhost:4444/wd/hub', description: 'Selenoid executor URL')
        string(name: 'APP_URL', defaultValue: 'http://opencart:8080', description: 'OpenCart application URL')
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Browser for testing')
        choice(name: 'BROWSER_VERSION', choices: ['latest', '100.0', '99.0'], description: 'Browser version')
        string(name: 'THREADS', defaultValue: '2', description: 'Number of parallel threads')
    }
    
    environment {
        PYTHONPATH = "${WORKSPACE}"
        ALLURE_RESULTS = "${WORKSPACE}/reports/allure-results"
        ALLURE_REPORT = "${WORKSPACE}/reports/allure-report"
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Vladimir180791/pva-hw36.git'
            }
        }
        
        stage('Setup Environment') {
            steps {
                sh '''
                    python -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    withEnv(["PATH+VENV=${WORKSPACE}/venv/bin"]) {
                        sh """
                            . venv/bin/activate
                            python run_tests.py \
                                --selenoid-url ${params.SELENOID_URL} \
                                --app-url ${params.APP_URL} \
                                --browser ${params.BROWSER} \
                                --browser-version ${params.BROWSER_VERSION} \
                                --threads ${params.THREADS}
                        """
                    }
                }
            }
        }
        
        stage('Generate Allure Report') {
            steps {
                sh '''
                    . venv/bin/activate
                    allure generate --clean $ALLURE_RESULTS -o $ALLURE_REPORT
                '''
            }
        }
    }
    
    post {
        always {
            allure includeProperties: false,
                jdk: '',
                results: [[path: 'reports/allure-results']]
            
            cleanWs()
        }
        success {
            emailext (
                subject: "SUCCESS: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: "Test execution completed successfully. Allure report: ${env.BUILD_URL}allure/",
                to: "pigal1807@yandex.ru"
            )
        }
        failure {
            emailext (
                subject: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: "Test execution failed. Check console output: ${env.BUILD_URL}console",
                to: "pigal1807@yandex.ru"
            )
        }
    }
}