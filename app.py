import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- Authenticate Google Sheets ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# --- Open your sheet ---
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1FMIanFpOTI3JXZFHMB_eAhFa0OkydcbTQjY-4jCq_Xw/edit"
spreadsheet = client.open_by_url(SPREADSHEET_URL)
sheet = spreadsheet.sheet1  # first worksheet

st.title("🔎 Puzzle Search")
st.write("Type a value to search")

# --- User input ---
search_text = st.text_input("Search term:", key="search")

# --- Get all rows ---
rows = sheet.get_all_values()
status = None  # for border feedback

if search_text.strip():
    result = None
    for row in rows:
        if row and row[0].strip().lower() == search_text.strip().lower():  # ignore case and spaces
            result = row
            break

    if result:
        key = result[0]
        values = result[1:]
        for val in values:
            if val.strip():  # skip empty cells
                # check if value is an image URL
                if val.lower().startswith("http") and any(val.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif", ".webp"]):
                    st.image(val, caption=f"{key}", use_container_width=True)
                else:
                    st.write(f"{key} = {val}")
        status = "success"
    else:
        st.error(f"No matches found for '{search_text}'")
        status = "error"

# --- Base CSS: remove default red box on focus ---
base_css = """
<style>
.stTextInput > div > div > input {
    border: 2px solid #ccc !important;
    box-shadow: none !important;
    outline: none !important;
}
.stTextInput > div > div > input:focus {
    border: 2px solid #ccc !important;
    box-shadow: none !important;
    outline: none !important;
}
</style>
"""
st.markdown(base_css, unsafe_allow_html=True)

# --- Conditional input borders ---
if status == "success":
    st.markdown(
        """
        <style>
        .stTextInput > div > div > input {
            border: 2px solid green !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
elif status == "error":
    st.markdown(
        """
        <style>
        .stTextInput > div > div > input {
            border: 2px solid red !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
