import os
import PyPDF2
from pathlib import Path

def extract_title_from_pdf(pdf_path):
    """Extract the first line from a PDF file as the title."""
    try:
        with open(pdf_path, 'rb') as file:
            # Create PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Get first page
            first_page = pdf_reader.pages[0]
            
            # Extract text from first page
            text = first_page.extract_text()
            
            # Get first line and clean it up
            title = text.split('\n')[0].strip()
            
            # If first line is 'preprint', use the next non-empty line
            if title.lower() == 'preprint':
                for line in text.split('\n')[1:]:
                    if line.strip():
                        title = line.strip()
                        break
            
            # Remove invalid filename characters
            invalid_chars = '<>:"/\\|?*'
            for char in invalid_chars:
                title = title.replace(char, '')
                
            # Limit filename length and ensure it's not empty
            title = title[:150] if title else "Untitled"
            return title
            
    except Exception as e:
        print(f"Error processing {pdf_path}: {str(e)}")
        return None

def rename_pdfs_in_folder(folder_path):
    """Rename all PDFs in the specified folder using their first line as title."""
    folder = Path(folder_path)
    
    # Process all PDF files in the folder
    for pdf_file in folder.glob('*.pdf'):
        # Extract title
        title = extract_title_from_pdf(pdf_file)
        
        if title:
            # Create new filename with original extension
            new_name = title + '.pdf'
            new_path = folder / new_name
            
            # Handle duplicate filenames by adding numbers
            counter = 1
            while new_path.exists():
                new_name = f"{title}_{counter}.pdf"
                new_path = folder / new_name
                counter += 1
            
            try:
                # Rename the file
                pdf_file.rename(new_path)
                print(f"Renamed: {pdf_file.name} -> {new_name}")
            except Exception as e:
                print(f"Error renaming {pdf_file.name}: {str(e)}")

if __name__ == "__main__":
    # Get folder path from user
    folder_path = input("Enter the folder path containing PDF files: ")
    
    # Check if folder exists
    if os.path.isdir(folder_path):
        rename_pdfs_in_folder(folder_path)
    else:
        print("Invalid folder path!")
