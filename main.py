# main.py
import os
import uuid
import shutil
import logging
import subprocess
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse

from templates import HTML_CONTENT
from converter import process_conversion

# --- [1. 로그 및 환경 설정] ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SixSense-Converter")

app = FastAPI(title="SixSense Doc-Converter")

# [수정] 컨테이너 내부 절대 경로로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp_storage")
os.makedirs(TEMP_DIR, exist_ok=True)

# --- [2. 로컬 파일 정리 함수] ---
def cleanup_local_files(*filepaths: str):
    for path in filepaths:
        try:
            if os.path.exists(path):
                os.remove(path)
                logger.info(f"Cleanup: Local file removed at {path}")
        except Exception as e:
            logger.error(f"Cleanup Error for {path}: {str(e)}")

# 1. 루트 경로
@app.get("/", response_class=HTMLResponse)
async def read_root():
    logger.info("Root page accessed")
    return HTML_CONTENT

# 2. 헬스 체크
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 3. 변환 경로
@app.post("/convert-to-pdf/")
async def convert_any_to_pdf(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    # 파일 용량 제한 체크 (100MB)
    MAX_SIZE = 100 * 1024 * 1024
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > MAX_SIZE:
        logger.warning(f"File size limit exceeded: {file.filename} ({file_size} bytes)")
        raise HTTPException(status_code=413, detail="파일이 너무 큽니다. 최대 100MB까지 가능합니다.")

    file_id = str(uuid.uuid4())
    ext = file.filename.split(".")[-1].lower()

    # [수정] 입력/출력 경로를 모두 절대 경로로 확정
    input_path = os.path.join(TEMP_DIR, f"{file_id}.{ext}")
    output_path = os.path.join(TEMP_DIR, f"{file_id}.pdf")

    logger.info(f"Starting conversion: {file.filename} (ID: {file_id})")

    # [수정] 파일 저장 시 디스크 쓰기 완료 보장
    try:
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            buffer.flush()
            os.fsync(buffer.fileno()) # 물리적 저장 확인
    except Exception as e:
        logger.error(f"File save error: {str(e)}")
        raise HTTPException(status_code=500, detail="서버에 파일을 저장하지 못했습니다.")

    try:
        # [수정] 변환 함수 호출 (절대 경로 전달)
        process_conversion(input_path, output_path, ext, TEMP_DIR)
        
        # 변환 결과 확인
        if not os.path.exists(output_path):
            raise FileNotFoundError(f"PDF generation failed: {output_path} not found")

        logger.info(f"Successfully converted: {file.filename}")

        # [수정] 파일 응답 및 전송 후 삭제 로직
        # 1. 입력 원본 파일은 즉시 삭제 예약
        background_tasks.add_task(cleanup_local_files, input_path)
        
        # 2. 출력 PDF 파일은 클라이언트가 다운로드를 마친 후에 삭제하도록 설정
        response = FileResponse(
            output_path,
            media_type="application/pdf",
            filename=f"converted_{file.filename.rsplit('.', 1)[0]}.pdf"
        )
        
        # FileResponse의 background 기능을 사용하여 전송 완료 후 삭제 실행
        response.background = BackgroundTasks()
        response.background.add_task(cleanup_local_files, output_path)

        return response

    except Exception as e:
        logger.error(f"Conversion failed for {file.filename}: {str(e)}")
        # 에러 발생 시 생성된 파일들 정리
        cleanup_local_files(input_path, output_path)
        raise HTTPException(status_code=500, detail=f"변환 실패: {str(e)}")
