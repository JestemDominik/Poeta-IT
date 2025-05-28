import streamlit as st
from openai import OpenAI
import os

#Required functions
def get_openai_client():
    return OpenAI(api_key = st.session_state['openai_api_key'])

#
## MAIN 
#
st.title('Zostań poetą IT!')
st.header('napisz wiersz na podstawie swojego kodu')

if not st.session_state.get('openai_api_key'):
    st.warning("Dodaj swój klucz API OpenAI")
    st.session_state["openai_api_key"] = st.text_input("Klucz API OpenAI", type="password")
    if st.button('Zatwierdź'):
        st.rerun()

if not st.session_state.get('openai_api_key'):
    st.stop()

user_code = st.text_area("Wpisz swój kod:")
autor = st.selectbox('Wybierz autora wiersza', ['William Shekspere', 'Homer', 'Adam Mickiewicz', 'Juliusz Słowacki'])
format1 = st.selectbox('Wybierz format wiersza', ['Ballada', 'Epos', 'Wiersz wolny', 'Sonet'])

prompt = f"Napisz krótki wiersz na podstawie tego kodu:\n{user_code}\nNapisz go tak, jakby autorem był: {autor}.\nFormat wiersza to: {format1}."


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
    if st.button("Zapisz ten wiersz"):
        st.session_state['saved_poems'].append({
            'autor': autor,
            'format': format1,
            'text': st.session_state['poem'],
            'audio': st.session_state.get('audio_path', None)
        })
        st.sidebar.success("✅ Wiersz zapisany!")

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


with st.sidebar.title("📚 Twoja sztuka"):
    if 'saved_poems' not in st.session_state:
        st.session_state['saved_poems'] = []

    # Wyświetl listę zapisanych wierszy
    for i, poem_data in enumerate(st.session_state['saved_poems']):
        with st.sidebar.expander(f"{i+1}. {poem_data['autor']} – {poem_data['format']}"):
            st.write(poem_data['text'])
            if poem_data['audio'] and os.path.exists(poem_data['audio']):
                st.audio(poem_data['audio'])

