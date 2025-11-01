#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os

def run_tests(selenoid_url, app_url, browser, browser_version, threads):
    """Запуск тестов с переданными параметрами"""
    
    # Установка переменных окружения
    env = os.environ.copy()
    env['SELENOID_URL'] = selenoid_url
    env['APP_URL'] = app_url
    env['BROWSER'] = browser
    env['BROWSER_VERSION'] = browser_version
    
    # Формирование команды pytest
    cmd = [
        'pytest',
        f'--numprocesses={threads}',
        '--alluredir=reports/allure-results',
        '--tb=short',
        '-v',
        'src/tests/'
    ]
    
    print(f"Running tests with command: {' '.join(cmd)}")
    print(f"Environment: SELENOID_URL={selenoid_url}, APP_URL={app_url}, "
          f"BROWSER={browser}, BROWSER_VERSION={browser_version}")
    
    # Запуск тестов
    result = subprocess.run(cmd, env=env)
    return result.returncode

def main():
    parser = argparse.ArgumentParser(description='Run OpenCart tests')
    parser.add_argument('--selenoid-url', required=True, help='Selenoid executor URL')
    parser.add_argument('--app-url', required=True, help='OpenCart application URL')
    parser.add_argument('--browser', default='chrome', help='Browser for testing')
    parser.add_argument('--browser-version', default='latest', help='Browser version')
    parser.add_argument('--threads', default='2', help='Number of parallel threads')
    
    args = parser.parse_args()
    
    exit_code = run_tests(
        args.selenoid_url,
        args.app_url,
        args.browser,
        args.browser_version,
        args.threads
    )
    
    sys.exit(exit_code)

if __name__ == '__main__':
    main()