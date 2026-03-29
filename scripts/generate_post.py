"""
JKW 투자 인사이트 - 자동 포스트 생성 스크립트

이 스크립트는 GitHub Actions에서 매일 실행되어 포스트를 자동 생성합니다.
각 카테고리별로 포스트 생성 함수를 확장하여 사용할 수 있습니다.

사용법:
    python scripts/generate_post.py --type daily
    python scripts/generate_post.py --type strategy
    python scripts/generate_post.py --type research
    python scripts/generate_post.py --type telegram
    python scripts/generate_post.py --type all
"""

import os
import argparse
from datetime import datetime, timezone, timedelta

# ============================================================
# 설정
# ============================================================
KST = timezone(timedelta(hours=9))
TODAY = datetime.now(KST)
DATE_STR = TODAY.strftime("%Y-%m-%d")
DATE_DISPLAY = TODAY.strftime("%Y.%m.%d")
WEEKDAY_KR = ["월", "화", "수", "목", "금", "토", "일"][TODAY.weekday()]

POSTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "posts")


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


# ============================================================
# 일일 시장 리포트
# ============================================================
def generate_daily_report():
    """
    일일 시장 리포트를 생성합니다.

    TODO: 실제 데이터 소스 연결
    - yfinance, pykrx 등으로 지수/종목 데이터 가져오기
    - 텔레그램 봇 API로 채널 메시지 수집
    - Claude API로 요약문 생성
    """
    post_dir = os.path.join(POSTS_DIR, f"{DATE_STR}-daily-report")
    ensure_dir(post_dir)

    # --------------------------------------------------------
    # 여기에 실제 데이터 수집 로직을 추가하세요
    # 예시:
    #   from data_fetcher import get_market_data
    #   data = get_market_data(DATE_STR)
    #   kospi = data['kospi']
    # --------------------------------------------------------

    # 데이터가 없을 때의 플레이스홀더
    kospi_val, kospi_chg = "—", "데이터 없음"
    kosdaq_val, kosdaq_chg = "—", "데이터 없음"
    sp500_val, sp500_chg = "—", "데이터 없음"
    usdkrw_val, usdkrw_chg = "—", "데이터 없음"
    summary = "시장 데이터가 아직 연결되지 않았습니다. `scripts/generate_post.py`에서 데이터 소스를 설정해주세요."
    sector_table = """| 섹터 | 등락률 | 비고 |
|:-----|:------:|:-----|
| — | — | 데이터 연결 필요 |"""
    events = "- 데이터 소스 연결 후 자동 생성됩니다."

    content = f"""---
title: "일일 시장 리포트 | {DATE_DISPLAY} ({WEEKDAY_KR})"
description: "일일 시장 동향 리포트 - 주요 지수, 섹터 동향, 수급 분석"
author: "AI 퀀트 운용본부"
date: "{DATE_STR}"
categories: [일일 리포트, 시장분석]
image: ""
format:
  html:
    code-fold: true
---

## 주요 지수 현황

::: {{.kpi-container}}
::: {{.kpi-card}}
[KOSPI]{{.kpi-label}}
[{kospi_val}]{{.kpi-value}}
[{kospi_chg}]{{.kpi-change}}
:::

::: {{.kpi-card}}
[KOSDAQ]{{.kpi-label}}
[{kosdaq_val}]{{.kpi-value}}
[{kosdaq_chg}]{{.kpi-change}}
:::

::: {{.kpi-card}}
[S&P 500]{{.kpi-label}}
[{sp500_val}]{{.kpi-value}}
[{sp500_chg}]{{.kpi-change}}
:::

::: {{.kpi-card}}
[원/달러]{{.kpi-label}}
[{usdkrw_val}]{{.kpi-value}}
[{usdkrw_chg}]{{.kpi-change}}
:::
:::

---

## 시장 요약

{summary}

## 섹터별 등락률

{sector_table}

## 주요 이벤트

{events}
"""

    with open(os.path.join(post_dir, "index.qmd"), "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[OK] 일일 리포트 생성: {post_dir}")
    return post_dir


# ============================================================
# 투자 전략 분석
# ============================================================
def generate_strategy():
    """
    투자 전략 분석 포스트를 생성합니다.

    TODO: 실제 전략 분석 로직 연결
    - 팩터 수익률 계산
    - 포트폴리오 리밸런싱 시그널
    - Claude API로 분석 요약 생성
    """
    post_dir = os.path.join(POSTS_DIR, f"{DATE_STR}-strategy")
    ensure_dir(post_dir)

    content = f"""---
title: "투자 전략 | 주간 퀀트 시그널 ({DATE_DISPLAY})"
description: "퀀트 팩터 기반 주간 투자 전략 업데이트"
author: "AI 퀀트 운용본부"
date: "{DATE_STR}"
categories: [투자 전략, 퀀트분석]
image: ""
format:
  html:
    code-fold: true
---

## 요약

투자 전략 데이터가 아직 연결되지 않았습니다.

`scripts/generate_post.py`의 `generate_strategy()` 함수에서 분석 로직을 구현해주세요.

::: {{.callout-note}}
### 구현 가이드
- `pykrx` 또는 자체 DB에서 종목 데이터 수집
- 팩터 수익률 계산 (모멘텀, 가치, 퀄리티 등)
- Claude API로 분석 인사이트 요약 생성
:::

::: {{.callout-important}}
### 면책사항
본 포스트는 정보 제공 목적이며, 투자 추천이 아닙니다.
:::
"""

    with open(os.path.join(post_dir, "index.qmd"), "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[OK] 투자 전략 생성: {post_dir}")
    return post_dir


