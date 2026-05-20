import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import re
from datetime import timedelta

st.set_page_config(
    page_title="지반개량 현황 분석 및 공정 예측 시스템",
    layout="wide"
)

st.title("AI 기반 지반개량 현황 분석 및 공정 예측 시스템")
st.caption("지반개량공사 현황표와 CCM 천공일지를 업로드하면 진행률, 잔여 물량, 예상 완료일, 장비 간 시공 편차를 자동 분석합니다.")

def to_num(x):
    return pd.to_numeric(x, errors="coerce")

def clean_machine_name(sheet_name):
    name = str(sheet_name).strip()
    name = name.replace("천공일지", "").replace("작업일지", "")
    name = name.replace("(", " (").replace(")", ")")
    return name

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
                    start = i + 1
                    for r in range(start, len(df)):
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
        summary["진행률"] = np.where(
            summary["진행률"] <= 1,
            summary["진행률"] * 100,
            summary["진행률"]
        )

    return summary, daily

def parse_drilling_file(uploaded_file):
    uploaded_file.seek(0)
    xls = pd.ExcelFile(uploaded_file)
    records = []

    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet, header=None)
        machine = clean_machine_name(sheet)
        current_zone_from_header = None

        for r in range(len(df)):
            row_text = " ".join([str(x) for x in df.iloc[r].tolist() if pd.notna(x)])

            zone_match = re.search(r"\(([A-E]\d+)\)", row_text)
            if "넘버링" in row_text and zone_match:
                current_zone_from_header = zone_match.group(1)

            try:
                col0 = df.iloc[r, 0]
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

            if actual <= 0 or actual > 30:
                status = "이상치"
            else:
                status = "정상"

            records.append({
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

    valid = drill_df[drill_df["상태"] == "정상"].copy()

    agg = (
        valid.groupby(["구역", "대구역", "천공번호", "장비"], as_index=False)
        .agg(
            설계심도=("설계심도", "mean"),
            시공심도=("시공심도", "mean"),
            계획대비편차=("계획대비편차", "mean")
        )
    )

    cases = []

    for zone, g in agg.groupby("구역"):
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

                    diff = abs(a["시공심도"] - b["시공심도"])

                    cases.append({
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
            f"현재 지반개량 공정은 총 설계수량 {format_num(total_design)} 대비 누계 {format_num(total_done)}가 완료되어 전체 진행률은 약 {progress:.1f}%입니다. 잔여 물량은 {format_num(total_remaining)}입니다."
        )

        low = summary.sort_values("진행률").head(1)
        if not low.empty:
            row = low.iloc[0]
            comments.append(
                f"공종별로는 {row['구분']} {row['규격']} 항목의 진행률이 {row['진행률']:.1f}%로 상대적으로 낮아 우선 관리 대상입니다."
            )

    if not daily.empty:
        daily2 = daily.copy()
        daily2["합계"] = daily2[["CCM-T", "CCM", "표층"]].sum(axis=1)
        recent = daily2.tail(7)
        avg_prod = recent["합계"].mean()
        comments.append(
            f"최근 실적 기준 일평균 생산량은 약 {avg_prod:.1f} 단위/일 수준입니다. 잔여 물량과 최근 생산성을 함께 검토하여 장비 투입계획을 조정할 필요가 있습니다."
        )

    if not adjacent_df.empty:
        top = adjacent_df.iloc[0]
        comments.append(
            f"천공일지 기준 서로 다른 장비가 인접 천공을 수행한 사례 중 최대 심도차는 {top['구역']} {top['천공번호1']}~{top['천공번호2']}번에서 {top['심도차']}m로 확인되었습니다. 해당 구간은 장비별 시공 조건 차이 또는 지반 조건 차이를 검토할 필요가 있습니다."
        )

    if not comments:
        comments.append("업로드된 파일에서 분석 가능한 데이터를 찾지 못했습니다. 파일 형식 또는 시트 구조 확인이 필요합니다.")

    return "\n\n".join(comments)

uploaded_files = st.file_uploader(
    "분석할 엑셀 파일을 업로드하세요. 지반개량공사현황 파일과 CCM천공일지 파일을 함께 올릴 수 있습니다.",
    type=["xlsx"],
    accept_multiple_files=True
)

if not uploaded_files:
    st.info("엑셀 파일을 업로드하면 대시보드가 자동 생성됩니다.")
    st.stop()

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
    except Exception as e:
        pass

    try:
        drill = parse_drilling_file(file)
        if not drill.empty:
            drill["파일명"] = name
            all_drill.append(drill)
    except Exception as e:
        pass

summary_df = pd.concat(all_summary, ignore_index=True) if all_summary else pd.DataFrame()
daily_df = pd.concat(all_daily, ignore_index=True) if all_daily else pd.DataFrame()
drill_df = pd.concat(all_drill, ignore_index=True) if all_drill else pd.DataFrame()
adjacent_df = make_adjacent_comparison(drill_df)

st.divider()

st.subheader("1. 공정 현황 요약")

if not summary_df.empty:
    total_design = summary_df["설계수량"].sum()
    total_done = summary_df["누계"].sum()
    total_remaining = summary_df["잔여량"].sum()
    total_progress = total_done / total_design * 100 if total_design > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("전체 진행률", f"{total_progress:.1f}%")
    col2.metric("총 설계수량", f"{total_design:,.1f}")
    col3.metric("누계 완료", f"{total_done:,.1f}")
    col4.metric("잔여 물량", f"{total_remaining:,.1f}")

    st.dataframe(
        summary_df[["구분", "규격", "단위", "설계수량", "전일", "누계", "잔여량", "진행률"]],
        use_container_width=True
    )

    fig = px.bar(
        summary_df,
        x="규격",
        y="진행률",
        color="구분",
        text=summary_df["진행률"].round(1),
        title="공종별 진행률"
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(yaxis_title="진행률(%)", xaxis_title="공종")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("지반개량공사 현황표 데이터를 찾지 못했습니다.")

st.divider()

st.subheader("2. 일자별 생산성 및 완료일 예측")

if not daily_df.empty:
    daily_df = daily_df.sort_values("날짜")
    daily_df["합계"] = daily_df[["CCM-T", "CCM", "표층"]].sum(axis=1)

    recent_avg = daily_df.tail(7)["합계"].mean()
    last_date = daily_df["날짜"].max()

    if not summary_df.empty:
        remaining = summary_df["잔여량"].sum()
        remain_days = remaining / recent_avg if recent_avg > 0 else np.nan
        expected_finish = last_date + timedelta(days=int(np.ceil(remain_days))) if pd.notna(remain_days) else None
    else:
        remaining = np.nan
        remain_days = np.nan
        expected_finish = None

    c1, c2, c3 = st.columns(3)
    c1.metric("최근 7개 작업일 평균 생산량", f"{recent_avg:,.1f}")
    c2.metric("예상 잔여일", "-" if pd.isna(remain_days) else f"{remain_days:.1f}일")
    c3.metric("예상 완료일", "-" if expected_finish is None else expected_finish.strftime("%Y-%m-%d"))

  st.markdown("#### 일자별 작업 실적 추이")

left, right = st.columns(2)

with left:
    st.markdown("##### 중층 작업 실적")
    middle_df = daily_df[["날짜", "CCM-T", "CCM"]].copy()
    middle_df["중층 합계"] = middle_df["CCM-T"] + middle_df["CCM"]

    fig_middle = px.line(
        middle_df,
        x="날짜",
        y=["CCM-T", "CCM", "중층 합계"],
        markers=True,
        title="중층 작업 실적 추이"
    )
    fig_middle.update_layout(
        yaxis_title="중층 실적(공)",
        xaxis_title="날짜"
    )
    st.plotly_chart(fig_middle, use_container_width=True)

with right:
    st.markdown("##### 표층 작업 실적")
    surface_df = daily_df[["날짜", "표층"]].copy()

    fig_surface = px.bar(
        surface_df,
        x="날짜",
        y="표층",
        text="표층",
        title="표층 작업 실적 추이"
    )
    fig_surface.update_traces(texttemplate="%{text:.0f}", textposition="outside")
    fig_surface.update_layout(
        yaxis_title="표층 실적(㎡)",
        xaxis_title="날짜"
    )
    st.plotly_chart(fig_surface, use_container_width=True)

    st.dataframe(daily_df, use_container_width=True)

else:
    st.warning("일자별 실적 데이터를 찾지 못했습니다.")

st.divider()

st.subheader("3. CCM 천공일지 장비별 분석")

if not drill_df.empty:
    normal_df = drill_df[drill_df["상태"] == "정상"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("천공 데이터 수", f"{len(drill_df):,}")
    c2.metric("정상 데이터 수", f"{len(normal_df):,}")
    c3.metric("이상치 수", f"{len(drill_df) - len(normal_df):,}")
    c4.metric("평균 시공심도", f"{normal_df['시공심도'].mean():.2f}m")

    machine_summary = (
        normal_df.groupby("장비", as_index=False)
        .agg(
            천공수=("천공번호", "count"),
            평균설계심도=("설계심도", "mean"),
            평균시공심도=("시공심도", "mean"),
            평균편차=("계획대비편차", "mean")
        )
        .sort_values("천공수", ascending=False)
    )

    st.dataframe(machine_summary.round(2), use_container_width=True)

    fig3 = px.bar(
        machine_summary,
        x="장비",
        y="평균시공심도",
        text=machine_summary["평균시공심도"].round(2),
        title="장비별 평균 시공심도"
    )
    fig3.update_layout(yaxis_title="평균 시공심도(m)", xaxis_title="장비")
    st.plotly_chart(fig3, use_container_width=True)

    zone_count = (
        normal_df.groupby("대구역", as_index=False)
        .agg(천공수=("천공번호", "count"), 평균시공심도=("시공심도", "mean"))
    )

    fig4 = px.bar(
        zone_count,
        x="대구역",
        y="천공수",
        text="천공수",
        title="구역별 천공 데이터 수"
    )
    st.plotly_chart(fig4, use_container_width=True)

else:
    st.warning("CCM 천공일지 데이터를 찾지 못했습니다.")

st.divider()

st.subheader("4. 인접 천공 장비 간 시공심도 차이")

if not adjacent_df.empty:
    c1, c2, c3 = st.columns(3)
    c1.metric("서로 다른 장비 인접 비교 사례", f"{len(adjacent_df):,}")
    c2.metric("평균 심도차", f"{adjacent_df['심도차'].mean():.2f}m")
    c3.metric("최대 심도차", f"{adjacent_df['심도차'].max():.2f}m")

    top_n = st.slider("표시할 상위 편차 사례 수", min_value=5, max_value=50, value=15)

    st.dataframe(
        adjacent_df.head(top_n),
        use_container_width=True
    )

    fig5 = px.bar(
        adjacent_df.head(top_n).sort_values("심도차"),
        x="심도차",
        y=adjacent_df.head(top_n).sort_values("심도차").apply(
            lambda x: f"{x['구역']} {x['천공번호1']}~{x['천공번호2']}", axis=1
        ),
        color="검토등급",
        orientation="h",
        title="인접 천공 장비 간 심도차 TOP 사례"
    )
    fig5.update_layout(xaxis_title="시공심도 차이(m)", yaxis_title="천공 구간")
    st.plotly_chart(fig5, use_container_width=True)

    area_summary = (
        adjacent_df.groupby("대구역", as_index=False)
        .agg(
            비교사례수=("심도차", "count"),
            평균심도차=("심도차", "mean"),
            최대심도차=("심도차", "max"),
            주의사례수=("검토등급", lambda s: (s == "주의").sum())
        )
        .sort_values("최대심도차", ascending=False)
    )

    st.markdown("#### 구역별 인접 장비 편차 요약")
    st.dataframe(area_summary.round(2), use_container_width=True)

else:
    st.info("서로 다른 장비가 인접 천공번호를 시공한 비교 사례를 찾지 못했습니다.")

st.divider()

st.subheader("5. AI 종합 분석 의견")

st.write(create_ai_comment(summary_df, daily_df, drill_df, adjacent_df))

st.divider()

st.subheader("6. 데이터 다운로드")

if not summary_df.empty:
    st.download_button(
        "공정 현황 요약 CSV 다운로드",
        summary_df.to_csv(index=False).encode("utf-8-sig"),
        file_name="공정현황_요약.csv",
        mime="text/csv"
    )

if not adjacent_df.empty:
    st.download_button(
        "인접 천공 장비 비교 CSV 다운로드",
        adjacent_df.to_csv(index=False).encode("utf-8-sig"),
        file_name="인접천공_장비비교.csv",
        mime="text/csv"
    )
