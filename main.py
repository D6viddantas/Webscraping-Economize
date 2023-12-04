import requests
from bs4 import BeautifulSoup
import re
import random
from criar_planilha import Planilha

class Economize:
    Modulo = Planilha()
    item = input('Escreva o que você quer consultar: ')
    lista_de_sites = (
'https://lista.mercadolivre.com.br/{0}',
'https://pt.aliexpress.com/w/wholesale-{0}.html?spm=a2g0o.home.auto_suggest.2.31c81c911jKo9h',
)
    lista_css_preco = ('andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript',
'multi--price-sale--U-S0jtj',
)
    sites = ['MERCADO LIVRE',
'ALIEXPRESS',]
    lista_css_nome_produto = ('ui-search-item__title','multi--titleText--nXeOvyr')
    classe_link_produto = ['ui-search-item__group__element ui-search-link__title-card ui-search-link',
'multi--container--1UZxxHY cards--card--3PJxwBm search-card-item',
]
    user_agent =[
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0']
    soup = None
    Modulo.Criar_planilha(sites)
    lista_resultado_da_busca_preco = []
    lista_resultado_da_busca_nome = []
    lista_resultado_da_busca_link = []
    def Requisicao_sites(self,link):
        agent = random.choice(self.user_agent)
        requisicao = requests.get(link,agent)
        self.soup = BeautifulSoup(requisicao.content, 'html.parser')
        if requisicao.status_code == 200:
            print('200')
            for css_preco,css_nome,css_link in zip(self.lista_css_preco,self.lista_css_nome_produto,self.classe_link_produto):
                self.Iniciar_coleta(css_link,css_preco,css_nome)
                
        else:
            soup = BeautifulSoup(requisicao.content, 'html.parser')
            title = soup.find('title')
            print('ERRo = {0} no site:{1},não é posivel buscar o produto.'.format(requisicao.status_code,title.get_text()))
                
    
    def Iniciar_progama(self):
        i = 0
        for site in self.lista_de_sites:
            self.Requisicao_sites(site.format(self.item))
            self.Modulo.Adicionar_dados(self.sites[i],self.lista_resultado_da_busca_nome,self.lista_resultado_da_busca_preco,self.lista_resultado_da_busca_link)
            self.lista_resultado_da_busca_preco = []
            self.lista_resultado_da_busca_nome = []
            self.lista_resultado_da_busca_link = []
            i += 1
        self.Modulo.Salvar_planilhas()
    def Coletar_preco(self,classe_css):
        busca_pelo_preco = self.soup.find_all(class_ = classe_css)
        for texto in busca_pelo_preco:
            preco = texto.get_text()
            precos = re.findall('\d+',preco)
            if len(precos) == 1:
               self.lista_resultado_da_busca_preco.append(precos[0])
            else:
                casa_decimal = '.'
                string = casa_decimal.join(precos)
                self.lista_resultado_da_busca_preco.append(string)
    def Coletar_nome_do_produto(self,classe_css):
        busca_nome_produto = self.soup.find_all(class_ = classe_css)
        for nome_do_produto in busca_nome_produto:
            resultado_da_busca_nome = nome_do_produto.get_text()
            self.lista_resultado_da_busca_nome.append(resultado_da_busca_nome)
    def Coletar_link(self,classe_css):
        buscar_link_produto = self.soup.find_all(class_ = classe_css)
        for url in buscar_link_produto:
            link = url.get('href')
            self.lista_resultado_da_busca_link.append(link)
    def Iniciar_coleta(self,css_link,css_preco,css_nome):
        self.Coletar_preco(css_preco)
        self.Coletar_nome_do_produto(css_nome)
        self.Coletar_link(css_link)
eco =  Economize()
eco.Iniciar_progama()
