import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Ler a lista de ativos obtidos em "https://statusinvest.com.br/acoes/busca-avancada"
data = pd.read_csv("datasets\statusinvest-busca-avancada.csv")

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

dados_list = []

for ativo in data['TICKER']:
    url1 = "https://www.fundamentus.com.br/detalhes.php?papel=" + ativo
    url2 = "https://www.fundamentus.com.br/resultados_trimestrais.php?papel=" + ativo + "&tipo=1"

    driver.get(url1)
    
    try:
        segmento = driver.find_elements(By.TAG_NAME, 'a')[30].text
        subsegmento = driver.find_elements(By.TAG_NAME, 'a')[31].text
        dy = driver.find_elements(By.TAG_NAME, 'a')
        
        print(dy)
        
        # Pegar o link do último relatório divulgado pela empresa        
        driver.get(url2)
        elemento_link = driver.find_element(By.XPATH, "//a[contains(@href, 'https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento')]")
        href_do_link = elemento_link.get_attribute('href')
        
        # Adicionar os dados lidos ao dicionário
        dados = {
            "ativo": ativo, 
            "segmento": segmento, 
            "sub-segmento": subsegmento, 
            "link_release": href_do_link
        }
        
        dados_list.append(dados)
        print(dados)

    except Exception as e:
        print(f"Erro ao processar {ativo}")
        continue

# Criar um DataFrame que armazenara os dados da lista
df = pd.DataFrame(dados_list)
df.to_csv('dados_extraidos.csv', index=False, encoding="latin-1")

# Fechar o navegador ao terminar de realizar a raspagem
driver.quit()
