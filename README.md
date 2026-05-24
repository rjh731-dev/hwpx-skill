# hwpx-skill

> Claude를 위한 HWPX 한글 문서 생성 스킬. **양식(template) + 메타파일(meta.json)** 한 쌍만 갖춰두면 어떤 양식이든 한 줄의 `render()` 호출로 채워서 만든다.

이 스킬은 한국 학교·공공기관에서 매일 쓰는 한글 양식 문서(보고서, 공문, 안내문, 계획서 등)를 Claude에게 맡기기 위해 만들어졌다. 양식을 한 번 등록해두면 매번 처음부터 만들지 않고도 데이터만 바꿔 끼울 수 있다.

---

## 핵심 아이디어

기존 방식의 문제: 양식이 바뀔 때마다 코드를 고치고, 양식이 늘어날 때마다 SKILL.md를 수정해야 한다.

이 스킬의 접근: **양식 옆에 자기 매핑 정보를 들고 다니는 메타파일을 둔다.** SKILL.md와 `render.py`는 어떤 양식이 와도 그대로다.

```
assets/
├── report/
│   ├── template.hwpx       # 양식 본체
│   └── template.meta.json  # 이 양식의 placeholder 명세
├── official-doc/           # (추가 양식)
│   ├── template.hwpx
│   └── template.meta.json
└── ...
```

새 양식 추가 = 폴더 하나 만들고 파일 두 개 넣기. 끝.

---

## 빠른 시작

### 1) 의존성 설치

```bash
pip install python-hwpx
```

### 2) 보고서 한 부 생성

```python
import sys
sys.path.insert(0, "scripts")
from render import render

render(
    template_dir="assets/report",
    output_path="output.hwpx",
    data={
        "기관명": "○○고등학교",
        "보고서_제목": "AI 활용 교사 연수 결과",
        "작성일": "today",                       # "today" / "2026-05-30" / date 객체 모두 가능
        "목차_1": ". 추진 배경",
        "목차_2": ". 추진 경과",
        "본문_1단계": [                          # 리스트 = 순차 치환
            "AI 도입 배경",
            "현장 적용 성과",
            "향후 계획",
        ],
    },
)
```

### 3) 결과 확인

`output.hwpx` 를 한컴오피스 한글에서 열어 확인한다.

---

## 디렉터리 구조

```
hwpx-skill/
├── SKILL.md                        # Claude가 읽는 스킬 명세 (양식 무관)
├── README.md                       # 이 파일
├── LICENSE
├── scripts/
│   ├── render.py                   # 단일 진입점 (양식 무관)
│   ├── scan_template.py            # 새 양식의 placeholder 자동 추출
│   ├── verify.py                   # 렌더 결과 검증
│   └── fix_namespaces.py           # HWPX 호환성 후처리 (자동 호출됨)
├── assets/
│   └── report/
│       ├── template.hwpx
│       └── template.meta.json
├── references/
│   ├── creating-new-template.md    # 새 양식 추가 가이드
│   ├── report-style.md             # 내부 보고서 양식 규약
│   ├── official-doc-style.md       # 공문서(기안문) 양식 규약
│   └── xml-internals.md            # HWPX XML 내부 구조
├── examples/
│   └── example_report.py           # 동작하는 최소 예제
└── evals/
    └── evals.json                  # 스킬 평가 케이스
```

---

## Claude에서 스킬로 사용하기

Claude는 이 스킬을 자동으로 인식하여 사용자의 "한글 보고서 만들어줘" 같은 요청이 들어오면 호출한다.

### Claude.ai (Free / Pro / Max / Team / Enterprise)

공식 안내에 따르면 다음 단계를 거친다:

1. Claude.ai 좌측 메뉴에서 **Settings → Capabilities** 로 이동, **Code execution and file creation** 토글을 켠다 (이 스킬이 스크립트를 실행하기 때문에 필수).
2. **Customize → Skills** 로 이동.
3. 우측 상단의 "+" 버튼 → **Create skill** → **Upload a skill**.
4. 이 저장소를 ZIP으로 압축해서 업로드. (저장소 루트 폴더 전체를 압축, 폴더 안에 `SKILL.md`가 있는 구조)
5. 업로드된 스킬을 토글로 활성화.

이후 Claude와의 대화에서 "한글로 보고서 작성해줘" 같은 요청이 들어오면 스킬이 자동으로 트리거된다.

Team / Enterprise 플랜에서는 owner가 organization-wide로 provision 할 수 있다.

