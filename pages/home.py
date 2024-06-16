import streamlit as st

st.title("Home Page")
st.write("Welcome to the Home Page!")

st.page_link("customer1.py", label="Home", icon="🏠")
st.page_link("pages/Traffic_회선.py", label="회선 트래픽 분석")
