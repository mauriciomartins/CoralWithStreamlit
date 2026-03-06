import streamlit as st
import re
import requests
import urllib3
from io import BytesIO
import pandas as pd

# =====================================================
# DATA LOADING
# =====================================================

sheet_id = st.secrets["SHEET_ID"]
gid = st.secrets["SHEET_GID"]
base_url = st.secrets["GOOGLE_SHEET_BASE"]

# montar url csv
DATA_URL = f"{base_url}/{sheet_id}/export?format=xlsx&gid={gid}"

# DATA_URL = "https://docs.google.com/spreadsheets/d/1o2ujjDwoHe1lybuOQ54TRrP-jK-cZs8U6glL4dKkiZU/export?format=xlsx"


def load_data(url: str) -> pd.DataFrame: 
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return pd.read_excel(BytesIO(response.content))
    except Exception:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(url, verify=False, timeout=30)
        response.raise_for_status()
        return pd.read_excel(BytesIO(response.content))


def music_detail(df: pd.DataFrame, id: int) -> pd.DataFrame:
    return df[df["ID"] == id]


def drive_audio(url):
    file_id = url.split("/d/")[1].split("/")[0]
    return f"https://drive.google.com/uc?export=download&id={file_id}"

def show_selected_music_sheet(selected_music_sheet):
    file_id = selected_music_sheet.split("/d/")[1].split("/")[0]
    partitura_link = f"https://drive.google.com/file/d/{file_id}/preview"

    html_code = f"""
    <div style="overflow-x:auto; white-space:nowrap;">
        <iframe src="{partitura_link}" width="100%" height="750"></iframe>
    </div>
    """

    st.components.v1.html(html_code, height=760)


def dashboard(selected_music: pd.DataFrame):
    st.header(f"Música: {selected_music['MUSIC'].values[0]}")
    st.write(f"Compositor: {selected_music['COMPOSITOR'].values[0]}")
    st.write(f"Álbum: {selected_music['ALBUM'].values[0]}")
    st.write(f"Tom: {selected_music['TOM'].values[0]}")
    
    # -------- COLUNAS 90% / 10% --------
    col_score, col_audio = st.columns([7, 3])

    # =====================================================
    # VOZ + AUDIO (10%)
    # =====================================================
    with col_audio:
            # -------- SELECIONAR Partitura --------
        music_sheet_list = selected_music[["MUSIC_SHEET_FILE_ID"]].dropna().reset_index(drop=True)
        
        if not music_sheet_list.empty:
            selected_music_sheet_index = st.selectbox(
                "📜 Escolha a partitura para visualização:",
                options=selected_music["MUSIC_SHEET_LABEL"].dropna()
            )
            selected_music_sheet = selected_music[selected_music["MUSIC_SHEET_LABEL"] == selected_music_sheet_index]["MUSIC_SHEET_FILE_ID"].iloc[0]

        voice = st.selectbox(
                "🎤 Escolha a voz para audição:",
                options=selected_music["VOICE_LABEL"].dropna(),
        )
        
        selected_music_audio = selected_music[selected_music["VOICE_LABEL"] == voice]["VOICE_AUDIO_LINK"].iloc[0]

        audio_link = drive_audio(selected_music_audio)

        audio_bytes = requests.get(audio_link).content

        st.audio(audio_bytes)

    # =====================================================
    # PARTITURA (90%)
    # =====================================================
    with col_score:
        if music_sheet_list.empty:
            st.warning("Nenhuma partitura disponível para esta música.")
        else:   
            show_selected_music_sheet(selected_music_sheet)

# =====================================================
# Streamlit screen
# =====================================================
def render_streamlit(df: pd.DataFrame):
    st.title("🎼 Coral - Biblioteca de Músicas")
    musicList = df["MUSIC"].drop_duplicates()
    # -------- SELECIONAR MUSICA --------
    musica = st.selectbox(
        "Escolha a música",
        musicList
    )

    selected_music = df[df["MUSIC"] == musica]
    st.session_state["selected_music"] = selected_music
    if musicList.empty:
       st.warning("No data loaded. Please go back to the home page.")
        
    dashboard(selected_music)


# =====================================================
# MAIN EXECUTION
# =====================================================
def main():
    st.set_page_config(layout="wide")
    if "df" not in st.session_state:
        df = load_data(DATA_URL)
        st.session_state["df"] = df
    render_streamlit(st.session_state["df"])


if __name__ == "__main__":
    main()
