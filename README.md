# 이때까지 DJANGO 순서

1. 가상환경 

```bash
# 가상환경 만들기
$ python -m venv venv

# 가상환경 적용
$ source venv/Scripts/activate

# 패키지 다운
$ pip install django

# 패키지 저장
$ pip freeze > requiremenets.txt
```

2. 버전 관리
- .gitignore 파일 생성
  
    git으로 관리하지 않을 때의 파일 목록을 작성해서 관리

```bash
# git 파일 생성
$ git init
```