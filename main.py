import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--logger_path', type=str, help='실행 로그 저장 위치 지정')

    args = parser.parse_args()

    logger_path = ''
