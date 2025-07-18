flowchart TD
    A[시작] --> B[사용자 입력 받기]
    B --> C{입력값이 비어있는가?}
    C -->|Yes| D[Invalid input 출력]
    C -->|No| E[문자열을 공백으로 분리]
    E --> F[각 부분을 숫자로 변환]
    F --> G{숫자 변환 성공?}
    G -->|No| D
    G -->|Yes| H[find_min_max 함수 호출]
    H --> I[첫 번째 숫자를 min, max로 설정]
    I --> J[모든 숫자와 비교]
    J --> K{i < min?}
    K -->|Yes| L[min 업데이트]
    K -->|No| M{i > max?}
    L --> M
    M -->|Yes| N[max 업데이트]
    M -->|No| O{더 비교할 숫자가 있는가?}
    N --> O
    O -->|Yes| J
    O -->|No| P[Min: min, Max: max 출력]
    D --> Q[종료]
    P --> Q