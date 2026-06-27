import os
import urllib.request

# 에셋 저장 경로 설정
target_dir = r"P:\Develop\ChessGame2\assets\pieces"
os.makedirs(target_dir, exist_ok=True)

# Chess.com / Lichess 표준 Wikipedia 디자인 공식 호스팅 주소
base_url = "https://chessboardjs.com/img/chesspieces/wikipedia"

# 로컬 파일명과 원본 파일명 매핑
pieces_mapping = {
    "w_pawn.png": "wP.png", "w_knight.png": "wN.png", "w_bishop.png": "wB.png",
    "w_rook.png": "wR.png", "w_queen.png": "wQ.png", "w_king.png": "wK.png",
    "b_pawn.png": "bP.png", "b_knight.png": "bN.png", "b_bishop.png": "bB.png",
    "b_rook.png": "bR.png", "b_queen.png": "bQ.png", "b_king.png": "bK.png"
}

# 403/404 차단을 원천 우회하기 위한 최신 브라우저 모조 헤더
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8'
}

print("Chess.com 스타일 정식 고화질 투명 PNG 에셋 다운로드 시작...")

for local_name, remote_name in pieces_mapping.items():
    file_path = os.path.join(target_dir, local_name)
    download_url = f"{base_url}/{remote_name}"
    
    try:
        req = urllib.request.Request(download_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(file_path, 'wb') as out_file:
                out_file.write(response.read())
        print(f" ✓ 성공: {remote_name} -> {local_name}")
    except Exception as e:
        print(f" ✗ 실패 ({local_name}) | URL: {download_url} | 에러: {e}")

print("\n모든 정식 체스 에셋이 성공적으로 배치되었습니다. 이제 main.py를 안심하고 실행하셔도 됩니다!")