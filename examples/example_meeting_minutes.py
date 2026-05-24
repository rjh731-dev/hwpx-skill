#!/usr/bin/env python3
"""회의록 양식 사용 예시"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(SKILL_ROOT, "scripts"))

from render import render


def main():
    template_dir = os.path.join(SKILL_ROOT, "assets", "meeting-minutes")
    output_path = "/tmp/example_meeting_minutes.hwpx"

    data = {
        "회의_제목": "2026학년도 1학기 정보부 회의록",
        "일시": "2026. 5. 30.(목) 15:00~16:30",
        "장소": "본관 2층 정보부 회의실",
        "참석자": "정보부장 김○○, 부원 박○○, 이○○, 최○○, 정○○ (총 5명)",
        "작성자": "정○○ 교사",
        "안건": [
            "AI 활용 교사 직무연수 결과 공유",
            "2학기 정보부 운영 계획 점검",
            "기타 안건",
        ],
        "논의_내용": [
            "5월 30일 대구창의융합교육원 직무연수 30명 참여, 만족도 4.7/5.0",
            "2학기 코딩 동아리 운영 방안, AI 디지털 교과서 활용 사례 공유 계획",
            "정보 윤리 교육 외부 강사 초빙 검토",
        ],
        "결정_사항": [
            "직무연수 결과 보고서 작성 (담당: 정○○, 기한: 6/7)",
            "2학기 운영 계획서 6월 15일까지 제출",
        ],
        "다음_회의": "2026. 6. 13.(금) 15:00, 같은 장소",
    }

    result = render(template_dir, output_path, data)
    print(f"✅ 생성 완료: {result}")


if __name__ == "__main__":
    main()
