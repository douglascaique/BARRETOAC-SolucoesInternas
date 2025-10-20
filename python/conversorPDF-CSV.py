import os
import pdfplumber
import pandas as pd

# Caminho para a pasta onde o script está
pasta = os.path.dirname(os.path.abspath(__file__))

# Lista arquivos PDF na pasta
arquivos_pdf = [f for f in os.listdir(pasta) if f.lower().endswith(".pdf")]

if not arquivos_pdf:
    print("Nenhum arquivo PDF encontrado.")
else:
    for nome_pdf in arquivos_pdf:
        caminho_pdf = os.path.join(pasta, nome_pdf)
        nome_csv = os.path.splitext(nome_pdf)[0] + ".csv"
        caminho_csv = os.path.join(pasta, nome_csv)

        todas_tabelas = []

        with pdfplumber.open(caminho_pdf) as pdf:
            for pagina in pdf.pages:
                tabelas = pagina.extract_tables()
                for tabela in tabelas:
                    if tabela:  # ignora tabelas vazias
                        df = pd.DataFrame(tabela)
                        todas_tabelas.append(df)

        if todas_tabelas:
            resultado = pd.concat(todas_tabelas, ignore_index=True)
            resultado.to_csv(caminho_csv, index=False)
            print(f"Arquivo convertido: {nome_pdf} → {nome_csv}")
        else:
            print(f"Nenhuma tabela encontrada em: {nome_pdf}")
