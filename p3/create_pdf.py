import qrcode
import arabic_reshaper
import os
from bidi.algorithm import get_display
from p1.code.Booklist import GetBookList
from fpdf import FPDF
import time
class PdfCover():
    def create_qrcode_img(self, url, qrcode_name):
        img = qrcode.make(url)
        img.save('{0}.png'.format(qrcode_name))   

    def delete_image(self, qrcode_name):
        os.remove("{0}.png".format(qrcode_name))
    
    def create_pdf_with_image(self, links, author_name, book_name):
        self.author_name  =  author_name
        self.book_name  = book_name

        self.author_name_final = ''
        self.book_name_final  = ''
        for i in links:
            self.pdf = FPDF()
            self.pdf.add_page()
            self.pdf.add_font('adobearabic', '', 'adobearabic.ttf', uni=True)
            self.pdf.set_font('adobearabic', '', 24)

            self.create_qrcode_img(i, links.index(i)) # Generating a qrcode 
            # Solving a reverse arabic letters in pdf 
            self.author_name_final = self.author_name[links.index(i)]
            self.author_name_final = arabic_reshaper.reshape(self.author_name_final)
            self.author_name_final = get_display(self.author_name_final)
            
            # # Solving a reverse arabic letters in pdf 
            self.book_name_final = self.book_name[links.index(i)]
            self.book_name_final = arabic_reshaper.reshape(self.book_name_final)
            self.book_name_final = get_display(self.book_name_final)
			# Adding image 
            self.pdf.image('{0}.png'.format(links.index(i)), x = 50, y = 10, w = 100, h = 100, type = '', link = "{}".format(i)  )
            self.pdf.cell(180, 200, "{0}".format(self.book_name_final),0, 0, align='C')
            self.pdf.cell(-180, 250, "{0}".format(self.author_name_final),0, 0, align='C')

            self.pdf.output('{0}.pdf'.format(links.index(i)))
            self.delete_image(links.index(i)) # deleting image after adding in pdf 

create_pdf  = PdfCover()
url  = "https://ar.wikipedia.org/wiki/%D9%82%D8%A7%D8%A6%D9%85%D8%A9_%D8%A3%D9%81%D8%B6%D9%84_%D9%85%D8%A6%D8%A9_%D8%B1%D9%88%D8%A7%D9%8A%D8%A9_%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9"
get_book = GetBookList(url)
links = get_book.get_hyper_link() # get all links 
author_name = get_book.get_author_name()
book_name = get_book.get_book_name()
# test = links[:10] # this for testing just creating 5 pdf 
# create_pdf.create_pdf_with_image(test, author_name, book_name) # create pdfs with qrcode with hyperlink embded
create_pdf.create_pdf_with_image(links, author_name, book_name) # create all pdfs with qrcode with hyperlink embded 




