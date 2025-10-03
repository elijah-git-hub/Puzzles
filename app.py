import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("puzzle-game.json", scope)
client = gspread.authorize(creds)

SHEET_ID = "1FMIanFpOTI3JXZFHMB_eAhFa0OkydcbTQjY-4jCq_Xw"
SHEET_NAME = "Sheet1"
sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

# Streamlit UI
st.title("Puzzle Search")
search_value = st.text_input("Enter value to search:")

if search_value:
    all_data = sheet.get_all_values()
    matches = [row for row in all_data if row and row[0] == search_value]  # search all rows including first

    if matches:
        st.write("Found match")
        for row in matches:
            for i, cell in enumerate(row):
                if i == 0 or not cell.strip():
                    continue  # skip empty cells & first column (since it's the search key)

                # IMAGE types
                if cell.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg")):
                    st.image(cell, caption=f"{row[0]}", use_container_width=True)

                # VIDEO types
                elif cell.lower().endswith((".mp4", ".webm", ".ogg", ".mov", ".mkv")):
                    st.video(cell)

                # AUDIO types
                elif cell.lower().endswith((".mp3", ".wav", ".ogg", ".flac", ".aac", ".m4a")):
                    st.audio(cell)

                # YouTube links
                elif "youtube.com" in cell.lower() or "youtu.be" in cell.lower():
                    st.video(cell)

                # Other links
                elif cell.startswith("http://") or cell.startswith("https://"):
                    st.markdown(f"{row[0]} = [Link]({cell})")

                # Plain text
                else:
                    st.write(f"{row[0]} = {cell}")
    else:
        st.warning("No matches found.")
