"""
1교시 데모 — Hello QAQC
======================

실행 방법:
    cd ~/Desktop/QAQC_streamlit
    streamlit run app/01_hello_qaqc.py

학습 목표:
- st.set_page_config / st.title / st.markdown / st.caption
- st.columns + st.metric (KPI 카드 4개)
- st.dataframe (인터랙티브 표)
- st.line_chart (시계열 차트)
- st.success / st.warning (상태 메시지)
"""

import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------------------------------------------------------
# 1) 페이지 기본 설정 — 반드시 다른 st.* 호출보다 먼저 실행
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Hello QAQC",
    page_icon="🏭",
    layout="wide",                # "centered" 또는 "wide"
    initial_sidebar_state="auto", # "expanded" / "collapsed" / "auto"
)

# -----------------------------------------------------------------------------
# 2) 헤더 영역 — 제목과 설명
# -----------------------------------------------------------------------------
st.title("🏭 Hello QAQC")
st.markdown(
    "**자동차 부품 가공 라인 A** — 오늘의 외경(mm) 측정 결과 요약 페이지입니다."
)
st.caption("측정 일시: 2026-05-18 14:30 · 작성자: 정강민")

st.divider()  # 구분선 (1.30 이상에서 동작)

# -----------------------------------------------------------------------------
# 3) 가짜 측정 데이터 생성
#    실제 강의에서는 3교시부터 CSV에서 읽어옵니다.
# -----------------------------------------------------------------------------
np.random.seed(42)                                # 결과 재현성 확보
TARGET = 50.000                                   # 목표 치수
USL, LSL = 50.200, 49.800                         # 규격 상·하한
N = 50                                            # 측정 개수

measurements = TARGET + np.random.randn(N) * 0.08  # 평균 50, 표준편차 0.08
df = pd.DataFrame({
    "측정번호": range(1, N + 1),
    "외경(mm)": measurements.round(3),
})

# 합격/불합격 자동 판정
df["합격여부"] = df["외경(mm)"].apply(
    lambda x: "합격" if LSL <= x <= USL else "불합격"
)

# KPI 계산
total = len(df)
pass_count = (df["합격여부"] == "합격").sum()
fail_count = total - pass_count
defect_rate = fail_count / total * 100

# Cpk 계산 (4교시에서 자세히 다룹니다 — 지금은 공식만)
mean = df["외경(mm)"].mean()
std = df["외경(mm)"].std()
cpk = min((USL - mean), (mean - LSL)) / (3 * std)

# -----------------------------------------------------------------------------
# 4) KPI 카드 4개 — st.columns + st.metric
# -----------------------------------------------------------------------------
st.subheader("📊 오늘의 KPI")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="측정 수",
        value=f"{total} 건",
        delta="+15 (전일比)",
    )

with col2:
    st.metric(
        label="합격",
        value=f"{pass_count} 건",
        delta=f"+{pass_count - 35}",
    )

with col3:
    st.metric(
        label="불량률",
        value=f"{defect_rate:.1f}%",
        delta="-0.6%p",
        delta_color="inverse",        # 줄어드는 게 좋은 지표
    )

with col4:
    st.metric(
        label="Cpk",
        value=f"{cpk:.2f}",
        delta="+0.05",
    )

st.divider()

# -----------------------------------------------------------------------------
# 5) 측정 데이터 표
# -----------------------------------------------------------------------------
st.subheader("📋 측정 데이터")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    height=300,
)

# 합격/불합격 카운트 (덤)
counts = df["합격여부"].value_counts().reset_index()
counts.columns = ["판정", "건수"]
st.caption(f"합격: {pass_count}건 / 불합격: {fail_count}건")

st.divider()

# -----------------------------------------------------------------------------
# 6) 측정값 추이 라인 차트
# -----------------------------------------------------------------------------
st.subheader("📈 측정값 추이")

# st.line_chart 는 인덱스를 x축으로 사용 → 측정번호를 인덱스로
chart_df = df[["측정번호", "외경(mm)"]].set_index("측정번호")
st.line_chart(chart_df, height=300)

st.caption(f"목표 {TARGET}mm · USL {USL}mm · LSL {LSL}mm")

st.divider()

# -----------------------------------------------------------------------------
# 7) 상태 메시지 — 불량률에 따라 색 다르게
# -----------------------------------------------------------------------------
st.subheader("🔔 종합 판정")

if defect_rate == 0:
    st.success("✅ 모든 측정값이 규격 이내입니다. 라인 정상 가동 가능.")
elif defect_rate < 3:
    st.info(f"ℹ️ 경미한 불량 발생 ({defect_rate:.1f}%). 모니터링 강화 권장.")
elif defect_rate < 10:
    st.warning(f"⚠️ 불량률 {defect_rate:.1f}% — 원인 점검 필요.")
else:
    st.error(f"❌ 불량률 {defect_rate:.1f}% — 라인 정지 후 즉시 점검.")

# 풍선 효과는 학습용 (실제 운영에는 보통 안 씁니다)
if st.button("🎉 보고 완료"):
    st.balloons()
    st.success("일일 QC 리포트가 기록되었습니다.")

# -----------------------------------------------------------------------------
# 8) 페이지 하단 푸터
# -----------------------------------------------------------------------------
st.divider()
st.caption("QA/QC × Streamlit 5시간 강의 · 1교시 데모 · 정강민")