> 출처: [Use Skills in Claude (Claude Help Center)](https://support.claude.com/en/articles/12512180-use-skills-in-claude)

### Claude Code (beta)

Claude Code에서는 skill 폴더를 다음 경로에 두면 자동으로 인식된다:

- 전체 사용자용: `~/.claude/skills/<skill-name>/`
- 프로젝트 전용: `<project>/.claude/skills/<skill-name>/`

```bash
git clone https://github.com/<your-username>/hwpx-skill ~/.claude/skills/hwpx
```

### API (code execution tool 사용 시)

API 통합은 Anthropic 공식 문서의 code execution tool 가이드를 참고. 이 스킬은 SKILL.md 기반의 표준 구조를 따르므로 그대로 사용 가능하다.

---

## 양식 추가하기

1. 한글에서 양식을 만든다. 채워질 자리에는 **본문에 절대 나오지 않을 고유한 placeholder 텍스트**를 박아둔다.

2. placeholder 자동 추출:
   ```bash
   python scripts/scan_template.py my-template.hwpx -o template.meta.json
   ```

3. 생성된 `template.meta.json`의 `key`, `name`, `description`, `required` 를 의미 있게 채운다. `TODO_field_01` 같은 자동 생성 키를 사람이 이해할 수 있는 이름으로 바꾸는 게 핵심이다.

4. 폴더 구조에 배치:
   ```
   assets/
   └── <양식종류>/
       ├── template.hwpx
       └── template.meta.json
   ```

5. 테스트:
   ```python
   render("assets/<양식종류>", "test.hwpx", data={...})
   ```

자세한 절차와 디자인 원칙은 [`references/creating-new-template.md`](references/creating-new-template.md) 참고.

---

## 메타파일 스키마

```json
{
  "name": "양식 이름",
  "description": "양식 설명 (AI가 양식 선택 시 참고)",
  "fields": [
    {
      "key": "기관명",
      "placeholder": "양식에 박혀있는 원본 텍스트",
      "type": "single",
      "required": true,
      "description": "사람용 설명"
    },
    {
      "key": "작성일",
      "placeholder": "2024. 5. 23.",
      "type": "date",
      "format": "YYYY. M. D.",
      "default": "today"
    },
    {
      "key": "본문_1단계",
      "placeholder": "헤드라인M 폰트 16포인트(문단 위 15)",
      "type": "sequential",
      "max_count": 8
    }
  ]
}
```

| type | 동작 | data 형태 |
|---|---|---|
| `single` | placeholder 등장 위치 모두 같은 값으로 치환 | 문자열 |
| `sequential` | 등장 위치를 순서대로 다른 값으로 치환 | 리스트 |
| `date` | "today" / 문자열 / date 객체를 `format` 으로 변환 | 문자열/date/`"today"` |

---

## 양식 카탈로그

| 양식 | 폴더 | 용도 |
|---|---|---|
| 내부 보고서 | [`assets/report/`](assets/report/) | 학교·기관 내부 보고서, 추진계획서, 결과보고서 |

> 양식 기여를 환영합니다. [`references/creating-new-template.md`](references/creating-new-template.md)의 절차를 따라 PR을 보내주세요.

---

## 자주 묻는 질문

**Q. 양식이 한컴오피스 한글에서 정상이지만 macOS 한컴 뷰어에서 빈 페이지로 나옵니다.**
A. 네임스페이스 후처리(`fix_namespaces.py`)가 빠진 경우입니다. `render()` 를 사용하면 자동 수행되지만, 직접 ZIP을 조작하는 경우 마지막에 명시적으로 호출해야 합니다.

**Q. `max_count` 보다 많은 본문 항목을 넣고 싶습니다.**
A. 양식 자체에 슬롯이 그 개수만 있어서 그렇습니다. 한글에서 양식을 열어 슬롯을 추가하거나, 그 다음 항목들은 한글에서 직접 입력하시는 게 빠릅니다.

**Q. 사용자 업로드 양식과 등록 양식 중 어느 게 우선인가요?**
A. 항상 사용자 업로드 양식이 우선입니다. `/mnt/user-data/uploads/` 에 `.hwpx`가 있으면 등록 양식을 무시하고 그것을 사용하도록 SKILL.md에 명시되어 있습니다.

**Q. 일반 Word(.docx) 문서도 만들 수 있나요?**
A. 이 스킬은 HWPX 전용입니다. Word는 별도의 `docx` 스킬을 사용하세요.

---

## 라이선스

코드: MIT License — [`LICENSE`](LICENSE) 참고.
양식 파일(`assets/**/template.hwpx`): 별도 명시가 없는 한 MIT.

이 프로젝트는 한컴(Hancom Inc.)과 무관하며, "HWPX"는 한컴의 상표입니다.

---

## 기여 (Contributing)

이슈와 PR을 환영합니다. 특히:

- 새 양식 추가 (학부모 안내문, 공문서, 회의록, 운영 계획서 등)
- placeholder 자동 감지 로직 개선 (`scan_template.py`)
- 다양한 한글 버전·환경에서의 호환성 테스트
- 다국어 문서 (영문 README 등)

PR 전에 `python examples/example_report.py` 가 정상 실행되는지 확인해주세요.

---

## 참고 자료

- [HWP/OWPML 형식 공식 다운로드 페이지 (한컴)](https://www.hancom.com/support/downloadCenter/hwpOwpml) — HWPX는 한국산업표준 KS X 6101의 OWPML 기반
- [HWPX 포맷 구조 살펴보기 (한컴테크 블로그)](https://tech.hancom.com/hwpxformat/)
- [Claude Skills 공식 문서](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
- [python-hwpx (PyPI)](https://pypi.org/project/python-hwpx/)
