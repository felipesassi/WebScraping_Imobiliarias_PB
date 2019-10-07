import requests
from bs4 import BeautifulSoup
import pandas as pd

class WebScrapperMoretti():
    """
    Essa classe é utilizada para realizar a raspagem de dados no site da construtora Moretti, em Pato Branco (PR).

    Parâmetros
    ----------

    start_url: url
        url inicial da página de imóveis a venda
    n_pages: int
        número de páginas a serem visitadas
    """
    def __init__(self, start_url="https://www.moretti.imb.br/imoveis-para-venda//page/", n_pages=4):
        self.start_url = start_url
        self.n_pages = n_pages

    def __get_request(self, url):
        """
        Essa função lida com as requições Web

        Parâmetros
        ----------

        url: url
            url a ser feita a requisição do tipo GET
        """
        return requests.get(url)

    def __scrap_links(self):
        """
        Retorna os links de todos os imóveis a venda, para consulta posterior
        """
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
        """
        Gera a lista de todos os imóveis presentes no site
        """
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
            data_dict["Link"] = link
            data_dict["Categoria"] = soup.find(class_ = "property_categs").get_text().split(" ")[0]
            dict_list.append(pd.DataFrame(data = data_dict, index = [0]))
            print("Imóvel: {}." .format(i))
        data_final = pd.concat(dict_list, axis = 0, ignore_index = True)
        data_final.to_csv("Lista_Imoveis.csv")

    def get_links(self):
        """
        Retorna os links de cada imóvel
        """
        return self.links

    def get_data(self):
        """
        Retorna o conjunto de dados final
        """
        return self.data_final

if __name__ == "__main__":
    WC = WebScrapperMoretti()
    WC.scrap_data()
