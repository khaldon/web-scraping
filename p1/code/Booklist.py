from os import link
from bs4 import BeautifulSoup
import requests
import pandas as pd 
import re 
url  = "https://ar.wikipedia.org/wiki/%D9%82%D8%A7%D8%A6%D9%85%D8%A9_%D8%A3%D9%81%D8%B6%D9%84_%D9%85%D8%A6%D8%A9_%D8%B1%D9%88%D8%A7%D9%8A%D8%A9_%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9"


class GetBookList():
    def __init__(self, url):
        self.html_content = requests.get(url).text  # get a body of html content
        self.soup = BeautifulSoup(self.html_content, features="html.parser")
        self.table = self.soup.find("table", attrs={"class":"wikitable"})# get a table its name "wikitable"
        self.body = self.table.find_all("tr")# get all rows and columns with their default tags 
    
    # A method to get a title of table for each row that's stored in <th> tag known as head 
    def heads_of_table(self):
        head = self.body[0] # getting a first row only 
        heads = []
        for i in head.find_all("th"):
            i = re.sub("(\n)","", i.text) # using regular expression to replace all text has \n with nothing (deleting them)
            heads.append(i)
        return heads 

    # A method to get a body of the table 
    def main_body_without_hyper_link(self):
        body = self.body[1:] # geting the whole row except first one 
        all_rows = [] # storing each row after handle them 
        for row_num in range(len(body)):
            row = []
            for row_item in body[row_num].find_all("td"): 
                a =  re.sub("(\n)|(\xa0)","",row_item.text) # using a regular expression to exclude or remove \n and \xa0 
                row.append(a)
            all_rows.append(row)
                
        return all_rows

    def get_author_name(self):
        body = self.body[1:]
        author_name  = []
        for i in range(len(body)): 
             author_name.append(self.main_body_without_hyper_link()[i][2])

        return author_name

    def get_book_name(self):
        body  = self.body[1:]
        book_name = []
        for i in range(len(body)):
            book_name.append(self.main_body_without_hyper_link()[i][1])
        return book_name 


    def get_hyper_link(self):
        body = self.body[1:] # geting the whole row except first one 
        all_rows_links = [] # storing each row after handle them 
        for row_num in range(len(body)):
            links = [] # storing all hyperlink of books 

            for row_item in body[row_num].find_all("a"):
                a =  re.sub("(/wiki/)","https://ar.wikipedia.org/wiki/",row_item['href']) # replacing /wiki/ to https://ar.wikipedia.org/wiki/
                links.append(a)

            all_rows_links.append(links[0]) # Appending only the first index 

        return all_rows_links

    def create_excel_file(self):
        body = self.main_body_without_hyper_link()
        head = self.heads_of_table()
        df = pd.DataFrame(data=body, columns=head)
        df.to_excel("Book_list.xlsx", index=False) # Creating excel file and index False to remove a index column 

    def show_head_of_data(self):
        body = self.main_body_without_hyper_link()
        head = self.heads_of_table()
        df = pd.DataFrame(data=body, columns=head)
        print(df.head())

#url  = "https://ar.wikipedia.org/wiki/%D9%82%D8%A7%D8%A6%D9%85%D8%A9_%D8%A3%D9%81%D8%B6%D9%84_%D9%85%D8%A6%D8%A9_%D8%B1%D9%88%D8%A7%D9%8A%D8%A9_%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9"
#get_book = GetBookList(url)
#get_book.create_excel_file() # generating a excel file with all data 
# get_book.show_head_of_data() # showing first 5 of rows only 
# get_book.get_hyper_link() # getting all hyperlinks 
# get_book.get_book_name() # getting all book names 
# get_book.get_author_name() # getting all author names 

