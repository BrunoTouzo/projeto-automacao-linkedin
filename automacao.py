## imports
# pandas
import pandas as pd

# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# time
from time import sleep, localtime
from datetime import date

##
def Main():
    ## passo 1: obter filtros desejados do usuário
    
    lista_vagas:list[dict] = []
    conjunto_filtros:dict = {
        "vagas":"",
        "localidade":"Brasil",
    }
    conjunto_filtros["vagas"] = input("cargo desejado:").strip()
    conjunto_filtros["localidade"] = input("Localidade desejada:").strip()
    limite:int = int(input("quantidade de vagas:").strip())

    # instanciando o navegador
    servico = Service(ChromeDriverManager().install()) # lidando com versão do webdriver automaticamente
    nv = webdriver.Chrome(service=servico) # instanciando o navegador através do serviço
    nv.set_window_size(1280,720)

    ## passo 2: procurar vagas compatíveis

    #indo para a página da web
    nv.get(f'https://www.linkedin.com/jobs/search?keywords={conjunto_filtros["vagas"]}&location={conjunto_filtros["localidade"]}')

    # esperando carregar a primeira vaga na tela
    while len(nv.find_elements(By.XPATH, '//*[@id="main-content"]/section[2]/ul/li[1]'))<1: 
        sleep(0.5)

    lista_elementos:list = [
            '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/a/h2', # nome da vaga
            '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[1]/span[1]/a', # nome da empresa
            '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[1]/span[2]', # local da vaga
            '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[2]/span[1]', # data de postagem da vaga
            '/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/h4/div[2]/span[2]', # quantidade de aplicações para a vaga
            '/html/body/div[1]/div/section/div[2]/div/section[1]/div/div/section/div', # descrição da vaga
            '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[1]/span', # nível de experiência da vaga
            '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[2]/span', # tipo de emprego da vaga
            '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[3]/span', # função da vaga
            '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[4]/span' #  setor de atuação da vaga

        ]
    
    # obtendo informações das primeiras 20 vagas encontradas
    for i in range(1, limite+1):
        print(f"i: {i}")

        while len(nv.find_elements(By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{i}]'))<1: # esperando carregar o card esquerdo
            print("esperando card esquerdo...")
            sleep(0.2)
        
        nv.find_element( By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{i}]').click() # clicando no card da vaga
        sleep(1)
        # obtendo informações da vaga e salvando em uma lista
        cont:int=0
        while len(nv.find_elements(By.XPATH, f'/html/body/div[1]/div/section/div[2]/section/div/div[1]/div/a/h2'))<1: #esperando o painel direito carregar
            # pequeno sistema de aguardo de carregamento de página
            cont+=1
            if cont >10 and i>1:
                nv.find_element( By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{i-1}]').click() # clicando no card da vaga
                sleep(0.2)
                nv.find_element( By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{i}]').click() # clicando no card da vaga
                sleep(0.2)
                cont = 0
            sleep(0.5)
        
        
        while len(nv.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]/div/section[1]/div/div/section/div').text.strip())<1: #esperando o painel direito carregar
            print("esperando descrição da vaga...")
            cont+=1
            if cont >10 and i>1:
                nv.find_element( By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{i-1}]').click() # clicando no card da vaga
                sleep(0.2)
                nv.find_element( By.XPATH, f'//*[@id="main-content"]/section[2]/ul/li[{i}]').click() # clicando no card da vaga
                sleep(0.2)
                cont = 0
            sleep(0.5)

        ## passo 3: retornar vagas e armazená-las
        # guardando informações de uma vaga em um dicionário
        d1:dict = {}
        
        d1["nome_vaga"] = nv.find_element(By.XPATH, lista_elementos[0]).text.strip()
        d1["nome_empresa_vaga"] = nv.find_element(By.XPATH, lista_elementos[1]).text.strip()
        d1["Local_vaga"] = nv.find_element(By.XPATH, lista_elementos[2]).text.strip()
        d1["data_postagem_vaga"] = nv.find_element(By.XPATH, lista_elementos[3]).text.strip()
        #d1["qtd_aplicacoes_vaga"] = nv.find_element(By.XPATH, lista_elementos[4]).text
        d1["descricao_vaga"] = nv.find_element(By.XPATH, lista_elementos[5]).text.strip()
        d1["nvl_experiencia_vaga"] = nv.find_element(By.XPATH, lista_elementos[6]).text.strip()
        d1["tipo_emprego_vaga"] = nv.find_element(By.XPATH, lista_elementos[7]).text.strip()
        d1["Funcao_vaga"] = nv.find_element(By.XPATH, lista_elementos[8]).text.strip()
        d1["setor_vaga"] = nv.find_element(By.XPATH, lista_elementos[9]).text.strip()
        
        lista_vagas.append(d1) # adicionando o elemento à lista

    
    ## passo 4: salvar informações em um arquivo xlsx
    # criando um dataframe
    tabela = pd.DataFrame({
        "nome_vaga":[],
        "nome_empresa_vaga":[],
        "Local_vaga":[],
        "data_postagem_vaga":[],
        "descricao_vaga":[],
        "nvl_experiencia_vaga":[],
        "tipo_emprego_vaga":[],
        "Funcao_vaga":[],
        "setor_vaga":[]
    })
    
    # adicionando linhas
    for i in range(len(lista_vagas)):
        d:dict = lista_vagas[i]
        tabela.loc[i] = [
            d["nome_vaga"],
            d["nome_empresa_vaga"],
            d["Local_vaga"],
            d["data_postagem_vaga"],
            d["descricao_vaga"],
            d["nvl_experiencia_vaga"],
            d["tipo_emprego_vaga"],
            d["Funcao_vaga"],
            d["setor_vaga"]
        ]

    
    # criando para uma planilha excel
    #with open(f'/busca_empregos_{date.today}.xlsx', 'w'):
    t = localtime()
    with pd.ExcelWriter(f'planilha-{date.today()}-{t.tm_hour}_{t.tm_min}_{t.tm_sec}.xlsx') as writer:
        tabela.to_excel(writer,sheet_name='vagas')


## chamando a main
Main()
