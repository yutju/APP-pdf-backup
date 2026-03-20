# converter.py
import os
import logging
import olefile  # HWP5 변환용
from PIL import Image  # 이미지 변환용
from reportlab.pdfgen import canvas  # PDF 생성용
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

logger = logging.getLogger("SixSense-Converter")

def process_conversion(input_path, output_path, ext, temp_dir):
    # 공통 설정: 한글 폰트 로드 (Dockerfile에서 설치한 나눔폰트)
    font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
    if not os.path.exists(font_path):
        # 폰트가 없는 경우 예외 처리 (인프라 설정 확인용)
        logger.error(f"Font not found at {font_path}. Check Dockerfile.")
        raise FileNotFoundError("System font missing.")
        
    pdfmetrics.registerFont(TTFont("NanumGothic", font_path))
    
    # [1] 이미지 변환 (PNG, JPG, BMP)
    if ext in ["png", "jpg", "jpeg", "bmp"]:
        try:
            img = Image.open(input_path)
            if img.mode != "RGB":
                img = img.convert("RGB")  # CMYK 등 특수 모드 대응
            img.save(output_path, "PDF")
            logger.info(f"Image conversion success: {output_path}")
            return
        except Exception as e:
            logger.error(f"Image Conversion Error: {str(e)}")
            raise e

    # [2] 문서 변환 (TXT, HWP)
    elif ext in ["txt", "hwp"]:
        try:
            # PDF 도화지 준비
            c = canvas.Canvas(output_path)
            c.setFont("NanumGothic", 10)
            
            y_position = 800  # 위에서부터 시작
            lines = []

            # 2-1. TXT 텍스트 추출 (인코딩 고려)
            if ext == "txt":
                try:
                    with open(input_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                except UnicodeDecodeError:
                    # cp949(EUC-KR) 대응
                    with open(input_path, 'r', encoding='cp949') as f:
                        lines = f.readlines()
            
            # 2-2. HWP 텍스트 추출 (OLE 구조 분석)
            elif ext == "hwp":
                ole = olefile.OleFileIO(input_path)
                if ole.exists('PrvText'):
                    data = ole.openstream('PrvText').read()
                    # UTF-16으로 인코딩된 텍스트 디코딩
                    text = data.decode('utf-16')
                    lines = text.split('\n')
                ole.close()

            # 추출된 텍스트를 PDF에 쓰기 (공통 로직)
            for line in lines:
                if line.strip():  # 빈 줄 방지
                    c.drawString(50, y_position, line.strip())
                    y_position -= 15  # 줄 간격
                    
                    # 페이지 하단 도달 시 새 페이지 생성
                    if y_position < 50:
                        c.showPage()
                        c.setFont("NanumGothic", 10)
                        y_position = 800
            
            c.save()
            logger.info(f"Document conversion success ({ext.upper()}): {output_path}")

        except Exception as e:
            logger.error(f"{ext.upper()} Conversion Error: {str(e)}")
            raise e
    else:
        # 지원하지 않는 확장자 예외 처리 (인프라 로그 남기기)
        raise ValueError(f"지원하지 않는 확장자입니다: {ext}")
