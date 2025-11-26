"""
    File   Timer_UI
    Simple Workout Stopwatch
    
"""

import cv2
import numpy as np
import time

# ----- 상태 변수 -----
running = False          # 타이머 동작 여부
elapsed = 0.0            # 누적 시간(초)
last_time = time.time()  # 마지막 프레임 기준 시각

# ----- 버튼 위치 -----
start_btn = ((50, 450), (245, 500))    # Start
pause_btn = ((255, 450), (450, 500))   # Pause
reset_btn = ((50, 510), (245, 560))    # Reset
lap_btn   = ((255, 510), (450, 560))   # Lap

font_timer = cv2.FONT_HERSHEY_SIMPLEX  # 폰트
laps = []                               # 랩타임 리스트
MAX_LAPS = 7                            # 화면에 표시할 최대 랩 개수


def is_button_clicked(btn, x, y):
    """(x, y)가 버튼 안에 있는지 확인"""
    return btn[0][0] <= x <= btn[1][0] and btn[0][1] <= y <= btn[1][1]


def on_mouse(event, x, y, flags, param):
    """마우스 클릭 처리"""
    global running, elapsed, last_time, laps

    if event != cv2.EVENT_LBUTTONDOWN:
        return

    if is_button_clicked(start_btn, x, y):
        if not running:
            running = True
            last_time = time.time()

    elif is_button_clicked(pause_btn, x, y):
        running = False

    elif is_button_clicked(reset_btn, x, y):
        running = False
        elapsed = 0.0
        laps = []

    elif is_button_clicked(lap_btn, x, y):
        if running and elapsed > 0:
            laps.append(elapsed)
            if len(laps) > MAX_LAPS:
                laps.pop(0)


def draw_button(frame, rect, label):
    """버튼 그리기"""
    (x1, y1), (x2, y2) = rect
    cv2.rectangle(frame, (x1, y1), (x2, y2), (60, 60, 60), -1)
    (tw, th), _ = cv2.getTextSize(label, font_timer, 0.7, 2)
    text_x = x1 + (x2 - x1 - tw) // 2
    text_y = y1 + (y2 - y1 + th) // 2
    cv2.putText(frame, label, (text_x, text_y), font_timer, 0.7, (255, 255, 255), 2)


# ----- 메인 루프 -----
cv2.namedWindow("WORKOUT TIMER")
cv2.setMouseCallback("WORKOUT TIMER", on_mouse)

while True:
    frame = np.zeros((600, 500, 3), dtype=np.uint8)

    # 시간 업데이트
    if running:
        now = time.time()
        elapsed += now - last_time
        last_time = now

    # 표시용 시간 포맷 (mm:ss.cc)
    total = elapsed
    minute = int(total // 60)
    second = total % 60
    timer_text = f"{minute:02d}:{int(second):02d}"
    frac_part = f".{int((second - int(second)) * 100):02d}"

    # 동작 상태에 따라 색 바꾸기 (운동 중: 초록 / 멈춤: 빨강)
    color = (0, 255, 0) if running else (0, 0, 255)

    cv2.putText(frame, timer_text, (115, 200), font_timer, 3, color, 5)
    cv2.putText(frame, frac_part, (380, 200), font_timer, 1, color, 2)

    # 버튼 그리기
    draw_button(frame, start_btn, "Start")
    draw_button(frame, pause_btn, "Pause")
    draw_button(frame, reset_btn, "Reset")
    draw_button(frame, lap_btn, "Lap")

    # 랩타임 출력
    base_x = 60
    base_y = 260
    line_gap = 25

    for idx, t in enumerate(laps):
        total_r = t
        m = int(total_r // 60)
        s = total_r % 60
        text_int = f"{m:02d}:{int(s):02d}"
        text_frac = f".{int((s - int(s)) * 100):02d}"
        lap_text = f"{idx + 1:02d}) {text_int}{text_frac}"
        y = base_y + idx * line_gap
        cv2.putText(frame, lap_text, (base_x, y), font_timer, 0.7, (200, 200, 200), 1)

    # 설명 텍스트 (키보드 조작도 가능하게)
    cv2.putText(frame, "S: Start/Pause  R: Reset  L: Lap  Q: Quit",
                (10, 30), font_timer, 0.5, (255, 255, 255), 1)

    cv2.imshow("WORKOUT TIMER", frame)

    key = cv2.waitKey(50) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        if not running:
            running = True
            last_time = time.time()
        else:
            running = False
    elif key == ord('r'):
        running = False
        elapsed = 0.0
        laps = []
    elif key == ord('l'):
        if running and elapsed > 0:
            laps.append(elapsed)
            if len(laps) > MAX_LAPS:
                laps.pop(0)

cv2.destroyAllWindows()
