# 선택 정렬 : 
# 주어진 리스트에서 최솟값을 찾아서 맨 앞의 값과 
# 교환하는 방식으로 정렬을 수행합니다.
def selection_sort(arr):
    for i in range(len(arr)):
        # 최솟값 찾기 
        min_i = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_i]:
                min_i = j
        # 값 교환 (스왑)
        arr[i], arr[min_i] = arr[min_i], arr[i]
    return arr

def main():
    try:
        # 문자열로 입력받기
        user_input = input("공백으로 구분된 숫자 입력: ")
        
        # 입력이 비어있는지 확인
        if not user_input.strip():
            print("Invalid input.")
            return
        
        # 문자열을 공백으로 분리하여 리스트로 변환
        input_list = user_input.strip().split()
        
        # 각 요소를 실수로 변환
        numbers = [float(i) for i in input_list]
        
        print("정렬 전:", numbers)
        print("정렬 후:", selection_sort(numbers))
        
    except ValueError:
        print("Invalid input.")
    except Exception:
        print("Invalid input.")

if __name__ == "__main__":
    main()