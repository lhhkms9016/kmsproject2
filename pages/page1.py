import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import xlwings as xw
import tempfile
import os

st.title("Page 1")
st.write("This is Page 1")

# 사이드바에 입력 위젯 추가
st.sidebar.header("조회조건")

# 날짜 선택 위젯을 나란히 배치
col1, col2 = st.sidebar.columns(2)
start_date = col1.date_input("Start date", pd.to_datetime("2023-01-01"), key='start_date')
end_date = col2.date_input("End date", pd.to_datetime("2023-12-31"), key='end_date')

# 데이터프레임 생성
date_range = pd.date_range(start="2023-01-01", end="2023-12-31")
values = np.random.randint(10000, 100000, size=len(date_range))
data = pd.DataFrame({'date': date_range, 'value': values})

# 선택한 날짜 범위에 따른 데이터 필터링
filtered_data = data[(data['date'] >= pd.to_datetime(start_date)) & (data['date'] <= pd.to_datetime(end_date))]

# 데이터프레임 표시
st.write(filtered_data)

# Altair 차트 생성
chart = alt.Chart(filtered_data).mark_line().encode(
    x=alt.X('date:T', axis=alt.Axis(format='%Y-%m-%d', title='date')),
    y='value:Q'
).properties(
    title='Value over Time'
)

# 차트 표시
st.altair_chart(chart, use_container_width=True)

# 사이드바에 버튼 추가
if st.sidebar.button("Result", key='result_button'):
    # 템포러리 디렉토리에서 작업
    with tempfile.TemporaryDirectory() as tmpdir:
        excel_file_path = os.path.join(tmpdir, "result.xlsx")
        chart_path = os.path.join(tmpdir, "chart.png")
        
        # Altair 차트를 이미지로 저장
        chart.save(chart_path)
        
        # 엑셀 파일 생성 및 데이터프레임 저장
        try:
            with xw.App(visible=False) as app:
                wb = app.books.add()
                ws = wb.sheets[0]
                ws.name = "Result"
                ws.range("A1").value = filtered_data
                
                # 이미지 파일 존재 여부 확인
                if os.path.exists(chart_path):
                    ws.pictures.add(chart_path, name='Chart', update=True, left=ws.range('E2').left, top=ws.range('E2').top)
                
                # 엑셀 파일 저장
                wb.save(excel_file_path)
                wb.close()
                
                # 사용자에게 다운로드 링크 제공
                with open(excel_file_path, "rb") as file:
                    st.download_button(label="Download Excel File", data=file, file_name="result.xlsx")
        
        except Exception as e:
            st.error(f"An error occurred: {e}")
