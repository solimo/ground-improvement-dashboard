import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import re
from datetime import timedelta

st.set_page_config(
    page_title="지반개량 현황 분석 및 공정 예측 시스템",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

html {
    scroll-behavior: smooth;
}

.stApp {
    background: linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #020617;
}

[data-testid="stSidebar"] * {
    color: #f8fafc !important;
}

.main-title {
    font-size: 36px;
    font-weight: 900;
    color: #0f172a;
    margin-bottom: 6px;
}

.sub-title {
    color: #64748b;
    font-size: 16px;
    margin-bottom: 22px;
}

.hero-card {
    background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 45%, #38bdf8 100%);
    padding: 34px;
    border-radius: 24px;
    margin-bottom: 24px;
    box-shadow: 0 18px 40px rgba(15, 23, 42, 0.16);
}

.hero-title {
    font-size: 30px;
    font-weight: 900;
    color: white;
    margin-bottom: 10px;
}

.hero-desc {
    color: #e0f2fe;
    font-size: 16px;
    line-height: 1.75;
}

.hero-list {
    color: white;
    line-height: 1.9;
    margin-top: 16px;
}

.hero-list li {
    margin-bottom: 4px;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    border: 1px solid #e2e8f0;
    text-align: center;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.07);
}

.metric-title {
    font-size: 14px;
    color: #64748b;
    margin-bottom: 8px;
}

.metric-value {
    font-size: 30px;
    font-weight: 900;
    color: #0f172a;
}

.section-card {
    background: white;
    padding: 22px;
    border-radius: 22px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
    margin-bottom: 24px;
}

