import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import re
from datetime import timedelta
from pathlib import Path

st.set_page_config(
    page_title="지반개량 현황 분석 및 공정 예측 시스템",
    layout="wide",
    initial_sidebar_state="expanded"
)

LOGO_PATH = "cj_logo.png"

st.markdown("""
<style>
html { scroll-behavior: smooth; }

.stApp {
    background: linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

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

[data-testid="stSidebar"] .block-container {
    padding-top: 1rem;
}

.logo-box {
    background: transparent;
    padding: 6px 0 18px 0;
    margin-bottom: 10px;
    text-align: center;
}

.main-title {
    font-size: clamp(26px, 2.1vw, 34px);
    font-weight: 900;
    color: #0f172a;
    margin-bottom: 8px;
    line-height: 1.22;
    word-break: keep-all;
    max-width: 100%;
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

.upload-panel {
    background: white;
    padding: 30px;
    border-radius: 24px;
    border: 1px solid #dbeafe;
    box-shadow: 0 14px 34px rgba(15, 23, 42, 0.08);
    margin-bottom: 24px;
}

.upload-title {
    font-size: 24px;
    font-weight: 900;
    color: #1e3a8a;
    margin-bottom: 8px;
}

.upload-desc {
    color: #475569;
    font-size: 15px;
    line-height: 1.7;
    margin-bottom: 18px;
}

[data-testid="stFileUploader"] {
    background: #f8fbff;
    border: 2px dashed #60a5fa;
    border-radius: 22px;
    padding: 28px;
}

[data-testid="stFileUploaderDropzone"] {
    background: white;
    border: 2px dashed #93c5fd;
    border-radius: 18px;
    min-height: 130px;
    padding: 24px;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #2563eb;
    background: #eff6ff;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    border: 1px solid #e2e8f0;
    text-align: center;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.07);
    min-height: 112px;
}

.metric-title {
    font-size: 14px;
    color: #64748b;
    margin-bottom: 8px;
    white-space: normal;
}

.metric-value {
    font-size: 26px;
    font-weight: 900;
    color: #0f172a;
    line-height: 1.2;
    word-break: keep-all;
    white-space: normal;
}

.status-good {
    background: linear-gradient(135deg, #dcfce7 0%, #ecfdf5 100%);
    color: #065f46;
    padding: 16px 18px;
    border-radius: 16px;
    font-weight: 800;
    border: 1px solid #bbf7d0;
    margin-top: 16px;
}

.status-watch {
    background: linear-gradient(135deg, #fef3c7 0%, #fffbeb 100%);
    color: #92400e;
    padding: 16px 18px;
    border-radius: 16px;
    font-weight: 800;
    border: 1px solid #fde68a;
    margin-top: 16px;
}

.status-risk {
    background: linear-gradient(135deg, #fee2e2 0%, #fef2f2 100%);
    color: #991b1b;
    padding: 16px 18px;
    border-radius: 16px;
    font-weight: 800;
    border: 1px solid #fecaca;
    margin-top: 16px;
}

.side-nav {
    display: block;
    padding: 14px 16px;
    margin: 8px 0;
    border-radius: 14px;
    background: white;
    color: #0f172a !important;
    text-decoration: none;
    font-weight: 800;
    transition: all 0.2s ease;
    border: 1px solid #dbe3ef;
    box-shadow: 0 5px 14px rgba(15, 23, 42, 0.05);
}

.side-nav:hover {
    background: linear-gradient(135deg, #2563eb 0%, #38bdf8 100%);
    transform: translateX(6px);
    color: white !important;
    box-shadow: 0 8px 20px rgba(37,99,235,0.25);
}

.side-section-title {
    margin-top: 28px;
    margin-bottom: 12px;
    font-size: 15px;
    font-weight: 900;
    color: #1e3a8a !important;
}

.small-chip {
    display: inline-block;
    padding: 7px 12px;
    border-radius: 999px;
    background: #eff6ff;
    color: #1d4ed8;
    font-weight: 800;
    font-size: 13px;
    margin-right: 7px;
    margin-bottom: 7px;
}

.anchor-offset {
    scroll-margin-top: 90px;
}

.section-title {
    font-size: 24px;
    font-weight: 900;
    color: #0f172a;
    margin-bottom: 4px;
}

.section-desc {
    color: #64748b;
    font-size: 14px;
    line-height: 1.6;
    margin-bottom: 16px;
}

[data-testid="stPlotlyChart"] {
    background: white;
    border-radius: 22px;
    padding: 16px;
    border: 1px solid #dbe3ef;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
    overflow: hidden;
    margin-bottom: 12px;
}

.js-plotly-plot .plotly,
.js-plotly-plot .plot-container,
.js-plotly-plot svg {
    border-radius: 18px !important;
}

.plotly .modebar {
    border-radius: 12px !important;
}

.stDownloadButton button, .stButton button {
    border-radius: 14px !important;
    font-weight: 800 !important;
    padding: 0.7rem 1rem !important;
}

.stAlert {
    border-radius: 16px;
}

[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)


def section_header(title, desc=None, anchor=None):
    if anchor:
        st.markdown(f'<div id="{anchor}" class="anchor-offset"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if desc:
        st.markdown(f'<div class="section-desc">{desc}</div>', unsafe_allow_html=True)


def apply_chart_style(fig, height=410):
    fig.update_layout(
        height=height,
        paper_bgcolor="white",
        plot_bgcolor="#f8fafc",
        font=dict(size=13, color="#334155"),
        margin=dict(l=30, r=30, t=60, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=False, zeroline=False, linecolor="#cbd5e1"),
        yaxis=dict(gridcolor="#e2e8f0", zeroline=False, linecolor="#cbd5e1")
    )
    return fig


def to_num(x):
    return pd.to_numeric(x, errors="coerce")


def clean_machine_name(sheet_name):
    name = str(sheet_name).strip()
    name = name.replace("천공일지", "").replace("작업일지", "")
    name = name.replace("(", " (").replace(")", ")")
    return name


def classify_machine_type(machine_name):
    name = str(machine_name)
    if "삼축" in name:
        return "삼축"
    if "일축" in name:
        return "일축"
    return "기타"


def parse_status_file(uploaded_file):
    uploaded_file.seek(0)
    xls = pd.ExcelFile(uploaded_file)
    summary_rows = []
    daily_rows = []

    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet, header=None)
        text_blob = " ".join(df.astype(str).fillna("").values.flatten())

        if "지반개량공사 총괄표" in text_blob:
            for i in range(len(df)):
                row = df.iloc[i].astype(str).tolist()
                if "설계수량" in row:
                    for r in range(i + 1, len(df)):
                        cat = df.iloc[r, 0] if df.shape[1] > 0 else np.nan
                        spec = df.iloc[r, 1] if df.shape[1] > 1 else np.nan
                        unit = df.iloc[r, 2] if df.shape[1] > 2 else np.nan
                        design = df.iloc[r, 3] if df.shape[1] > 3 else np.nan
                        prev = df.iloc[r, 4] if df.shape[1] > 4 else np.nan
                        done = df.iloc[r, 5] if df.shape[1] > 5 else np.nan
                        remaining = df.iloc[r, 6] if df.shape[1] > 6 else np.nan
                        progress = df.iloc[r, 7] if df.shape[1] > 7 else np.nan

                        if pd.isna(spec) and pd.isna(design):
                            continue

                        summary_rows.append({
                            "구분": cat,
                            "규격": spec,
                            "단위": unit,
                            "설계수량": to_num(design),
                            "전일": to_num(prev),
                            "누계": to_num(done),
                            "잔여량": to_num(remaining),
                            "진행률": to_num(progress)
                        })

        if "지반개량공사 현황" in text_blob:
            header_row = None
            for i in range(len(df)):
                if df.iloc[i].astype(str).str.contains("시공일", na=False).any():
                    header_row = i
                    break

            if header_row is not None:
                year = 2026
                for value in df.values.flatten():
                    if isinstance(value, pd.Timestamp):
                        year = value.year
                        break

                current_month = None

                for r in range(header_row + 2, len(df)):
                    month = df.iloc[r, 0] if df.shape[1] > 0 else np.nan
                    day = df.iloc[r, 1] if df.shape[1] > 1 else np.nan

                    if pd.notna(month):
                        try:
                            current_month = int(month)
                        except:
                            pass

                    if pd.isna(day) or current_month is None:
                        continue

                    try:
                        date = pd.Timestamp(year=year, month=int(current_month), day=int(day))
                    except:
                        continue

                    ccm_t = to_num(df.iloc[r, 3]) if df.shape[1] > 3 else np.nan
                    ccm = to_num(df.iloc[r, 4]) if df.shape[1] > 4 else np.nan
                    surface = to_num(df.iloc[r, 5]) if df.shape[1] > 5 else np.nan

                    if pd.isna(ccm_t) and pd.isna(ccm) and pd.isna(surface):
                        continue

                    daily_rows.append({
                        "날짜": date,
                        "CCM-T": 0 if pd.isna(ccm_t) else float(ccm_t),
                        "CCM": 0 if pd.isna(ccm) else float(ccm),
                        "표층": 0 if pd.isna(surface) else float(surface)
                    })

    summary = pd.DataFrame(summary_rows)
    daily = pd.DataFrame(daily_rows)

    if not summary.empty:
        summary["구분"] = summary["구분"].ffill()
        summary = summary.dropna(subset=["규격", "설계수량"], how="all")
        summary["진행률"] = np.where(summary["진행률"] <= 1, summary["진행률"] * 100, summary["진행률"])

    return summary, daily


def parse_drilling_file(uploaded_file):
    uploaded_file.seek(0)
    xls = pd.ExcelFile(uploaded_file)
    records = []

    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet, header=None)
        machine = clean_machine_name(sheet)
        machine_type = classify_machine_type(machine)
        current_zone_from_header = None

        for r in range(len(df)):
            row_text = " ".join([str(x) for x in df.iloc[r].tolist() if pd.notna(x)])
            zone_match = re.search(r"\(([A-E]\d+)\)", row_text)

            if "넘버링" in row_text and zone_match:
                current_zone_from_header = zone_match.group(1)

            try:
                col1 = df.iloc[r, 1] if df.shape[1] > 1 else np.nan
                col2 = df.iloc[r, 2] if df.shape[1] > 2 else np.nan
                design = df.iloc[r, 3] if df.shape[1] > 3 else np.nan
                actual = df.iloc[r, 8] if df.shape[1] > 8 else np.nan
                excess = df.iloc[r, 10] if df.shape[1] > 10 else np.nan
            except:
                continue

            zone = None
            hole_no = None

            if isinstance(col1, str) and re.fullmatch(r"[A-E]\d+", col1.strip()):
                zone = col1.strip()
                hole_no = col2
            elif current_zone_from_header is not None:
                zone = current_zone_from_header
                hole_no = col2

            if zone is None:
                continue

            hole_no = to_num(hole_no)
            design = to_num(design)
            actual = to_num(actual)
            excess = to_num(excess)

            if pd.isna(hole_no) or pd.isna(actual):
                continue

            status = "이상치" if actual <= 0 or actual > 30 else "정상"

            records.append({
                "장비유형": machine_type,
                "장비": machine,
                "시트": sheet,
                "구역": zone,
                "대구역": zone[0],
                "천공번호": int(hole_no),
                "설계심도": design,
                "시공심도": actual,
                "계획대비편차": excess,
                "상태": status
            })

    return pd.DataFrame(records)


def make_adjacent_comparison(drill_df):
    if drill_df.empty:
        return pd.DataFrame()

    valid = drill_df[(drill_df["상태"] == "정상") & (drill_df["장비유형"].isin(["삼축", "일축"]))].copy()

    agg = (
        valid.groupby(["장비유형", "구역", "대구역", "천공번호", "장비"], as_index=False)
        .agg(
            설계심도=("설계심도", "mean"),
            시공심도=("시공심도", "mean"),
            계획대비편차=("계획대비편차", "mean")
        )
    )

    cases = []

    for (machine_type, zone), g in agg.groupby(["장비유형", "구역"]):
        g = g.sort_values("천공번호")
        holes = sorted(g["천공번호"].unique())

        for i in range(len(holes) - 1):
            h1, h2 = holes[i], holes[i + 1]
            lefts = g[g["천공번호"] == h1]
            rights = g[g["천공번호"] == h2]

            for _, a in lefts.iterrows():
                for _, b in rights.iterrows():
                    if a["장비"] == b["장비"]:
                        continue
                    if a["장비유형"] != b["장비유형"]:
                        continue

                    diff = abs(a["시공심도"] - b["시공심도"])

                    cases.append({
                        "비교유형": f"{machine_type}끼리 비교",
                        "장비유형": machine_type,
                        "대구역": a["대구역"],
                        "구역": zone,
                        "천공번호1": h1,
                        "장비1": a["장비"],
                        "시공심도1": round(a["시공심도"], 2),
                        "천공번호2": h2,
                        "장비2": b["장비"],
                        "시공심도2": round(b["시공심도"], 2),
                        "심도차": round(diff, 2),
                        "검토등급": "주의" if diff >= 3 else ("관찰" if diff >= 2 else "보통")
                    })

    return pd.DataFrame(cases).sort_values("심도차", ascending=False) if cases else pd.DataFrame()


def format_num(x):
    try:
        return f"{float(x):,.1f}"
    except:
        return "-"


def create_ai_comment(summary, daily, drill_df, adjacent_df):
    comments = []

    if not summary.empty:
        total_design = summary["설계수량"].sum()
        total_done = summary["누계"].sum()
        total_remaining = summary["잔여량"].sum()
        progress = total_done / total_design * 100 if total_design > 0 else 0

        comments.append(
            f"공정 현황표 기준 총 설계수량 {format_num(total_design)} 대비 누계 {format_num(total_done)}가 완료되어 전체 진행률은 약 {progress:.1f}%입니다. 잔여 물량은 {format_num(total_remaining)}입니다."
        )

    if not daily.empty:
        daily2 = daily.copy()
        daily2["중층합계"] = daily2["CCM-T"] + daily2["CCM"]
        surface_avg = daily2.tail(7)["표층"].mean()
        middle_avg = daily2.tail(7)["중층합계"].mean()

        comments.append(
            f"최근 7개 작업일 기준 중층 평균 생산량은 약 {middle_avg:.1f}공/일, 표층 평균 생산량은 약 {surface_avg:.1f}㎡/일입니다."
        )

    if not adjacent_df.empty:
        top = adjacent_df.iloc[0]
        comments.append(
            f"천공일지 기준 동일 장비유형 내 인접 천공 최대 심도차는 {top['구역']} {top['천공번호1']}~{top['천공번호2']}번에서 {top['심도차']}m입니다."
        )

    if not comments:
        comments.append("업로드된 파일에서 분석 가능한 데이터를 찾지 못했습니다.")

    return "\n\n".join(comments)


with st.sidebar:
    if Path(LOGO_PATH).exists():
        st.markdown('<div class="logo-box">', unsafe_allow_html=True)
        st.image(LOGO_PATH, width=240)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.caption("로고 파일 없음: cj_logo.png")

    st.markdown("## 공정 분석 시스템")
    st.markdown("---")
    st.markdown("### 분석 항목")
    st.markdown("""
    <a class="side-nav" href="#upload-section">파일 업로드</a>
    <a class="side-nav" href="#status-summary">공정 현황 요약</a>
    <a class="side-nav" href="#progress-section">공종별 진행률</a>
    <a class="side-nav" href="#schedule-section">완료일 예측</a>
    <a class="side-nav" href="#daily-section">일자별 실적</a>
    <a class="side-nav" href="#drilling-section">천공 장비 분석</a>
    <a class="side-nav" href="#adjacent-section">장비 편차 분석</a>
    <a class="side-nav" href="#comment-section">종합 의견</a>
    <a class="side-nav" href="#download-section">데이터 다운로드</a>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="main-title">
AI 기반 지반개량 현황 분석 및<br>
공정 예측 시스템
</div>
""", unsafe_allow_html=True)
st.markdown('<div class="sub-title">지반개량공사 현황표와 CCM 천공일지를 기반으로 공정 현황, 생산성, 완료일, 장비 간 편차를 자동 분석합니다.</div>', unsafe_allow_html=True)

st.markdown("""
<div class="hero-card">
    <div class="hero-title">지반개량 공정 데이터를 업로드하세요</div>
    <div class="hero-desc">
        현황표와 천공일지를 함께 업로드하면 공정 진행률, 잔여 물량, 예상 완료일,
        장비별 시공심도, 동일 장비유형 내 인접 천공 편차를 한 번에 분석합니다.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div id="upload-section" class="anchor-offset"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="upload-panel">
    <div class="upload-title">분석 파일 업로드</div>
    <div class="upload-desc">
        아래 영역에 지반개량공사 현황표와 CCM 천공일지를 드래그앤드롭하거나 클릭하여 선택하세요.
        현황표만 업로드하면 공정률 분석만, 천공일지만 업로드하면 장비 편차 분석만 표시됩니다.
    </div>
    <span class="small-chip">현황표 XLSX</span>
    <span class="small-chip">천공일지 XLSX</span>
    <span class="small-chip">다중 파일 업로드 가능</span>
    <span class="small-chip">드래그앤드롭 지원</span>
</div>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "엑셀 파일을 여기에 드래그앤드롭하거나 클릭해서 업로드하세요",
    type=["xlsx"],
    accept_multiple_files=True,
    help="지반개량공사 현황표와 CCM 천공일지를 함께 업로드할 수 있습니다."
)

