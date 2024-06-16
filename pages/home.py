import streamlit as st

st.title("Home Page")
st.write("Welcome to the Home Page!")

st.page_link("app.py", label="Home", icon="🏠")
st.page_link("pages/traffic1.py", label="회선 트래픽 분석")
