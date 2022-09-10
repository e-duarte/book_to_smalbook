import livreto
import os

dir_path = '/home/ewerton/Documents/Dulcineia/LIVROS PNA/colorir'
dest = 'out'

pdfs = os.listdir(dir_path)

for pdf in pdfs:
    livreto.main(os.path.join(dir_path, pdf), dest)
