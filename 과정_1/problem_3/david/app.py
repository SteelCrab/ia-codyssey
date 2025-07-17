from flask import Flask, request, Response
import os
from io import BytesIO
from gtts import gTTS

# 기본 언어 설정 (환경변수 또는 한국어)
DEFAULT_LANG = os.getenv('DEFAULT_LANG', 'ko')

# Flask 웹 애플리케이션 생성
app = Flask(__name__)

# 메인 페이지 라우트 설정
@app.route("/")
def home():
    # 음성으로 변환할 텍스트
    text = "Hello, DevOps"

    # URL 파라미터에서 언어 가져오기 (예: ?lang=en)
    lang = request.args.get('lang', DEFAULT_LANG)
    
    # 메모리 버퍼 생성
    fp = BytesIO()
    
    # gTTS로 텍스트를 음성 파일로 변환
    gTTS(text, "com", lang).write_to_fp(fp)

    # 음성 파일을 브라우저로 직접 전송 (자동 재생)
    return Response(fp.getvalue(), mimetype='audio/mpeg')

# 웹서버 실행 (모든 IP에서 접근 가능, 80번 포트)
if __name__ == '__main__':
    app.run('0.0.0.0', 80)
