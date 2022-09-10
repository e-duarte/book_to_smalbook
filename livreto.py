from pdf2image import convert_from_path
from PIL import Image
import numpy as np
from PyPDF2 import PdfFileMerger

import os
import shutil
from pathlib import Path

def pdf_to_images_array(pdf):
    images = convert_from_path(pdf)
    image_array = [np.array(image) for image in images]

    return image_array

def concatenate_image(page_left, page_right):
    return np.concatenate((page_left, page_right), axis=1)

def build_livreto(images):
    pages = []

    # idx_left = len(images)

    for i in range(int(len(images)/2)):
        # idx_right = i
        

        # img_right = images[i] if (idx_right+1) % 2 != 0 else images[-i - 1]
        # img_left = images[-i - 1] if (idx_left) % 2 == 0 else images[i]

        # idx_right -= 1

        if (i + 1) % 2 == 0:
            img_right = images[-i - 1]
            img_left = images[i]
        else:
            img_right = images[i]
            img_left = images[-i - 1]


        
        pages.append(concatenate_image(img_left, img_right))
    
    return pages

def save_page(page, filename):
    im = Image.fromarray(page)
    imrgb = im.convert('RGB')

    imrgb.save(filename)

def merge_pdfs(pdfs, merged_pdf_name, dest):
    merger = PdfFileMerger()

    for path in pdfs:
        merger.append(path)

    merger.write(os.path.join(dest, merged_pdf_name))

    merger.close()

def main(original_pdf_path, dest):
    pdf_file = Path(original_pdf_path)

    images = pdf_to_images_array(pdf_file)

    pages = build_livreto(images)

    os.mkdir('./tmp')

    for i, page in enumerate(pages):
        save_page(page, f'tmp/page_{i}.pdf')

    pages_path = [f'tmp/page_{i}.pdf' for i in range(len(pages))]

    merge_pdfs(pages_path, pdf_file.name, dest)

    shutil.rmtree('./tmp')


if __name__ == '__main__':
    path_pdf = "/home/ewerton/Documents/Dulcineia/LIVROS PNA/cantigas_para_colorir.pdf"
    main(path_pdf)