# ============================================================
# 리서치 요약
# ============================================================
def generate_research():
    """
    리서치센터 리포트 요약 포스트를 생성합니다.

    TODO: 실제 리서치 데이터 연결
    - 증권사 리포트 PDF 수집 / 파싱
    - Claude API로 핵심 요약 생성
    """
    post_dir = os.path.join(POSTS_DIR, f"{DATE_STR}-research")
    ensure_dir(post_dir)

    content = f"""---
title: "리서치 요약 | {DATE_DISPLAY}"
description: "주요 증권사 리서치 리포트 핵심 요약"
author: "AI 퀀트 운용본부"
date: "{DATE_STR}"
categories: [리서치 요약]
image: ""
format:
  html:
    code-fold: true
---

## 오늘의 리서치 요약

리서치 리포트 데이터가 아직 연결되지 않았습니다.

`scripts/generate_post.py`의 `generate_research()` 함수에서 데이터 소스를 구현해주세요.

::: {{.callout-note}}
### 구현 가이드
- 증권사 리포트 PDF 자동 수집 (이메일, 웹 크롤링 등)
- PDF 텍스트 추출 후 Claude API로 요약
- 종목별 투자의견 변경 사항 정리
:::

::: {{.callout-important}}
### 면책사항
본 포스트는 정보 제공 목적이며, 투자 추천이 아닙니다.
:::
"""

    with open(os.path.join(post_dir, "index.qmd"), "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[OK] 리서치 요약 생성: {post_dir}")
    return post_dir


# ============================================================
# 텔레그램 요약
# ============================================================
def generate_telegram():
    """
    텔레그램 채널 요약 포스트를 생성합니다.

    TODO: 텔레그램 봇 API 연결
    - python-telegram-bot 또는 telethon 사용
    - 특정 채널의 최근 메시지 수집
    - Claude API로 핵심 내용 요약
    """
    post_dir = os.path.join(POSTS_DIR, f"{DATE_STR}-telegram")
    ensure_dir(post_dir)

    content = f"""---
title: "텔레그램 요약 | {DATE_DISPLAY}"
description: "투자 관련 텔레그램 채널 주요 소식 요약"
author: "AI 퀀트 운용본부"
date: "{DATE_STR}"
categories: [텔레그램 요약]
image: ""
format:
  html:
    code-fold: true
---

## 텔레그램 채널 요약

텔레그램 데이터가 아직 연결되지 않았습니다.

`scripts/generate_post.py`의 `generate_telegram()` 함수에서 텔레그램 봇을 설정해주세요.

::: {{.callout-note}}
### 구현 가이드
1. [BotFather](https://t.me/botfather)에서 봇 생성 → 토큰 발급
2. GitHub Secrets에 `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHANNEL_IDS` 저장
3. `telethon` 또는 `python-telegram-bot`으로 메시지 수집
4. Claude API로 요약 생성
:::

::: {{.callout-important}}
### 면책사항
본 포스트는 정보 제공 목적이며, 투자 추천이 아닙니다.
:::
"""

    with open(os.path.join(post_dir, "index.qmd"), "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[OK] 텔레그램 요약 생성: {post_dir}")
    return post_dir


# ============================================================
# 메인
# ============================================================
GENERATORS = {
    "daily": generate_daily_report,
    "strategy": generate_strategy,
    "research": generate_research,
    "telegram": generate_telegram,
}


def main():
    parser = argparse.ArgumentParser(description="JKW 블로그 포스트 자동 생성")
    parser.add_argument(
        "--type",
        choices=["daily", "strategy", "research", "telegram", "all"],
        default="all",
        help="생성할 포스트 유형 (기본: all)",
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="포스트 날짜 지정 (YYYY-MM-DD, 기본: 오늘)",
    )
    args = parser.parse_args()

    # 날짜 오버라이드
    global DATE_STR, DATE_DISPLAY, TODAY, WEEKDAY_KR
    if args.date:
        TODAY = datetime.strptime(args.date, "%Y-%m-%d").replace(tzinfo=KST)
        DATE_STR = TODAY.strftime("%Y-%m-%d")
        DATE_DISPLAY = TODAY.strftime("%Y.%m.%d")
        WEEKDAY_KR = ["월", "화", "수", "목", "금", "토", "일"][TODAY.weekday()]

    print(f"=== JKW 포스트 생성 ({DATE_STR} {WEEKDAY_KR}요일) ===")
    print()

    if args.type == "all":
        for name, gen_func in GENERATORS.items():
            try:
                gen_func()
            except Exception as e:
                print(f"[ERROR] {name}: {e}")
    else:
        try:
            GENERATORS[args.type]()
        except Exception as e:
            print(f"[ERROR] {args.type}: {e}")

    print()
    print("=== 완료 ===")


if __name__ == "__main__":
    main()
