from PyPDF2 import PdfReader, PdfWriter
import file_explorer
file_names = ''

def mergePdf():
    file_paths = file_explorer.get_file_info()
    writer = PdfWriter()

    for item in file_paths:
        reader = PdfReader(item[0])
        for page in reader.pages:
            writer.add_page(page)
    writer.write(f"{file_paths[0][1]}_merged.pdf")
    return print('Check your directory folder to see the merged file.')

def rotatePdf():
    file_paths = file_explorer.get_file_info()

    if file_paths is False:
        print('You need to select a pdf file')
        return

    if len(file_paths) > 1:
        print('You can only rotate one pdf at a time')
        return

    try:
        degrees = float(input('Type the degrees you want to rotate the pdf: '))
        if degrees > 360:
            print('The degrees must be lower than 360°')
            return
        elif degrees < 0:
            print('The degrees must be higher than 0°')
            return
        elif degrees%90 != 0:
            print('The degrees must be a multiple of 90°')
            return
    except:
        print('You need to type a number')
        rotatePdf()
    
    reader = PdfReader(file_paths[0][0])
    writer = PdfWriter()

    for page in reader.pages:
        page.rotate(degrees)
        writer.add_page(page)
    writer.write(f"{file_paths[0][1]}_rotated.pdf")
    return print('Check your directory folder to see the rotated file.')

def extractText():
    file_paths = list(file_explorer.select_files())

    for file in file_paths:
        file_names.append(file.split("/")[-1].split(".")[0])

    for file in file_paths:
        with open(file_paths[file], "rb") as f:
            reader = PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
    return text


def extractImages():
    file_paths = list(file_explorer.select_files())

    for file in file_paths:
        file_names.append(file.split("/")[-1].split(".")[0])

    for file in file_paths:
        with open(file_paths[file], "rb") as f:
            reader = PdfReader(f)
            images = []
            for page in reader.pages:
                images.append(page.images)
    return images

def resizePdf():
    file_paths = list(file_explorer.select_files())

    for file in file_paths:
        file_names.append(file.split("/")[-1].split(".")[0])

    for file in file_paths:
        reader = PdfReader(file_paths[count])
        writer = PdfWriter()

        for page in reader.pages:
            page.compress_content_streams()
            writer.add_page(page)

        writer.add_metadata(reader.metadata)

        with open(f'{file_names[count]}_reduced.pdf', "wb") as fp:
            writer.write(fp)
        
        count += 1

def encryptPdf():
    while True:
        password = input('Type a password')
        confirm = input('Confirm password')

        if password != confirm:
            print('Passwords do not match')
        elif password == confirm:
            break
            
    file_paths = list(file_explorer.select_files())

    for file in file_paths:
        file_names.append(file.split("/")[-1].split(".")[0])

    for file in file_paths:
        reader = PdfReader(file_paths[count])
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt(password)

        with open(f'{file_names[count]}_encrypted.pdf', "wb") as fp:
            writer.write(fp)
        count += 1

def decryptPdf():
    file_paths = list(file_explorer.select_files())

    for file in file_paths:
        file_names.append(file.split("/")[-1].split(".")[0])
        
    while True:
        password = input('Type a password')
        confirm = input('Confirm password')

        if password != confirm:
            print('Passwords do not match')
        elif password == confirm:
            break
            

    for file in file_paths:
        reader = PdfReader(file_paths[count])
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.decrypt(password)

        with open(f'{file_names[count]}_decrypted.pdf', "wb") as fp:
            writer.write(fp)
        count += 1

