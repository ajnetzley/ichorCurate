import streamlit as st
import fitz  # PyMuPDF
import plotly.express as px
import pandas as pd
import os
from PIL import Image
from streamlit_shortcuts import button, add_keyboard_shortcuts

# Setting page formats
st.set_page_config(layout="wide")

# Title of the app
st.title('IchorCurate')

# Specify the directory containing your PDFs
pdf_directory = "../IchorCNA/521R02_B01_CFFv2_ND0814_S2/"

# Load up to 10 PDFs containing "genomeWide_n" and ending with ".pdf"
pdf_files = [
    f for f in os.listdir(pdf_directory)
    if "genomeWide_n" in f and f.endswith(".pdf")
]

# State for tracking which PDF is currently displayed
if "pdf_index" not in st.session_state:
    st.session_state.pdf_index = 0
if "solution_pdf" not in st.session_state:
    st.session_state.solution_pdf = None

# Function to get the first page as an image from a PDF
def get_pdf_first_page_image(pdf_path):
    with fitz.open(pdf_path) as pdf:
        # Render the first page as an image
        first_page = pdf[0]
        pix = first_page.get_pixmap()  
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return img

# # Layout: Split into two columns for navigation and solution display
# col_sol, col_nav = st.columns(2)

# # Navigation Controls Column
# with col_nav:
st.subheader("Potential Solutions")
# Display navigation buttons
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if button("Previous", "ArrowLeft", None, hint=True) and st.session_state.pdf_index > 0:
        st.session_state.pdf_index -= 1

with col2:
    if button("Next", "ArrowRight", None, hint=True) and st.session_state.pdf_index < len(pdf_files) - 1:
        st.session_state.pdf_index += 1

# Display the current PDF as an image
if pdf_files:
    current_pdf = pdf_files[st.session_state.pdf_index]
    file_path = os.path.join(pdf_directory, current_pdf)
    pdf_image = get_pdf_first_page_image(file_path)

    #st.subheader(f"Displaying {current_pdf}")
    st.image(pdf_image, use_column_width=True)

    st.write(f"Showing Potential Solution {st.session_state.pdf_index + 1} of {len(pdf_files)}")

    # Button to set the current PDF as the solution
    with col3:
        if button("Set as Solution", "Enter", None, hint=True):
            st.session_state.solution_pdf = current_pdf
else:
    st.write("No PDF files found matching the pattern.")

# # Solution Display Column
# with col_sol:
st.subheader("Selected Solution")
if st.session_state.solution_pdf:
    solution_path = os.path.join(pdf_directory, st.session_state.solution_pdf)
    solution_image = get_pdf_first_page_image(solution_path)
    #st.write(f"Solution PDF: {st.session_state.solution_pdf}")
    st.image(solution_image, use_column_width=True)
    
else:
    st.write("No solution selected.")

################################################
### CODE FOR UPLOADING AND DISPLAYING A PDF ###
################################################
# File uploader to upload PDF files
# uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# if uploaded_file is not None:
#     # Display the uploaded PDF
#     with fitz.open(stream=uploaded_file.read(), filetype="pdf") as pdf_document:
#         num_pages = pdf_document.page_count
        
#         # Display the number of pages in the PDF
#         st.write(f"Total pages: {num_pages}")
        
#         # Loop through all the pages and render them
#         for page_number in range(num_pages):
#             page = pdf_document.load_page(page_number)
#             pix = page.get_pixmap()
            
#             # Convert pixmap to image
#             image = pix.tobytes("png")
#             st.image(image, caption=f"Solution {page_number + 1}", use_column_width=True)

################################################
### CODE FOR READING IN DATA AND PLOTTING IT ###
################################################
# # Sample data)
# segment_data = pd.read_csv('../IchorCNA/output/521R02_B01_CFFv2_ND0814_S2.cna.seg', sep='\t')
# x = segment_data['521R02_B01_CFFv2_ND0814_S2.logR'].values
# # copyNumberStates = np.array([1,2,3,4,5])
# # K = len(copyNumberStates)

# # plt.figure(figsize=(14,6))
# # plt.plot(x, marker='o', linestyle='None')
# # plt.title('Copy Number Alteration')
# # plt.ylabel('Copy Number (Log2 Ratio)')
# # plt.xlabel('Position')
# # plt.ylim([-2, 2])

# # Create a Plotly figure
# fig = px.scatter(segment_data, x='start', y='521R02_B01_CFFv2_ND0814_S2.logR', title='Copy Number Alteration')

# # Display the figure in Streamlit
# st.plotly_chart(fig)

