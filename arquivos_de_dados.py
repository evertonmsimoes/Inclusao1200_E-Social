import pandas as pd
import os
import csv


class arquivos_de_dados:

    diretorio_atual = os.getcwd()

    def lendo_base_de_dados(self):

        df_excel = pd.read_excel('Dados\Dados_CPF.xlsx',  dtype={'CPF': 'object', 'Id do demostrativo': 'object', 'Data do Pagamento': 'object', 'Comp Ref o Pagamento': 'object', 'Id do demostrativo': 'object', 'Valor': 'object'})
        df_csv = pd.read_csv('Dados\InformacoesGeradas.csv', sep=';', encoding='latin-1', dtype={'CPF': 'object'})

        # Encontre as entradas que estão na planilha, mas não estão no CSV
        resultado = df_excel[~df_excel['CPF'].isin(df_csv['CPF'])]

        # Salve o resultado em um novo arquivo Excel, se desejar
        resultado.to_excel(r'Dados\resultado.xlsx', index=False)
        Df_res = pd.read_excel(r'Dados\resultado.xlsx', dtype={'CPF': 'object', 'Id do demostrativo': 'object', 'Data do Pagamento': 'object', 'Comp Ref o Pagamento': 'object', 'Id do demostrativo': 'object', 'Valor': 'object'})
        return Df_res


    
    
    def GravLog(self, CPF, resposta):
        nome_arquivo_csv = "Dados\InformacoesGeradas.csv"

        try:
            with open(nome_arquivo_csv, "a", newline="", encoding="utf-8") as arquivo_csv:
                escritor_csv = csv.writer(arquivo_csv, delimiter=";")
                escritor_csv.writerow([CPF, resposta])
            print("Informações gravadas com sucesso no arquivo Log.csv!")
        except Exception as e:
            print("Ocorreu um erro ao gravar as informações:", e)  



