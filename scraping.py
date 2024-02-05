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
#    url2 = "https://www.fundamentus.com.br/resultados_trimestrais.php?papel=" + ativo + "&tipo=1"

    driver.get(url1)

    try:
        segmento = driver.find_elements(By.TAG_NAME, 'a')[30].text
        subsegmento = driver.find_elements(By.TAG_NAME, 'a')[31].text
        valorMercado = driver.find_elements(By.CLASS_NAME, 'txt')[21].text
        ultimoBalanco = driver.find_elements(By.CLASS_NAME, 'txt')[23].text
        nroAcoes = driver.find_elements(By.CLASS_NAME, 'txt')[27].text
        varMes = driver.find_elements(By.TAG_NAME, "font")[1].text
        var12Meses = driver.find_elements(By.TAG_NAME, "font")[2].text
        var2024 = driver.find_elements(By.TAG_NAME, "font")[4].text
        var2023 = driver.find_elements(By.TAG_NAME, "font")[5].text
        var2022 = driver.find_elements(By.TAG_NAME, "font")[6].text
        var2021 = driver.find_elements(By.TAG_NAME, "font")[7].text
        var2020 = driver.find_elements(By.TAG_NAME, "font")[8].text
        var2019 = driver.find_elements(By.TAG_NAME, "font")[9].text
        pl = driver.find_elements(By.CLASS_NAME, "txt")[32].text
        lpa = driver.find_elements(By.CLASS_NAME, "txt")[34].text
        pvp = driver.find_elements(By.CLASS_NAME, "txt")[37].text
        vpa = driver.find_elements(By.CLASS_NAME, "txt")[39].text
        pebit = driver.find_elements(By.CLASS_NAME, "txt")[42].text
        margemBruta = driver.find_elements(By.CLASS_NAME, "txt")[44].text

        # Pegar o link do último relatório divulgado pela empresa
#        driver.get(url2)
#        elemento_link = driver.find_element(By.XPATH, "//a[contains(@href, 'https://www.rad.cvm.gov.br')]")
#        href_do_link = elemento_link.get_attribute('href')

        # Adicionar os dados lidos ao dicionário
        dados = {
            "ativo": ativo,
            "segmento": segmento,
            "sub_segmento": subsegmento,
            "valor_mercado": valorMercado,
            "ultimo_balanco": ultimoBalanco,
            "nro_acoes": nroAcoes,
            "varMes": varMes,
            "var12Mes": var12Meses,
            "var2024": var2024,
            "var2023": var2023,
            "var2022": var2022,
            "var2021": var2021,
            "var2020": var2020,
            "var2019": var2019,
            "P/L": pl,
            "LPA": lpa,
            "P/VP": pvp,
            "VPA": vpa,
            "P/EBIT": pebit,
            "Marg. Bruta": margemBruta,
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
