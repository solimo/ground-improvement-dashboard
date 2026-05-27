# ==============================
# AI 기반 공정 분석 시스템
# ==============================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import re
from datetime import timedelta
from pathlib import Path

# ==============================
# 페이지 설정
# ==============================
st.set_page_config(
    page_title="AI 기반 공정 분석 시스템",
    layout="wide",
    initial_sidebar_state="expanded"
)

LOGO_PATH = "cj_logo.png"

COLOR_SEQ = [
    "#005BAC",
    "#00AEEF",
    "#F58220",
    "#ED1C24",
    "#4F46E5",
    "#10B981"
]

# ==============================
# CSS
# ==============================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800;900&display=swap');

html {
    scroll-behavior: smooth;
}

* {
    font-family: 'Pretendard', sans-serif !important;
}

/* =========================
   애니메이션
========================= */

@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(22px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes scaleIn {
    from {
        opacity: 0;
        transform: scale(0.96);
    }

    to {
        opacity: 1;
        transform: scale(1);
    }
}

/* =========================
   전체 배경
========================= */

.stApp {
    background:
        radial-gradient(circle at 85% 0%, rgba(0,174,239,0.15) 0%, rgba(0,174,239,0) 32%),
        radial-gradient(circle at 5% 10%, rgba(0,91,172,0.08) 0%, rgba(0,91,172,0) 30%),
        linear-gradient(180deg, #F8FBFF 0%, #EEF4FA 100%);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1550px;
}

/* =========================
   사이드바
========================= */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f8fafc 0%, #eaf1fb 100%);
    border-right: 1px solid #dbe3ef;
}

[data-testid="stSidebar"] * {
    color: #0f172a !important;
}

[data-testid="stSidebar"] .block-container {
    padding-top: 1rem;
}

.logo-box {
    text-align: center;
    margin-bottom: 16px;
}

.side-nav {
    display: block;
    padding: 15px 17px;
    margin: 8px 0;
    border-radius: 16px;
    background: white;
    color: #0f172a !important;
    text-decoration: none;
    font-weight: 800;
    transition: all 0.22s ease;
    border: 1px solid #dbe3ef;
    box-shadow: 0 6px 16px rgba(15, 23, 42, 0.05);
}

.side-nav:hover {
    background: linear-gradient(135deg, #005BAC 0%, #00AEEF 100%);
    color: white !important;
    transform: translateX(7px);
    box-shadow: 0 12px 28px rgba(0,91,172,0.20);
}

/* =========================
   메인 타이틀
========================= */

.main-title {
    font-size: clamp(46px, 4vw, 72px);
    font-weight: 900;
    color: #071B3A;
    line-height: 1.03;
    letter-spacing: -2px;
    margin: 10px 0 12px 0;
    animation: fadeUp 0.7s ease both;
}

.sub-title {
    color: #52657A;
    font-size: 20px;
    font-weight: 600;
    line-height: 1.7;
    margin-bottom: 30px;
    animation: fadeUp 0.8s ease both;
}

/* =========================
   HERO
========================= */

.hero-card {
    position: relative;
    overflow: hidden;

    background:
        radial-gradient(circle at 88% 15%, rgba(255,255,255,0.25) 0%, rgba(255,255,255,0) 30%),
        linear-gradient(135deg, #071B3A 0%, #005BAC 52%, #00AEEF 100%);

    padding: 42px 48px;
    border-radius: 34px;

    margin-bottom: 30px;

    box-shadow:
        0 28px 70px rgba(0,91,172,0.22),
        0 8px 24px rgba(15,23,42,0.08);

    animation: fadeUp 0.85s ease both;
}

.hero-title {
    font-size: clamp(32px, 3vw, 46px);
    font-weight: 900;
    color: white;
    margin-bottom: 12px;
}

.hero-desc {
    color: #EAF7FF;
    font-size: 18px;
    line-height: 1.85;
    font-weight: 600;
    max-width: 950px;
}

/* =========================
   업로드 박스
========================= */

.upload-panel {
    background:
        radial-gradient(circle at top right, rgba(0,174,239,0.10), transparent 35%),
        rgba(255,255,255,0.94);

    padding: 34px;
    border-radius: 30px;

    border: 1px solid #CFE0F3;

    box-shadow:
        0 20px 48px rgba(15,23,42,0.07),
        0 4px 12px rgba(0,91,172,0.05);

    margin-bottom: 30px;

    animation: fadeUp 0.8s ease both;
}

.upload-title {
    font-size: 30px;
    font-weight: 900;
    color: #071B3A;
    margin-bottom: 10px;
}

.upload-desc {
    color: #52657A;
    font-size: 18px;
    line-height: 1.75;
    margin-bottom: 20px;
}

.small-chip {
    display: inline-block;
    padding: 9px 15px;
    border-radius: 999px;
    background: #EAF4FF;
    color: #005BAC;
    font-weight: 900;
    font-size: 14px;
    margin-right: 9px;
    margin-bottom: 9px;
    border: 1px solid #CFE5FF;
}

/* =========================
   파일 업로더
========================= */

[data-testid="stFileUploader"] {
    background: #F8FBFF;
    border: 2px dashed #7CBCEB;
    border-radius: 28px;
    padding: 32px;
}

[data-testid="stFileUploaderDropzone"] {
    background: white;
    border: 2px dashed #A6D7FA;
    border-radius: 24px;
    min-height: 160px;
    padding: 32px;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #005BAC;
    background: #EDF7FF;
}

/* =========================
   섹션
========================= */

.anchor-offset {
    scroll-margin-top: 100px;
}

.section-title {
    font-size: clamp(32px, 2.6vw, 44px);
    font-weight: 900;
    color: #071B3A;
    margin: 40px 0 8px 0;
    letter-spacing: -1px;
    animation: fadeUp 0.6s ease both;
}

.section-title:before {
    content: "";
    display: inline-block;
    width: 10px;
    height: 30px;
    border-radius: 8px;
    background: linear-gradient(180deg, #005BAC, #00AEEF);
    margin-right: 13px;
    vertical-align: -4px;
}

.section-desc {
    color: #52657A;
    font-size: 18px;
    line-height: 1.7;
    margin-bottom: 18px;
}

/* =========================
   KPI 카드
========================= */

.metric-card {
    background:
        radial-gradient(circle at top right, rgba(0,174,239,0.16), transparent 35%),
        linear-gradient(180deg, #ffffff 0%, #f3f9ff 100%);

    padding: 32px 22px;
    border-radius: 30px;

    border: 1px solid #C9DDF2;

    text-align: center;

    box-shadow:
        0 22px 52px rgba(0,91,172,0.13),
        0 6px 16px rgba(15,23,42,0.05);

    min-height: 170px;

    transition: all 0.25s ease;

    animation: scaleIn 0.55s ease both;
}

.metric-card:hover {
    transform: translateY(-7px);
}

.metric-title {
    font-size: 18px;
    color: #52657A;
    margin-bottom: 18px;
    font-weight: 900;
}

.metric-value {
    font-size: clamp(36px, 2.8vw, 54px);
    font-weight: 900;
    color: #071B3A;
    line-height: 1.05;
    letter-spacing: -1.4px;
}

/* =========================
   그래프
========================= */

[data-testid="stPlotlyChart"] {
    background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
    border-radius: 32px;
    padding: 24px;

    border: 1px solid #C9DDF2;

    box-shadow:
        0 24px 60px rgba(0,91,172,0.12),
        0 8px 20px rgba(15,23,42,0.06);

    overflow: hidden;

    margin: 16px 0 32px 0;

    animation: fadeUp 0.72s ease both;
}

/* =========================
   컨테이너
========================= */

[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 30px !important;
    border-color: #C9DDF2 !important;

    background:
        radial-gradient(circle at top right, rgba(0,174,239,0.08), transparent 30%),
        rgba(255,255,255,0.80);

    box-shadow:
        0 18px 48px rgba(15,23,42,0.06),
        0 4px 12px rgba(0,91,172,0.04);
}

/* =========================
   dataframe
========================= */

[data-testid="stDataFrame"] {
    border-radius: 24px;
    overflow: hidden;
    border: 1px solid #D4E2F0;

    box-shadow:
        0 14px 34px rgba(15,23,42,0.06),
        0 4px 12px rgba(0,91,172,0.04);
}

/* =========================
   상태
========================= */

.status-good,
.status-watch,
.status-risk {
    padding: 20px 24px;
    border-radius: 22px;
    font-weight: 900;
    font-size: 18px;
    margin: 20px 0;
}

.status-good {
    background: #E8F8EF;
    color: #06613C;
    border: 1px solid #B9EBCF;
}

.status-watch {
    background: #FFF7E6;
    color: #8A5200;
    border: 1px solid #F5D38B;
}

.status-risk {
    background: #FFF0F0;
    color: #B00020;
    border: 1px solid #F2B8B8;
}

/* =========================
   버튼
========================= */

.stButton button,
.stDownloadButton button {

    border-radius: 18px !important;

    font-weight: 900 !important;

    font-size: 17px !important;

    padding: 0.85rem 1.2rem !important;

    box-shadow: 0 10px 24px rgba(0,91,172,0.12);
}

</style>
""", unsafe_allow_html=True)

# ==============================
# 함수
# ==============================

def section_header(title, desc=None, anchor=None):

    if anchor:
        st.markdown(
            f'<div id="{anchor}" class="anchor-offset"></div>',
            unsafe_allow_html=True
        )

    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True
    )

    if desc:
        st.markdown(
            f'<div class="section-desc">{desc}</div>',
            unsafe_allow_html=True
        )


def apply_chart_style(fig, height=620, legend=True):

    fig.update_layout(
        height=height,

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",

        font=dict(
            family="Pretendard",
            size=20,
            color="#071B3A"
        ),

        title=dict(
            font=dict(
                size=31,
                color="#071B3A"
            ),
            x=0.02,
            xanchor="left",
            y=0.96
        ),

        margin=dict(
            l=100,
            r=58,
            t=115,
            b=110
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="right",
            x=1,
            font=dict(size=18)
        ),

        xaxis=dict(
            title_font=dict(size=22),
            tickfont=dict(size=18),
            showgrid=False,
            linecolor="#B7C9DC"
        ),

        yaxis=dict(
            title_font=dict(size=22),
            tickfont=dict(size=18),
            gridcolor="#E2ECF7",
            linecolor="#B7C9DC"
        )
    )

    if not legend:
        fig.update_layout(showlegend=False)

    fig.update_traces(
        marker_line_width=0,
        textfont=dict(size=21),
        hoverlabel=dict(
            bgcolor="white",
            font_size=18
        )
    )

    return fig


def to_num(x):
    return pd.to_numeric(x, errors="coerce")

# 이하 기존 parse 함수 / 분석 함수 동일
# ==============================
# 여기부터는 형 기존 코드 그대로 사용
# parse_status_file
# parse_drilling_file
# make_adjacent_comparison
# create_ai_comment
# 전부 그대로 유지
# ==============================

# ===================================
# 사이드바
# ===================================

with st.sidebar:

    if Path(LOGO_PATH).exists():
        st.markdown('<div class="logo-box">', unsafe_allow_html=True)
        st.image(LOGO_PATH, width=240)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("## CJ제일제당 저온HUB센터 신축공사")
    st.markdown("---")

    st.markdown("""
    <a class="side-nav" href="#upload-section">파일 업로드</a>
    <a class="side-nav" href="#status-summary">공정 현황 요약</a>
    <a class="side-nav" href="#progress-section">공정별 진행률</a>
    <a class="side-nav" href="#daily-section">일자별 실적</a>
    <a class="side-nav" href="#drilling-section">장비 분석</a>
    <a class="side-nav" href="#adjacent-section">편차 분석</a>
    """, unsafe_allow_html=True)

# ===================================
# 메인
# ===================================

st.markdown(
    '<div class="main-title">AI 기반 공정 분석 시스템</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">현장 데이터를 자동 분석하여 공정률, 생산성, 장비 편차를 시각화합니다.</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="hero-card">
    <div class="hero-title">공정 데이터를 업로드하세요</div>

    <div class="hero-desc">
        현황표와 천공일지를 업로드하면
        공정률, 잔여 물량, 예상 완료일,
        장비별 시공심도 및 편차를
        자동 분석합니다.
    </div>
</div>
""", unsafe_allow_html=True)

# ===================================
# 업로드
# ===================================

st.markdown(
    '<div id="upload-section" class="anchor-offset"></div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="upload-panel">

    <div class="upload-title">
        분석 파일 업로드
    </div>

    <div class="upload-desc">
        공정현황표 및 CCM 천공일지를 업로드하세요.
    </div>

    <span class="small-chip">현황표 XLSX</span>
    <span class="small-chip">천공일지 XLSX</span>
    <span class="small-chip">Drag & Drop</span>

</div>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "엑셀 파일 업로드",
    type=["xlsx"],
    accept_multiple_files=True
)

if not uploaded_files:
    st.stop()

# ===================================
# 예시 KPI
# ===================================

section_header(
    "공정 현황 요약",
    "표층 및 중층 진행률을 분리하여 분석합니다.",
    "status-summary"
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">중층 진행률</div>
        <div class="metric-value">82.4%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">표층 진행률</div>
        <div class="metric-value">94.1%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">중층 평균 생산량</div>
        <div class="metric-value">152공</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">예상 완료일</div>
        <div class="metric-value">2026-05-31</div>
    </div>
    """, unsafe_allow_html=True)

# ===================================
# 그래프 예시
# ===================================

section_header(
    "공종별 진행률",
    "공종별 진행 현황 분석",
    "progress-section"
)

sample_df = pd.DataFrame({
    "공종": ["표층", "중층", "CCM-T", "CCM"],
    "진행률": [94, 82, 79, 85]
})

fig = px.bar(
    sample_df,
    x="공종",
    y="진행률",
    text="진행률",
    color="공종",
    color_discrete_sequence=COLOR_SEQ
)

fig.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig.update_layout(
    yaxis_title="진행률(%)",
    xaxis_title="공종"
)

fig = apply_chart_style(fig)

st.plotly_chart(fig, use_container_width=True)
