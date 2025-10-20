import os
import csv
import xml.etree.ElementTree as ET

# Namespace usado no XML da NFe
NFE_NAMESPACE = 'http://www.portalfiscal.inf.br/nfe'
NAMESPACE = {'ns': NFE_NAMESPACE}

ET.register_namespace('', NFE_NAMESPACE)

# Diretório onde está o script
script_dir = os.path.dirname(os.path.abspath(__file__))
print("📁 Diretório encontrado:", script_dir)

# Lista para armazenar os dados: [Arquivo XML, cProd, xProd]
produtos_data = []

# Iterar sobre todos os arquivos XML no diretório
for filename in os.listdir(script_dir):
    if filename.endswith('.xml'):
        file_path = os.path.join(script_dir, filename)
        try:
            print(f"📄 Lendo arquivo: {file_path}")
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Buscar elementos <prod> dentro de <det>
            for prod_element in root.findall('.//ns:det/ns:prod', NAMESPACE):
                cprod_tag = prod_element.find('ns:cProd', NAMESPACE)
                xprod_tag = prod_element.find('ns:xProd', NAMESPACE)

                cprod_text = cprod_tag.text.strip() if cprod_tag is not None and cprod_tag.text else ''
                xprod_text = xprod_tag.text.strip() if xprod_tag is not None and xprod_tag.text else ''

                # Salva mesmo que não tenha números, para não perder registros
                if cprod_text or xprod_text:
                    produtos_data.append([filename, cprod_text, xprod_text])

        except ET.ParseError:
            print(f"❌ Erro ao analisar XML: {filename}")
        except Exception as e:
            print(f"⚠️ Erro ao processar {filename}: {str(e)}")

# Caminho do arquivo CSV de saída
csv_file_path = os.path.join(script_dir, 'cprod_resultado.csv')

# Escrever o CSV com separador ";"
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(['Arquivo XML', 'Cprod', 'Nome do Produto'])  # Cabeçalho
    writer.writerows(produtos_data)

print(f"\n✅ Arquivo CSV salvo com sucesso: {csv_file_path}")
