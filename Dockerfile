# 1단계: 베이스 이미지 선택 (앤서블의 'python3-pip' 역할)
# 파이썬 3.9가 설치된 가벼운 리눅스(slim) 이미지를 사용합니다.
FROM python:3.9-slim

# 2단계: 환경변수 설정 (파이썬 버퍼링 방지 등)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3단계: 시스템 패키지 설치 (앤서블의 'apt' 역할 - LibreOffice, 폰트)
# 한글 폰트(fonts-nanum)가 없으면 PDF의 한글이 깨집니다. 
# 설치 후 apt 캐시를 지워 이미지 용량을 줄입니다.
RUN apt-get update && apt-get install -y \
    libreoffice-writer \
    libreoffice-java-common \
    fonts-nanum \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 4단계: 작업 디렉토리 생성 (앤서블의 'file' 역할)
WORKDIR /app

# 5단계: 파이썬 라이브러리 설치 (앤서블의 'pip' 역할)
# 요구사항 파일을 먼저 복사해서 레이어 캐시를 활용합니다.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6단계: 소스 코드 복사
COPY . .

# 7단계: 임시 저장소 폴더 권한 설정 (컨테이너 내부용)
RUN mkdir -p temp_storage && chmod 777 temp_storage

# 8단계: 컨테이너 실행 명령어 (Uvicorn으로 FastAPI 가동)
# K3s 파드로 띄울 때 외부 접속을 위해 0.0.0.0으로 엽니다.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