if not uploaded_files:
    st.info("먼저 엑셀 파일을 업로드하세요.")
    st.stop()

generate = st.button("분석 결과 생성하기", type="primary", use_container_width=True)

if not generate:
    st.warning("파일 업로드가 완료되었습니다. 위 버튼을 눌러 분석을 시작하세요.")
    st.stop()

with st.spinner("데이터를 분석하고 대시보드를 생성하는 중입니다..."):
    all_summary = []
    all_daily = []
    all_drill = []

    for file in uploaded_files:
        name = file.name

        try:
            summary, daily = parse_status_file(file)
            if not summary.empty:
                summary["파일명"] = name
                all_summary.append(summary)
            if not daily.empty:
                daily["파일명"] = name
                all_daily.append(daily)
        except:
            pass

        try:
            drill = parse_drilling_file(file)
            if not drill.empty:
                drill["파일명"] = name
                all_drill.append(drill)
        except:
            pass

    summary_df = pd.concat(all_summary, ignore_index=True) if all_summary else pd.DataFrame()
    daily_df = pd.concat(all_daily, ignore_index=True) if all_daily else pd.DataFrame()
    drill_df = pd.concat(all_drill, ignore_index=True) if all_drill else pd.DataFrame()
    adjacent_df = make_adjacent_comparison(drill_df)

