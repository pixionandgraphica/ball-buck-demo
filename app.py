import streamlit as st
import pandas as pd
import dropbox
import io

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
            filtered = filtered[
                filtered.apply(
                    lambda row: row.astype(str).str.contains(word, case=False).any(),
                    axis=1
                )
            ]
    else:
        filtered = df

    st.subheader("Search Results")
    st.write(f"{len(filtered)} images found")
    st.dataframe(filtered)

    if len(filtered) > 0:
        st.subheader("Image Preview")
        preview_rows = filtered.head(12)

        cols = st.columns(3)

        for i, (_, row) in enumerate(preview_rows.iterrows()):
            try:
                path = row["path"]
                _, res = dbx.files_download(path)
                image_bytes = io.BytesIO(res.content)

                with cols[i % 3]:
                    st.image(image_bytes, caption=row["name"], use_container_width=True)
            except Exception as e:
                with cols[i % 3]:
                    st.write(f"Could not load image: {row['name']}")
