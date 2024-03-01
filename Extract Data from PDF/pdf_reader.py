from PyPDF2 import PdfReader, PdfWriter
import file_explorer 

file_paths = list(file_explorer.select_files())
file_names = []

for file in file_paths:
    file_names.append(file.split("/")[-1].split(".")[0])

def mergePdf(file_paths):
    writer = PdfWriter()
    for file_path in file_paths:
        reader = PdfReader(file_path)
        for page in reader.pages:
            writer.add_page(page)
    writer.write(f"{file_names[0]}_merged.pdf")


def rotatePdf(file_path, degrees):
    reader = PdfReader(file_path[0])
    writer = PdfWriter()
    for page in reader.pages:
        page.rotate(degrees)
        writer.add_page(page)
    writer.write(f"{file_names[0]}_rotated.pdf")


def extractText(file_path):
    for file in file_path:
        with open(file_path[file], "rb") as f:
            reader = PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
    return text


def extractImages(file_path):
    for file in file_path:
        with open(file_path[file], "rb") as f:
            reader = PdfReader(f)
            images = []
            for page in reader.pages:
                images.append(page.images)
    return images

def reducePdf(file_path):
    count = 0

    for file in file_path:
        reader = PdfReader(file_path[count])
        writer = PdfWriter()

        for page in reader.pages:
            page.compress_content_streams()
            writer.add_page(page)

        writer.add_metadata(reader.metadata)

        with open(f'{file_names[count]}_reduced.pdf', "wb") as fp:
            writer.write(fp)
        
        count += 1