has_status = not summary_df.empty or not daily_df.empty
has_drilling = not drill_df.empty

st.success("분석 결과가 생성되었습니다.")

if has_status:
    section_header("공정 현황 요약", "지반개량공사 현황표 기준으로 전체 진행률, 잔여 물량, 최근 생산성, 예상 완료일을 요약합니다.", "status-summary")

    with st.container(border=True):
        total_design = summary_df["설계수량"].sum() if not summary_df.empty else 0
        total_done = summary_df["누계"].sum() if not summary_df.empty else 0
        total_remaining = summary_df["잔여량"].sum() if not summary_df.empty else 0
        total_progress = total_done / total_design * 100 if total_design > 0 else 0

        expected_finish_text = "-"
        surface_recent_avg_text = "-"
        middle_recent_avg_text = "-"

        if not daily_df.empty:
            daily_df = daily_df.sort_values("날짜")
            daily_df["중층합계"] = daily_df["CCM-T"] + daily_df["CCM"]

            surface_recent_avg = daily_df.tail(7)["표층"].mean()
            middle_recent_avg = daily_df.tail(7)["중층합계"].mean()

            surface_recent_avg_text = f"{surface_recent_avg:,.1f}㎡/일"
            middle_recent_avg_text = f"{middle_recent_avg:,.1f}공/일"

            surface_summary = summary_df[summary_df["단위"].astype(str).str.contains("㎡", na=False)] if not summary_df.empty else pd.DataFrame()
            surface_remaining = surface_summary["잔여량"].sum() if not surface_summary.empty else total_remaining

            if surface_remaining > 0 and surface_recent_avg > 0:
                last_date = daily_df["날짜"].max()
                remain_days = surface_remaining / surface_recent_avg
                expected_finish = last_date + timedelta(days=int(np.ceil(remain_days)))
                expected_finish_text = expected_finish.strftime("%Y-%m-%d")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-title">전체 진행률</div><div class="metric-value">{total_progress:.1f}%</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><div class="metric-title">잔여 물량</div><div class="metric-value">{total_remaining:,.0f}</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><div class="metric-title">표층 최근 평균</div><div class="metric-value">{surface_recent_avg_text}</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="metric-card"><div class="metric-title">표층 예상 완료일</div><div class="metric-value">{expected_finish_text}</div></div>', unsafe_allow_html=True)

    section_header("1. 공종별 진행률", "공종별 설계수량 대비 누계 기준 진행률을 비교합니다.", "progress-section")
    with st.container(border=True):
        if not summary_df.empty:
            chart_df = summary_df.copy()
            chart_df["공종"] = chart_df["구분"].astype(str) + " " + chart_df["규격"].astype(str)

            fig = px.bar(
                chart_df,
                x="공종",
                y="진행률",
                color="구분",
                text=chart_df["진행률"].round(1),
                title="공종별 진행률"
            )
            fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig.update_layout(yaxis_title="진행률(%)", xaxis_title="공종")
            fig = apply_chart_style(fig)
            st.plotly_chart(fig, use_container_width=True)

            with st.expander("공정 현황 상세표 보기"):
                st.dataframe(
                    summary_df[["구분", "규격", "단위", "설계수량", "전일", "누계", "잔여량", "진행률"]],
                    use_container_width=True,
                    hide_index=True
                )

    section_header("2. 완료일 예측", "최근 작업 실적을 기준으로 표층 잔여 물량의 예상 완료일을 산정합니다.", "schedule-section")
    with st.container(border=True):
        if not daily_df.empty:
            c1, c2, c3 = st.columns(3)
            c1.metric("중층 최근 평균", middle_recent_avg_text)
            c2.metric("표층 최근 평균", surface_recent_avg_text)
            c3.metric("표층 기준 예상 완료일", expected_finish_text)
            st.caption("※ 중층은 공 단위, 표층은 ㎡ 단위로 산정되어 생산성 및 완료일 예측은 분리 해석합니다.")

    if not daily_df.empty:
        section_header("3. 일자별 작업 실적 추이", "중층과 표층은 단위가 다르므로 그래프를 분리하여 표시합니다.", "daily-section")
        left, right = st.columns(2)

        with left:
            with st.container(border=True):
                st.markdown("#### 중층 작업 실적")
                middle_df = daily_df[["날짜", "CCM-T", "CCM"]].copy()
                middle_df["중층 합계"] = middle_df["CCM-T"] + middle_df["CCM"]

                fig_middle = px.line(
                    middle_df,
                    x="날짜",
                    y=["CCM-T", "CCM", "중층 합계"],
                    markers=True,
                    title="중층 작업 실적 추이"
                )
                fig_middle.update_layout(yaxis_title="중층 실적(공)", xaxis_title="날짜")
                fig_middle = apply_chart_style(fig_middle)
                st.plotly_chart(fig_middle, use_container_width=True)

        with right:
            with st.container(border=True):
                st.markdown("#### 표층 작업 실적")
                surface_df = daily_df[["날짜", "표층"]].copy()

                fig_surface = px.bar(
                    surface_df,
                    x="날짜",
                    y="표층",
                    text="표층",
                    title="표층 작업 실적 추이"
                )
                fig_surface.update_traces(texttemplate="%{text:.0f}", textposition="outside")
                fig_surface.update_layout(yaxis_title="표층 실적(㎡)", xaxis_title="날짜")
                fig_surface = apply_chart_style(fig_surface)
                st.plotly_chart(fig_surface, use_container_width=True)

        with st.expander("일자별 실적 상세표 보기"):
            st.dataframe(daily_df, use_container_width=True, hide_index=True)

