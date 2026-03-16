import streamlit as st
import pandas as pd
import dropbox

dbx = dropbox.Dropbox(st.secrets["DROPBOX_TOKEN"])

st.title("Archive Intelligence Demo")

st.write("Upload the metadata CSV generated from the image clustering pipeline.")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Metadata Table")
    st.dataframe(df)

    search = st.text_input("Search images by keyword")

    if search:
        keywords = search.split()
        filtered = df
        for word in keywords:
            filtered = filtered[filtered.apply(
                lambda row: row.astype(str).str.contains(word, case=False).any(), axis=1
            )]
    else:
        filtered = df

    st.subheader("Search Results")
    st.write(f"{len(filtered)} images found")

    st.dataframe(filtered)
