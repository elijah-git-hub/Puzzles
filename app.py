import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# --- Define proper scopes ---
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# --- Authenticate using Streamlit secrets ---
service_account_info = st.secrets["gspread_service_account"]
creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
client = gspread.authorize(creds)

# --- Open your spreadsheet ---
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1FMIanFpOTI3JXZFHMB_eAhFa0OkydcbTQjY-4jCq_Xw/edit"
try:
    spreadsheet = client.open_by_url(SPREADSHEET_URL)
    sheet = spreadsheet.sheet1
except Exception as e:
    st.error(f"Error accessing sheet: {e}")
    st.stop()

# --- Streamlit UI ---
st.title("🔎 Puzzle Search")
search_text = st.text_input("Enter text to search:")

# Dynamic border colors
border_style = ""
match_found = False

if search_text:
    rows = sheet.get_all_values()
    matches = []

    for row in rows:
        if row[0].strip() == search_text.strip():
            # Create "key = value" for non-empty cells after first column
            for i in range(1, len(row)):
                if row[i].strip():  # skip empty cells
                    matches.append(f"{row[0]} = {row[i]}")

    if matches:
        match_found = True
        border_style = "2px solid green"
        for match in matches:
            # Display image if value is an URL
            if match.split(" = ")[1].startswith("http"):
                st.image(match.split(" = ")[1], use_container_width=True)
            else:
                st.write(match)
    else:
        border_style = "2px solid red"
        st.warning("No matches found!")

# Apply dynamic border color via custom CSS
st.markdown(
    f"""
    <style>
    div[data-baseweb="input"] input {{
        border: {border_style} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
