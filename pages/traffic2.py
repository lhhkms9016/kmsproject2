import streamlit as st
import sqlite3
import pandas as pd

# 데이터베이스 초기화 함수
def init_db():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS entries
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, content1 TEXT, content2 TEXT, image_url TEXT)''')
    conn.commit()
    conn.close()

# 데이터베이스에 값 삽입 함수
def insert_entry(content1, content2, image_url):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("INSERT INTO entries (content1, content2, image_url) VALUES (?, ?, ?)", (content1, content2, image_url))
    conn.commit()
    conn.close()

# 데이터베이스에서 조건에 맞는 항목 조회 함수
def get_matching_entries(content1):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    query = "SELECT * FROM entries WHERE 1=1 AND content1 = ?"
    c.execute(query, (content1,))
    rows = c.fetchall()
    conn.close()
    return rows

# 데이터베이스에서 모든 항목 조회 함수
def get_all_entries():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("SELECT * FROM entries")
    rows = c.fetchall()
    conn.close()
    return rows

# 데이터베이스에서 항목 삭제 함수
def delete_entry(entry_id):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()

def app():
    st.title('Streamlit과 SQLite 예제')

    # 초기화 함수 호출
    init_db()

    # 모든 항목을 테이블로 표시
    all_entries = get_all_entries()
    if all_entries:
        df = pd.DataFrame(all_entries, columns=['ID', 'Content1', 'Content2', 'Image URL'])
        st.table(df)
    else:
        st.write('저장된 값이 없습니다.')

    st.write('텍스트 박스에 값을 입력하고, 버튼을 누르면 값이 데이터베이스에 저장됩니다.')

    # 텍스트 박스와 버튼
    user_input1 = st.text_input('값을 입력하세요 (컬럼 1):')
    user_input2 = st.text_input('값을 입력하세요 (컬럼 2):')
    user_input3 = st.text_input('이미지 URL을 입력하세요 (컬럼 3):')  # 새로운 텍스트 박스 추가
    if st.button('저장'):
        if user_input1 and user_input2 and user_input3:
            insert_entry(user_input1, user_input2, user_input3)
            st.success('값이 성공적으로 저장되었습니다.')
            st.experimental_rerun()  # 저장 후 페이지를 다시 로드하여 테이블 업데이트
        else:
            st.error('모든 값을 입력하세요.')

    # 저장된 항목 조회
    if st.button('조회'):
        if user_input1:
            entries = get_matching_entries(user_input1)
            if entries:
                st.write('저장된 값:')
                for entry in entries:
                    st.write(f"ID: {entry[0]} - 컬럼 1: {entry[1]}, 컬럼 2: {entry[2]}, 이미지 URL: {entry[3]}")
                    if entry[3]:  # 이미지 URL이 있으면 이미지를 표시
                        st.image(entry[3], caption=f"ID: {entry[0]}")
            else:
                st.write('매칭되는 값이 없습니다.')
        else:
            st.error('조회할 값을 입력하세요 (컬럼 1).')

    # 항목 삭제
    entry_id_to_delete = st.text_input('삭제할 항목의 ID를 입력하세요:')
    if st.button('삭제'):
        if entry_id_to_delete:
            delete_entry(entry_id_to_delete)
            st.success(f'ID {entry_id_to_delete} 항목이 성공적으로 삭제되었습니다.')
            st.experimental_rerun()  # 삭제 후 페이지를 다시 로드하여 테이블 업데이트
        else:
            st.error('삭제할 항목의 ID를 입력하세요.')

if __name__ == "__main__":
    app()
