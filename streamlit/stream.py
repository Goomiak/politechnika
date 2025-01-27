import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import base64

# Funkcja do konwersji obrazu na link HTML
def get_image_download_link(img, key):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="javascript:document.getElementById(\'{key}\').click();"><img src="data:image/png;base64,{img_str}" width="200"></a>'
    return href

def main():
    st.title("Edukacyjna Aplikacja Streamlit")
    
    # Wczytywanie ikonek
    icons = ["1-png.png", "2-png.png", "3-png.png"]
    icon_images = [Image.open(icon) for icon in icons]

    # Tworzenie kolumn dla ikonek
    col1, col2, col3 = st.columns(3)

    # Przekierowanie po kliknięciu na ikonę
    with col1:
        if st.button("", key="icon1"):
            st.session_state['module'] = 1
        st.markdown(get_image_download_link(icon_images[0], "icon1"), unsafe_allow_html=True)

    with col2:
        if st.button("", key="icon2"):
            st.session_state['module'] = 2
        st.markdown(get_image_download_link(icon_images[1], "icon2"), unsafe_allow_html=True)

    with col3:
        if st.button("", key="icon3"):
            st.session_state['module'] = 3
        st.markdown(get_image_download_link(icon_images[2], "icon3"), unsafe_allow_html=True)

    # Przeniesienie do poszczególnych modułów
    if 'module' in st.session_state:
        if st.session_state['module'] == 1:
            module_one()
        elif st.session_state['module'] == 2:
            module_two()
        elif st.session_state['module'] == 3:
            module_three()

def module_one():
    st.header("Moduł Edukacyjny 1")
    st.write("Tutaj znajduje się opis pierwszego modułu edukacyjnego.")
    interactive_plot()

def module_two():
    st.header("Moduł Edukacyjny 2")
    st.write("Tutaj znajduje się opis drugiego modułu edukacyjnego.")
    interactive_plot()

def module_three():
    st.header("Moduł Edukacyjny 3")
    st.write("Tutaj znajduje się opis trzeciego modułu edukacyjnego.")
    interactive_plot()

def interactive_plot():
    st.write("Interaktywna symulacja:")
    
    # Parametry suwaków
    a = st.slider("Parametr a", 0.1, 10.0, 1.0)
    b = st.slider("Parametr b", 0.1, 10.0, 2.0)
    
    # Tworzenie wykresu
    x = np.linspace(0, 10, 100)
    y = a * np.sin(b * x)
    
    fig, ax = plt.subplots()
    ax.plot(x, y)
    st.pyplot(fig)

if __name__ == "__main__":
    if 'module' not in st.session_state:
        st.session_state['module'] = 0
    main()
