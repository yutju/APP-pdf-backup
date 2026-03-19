# main.py
import os
import uuid
import shutil
import logging  # 로그 모듈 추가
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse

from templates import HTML_CONTENT
from converter import process_conversion

# --- [1. 로그 설정] ---
# 로그를 파일(app.log)과 콘솔(Terminal) 모두에 남기도록 설정합니다.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log", encoding='utf-8'), # 파일에 저장
        logging.StreamHandler() # 터미널에 출력
    ]
)
logger = logging.getLogger("SixSense-Converter")

app = FastAPI(title="SixSense Doc-Converter")
TEMP_DIR = "temp_storage"
os.makedirs(TEMP_DIR, exist_ok=True)

# 임시 파일 삭제 함수
def cleanup_temp_file(path: str):
    if os.path.exists(path):
        os.remove(path)
        logger.info(f"Cleanup: Temporary file removed at {path}")

# 1. 루트 경로 (화면 출력)
@app.get("/", response_class=HTMLResponse)
async def read_root():
    logger.info("Root page accessed")
    return HTML_CONTENT

# 2. 헬스 체크 (K3s 모니터링용)
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 3. 변환 경로
@app.post("/convert-to-pdf/")
async def convert_any_to_pdf(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    # 파일 용량 제한 (100MB)
    MAX_SIZE = 100 * 1024 * 1024
    await file.seek(0, os.SEEK_END)
    file_size = await file.tell()
    await file.seek(0)

    if file_size > MAX_SIZE:
        logger.warning(f"File size limit exceeded: {file.filename} ({file_size} bytes)")
        raise HTTPException(status_code=413, detail="파일이 너무 큽니다. 최대 100MB까지 가능합니다.")
    
    file_id = str(uuid.uuid4())
    ext = file.filename.split(".")[-1].lower()
    input_path = os.path.join(TEMP_DIR, f"{file_id}.{ext}")
    output_path = os.path.join(TEMP_DIR, f"{file_id}.pdf")

    logger.info(f"Starting conversion: {file.filename} -> {file_id}.pdf")

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        process_conversion(input_path, output_path, ext, TEMP_DIR)
        
        # 파일 전송 후 삭제 예약
        background_tasks.add_task(cleanup_temp_file, output_path)
        
        logger.info(f"Successfully converted: {file.filename}")
        
        return FileResponse(
            output_path, 
            media_type="application/pdf", 
            filename=f"converted_{file.filename.rsplit('.', 1)[0]}.pdf"
        )
    except Exception as e:
        logger.error(f"Conversion failed for {file.filename}: {str(e)}")
        if os.path.exists(output_path):
            os.remove(output_path)
        raise HTTPException(status_code=500, detail=f"변환 실패: {str(e)}")
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
