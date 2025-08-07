# priority_calculator.py
# 사칙연산 우선순위를 고려한 계산기 (괄호 지원)

# 기존 calculator.py의 연산 함수들 재사용
def add(a, b):
    # 덧셈 연산
    return a + b

def subtract(a, b):
    # 뺄셈 연산
    return a - b

def multiply(a, b):
    # 곱셈 연산
    return a * b

def divide(a, b):
    # 나눗셈 연산
    if b == 0:
        raise ZeroDivisionError("Division by zero")
    return a / b

def is_number(token):
    # 토큰이 숫자인지 확인
    try:
        float(token)
        return True
    except ValueError:
        return False

def tokenize(expression):
    # 표현식을 토큰으로 분리 (괄호 포함)
    tokens = []
    current_token = ""
    
    for char in expression:
        # 공백은 토큰 구분자로 사용
        if char == ' ':
            if current_token:
                tokens.append(current_token)
                current_token = ""
        # 숫자나 소수점은 하나의 토큰으로 묶음
        elif char in '()+-*/':
            if current_token:
                tokens.append(current_token)
                current_token = ""
            tokens.append(char)
        else:
            current_token += char
    
    if current_token:
        tokens.append(current_token)
    
    return tokens

def infix_to_postfix(tokens):
    # 중위 표기법을 후위 표기법으로 변환 
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    stack = []
    postfix = []
    
    for token in tokens:
        if is_number(token):
            postfix.append(float(token))
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            if stack and stack[-1] == '(':
                stack.pop()  # '(' 제거
            else:
                raise ValueError("Mismatched parentheses")
        elif token in precedence:
            while (stack and stack[-1] != '(' and 
                   stack[-1] in precedence and
                   precedence[stack[-1]] >= precedence[token]):
                postfix.append(stack.pop())
            stack.append(token)
        else:
            raise ValueError("Invalid token")
    
    while stack:
        if stack[-1] in '()':
            raise ValueError("Mismatched parentheses")
        postfix.append(stack.pop())
    
    return postfix

def evaluate_postfix(postfix):
    # 후위 표기법으로 표현된 식을 계산
    stack = []
    
    for token in postfix:
        if isinstance(token, float):  # 숫자인 경우
            stack.append(token)
        else:  # 연산자인 경우
            if len(stack) < 2:
                raise ValueError("Invalid expression")
            
            b = stack.pop()
            a = stack.pop()
            
            if token == '+':
                result = add(a, b)
            elif token == '-':
                result = subtract(a, b)
            elif token == '*':
                result = multiply(a, b)
            elif token == '/':
                result = divide(a, b)
            else:
                raise ValueError("Invalid operator")
            
            stack.append(result)
    
    if len(stack) != 1:
        raise ValueError("Invalid expression")
    
    return stack[0]

def evaluate_simple_expression(tokens):
    # 괄호 없는 간단한 표현식 계산 (기본 우선순위만)
    # 숫자와 연산자를 분리
    numbers = []
    operators = []
    
    # 토큰 파싱
    for i, token in enumerate(tokens):
        if i % 2 == 0:  # 짝수 인덱스는 숫자
            try:
                numbers.append(float(token))
            except ValueError:
                raise ValueError("Invalid number format")
        else:  # 홀수 인덱스는 연산자
            if token not in ['+', '-', '*', '/']:
                raise ValueError("Invalid operator")
            operators.append(token)
    
    # 연산자와 숫자 개수 검증
    if len(numbers) != len(operators) + 1:
        raise ValueError("Invalid expression format")
    
    # 1단계: 곱셈과 나눗셈 먼저 처리
    i = 0
    while i < len(operators):
        if operators[i] in ['*', '/']:
            if operators[i] == '*':
                result = multiply(numbers[i], numbers[i + 1])
            else:  # '/'
                result = divide(numbers[i], numbers[i + 1])
            
            # 결과로 대체
            numbers[i] = result
            numbers.pop(i + 1)
            operators.pop(i)
        else:
            i += 1
    
    # 2단계: 덧셈과 뺄셈 처리
    i = 0
    while i < len(operators):
        if operators[i] == '+':
            result = add(numbers[i], numbers[i + 1])
        else:  # '-'
            result = subtract(numbers[i], numbers[i + 1])
        
        # 결과로 대체
        numbers[i] = result
        numbers.pop(i + 1)
        operators.pop(i)
    
    return numbers[0]

def evaluate_expression(expression):
    # 표현식을 계산 (괄호 지원)
    tokens = tokenize(expression)
    
    # 괄호가 있는지 확인
    has_parentheses = '(' in tokens or ')' in tokens
    
    if has_parentheses:
        # 괄호가 있으면 후위 표기법 사용
        postfix = infix_to_postfix(tokens)
        return evaluate_postfix(postfix)
    else:
        # 괄호가 없으면 간단한 방법 사용
        return evaluate_simple_expression(tokens)

def main():
    try:
        expression = input()
        
        if not expression.strip():
            print("Invalid input.")
            return
        
        result = evaluate_expression(expression)
        print(f"Result: {result}")
        
    except ZeroDivisionError:
        print("Error: Division by zero.")
    except (ValueError, IndexError):
        print("Invalid input.")
    except Exception:
        print("Invalid input.")

if __name__ == "__main__":
    main()