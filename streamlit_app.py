import os
import streamlit as st
from pdf2image import convert_from_path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import io

def pdf_to_images(pdf_path, output_folder, image_format='PNG'):
    # Convert PDF to images
    images = convert_from_path(pdf_path)
    
    # Save images to the output folder with the same filename as the PDF
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    image_paths = []
    for i, image in enumerate(images):
        # Set the image filename, keeping the PDF name and choosing the correct format
        image_path = os.path.join(output_folder, f"{pdf_name}_{i + 1}.{image_format.lower()}")
        image.save(image_path, image_format)
        image_paths.append(image_path)
    
    return image_paths

def main():
    st.title("PDF to Image Converter")
    st.markdown("This app only supports single-page PDF files. Have fun! 😎")
    # File uploader for multiple PDF files
    uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
    
    # Dropdown for selecting image format
    image_format = st.selectbox("Choose the image format", ["PNG", "JPEG"])
    
    # Convert button
    if st.button("Convert"):
        if uploaded_files:
            # Temporary directory to save images
            with TemporaryDirectory() as temp_dir:
                all_image_paths = []
                for uploaded_file in uploaded_files:
                    try:
                        # Convert the uploaded PDF to images
                        pdf_path = os.path.join(temp_dir, uploaded_file.name)
                        with open(pdf_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        st.write(f"Converting {uploaded_file.name} to {image_format}...")
                        image_paths = pdf_to_images(pdf_path, temp_dir, image_format)
                        all_image_paths.extend(image_paths)
                        
                        st.write(f"Conversion completed for {uploaded_file.name}!")
                        
                        # Display and provide download links for the images
                        for image_path in image_paths:
                            st.image(image_path, caption=os.path.basename(image_path))
                    
                    except Exception as e:
                        st.warning(f"An error occurred while converting {uploaded_file.name}: {e}")
                        continue
                
                if all_image_paths:
                    # Create a ZIP file for all images
                    zip_buffer = io.BytesIO()
                    with ZipFile(zip_buffer, "w") as zip_file:
                        for image_path in all_image_paths:
                            zip_file.write(image_path, os.path.basename(image_path))
                    
                    zip_buffer.seek(0)
                    
                    # Provide a download link for the ZIP file
                    st.download_button(
                        label="Download all images as ZIP",
                        data=zip_buffer,
                        file_name="converted_images.zip",
                        mime="application/zip"
                    )
        else:
            st.warning("Please upload at least one PDF file.")

if __name__ == "__main__":
    main()
