# imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# set up our app
st.set_page_config(page_title="🧹Data Sweeper App", layout="wide")
st.title("📅🧹 Data Sweeper App")
st.write("Smart CSV & Excel Converter Clean, Transform & Visualize Data Effortlessly!")
 
upload_files = st.file_uploader("Upload your files (CSV or Excel)", type=["csv", "xlsx"], accept_multiple_files=True)

if upload_files:
    for file in upload_files:
        file_ext = os.path.splitext(file.name)[-1].lower()


        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file, engine="openpyxl")  # Ensure Excel compatibility
        else:
            st.error(f"Please upload CSV or Excel files only. {file_ext} files are not supported.")
            continue

            # Display file info
        st.write(f"**📂 File Name:** {file.name}")
        st.write(f"**📏 File Size:** {round(file.size / 1024, 2)} KB")

          # Show first 5 rows
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head())

         # Data Cleaning & Transformation
        st.subheader("🛠 Data Cleaning & Transformation")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates Removed!")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing Values Filled!")


# Choose specific columns  to keep or convert
    st.subheader("🎯 Select Columns to Convert")
    columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
    df = df[columns]

        # Data Visualization
    st.subheader("📊 Data Visualization")
    if st.checkbox(f"Show Visualization for {file.name}"):
        st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # File Conversion
    st.subheader("🔁 Conversion Options")
    conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

    if st.button(f"Convert {file.name}"):
        buffer = BytesIO()
        if conversion_type == "CSV":
            df.to_csv(buffer, index=False)
            file_name = file.name.replace(file_ext, ".csv")
            mime_type = "text/csv"
        elif conversion_type == "Excel":
            df.to_excel(buffer, index=False, engine="openpyxl")  # Ensure proper Excel saving
            file_name = file.name.replace(file_ext, ".xlsx")
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        buffer.seek(0)
   
        # Download Button
        st.download_button(
            label=f"⬇ Download {file.name} as {conversion_type}",
            data=buffer,
            file_name=file_name,
            mime=mime_type
        )

st.success("🎉 All files processed successfully!")