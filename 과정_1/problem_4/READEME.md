# 1.기초 git 환경 구축

Git 버전 확인
```bash
git --version 
```

출력결과

```bash 
git version 2.34.1
```

#  전역 설정 
> 모든 Git 프로젝트에 적용되며, 로컬 설정은 특정 프로젝트에만 영향을 준다. 같은 설정이 존재할 경우, 로컬 설정이 전역 설정을 덮어쓴다.
## 전역 설정 목록 확인 
```
git config --global --list
```

##  개행문자

### 개행문자 설정 

>개행문자: Enter 키를 눌렀을 떄 다음 줄로 넘어가는 것을 컴퓨터로 표현하는 방식 
```
git config --global core.autocrlf input
```
### 개행문자 설정 확인 
```
git config --global core.autocrlf
```

##  에디터
### 기본 에디터를 VS Code로 변경 
>  `--wait` 플래그의 기능 :
파일이 완전히 닫힐 때까지 터미널 프로세스가 대기  
*  VS Code 열림, 터미널 즉시 프롬프트 복귀
*  VS Code 열림, 터미널은 대기 상태 (VS Code 닫을 때까지)

```
git config --global core.editor "code --wait"
``` 

### 기본 에디터를 vim로 변경 
```
git config --global core.editor vim 
```
### 에디터 설정 확인
```
git config --global core.editor
```

