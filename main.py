import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from io import BytesIO

# Google Sheets API 인증
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)

# Google 스프레드시트 데이터 가져오기
spreadsheet_url = "https://docs.google.com/spreadsheets/d/14Q89GUb0IF_4Ob0Acret4_yZ-g8_L_n_VlIGHWXs25E/edit?usp=sharing"
spreadsheet_id = spreadsheet_url.split("/d/")[1].split("/")[0]  # 스프레드시트 ID 추출

sheet = client.open_by_key(spreadsheet_id).sheet1
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Streamlit 앱 UI
st.title("Google Sheets Downloader")
st.write("아래 버튼을 눌러 데이터를 다운로드하세요.")

# CSV로 변환
csv_data = df.to_csv(index=False).encode('utf-8')
buffer = BytesIO(csv_data)

st.download_button(
    label="📥 스프레드시트 다운로드 (CSV)",
    data=buffer,
    file_name="google_sheet_data.csv",
    mime="text/csv"
)

st.write("데이터 미리보기:")
st.dataframe(df)

