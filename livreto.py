from pdf2image import convert_from_path
from PIL import Image
import numpy as np
from PyPDF2 import PdfFileMerger

import os
import shutil
from pathlib import Path


class Livreto:
    def __init__(self, pdf_path, dest_path):
        self.pdf_file = Path(pdf_path)
        self.dest = Path(dest_path)
        
        self.images = self.pdf_to_images_array(self.pdf_file)
        self.pages = self.build_livreto(self.images)
        self.pages_path = [f"tmp/page_{i}.pdf" for i in range(len(self.pages))]

    def pdf_to_images_array(self, pdf_path):
        images = convert_from_path(pdf_path)
        image_array = [np.array(image) for image in images]

        return image_array

    def concatenate_image(self, page_left, page_right):
        return np.concatenate((page_left, page_right), axis=1)

    def append_blank_page(self, images):
        blank_page = np.array(images[0], copy=True)
        blank_page.fill(255)
        images.append(blank_page)

        return images

    def build_livreto(self, images):
        images = self.append_blank_page(images) if (len(images) % 2) != 0 else images
        pages = []

        for i in range(int(len(images)/2)):
            if (i + 1) % 2 == 0:
                img_right = images[-i - 1]
                img_left = images[i]
            else:
                img_right = images[i]
                img_left = images[-i - 1]

            pages.append(self.concatenate_image(img_left, img_right))

        return pages

    def save_page(self, page, filename):
        im = Image.fromarray(page)
        imrgb = im.convert('RGB')

        imrgb.save(filename)

    def merge_pdfs(self):
        merger = PdfFileMerger()

        print(self.pages_path)
        print('aqui')
        for path in self.pages_path:
            merger.append(path)

        merger.write(self.dest / self.pdf_file.name)

        merger.close()

    def create_temp_folder(self):
        os.mkdir('tmp')

    def delete_temp_folder(self):
        shutil.rmtree('tmp')

    def generate_livreto(self):
        self.create_temp_folder()

        for i, page in enumerate(self.pages):
            self.save_page(page, f"tmp/page_{i}.pdf")

        self.merge_pdfs()

        self.delete_temp_folder()


if __name__ == '__main__':
    path_pdf = "/home/ewerton/Projects/book_to_smallbook-main/atividade eglia.pdf"
    dest_path = "./"
    
    livreto = Livreto(path_pdf, dest_path)
    livreto.generate_livreto()
