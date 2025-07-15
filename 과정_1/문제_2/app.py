#Flask class 가져옴
from flask import Flask

# Flask 애플리케이션 생성(인스턴스)
app = Flask(__name__)

#라우트 데코레이터 :  URL 경로 "/" 요청 처리
# 브라우저에서 http://localhost:8080/ 접속 시 아래 함수가 실행됨
@app.route('/')
def hello_world():
    return 'Hello, DevOps!'

if __name__ == '__main__':
    # Flask 웹 서버 시작
    # host="0.0.0.0": 모든 네트워크 인터페이스에서 접속 허용
    # port=8080: 8080 포트에서 서버 실행
    app.run(host="0.0.0.0", port=8080)
    #실행중 출력 
    print("Flask server is running on http://localhost:8080/")

