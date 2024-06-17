import streamlit as st
from pages.traffic1 import traffic1

def main():

    # 세션 상태 초기화
    if 'page' not in st.session_state:
        st.session_state.page = 'Home'

    # 사이드바에 입력 위젯 추가
    st.sidebar.title("Menu")
    page = st.sidebar.selectbox("Select a page", ["Home", "Traffic_1"], index=0)

    # 선택된 페이지에 따라 세션 상태 업데이트
    st.session_state.page = page

    # 선택된 페이지에 따라 다른 스크립트 실행
    if page == "Home":
        st.write("여기는 메인 페이지입니다.")
    elif page == "Traffic_1":
        traffic1()

if __name__ == '__main__':
    main()
