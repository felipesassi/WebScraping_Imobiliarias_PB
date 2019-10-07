import requests
from bs4 import BeautifulSoup
import pandas as pd

class WebScrapperMoretti():

    def __init__(self, start_url="https://www.moretti.imb.br/apartamentos-para-venda/page/", n_pages=2):
        self.start_url = start_url
        self.n_pages = n_pages

    def __get_request(self, url):
        return requests.get(url)

    def __scrap_links(self):
        self.links = []
        for i in range(self.n_pages):
            url = self.start_url + str(i + 1)
            page = self.__get_request(url)
            soup = BeautifulSoup(page.text, "html.parser")
            link = soup.findAll(class_ = "property_listing")
            for l in link:
                self.links.append(l.find("a")["href"])
            self.n_links = len(self.links)

    def scrap_data(self):
        self.__scrap_links()
        data_dict = dict()
        dict_list = list()
        for i, link in enumerate(self.links):
            page = self.__get_request(link)
            soup = BeautifulSoup(page.text, "html.parser")
            data = soup.findAll(class_ = "listing_detail")
            for d in data:
                if d.find("strong") != None:
                    key = d.find("strong").get_text()
                    data = d.get_text()
                    data = data.replace(key, "")
                    data_dict[key] = data
            data_dict["link"] = link
            dict_list.append(pd.DataFrame(data = data_dict, index = [0]))
            print("Imóvel: {}." .format(i))
        data_final = pd.concat(dict_list, axis = 0, ignore_index = True)
        data_final.to_csv("Lista_Imoveis.csv")

    def get_links(self):
        return self.links

    def get_data(self):
        return self.data

if __name__ == "__main__":
    WC = WebScrapperMoretti()
    WC.scrap_data()
