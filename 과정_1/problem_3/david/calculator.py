
# 덧셈 함수
def add(a, b):
    return a + b

# 뺄셈 함수 
def subtract(a, b):
    return a - b

# 곱셈 함수
def multiply(a, b):
    return a * b

# 나눗셈 함수 - 0으로 나누기 방지
def divide(a, b):
    if b == 0:
        return "오류: 0으로 나눌 수 없습니다."
    return a / b

# 문자열 수식 계산 함수 (보너스 과제)
def parse_expression(expression):
    # 공백으로 문자열 분리
    parts = expression.split()
    
    # 입력 형식 검사 (숫자 연산자 숫자)
    if len(parts) != 3:
        return "오류: 잘못된 형식입니다"
    
    # 첫 번째 숫자, 연산자, 두 번째 숫자 추출
    num1 = float(parts[0])  # 첫 번째 숫자
    operator = parts[1]     # 연산자
    num2 = float(parts[2])  # 두 번째 숫자
    
    # 연산자별 계산 수행
    if operator == '+':
        return add(num1, num2)
    elif operator == '-':
        return subtract(num1, num2)
    elif operator == '*':
        return multiply(num1, num2)
    elif operator == '/':
        return divide(num1, num2)
    else:
        return "오류: 잘못된 연산자입니다."

# 기본 계산기 모드 - 숫자와 연산자를 순서대로 입력
def basic_calculator():
    print("=== 기본 계산기 ===")
    
    # 사용자로부터 숫자와 연산자 입력받기
    num1 = float(input("첫 번째 숫자: "))
    operator = input("연산자 (+, -, *, /): ")
    num2 = float(input("두 번째 숫자: "))
    
    # 입력받은 연산자에 따라 계산 수행
    if operator == '+':
        result = add(num1, num2)
    elif operator == '-':
        result = subtract(num1, num2)
    elif operator == '*':
        result = multiply(num1, num2)
    elif operator == '/':
        result = divide(num1, num2)
    else:
        result = "오류: 잘못된 연산자입니다."
    
    # 계산 결과 출력
    print(f"결과: {result}")

# 수식 입력 계산기 모드 (보너스) - 한 줄로 수식 입력
def expression_calculator():
    
    # 수식을 한 줄로 입력받기
    expression = input("수식 입력: ")
    # 수식 파싱 및 계산
    result = parse_expression(expression)
    # 결과 출력
    print(f"결과: {result}")

# 메인 실행 부분
if __name__ == "__main__":
    # 프로그램 시작 메시지
    print("반달곰 커피 계산기")
    print("1. 기본 계산기")
    print("2. 수식 입력 계산기")
    
    # 사용자 모드 선택
    mode = input("모드 선택 (1 또는 2): ")
    
    # 선택한 모드에 따라 해당 함수 실행
    if mode == "1":
        basic_calculator()
    elif mode == "2":
        expression_calculator()
    else:
        print("잘못된 선택입니다.")