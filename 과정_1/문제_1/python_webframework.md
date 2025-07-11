# Python 웹프레임워크 3가지

## 1. Flask
**마이크로 프레임워크**
- 최소한의 기능으로 시작하여 필요에 따라 확장
- 작은 프로젝트나 프로토타입에 적합
- 높은 유연성과 커스터마이징 자유도

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Flask!"
```

## 2. Django
**풀스택 프레임워크**
- 웹 개발에 필요한 모든 기능을 기본 제공
- ORM, 관리자 패널, 인증 시스템 내장
- 대규모 웹 애플리케이션에 적합

```python
# views.py
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello, Django!")
```

## 3. FastAPI
**모던 API 프레임워크**
- 매우 빠른 성능 (Node.js, Go 수준)
- 자동 API 문서 생성 (OpenAPI/Swagger)
- 타입 힌트 기반 자동 검증

```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def hello():
    return {"message": "Hello, FastAPI!"}
```

## 비교표

| 특성 | Flask | Django | FastAPI |
|------|-------|--------|---------|
| **타입** | 마이크로 | 풀스택 | API 중심 |
| **학습 난이도** | 쉬움 | 어려움 | 중간 |
| **성능** | 보통 | 보통 | 높음 |
| **적합한 규모** | 소-중 | 대 | 소-중-대 |
| **개발 속도** | 빠름 | 느림 | 매우 빠름 |
| **내장 기능** | 최소 | 풍부 | API 특화 |
| **API 개발** | 보통 | 좋음 | 최고 |
| **문서화** | 수동 | 수동 | 자동 |

## 선택 가이드
- **Flask**: 간단한 웹앱, 프로토타입, 학습용
- **Django**: 대규모 웹사이트, 관리자 기능 필요
- **FastAPI**: REST API, 마이크로서비스, 고성능 필요
