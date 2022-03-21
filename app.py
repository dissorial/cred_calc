import streamlit as st
from pages import gpu, cc_vp


st.set_page_config(layout="wide")

PAGES = {
    "Cyber Credits & Victory Points": cc_vp,
    "GPU": gpu,
}


st.sidebar.title('Navigation')
selection = st.sidebar.selectbox("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
