import streamlit as st

# Lista slajdów
slides = [
    {"title": "Slajd 1", "image": "1-png.png", "text": "Opis slajdu 1"},
    {"title": "Slajd 2", "image": "2-png.png", "text": "Opis slajdu 2"},
    {"title": "Slajd 3", "image": "3-png.png", "text": "Opis slajdu 3"},
]

# Inicjalizacja stanu sesji
if 'slide_index' not in st.session_state:
    st.session_state.slide_index = 0

# Funkcje obsługujące przejścia między slajdami
def next_slide():
    if st.session_state.slide_index < len(slides) - 1:
        st.session_state.slide_index += 1

def previous_slide():
    if st.session_state.slide_index > 0:
        st.session_state.slide_index -= 1

# Wyświetlanie slajdu
slide = slides[st.session_state.slide_index]
st.title(slide["title"])
st.image(slide["image"], caption=slide["title"])
st.markdown(slide["text"])

# Przyciski nawigacyjne
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Wstecz"):
        previous_slide()
with col2:
    if st.button("Dalej"):
        next_slide()
