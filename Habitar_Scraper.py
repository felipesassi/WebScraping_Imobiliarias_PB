import requests
from bs4 import BeautifulSoup
import pandas as pd


class WebScrapperHabitar():
    """
    Essa classe é utilizada para realizar a raspagem de dados no site da construtora Habitar, em Pato Branco (PR).

    Parâmetros
    ----------

    start_url: url
        url inicial da página de imóveis a venda
    n_pages: int
        número de páginas a serem visitadas
    """
    def __init__(self, start_url, n_pages=4):
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
        Retorna os links de todofind("a") os imóveis a venda, para consulta posterior
        """
        self.links = []
        for i in range(self.n_pages):
            url = self.start_url
            page = self.__get_request(url)
            soup = BeautifulSoup(page.text, "html.parser")
            link = soup.find_all("a")
            for l in link:
                if (l["href"].split("/")[1] == "imoveis") and (len(l["href"].split("/")) > 3):
                    default_url = "http://www.habitar.imb.br"
                    link_c = default_url + l["href"]
                    self.links.append(link_c)
            self.n_links = len(self.links)

    def scrap_data(self, save_to):
        """
        Gera a lista de todos os imóveis presentes no site
        """
        self.__scrap_links()
        data_dict = dict()
        dict_list = list()
        for i, link in enumerate(self.links):
            page = self.__get_request(link)
            soup = BeautifulSoup(page.text, "html.parser")
            data = soup.findAll(class_="details")
            for d in data:
                data_dict["Preço"] = d.find("h5").get_text()
                data_dict["Detalhes"] = d.find(class_="description").get_text()
            data_dict["Link"] = link
            # data_dict["Categoria"] = soup.find(class_="property_categs").get_text().split(" ")[0]
            dict_list.append(pd.DataFrame(data=data_dict, index=[0]))
            print("Imóvel: {}." .format(i))
        data_final = pd.concat(dict_list, axis=0, ignore_index=True)
        save_to = save_to + ".csv"
        data_final.to_csv(save_to)

    def get_links(self):
        """
        Retorna os links de cada imóvel
        """
        return self.links

    def get_data(self):
        """
        Retorna o conjunto de dados final    # WC = WebScrapperHabitar(start_url="http://www.habitar.imb.br/imoveis/", n_pages=1)
    # WC.scrap_data("Lista_Imoveis_Generica_Habitar")
        """
        return self.data_final

if __name__ == "__main__":
    WC = WebScrapperHabitar(start_url="http://www.habitar.imb.br/imoveis/", n_pages=1)
    WC.scrap_data("Lista_Imoveis_Generica_Habitar")
