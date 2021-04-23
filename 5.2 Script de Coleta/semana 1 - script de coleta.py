import requests
from requests.api import head
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_meses_e_anos():
    meses_anos = list()
    #laco para percorrer os anos
    for ano in range(1997, 2018):

        #laco para percorrer os meses
        for mes in range(1, 13):

            #exclui meses antes de setembro de 1997
            if ano == 1997 and mes < 9:
                continue

            #exclui meses apos agosto de 2017
            if ano == 2017 and mes > 8:
                continue

            #forma a string MM/ANO para buscar apenas pelos meses e anos solicitados
            #converte o mes para string e usa a funcao zfill da string para preencher com 0 a esquerda
            href_text = str(mes).zfill(2)+'/'+str(ano)

            meses_anos.append(href_text)
    return meses_anos


def main():
    # base_url principal
    base_url = 'http://www.nuforc.org/webreports/'

    #realiza request inicial
    req = requests.get(base_url + 'ndxevent.html')

    #pega a resposta html em form de string
    body = req.text

    #passa o corpo da pagina para o BeautifulSoup
    soup = BeautifulSoup(body, features="html.parser")

    #pega a tag tbody da tabela contida na pagina
    tbody = soup.find('tbody')
    header=True
    
    meses_anos = get_meses_e_anos()

    #laco que percorre os links da tabela inicial
    for link in tbody.find_all('a'):

        #filtra o link por mes/ano
        if(link.get_text().strip() not in meses_anos):
            continue

        #realiza uma nova request com o link encontrado
        data = requests.get(base_url + link.get('href'))

        #cria uma nova instancia do BeautifulSoup com o conteudo da resposta
        table = BeautifulSoup(data.text, features="html.parser")
        
        #pega a tabela da pagina convertida em string e passa para o pandas na funcao read_html
        #foi necessario instalar a biblioteca lxml
        df = pd.read_html(str(table))[0]

        print(df)

        #header verdadeirao cria o arquivo csv com o cabecalho da tabela
        if header:
            df.to_csv('OVNIS.csv', mode='w', header=True)      

            #seta para falso para que as novas linhas sejam inserias ao final do arquivo                  
            header = False

            #sleep para nao sobrecarregar o servidor com varias requests
            time.sleep(30)

            continue
        
        #demais linhas ele apenas da o apend no arquivo
        df.to_csv('OVNIS.csv', mode='a', header=False)
    
        #sleep para nao sobrecarregar o servidor com varias requests
        time.sleep(30)


if __name__ == "__main__":
    main()