else:
    st.info("지반개량공사 현황표가 업로드되지 않았거나 인식되지 않아 공정률 관련 분석은 표시하지 않습니다.")

if has_drilling:
    section_header("4. CCM 천공일지 장비별 분석", "천공일지 기준 장비별 시공심도, 이상치, 구역별 천공 데이터를 분석합니다.", "drilling-section")

    with st.container(border=True):
        normal_df = drill_df[drill_df["상태"] == "정상"]

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("천공 데이터 수", f"{len(drill_df):,}")
        c2.metric("정상 데이터 수", f"{len(normal_df):,}")
        c3.metric("이상치 수", f"{len(drill_df) - len(normal_df):,}")
        c4.metric("평균 시공심도", f"{normal_df['시공심도'].mean():.2f}m")

        machine_summary = (
            normal_df.groupby(["장비유형", "장비"], as_index=False)
            .agg(
                천공수=("천공번호", "count"),
                평균설계심도=("설계심도", "mean"),
                평균시공심도=("시공심도", "mean"),
                평균편차=("계획대비편차", "mean")
            )
            .sort_values(["장비유형", "천공수"], ascending=[True, False])
        )

        left, right = st.columns(2)

        with left:
            fig3 = px.bar(
                machine_summary,
                x="장비",
                y="평균시공심도",
                color="장비유형",
                text=machine_summary["평균시공심도"].round(2),
                title="장비별 평균 시공심도"
            )
            fig3.update_layout(yaxis_title="평균 시공심도(m)", xaxis_title="장비")
            fig3 = apply_chart_style(fig3)
            st.plotly_chart(fig3, use_container_width=True)

        with right:
            zone_count = (
                normal_df.groupby(["장비유형", "대구역"], as_index=False)
                .agg(천공수=("천공번호", "count"), 평균시공심도=("시공심도", "mean"))
            )

            fig4 = px.bar(
                zone_count,
                x="대구역",
                y="천공수",
                color="장비유형",
                text="천공수",
                title="구역별 천공 데이터 수"
            )
            fig4.update_layout(yaxis_title="천공 데이터 수", xaxis_title="구역")
            fig4 = apply_chart_style(fig4)
            st.plotly_chart(fig4, use_container_width=True)

        with st.expander("천공 장비별 상세표 보기"):
            st.dataframe(machine_summary.round(2), use_container_width=True, hide_index=True)

    section_header("5. 동일 장비유형 인접 천공 TOP 10", "삼축은 삼축끼리, 일축은 일축끼리만 비교하며 삼축↔일축 비교는 제외합니다.", "adjacent-section")

    with st.container(border=True):
        if not adjacent_df.empty:
            max_depth_diff = adjacent_df["심도차"].max()

            if max_depth_diff >= 3:
                st.markdown(f'<div class="status-risk">주의: 동일 장비유형 내 인접 천공 장비 간 최대 심도차가 {max_depth_diff:.2f}m로 확인되었습니다.</div>', unsafe_allow_html=True)
            elif max_depth_diff >= 2:
                st.markdown(f'<div class="status-watch">관찰: 동일 장비유형 내 인접 천공 장비 간 심도차가 일부 확인됩니다.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-good">양호: 동일 장비유형 내 장비 간 편차가 관리 가능한 수준입니다.</div>', unsafe_allow_html=True)

            top_cases = adjacent_df.head(10).copy()
            top_cases["비교구간"] = top_cases.apply(lambda x: f"{x['구역']} {x['천공번호1']}~{x['천공번호2']}", axis=1)
            top_cases["장비비교"] = top_cases.apply(lambda x: f"{x['장비1']} ↔ {x['장비2']}", axis=1)

            c1, c2, c3 = st.columns(3)
            c1.metric("동일유형 인접 비교", f"{len(adjacent_df):,}건")
            c2.metric("평균 심도차", f"{adjacent_df['심도차'].mean():.2f}m")
            c3.metric("최대 심도차", f"{adjacent_df['심도차'].max():.2f}m")

            st.dataframe(
                top_cases[["비교유형", "비교구간", "장비비교", "시공심도1", "시공심도2", "심도차", "검토등급"]],
                use_container_width=True,
                hide_index=True
            )

            fig5 = px.bar(
                top_cases.sort_values("심도차"),
                x="심도차",
                y="비교구간",
                color="장비유형",
                orientation="h",
                title="동일 장비유형 인접 천공 심도차 TOP 10"
            )
            fig5.update_layout(xaxis_title="시공심도 차이(m)", yaxis_title="천공 구간")
            fig5 = apply_chart_style(fig5)
            st.plotly_chart(fig5, use_container_width=True)

            type_summary = (
                adjacent_df.groupby("장비유형", as_index=False)
                .agg(
                    비교사례수=("심도차", "count"),
                    평균심도차=("심도차", "mean"),
                    최대심도차=("심도차", "max"),
                    주의사례수=("검토등급", lambda s: (s == "주의").sum())
                )
                .sort_values("최대심도차", ascending=False)
            )

            area_summary = (
                adjacent_df.groupby(["장비유형", "대구역"], as_index=False)
                .agg(
                    비교사례수=("심도차", "count"),
                    평균심도차=("심도차", "mean"),
                    최대심도차=("심도차", "max"),
                    주의사례수=("검토등급", lambda s: (s == "주의").sum())
                )
                .sort_values("최대심도차", ascending=False)
            )

            with st.expander("장비유형별 편차 요약 보기"):
                st.dataframe(type_summary.round(2), use_container_width=True, hide_index=True)

            with st.expander("구역별 인접 장비 편차 요약 보기"):
                st.dataframe(area_summary.round(2), use_container_width=True, hide_index=True)

            with st.expander("인접 천공 장비 비교 전체 목록 보기"):
                st.dataframe(adjacent_df, use_container_width=True, hide_index=True)

        else:
            st.info("동일 장비유형 내 서로 다른 장비가 인접 천공번호를 시공한 비교 사례를 찾지 못했습니다.")

else:
    st.info("CCM 천공일지가 업로드되지 않았거나 인식되지 않아 장비 간 편차 분석은 표시하지 않습니다.")

section_header("6. AI 종합 분석 의견", "업로드된 데이터 기준으로 공정 현황과 천공 편차를 종합 요약합니다.", "comment-section")
with st.container(border=True):
    st.write(create_ai_comment(summary_df, daily_df, drill_df, adjacent_df))

section_header("7. 데이터 다운로드", "분석 결과를 CSV 파일로 저장하여 후속 보고서 작성에 활용할 수 있습니다.", "download-section")
with st.container(border=True):
    if has_status and not summary_df.empty:
        st.download_button(
            "공정 현황 요약 CSV 다운로드",
            summary_df.to_csv(index=False).encode("utf-8-sig"),
            file_name="공정현황_요약.csv",
            mime="text/csv"
        )

    if has_drilling and not adjacent_df.empty:
        st.download_button(
            "동일유형 인접 천공 비교 CSV 다운로드",
            adjacent_df.to_csv(index=False).encode("utf-8-sig"),
            file_name="동일유형_인접천공_장비비교.csv",
            mime="text/csv"
        )
