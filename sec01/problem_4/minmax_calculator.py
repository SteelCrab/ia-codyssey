# 숫자 리스트에서 최소값과 최대값을 찾는 함수
def find_min_max(numbers):
    # 첫 번째 숫자를 초기값으로 설정
    min = numbers[0]
    max = numbers[0]
    
    # 모든 숫자를 하나씩 비교
    for i in numbers:
        # 현재 숫자가 최소값보다 작으면 최소값
        if i < min:
            min = i
        # 현재 숫자가 최대값보다 크면 최대값
        if i > max:
            max = i

    return min, max

# 메인 실행 함수
def main():
    # 사용자로부터 공백으로 구분된 숫자들 입력받기
    user_input = input("숫자들을 공백으로 구분해서 입력하세요: ")
    
    # 공백으로 문자열 분리
    # split() : 문자열을 공백 기준으로 분리하여 리스트로 반환
    input_parts = user_input.split()
    
    # 입력값이 없으면 잘못된 입력 처리
    # if not input_parts : input_parts가 비어있으면 True
    if not input_parts:
        print("Invalid input.")
        return
    
    # 문자열을 숫자로 변환
    numbers = []
    for part in input_parts:
        try:
            # float()로 숫자 변환
            
            number = float(part)
            numbers.append(number)
        except ValueError:
            # 숫자가 아닌 값이 입력된 경우
            print("Invalid input.")
            return
    
    # 최소값과 최대값 계산
    min, max = find_min_max(numbers)
    
    # 요구사항에 맞는 출력 형식
    print(f"Min: {min}, Max: {max}")

# 메인 실행 블록
if __name__ == "__main__":
    main()