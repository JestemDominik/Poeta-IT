import streamlit as st
from openai import OpenAI
import os
# from qdrant_client import QdrantClient
# import sqlite3


def get_openai_client():
    return OpenAI(api_key = st.session_state['openai_api_key'])

# DATABASE
# def init_db():
#     conn = sqlite3.connect("quadrant.db")
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS notes (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             content TEXT NOT NULL,
#             author TEXT,
#             format TEXT
#         )
#     ''')
#     conn.commit()
#     conn.close()

# def add_note_to_db(content, author, format_):
#     conn = sqlite3.connect("quadrant.db")
#     cursor = conn.cursor()
#     cursor.execute('''
#         INSERT INTO notes (content, author, format)
#         VALUES (?, ?, ?, ?)
#     ''', (content, author, format_))
#     conn.commit()
#     conn.close()

# def get_all_notes():
#     conn = sqlite3.connect("quadrant.db")
#     cursor = conn.cursor()
#     cursor.execute('SELECT id, content, author, format, created_at FROM notes')
#     notes = cursor.fetchall()
#     conn.close()
#     return notes

st.title('Zostań poetą IT!')
st.header('napisz wiersz na podstawie swojego kodu')

user_code = st.text_area("Wpisz swój kod:")
autor = st.selectbox('Wybierz autora wiersza', ['William Shekspere', 'Homer', 'Adam Mickiewicz', 'Juliusz Słowacki'])
format1 = st.selectbox('Wybierz format wiersza', ['Ballada', 'Epos', 'Wiersz wolny', 'Sonet'])

prompt = f"Napisz krótki wiersz na podstawie tego kodu:\n{user_code}\nNapisz go tak, jakby autorem był: {autor}.\nFormat wiersza to: {format1}."


if not st.session_state.get('openai_api_key'):
    st.session_state["openai_api_key"] = st.text_input("Klucz API OpenAI", type="password")
    st.stop()


if st.button('Napisz wiersz!:lower_left_fountain_pen:'):
    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Jesteś poetą programistą."},
            {"role": "user", "content": prompt}
        ]
    )
    st.session_state['poem'] = response.choices[0].message.content

if 'poem' in st.session_state:
    st.markdown("### Wiersz:")
    st.write(st.session_state['poem'])
    num_chars = len(st.session_state['poem'])
    cost = (num_chars / 1000) * 0.015
    st.write(f"💰 Szacowany koszt przeczytania wiersza: **${round(cost, 4)}**")

# Funkcja do generowania mowy
def generate_speech(text, voice, output_audio_path):
    client = get_openai_client()
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        response_format="mp3",
        input=text,
    )
    with open(output_audio_path, "wb") as f:
        f.write(response.content)
    return output_audio_path

# Generowanie głosu
if st.button('Przeczytaj wiersz!'):
    if 'poem' not in st.session_state:
        st.warning("Najpierw wygeneruj wiersz.")
    else:
        path = generate_speech(
            text=st.session_state['poem'],
            voice="onyx",
            output_audio_path="wiersz.mp3",
        )
        st.audio(path)