.status-good {
    background: linear-gradient(135deg, #dcfce7 0%, #ecfdf5 100%);
    color: #065f46;
    padding: 16px 18px;
    border-radius: 16px;
    font-weight: 800;
    border: 1px solid #bbf7d0;
}

.status-watch {
    background: linear-gradient(135deg, #fef3c7 0%, #fffbeb 100%);
    color: #92400e;
    padding: 16px 18px;
    border-radius: 16px;
    font-weight: 800;
    border: 1px solid #fde68a;
}

.status-risk {
    background: linear-gradient(135deg, #fee2e2 0%, #fef2f2 100%);
    color: #991b1b;
    padding: 16px 18px;
    border-radius: 16px;
    font-weight: 800;
    border: 1px solid #fecaca;
}

.notice-card {
    background: white;
    border: 1px solid #dbeafe;
    border-left: 6px solid #2563eb;
    padding: 18px 20px;
    border-radius: 18px;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
    margin-bottom: 18px;
}

.notice-title {
    color: #1e3a8a;
    font-weight: 900;
    font-size: 18px;
    margin-bottom: 6px;
}

.notice-desc {
    color: #475569;
    line-height: 1.7;
}

.small-chip {
    display: inline-block;
    padding: 6px 11px;
    border-radius: 999px;
    background: #eff6ff;
    color: #1d4ed8;
    font-weight: 700;
    font-size: 13px;
    margin-right: 6px;
    margin-bottom: 6px;
}

.side-nav {
    display: block;
    padding: 14px 16px;
    margin: 8px 0;
    border-radius: 14px;
    background: rgba(255,255,255,0.05);
    color: #f8fafc !important;
    text-decoration: none;
    font-weight: 800;
    transition: all 0.2s ease;
    border: 1px solid rgba(255,255,255,0.08);
}

.side-nav:hover {
    background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
    transform: translateX(6px);
    color: white !important;
    box-shadow: 0 8px 20px rgba(37,99,235,0.35);
}

.side-section-title {
    margin-top: 28px;
    margin-bottom: 12px;
    font-size: 15px;
    font-weight: 900;
    color: #93c5fd !important;
}

hr {
    margin-top: 1.8rem;
    margin-bottom: 1.8rem;
}

</style>
""", unsafe_allow_html=True)

with st.sidebar:

    st.markdown("## 공정 분석 시스템")
    st.markdown("---")

    st.markdown('<div class="side-section-title">분석 항목</div>', unsafe_allow_html=True)

    st.markdown("""
    <a class="side-nav" href="#core-summary">공정 진행률</a>
    <a class="side-nav" href="#remaining">잔여 물량</a>
    <a class="side-nav" href="#schedule">완료일 예측</a>
    <a class="side-nav" href="#drilling">장비별 천공 분석</a>
    <a class="side-nav" href="#adjacent">동일 유형 장비 편차</a>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="side-section-title">비교 기준</div>', unsafe_allow_html=True)

    st.markdown("""
    <a class="side-nav" href="#adjacent">삼축 ↔ 삼축</a>
    <a class="side-nav" href="#adjacent">일축 ↔ 일축</a>
    <a class="side-nav" href="#adjacent">삼축 ↔ 일축 제외</a>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">AI 기반 지반개량 현황 분석 및 공정 예측 시스템</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="sub-title">지반개량공사 현황표와 CCM 천공일지를 기반으로 공정 현황, 생산성, 완료일, 장비 간 편차를 자동 분석합니다.</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="hero-card">
    <div class="hero-title">지반개량 공정 데이터를 업로드하세요</div>
    <div class="hero-desc">
        현황표와 천공일지를 함께 업로드하면 공정 진행률, 잔여 물량, 예상 완료일,
        장비별 시공심도, 동일 장비유형 내 인접 천공 편차를 한 번에 분석합니다.
    </div>

    <ul class="hero-list">
        <li><b>현황표 분석</b>: 전체 진행률, 공종별 진행률, 잔여 물량, 완료일 예측</li>
        <li><b>천공일지 분석</b>: 장비별 시공심도, 이상치, 인접 천공 심도차 분석</li>
        <li><b>비교 기준</b>: 삼축은 삼축끼리, 일축은 일축끼리만 비교</li>
        <li><b>업로드 방식</b>: 드래그앤드롭 또는 파일 선택</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="notice-card">
    <div class="notice-title">사용 방법</div>

    <div class="notice-desc">
        ① 지반개량공사 현황표와 CCM 천공일지를 업로드합니다.<br>
        ② <b>분석 결과 생성하기</b> 버튼을 누릅니다.<br>
        ③ 공정 현황과 관리 필요 구간을 대시보드에서 확인합니다.
    </div>

    <div style="margin-top:12px;">
        <span class="small-chip">Excel 업로드</span>
        <span class="small-chip">자동 분석</span>
        <span class="small-chip">대시보드 출력</span>
        <span class="small-chip">CSV 다운로드</span>
    </div>
</div>
""", unsafe_allow_html=True)


def to_num(x):
    return pd.to_numeric(x, errors="coerce")


def clean_machine_name(sheet_name):
    name = str(sheet_name).strip()
    name = name.replace("천공일지", "")
    name = name.replace("작업일지", "")
    return name


def classify_machine_type(machine_name):
    name = str(machine_name)

    if "삼축" in name:
        return "삼축"

    if "일축" in name:
        return "일축"

    return "기타"


uploaded_files = st.file_uploader(
    "엑셀 파일을 여기에 드래그앤드롭하거나 클릭해서 업로드하세요",
    type=["xlsx"],
    accept_multiple_files=True,
    help="지반개량공사 현황표와 CCM 천공일지를 함께 업로드할 수 있습니다."
)

if not uploaded_files:
    st.info("먼저 엑셀 파일을 업로드하세요.")
    st.stop()

generate = st.button(
    "분석 결과 생성하기",
    type="primary",
    use_container_width=True
)

if not generate:
    st.warning("파일 업로드가 완료되었습니다. 위 버튼을 눌러 분석을 시작하세요.")
    st.stop()

with st.spinner("데이터를 분석하고 대시보드를 생성하는 중입니다..."):
    pass

st.success("분석 결과가 생성되었습니다.")

st.markdown('<h2 id="core-summary">핵심 현황 요약</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">전체 진행률</div>
        <div class="metric-value">72.4%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">잔여 물량</div>
        <div class="metric-value">12,450</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">표층 최근 평균</div>
        <div class="metric-value">1,250㎡/일</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">동일유형 최대 심도차</div>
        <div class="metric-value">2.84m</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

st.markdown(
    '<div class="status-watch">관찰: 동일 장비유형 내 인접 천공 장비 간 심도차가 일부 확인됩니다. 주요 구간 모니터링이 필요합니다.</div>',
    unsafe_allow_html=True
)

st.divider()

left, right = st.columns([1.1, 1])

with left:

    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    st.markdown('<h2 id="remaining">1. 공종별 진행률</h2>', unsafe_allow_html=True)

    dummy = pd.DataFrame({
        "공종": ["CCM-T", "CCM", "표층"],
        "진행률": [84, 68, 52]
    })

    fig = px.bar(
        dummy,
        x="공종",
        y="진행률",
        color="공종",
        text="진행률"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

with right:

    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    st.markdown('<h2 id="schedule">2. 완료일 예측</h2>', unsafe_allow_html=True)

    st.metric("중층 최근 평균", "92공/일")
    st.metric("표층 최근 평균", "1,250㎡/일")
    st.metric("표층 기준 예상 완료일", "2026-06-28")

    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

st.markdown('<div class="section-card">', unsafe_allow_html=True)

st.subheader("3. 일자별 작업 실적 추이")

dummy2 = pd.DataFrame({
    "날짜": pd.date_range("2026-05-01", periods=10),
    "CCM-T": np.random.randint(20, 60, 10),
    "CCM": np.random.randint(10, 40, 10),
    "표층": np.random.randint(800, 1600, 10)
})

left, right = st.columns(2)

with left:

    fig_middle = px.line(
        dummy2,
        x="날짜",
        y=["CCM-T", "CCM"],
        markers=True,
        title="중층 작업 실적 추이"
    )

    st.plotly_chart(fig_middle, use_container_width=True)

with right:

    fig_surface = px.bar(
        dummy2,
        x="날짜",
        y="표층",
        text="표층",
        title="표층 작업 실적 추이"
    )

    st.plotly_chart(fig_surface, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

st.divider()

st.markdown('<div class="section-card">', unsafe_allow_html=True)

st.markdown('<h2 id="drilling">4. CCM 천공일지 장비별 분석</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

col1.metric("천공 데이터 수", "2,412")
col2.metric("정상 데이터 수", "2,355")
col3.metric("이상치 수", "57")
col4.metric("평균 시공심도", "11.42m")

dummy3 = pd.DataFrame({
    "장비": ["삼축 1호기", "삼축 2호기", "일축 1호기", "일축 2호기"],
    "평균심도": [11.4, 10.8, 9.7, 10.2],
    "장비유형": ["삼축", "삼축", "일축", "일축"]
})

left, right = st.columns(2)

with left:

    fig3 = px.bar(
        dummy3,
        x="장비",
        y="평균심도",
        color="장비유형",
        text="평균심도"
    )

    st.plotly_chart(fig3, use_container_width=True)

with right:

    dummy4 = pd.DataFrame({
        "구역": ["A", "B", "C", "D", "E"],
        "천공수": [220, 310, 270, 190, 150]
    })

    fig4 = px.bar(
        dummy4,
        x="구역",
        y="천공수",
        text="천공수"
    )

    st.plotly_chart(fig4, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

st.divider()

st.markdown('<div class="section-card">', unsafe_allow_html=True)

st.markdown('<h2 id="adjacent">5. 동일 장비유형 인접 천공 TOP 10</h2>', unsafe_allow_html=True)

st.caption("※ 비교 기준: 삼축은 삼축끼리, 일축은 일축끼리만 비교합니다.")

dummy5 = pd.DataFrame({
    "비교구간": ["B2 12~13", "D1 55~56", "E3 10~11"],
    "심도차": [2.84, 2.42, 2.01],
    "장비유형": ["삼축", "일축", "삼축"]
})

fig5 = px.bar(
    dummy5,
    x="심도차",
    y="비교구간",
    color="장비유형",
    orientation="h"
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

st.divider()

st.markdown('<div class="section-card">', unsafe_allow_html=True)

st.subheader("6. AI 종합 분석 의견")

st.write("""
현재 지반개량 공정은 안정적으로 진행 중이며,
삼축 장비 구간 일부에서 인접 천공 간 심도차가 상대적으로 크게 나타났습니다.

특히 B2 구간은 장비별 편차 검토가 필요하며,
표층 생산량은 최근 증가 추세를 보이고 있어 예상 완료일은 계획 범위 내로 판단됩니다.
""")

st.markdown('</div>', unsafe_allow_html=True)

st.divider()

st.markdown('<div class="section-card">', unsafe_allow_html=True)

st.subheader("7. 데이터 다운로드")

st.download_button(
    "공정 현황 요약 CSV 다운로드",
    data="sample",
    file_name="공정현황.csv"
)

st.download_button(
    "동일유형 인접 천공 비교 CSV 다운로드",
    data="sample",
    file_name="인접천공비교.csv"
)

st.markdown('</div>', unsafe_allow_html=True)
