import streamlit as st

st.title("Home Page")
st.write("Welcome to the Home Page!")

st.page_link("customer1.py", label="Home", icon="🏠")
st.page_link("pages/page1.py", label="Page 1", icon="1️⃣")
st.page_link("pages/page2.py", label="회선 트래픽 분석")
