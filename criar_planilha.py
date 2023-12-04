from openpyxl import Workbook 


class Planilha:    
    wb = None
    def Criar_planilha(self,sites):
        self.sites = sites
        self.wb = Workbook()
        title = self.sites[0]
        plan =  self.wb.active
        plan.title = '{0}'.format(title)
        for i in range(0,len(self.sites)):
            if i == 0:
               plan['B1'] = 'NOME DO PRODUTO:'
               plan['C1'] = 'LINK DO PRODUTO:'
               plan['D1'] = 'PREÇO:'
               plan['F1'] = 'MELHOR PRODUTO COM BASE EM PREÇO:'
               plan['F2'] = 'NOME:'
               plan['F3'] = 'PREÇO:'
               plan['F4'] = 'LINK:'
            else:
                self.wb.create_sheet(title=self.sites[i])
                planilha = self.wb[self.sites[i]]
                planilha['B1'] = 'NOME DO PRODUTO:'
                planilha['C1'] = 'LINK DO PRODUTO:'
                planilha['D1'] = 'PREÇO:'
                planilha['F1'] = 'MELHOR PRODUTO COM BASE EM PREÇO:'
                planilha['F2'] = 'NOME:'
                planilha['F3'] = 'PREÇO:'
                planilha['F4'] = 'LINK:'
    def Adicionar_dados(self,site,nomes,precos,links):
    #acessando as planilhas
        print('adicionando dados...')
        self.site = site
        self.nomes = nomes
        self.precos = precos
        self.links = links
        contador = 2
    #criando tabelas bases e acessando elas com os seus titulos
        for nome,link,preco, in zip(self.nomes,self.links,self.precos,):
            planilha = self.wb[self.site]
            B =f'B{contador}'
            C =f'C{contador}'
            D =f'D{contador}'
            #adicionando nome dos produtos e links
            planilha[B] = nome
            #adicionando o link dos produtos
            planilha[C] = link
            #adicionando npreço
            planilha[D] = preco
            contador += 1
        lista_precos_sem_separador =[] 
        for valor in self.precos:
            novo_valor = valor.replace('.','')
            lista_precos_sem_separador.append(novo_valor)
        planilha = self.wb[self.site]
        melhor_valor = min(lista_precos_sem_separador)
        indice = lista_precos_sem_separador.index(melhor_valor)
        planilha['G3'] = self.precos[indice]
        planilha['G2'] = self.nomes[indice]
        planilha['G4'] = self.links[indice]
    def Salvar_planilhas(self):
        nome_da_planilha = input('DIGITE O NOME DA PLANILHA:')
        self.wb.save(nome_da_planilha + '.xlsx')
        print('planilha salva!') 
