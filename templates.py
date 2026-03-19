# templates.py

# 전역 CSS 변수와 최신 UI 트렌드(Glassmorphism, Neumorphism 세련된 조합)를 적용한 프리미엄 테마입니다.
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SixSense Doc-Converter | 프리미엄 문서 PDF 변환 서비스</title>
    
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Poppins:wght@400;600;700;800&display=swap" rel="stylesheet">
    
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    
    <style>
        /* 글로벌 스타일 및 커스텀 클래스 */
        :root {
            --primary: #4F46E5; /* Indigo */
            --primary-dark: #4338CA;
            --secondary: #10B981; /* Emerald */
            --bg-main: #F9FAFB;
            --text-main: #1F2937;
            --glass-bg: rgba(255, 255, 255, 0.8);
            --glass-border: rgba(255, 255, 255, 0.2);
        }

        body { 
            font-family: 'Noto Sans KR', sans-serif; 
            background-color: var(--bg-main);
            color: var(--text-main);
            scroll-behavior: smooth;
        }
        
        .font-poppins { font-family: 'Poppins', sans-serif; }

        /* 세련된 그라데이션 애니메이션 배경 */
        .gradient-bg {
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }

        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Glassmorphism 카드 스타일 */
        .glass-card {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
        }

        /* 애니메이션 효과 */
        .hover-lift {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .hover-lift:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }

        /* 드롭존 커스텀 애니메이션 */
        .drop-zone {
            border: 3px dashed #d1d5db;
            transition: all 0.3s ease;
        }
        .drop-zone.active {
            border-color: var(--primary);
            background-color: #EEF2FF; /* Indigo 50 */
            transform: scale(1.02);
        }

        /* 로더 스타일 */
        .loader-ring {
            display: inline-block;
            width: 80px;
            height: 80px;
        }
        .loader-ring div {
            box-sizing: border-box;
            display: block;
            position: absolute;
            width: 64px;
            height: 64px;
            margin: 8px;
            border: 8px solid var(--primary);
            border-radius: 50%;
            animation: loader-ring 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
            border-color: var(--primary) transparent transparent transparent;
        }
        .loader-ring div:nth-child(1) { animation-delay: -0.45s; }
        .loader-ring div:nth-child(2) { animation-delay: -0.3s; }
        .loader-ring div:nth-child(3) { animation-delay: -0.15s; }
        @keyframes loader-ring {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body class="min-h-screen">

    <nav class="glass-card sticky top-0 z-50 border-b shadow-sm">
        <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
            <div class="flex items-center space-x-2">
                <span class="text-3xl filter drop-shadow">👀</span>
                <span class="text-3xl font-extrabold tracking-tighter text-gray-900 font-poppins">
                    Six<span class="text-indigo-600">Sense</span>
                </span>
            </div>
            <div class="flex items-center space-x-6 text-sm font-medium text-gray-700">
                <span class="hover:text-indigo-600 cursor-pointer transition">서비스 소개</span>
                <span class="hover:text-indigo-600 cursor-pointer transition">지원 형식</span>
                <span class="hover:text-indigo-600 cursor-pointer transition">API 문서</span>
                <button class="bg-indigo-600 text-white px-5 py-2 rounded-full text-xs font-bold hover:bg-indigo-700 transition transform hover:scale-105 shadow-md">
                    프리미엄 가입
                </button>
            </div>
        </div>
    </nav>

    <header class="gradient-bg py-24 text-white text-center shadow-inner">
        <div class="max-w-5xl mx-auto px-6">
            <h1 class="text-6xl font-black tracking-tight leading-tight font-poppins mb-6">
                단 한 번의 드래그로,<br>모든 문서를 <span class="text-yellow-300">완벽한 PDF</span>로
            </h1>
            <p class="text-xl font-light opacity-90 max-w-3xl mx-auto leading-relaxed">
                PNG, JPG 이미지부터 DOCX, HWP, TXT 문서까지.<br>인프라 팀의 시간을 아껴주는 초고속 프리미엄 변환 서비스를 경험하세요.
            </p>
            <button class="mt-12 bg-white text-indigo-700 font-extrabold text-lg px-12 py-4 rounded-xl shadow-2xl hover:bg-gray-100 transition transform hover:-translate-y-1">
                지금 바로 변환 시작
            </button>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 -mt-20 pb-32 relative z-10">
        <div class="glass-card p-12 rounded-3xl shadow-2xl hover-lift">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-10 items-center">
                
                <div class="md:col-span-1 pr-6 border-r border-gray-100">
                    <h2 class="text-3xl font-extrabold tracking-tight text-gray-900 mb-4">스마트 업로드</h2>
                    <p class="text-gray-600 leading-relaxed mb-6">
                        변환하고 싶은 파일을 오른쪽 영역에 끌어다 놓으세요. 여러 파일도 동시에 처리가 가능합니다. (최대 100MB)
                    </p>
                    <div class="space-y-3">
                        <div class="flex items-center space-x-2 text-sm text-green-700 font-medium bg-green-50 p-3 rounded-lg border border-green-100">
                            <span>✅</span> <span>나눔고딕 폰트 탑재로 한글 완벽 지원</span>
                        </div>
                        <div class="flex items-center space-x-2 text-sm text-indigo-700 font-medium bg-indigo-50 p-3 rounded-lg border border-indigo-100">
                            <span>✅</span> <span>인프라 팀의 전용 프라이빗 서비스</span>
                        </div>
                    </div>
                </div>

                <div class="md:col-span-2">
                    <form id="uploadForm" class="space-y-8">
                        <div id="dropZone" class="drop-zone p-16 text-center rounded-3xl cursor-pointer shadow-inner group bg-gray-50 hover:bg-white">
                            <div class="text-6xl filter drop-shadow-md transition-transform group-hover:scale-110">📄</div>
                            <p class="mt-6 text-2xl font-bold text-gray-800 tracking-tight">여기에 파일을 던져주세요</p>
                            <p class="text-sm text-gray-500 mt-2">또는 클릭하여 내 컴퓨터에서 선택 (PNG, JPG, DOCX, HWP, TXT)</p>
                            <input type="file" id="fileInput" name="file" class="hidden" required>
                        </div>
                        
                        <div id="fileInfo" class="hidden transition-opacity duration-300 opacity-0 transform translate-y-2 bg-indigo-50 p-5 rounded-2xl border border-indigo-200 flex items-center justify-between shadow-sm">
                            <div class="flex items-center space-x-3">
                                <span class="text-3xl">📎</span>
                                <div>
                                    <p id="fileName" class="text-lg font-bold text-indigo-900 tracking-tight"></p>
                                    <p class="text-xs text-indigo-600">변환 준비 완료</p>
                                </div>
                            </div>
                            <button type="button" id="removeFile" class="text-gray-400 hover:text-red-500 transition text-xl">❌</button>
                        </div>

                        <button type="submit" class="w-full bg-indigo-600 text-white font-extrabold py-5 rounded-2xl text-xl shadow-lg hover:bg-indigo-700 transition transform hover:-translate-y-1 shadow-indigo-200">
                            프리미엄 PDF 변환 시작 ✨
                        </button>
                    </form>

                    <div id="loadingScreen" class="hidden fixed inset-0 bg-gray-900 bg-opacity-70 flex items-center justify-center z-50 backdrop-blur-sm">
                        <div class="bg-white p-12 rounded-3xl text-center shadow-2xl">
                            <div class="loader-ring mx-auto mb-6"><div></div><div></div><div></div><div></div></div>
                            <p class="text-2xl font-extrabold text-gray-900 animate-pulse">인프라 엔진 가동 중...</p>
                            <p class="text-sm text-gray-500 mt-2">LibreOffice와 Pillow가 열심히 변환하고 있습니다.</p>
                        </div>
                    </div>

                    <div id="resultArea" class="hidden mt-10 bg-white p-8 rounded-3xl border-2 border-green-300 text-center shadow-xl">
                        <span class="text-6xl">🎉</span>
                        <h2 class="text-3xl font-black text-green-800 mt-6 tracking-tight">변환 성공!</h2>
                        <p class="text-green-700 mt-2 font-medium">당신의 프리미엄 문서를 받아보세요.</p>
                        <a id="downloadLink" href="#" class="inline-block mt-8 gradient-bg text-white font-extrabold py-4 px-12 rounded-full text-xl shadow-lg hover:opacity-90 transition transform hover:-translate-y-1 shadow-green-200" download>
                            📥 PDF 파일 다운로드
                        </a>
                    </div>
                </div>
            </div>
        </div>
        
        <p class="text-center text-gray-400 text-sm mt-16 font-poppins">© 2026 SixSense Project | Built with ❤ for Infrastructure Engineers</p>
    </main>

    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    <script>
        const uploadForm = document.getElementById('uploadForm');
        const fileInput = document.getElementById('fileInput');
        const dropZone = document.getElementById('dropZone');
        const fileInfo = document.getElementById('fileInfo');
        const fileNameDisp = document.getElementById('fileName');
        const removeFileBtn = document.getElementById('removeFile');
        const loadingScreen = document.getElementById('loadingScreen');
        const resultArea = document.getElementById('resultArea');
        const downloadLink = document.getElementById('downloadLink');

        fileInput.addEventListener('change', (e) => handleFileSelect(e.target.files[0]));
        dropZone.addEventListener('click', () => fileInput.click()); 
        dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('active'); });
        dropZone.addEventListener('dragleave', () => dropZone.classList.remove('active'));
        dropZone.addEventListener('drop', (e) => { e.preventDefault(); dropZone.classList.remove('active'); const file = e.dataTransfer.files[0]; fileInput.files = e.dataTransfer.files; handleFileSelect(file); });

        function handleFileSelect(file) {
            if (file) {
                fileNameDisp.textContent = file.name;
                fileInfo.classList.remove('hidden');
                setTimeout(() => { fileInfo.classList.remove('opacity-0', 'translate-y-2'); }, 10); // 애니메이션
                resultArea.classList.add('hidden');
            }
        }

        removeFileBtn.addEventListener('click', () => {
            fileInput.value = '';
            fileInfo.classList.add('opacity-0', 'translate-y-2');
            setTimeout(() => { fileInfo.classList.add('hidden'); }, 300);
        });

        uploadForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const file = fileInput.files[0];
            if (!file) return;

            const formData = new FormData();
            formData.append('file', file);
            loadingScreen.classList.remove('hidden');
            resultArea.classList.add('hidden');

            try {
                const response = await axios.post('/convert-to-pdf/', formData, { responseType: 'blob' });
                const pdfUrl = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
                downloadLink.href = pdfUrl;
                downloadLink.download = file.name.split('.').slice(0, -1).join('.') + '.pdf';
                resultArea.classList.remove('hidden');
            } catch (error) {
                alert('변환 실패! 서버 로그(temp_storage 권한 또는 LibreOffice 설치 여부)를 확인하세요.');
            } finally {
                loadingScreen.classList.add('hidden');
            }
        });
    </script>
</body>
</html>
"""
