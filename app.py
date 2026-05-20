import streamlit as st

st.set_page_config(page_title="지반개량 공정 분석 시스템", layout="wide")

st.title("AI 기반 지반개량 현황 분석 및 공정 예측 시스템")

st.write("파일 업로드 후 지반개량 현황과 공정 예측 결과를 대시보드로 확인합니다.")

uploaded_file = st.file_uploader("지반개량 현황표 또는 천공일지 엑셀 파일을 업로드하세요", type=["xlsx"])

if uploaded_file:
    st.success("파일 업로드 완료")
    st.write("다음 단계에서 실제 분석 기능을 연결합니다.")
