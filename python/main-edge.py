import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time
import os

# Diretório base (pasta onde o script está)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminhos dos arquivos
CSV_PATH = os.path.join(BASE_DIR, "ARUBA GRILL LTDA.csv")
DRIVER_PATH = os.path.join(BASE_DIR, "msedgedriver.exe")
print("📂 Arquivos CSV encontrados na pasta:")
print([f for f in os.listdir(BASE_DIR) if f.endswith(".csv")])


# === 1. Ler as chaves da empresa desejada ===
def carregar_chaves(csv_path):
    df = pd.read_csv(csv_path, sep=";")

    print(f"🔍 {len(df)} NFs carregadas do arquivo.")
    
    chaves = df["Chave de Acesso"].astype(str).str.strip().str.replace("'", "")
    return chaves.tolist()


# === 2. Abrir navegador Edge com Selenium ===
def iniciar_navegador(driver_path):
    options = webdriver.EdgeOptions()
    
    # Caminho direto do perfil do Edge com certificado
    options.add_argument(r"user-data-dir=C:\Users\antonio.everton\AppData\Local\Microsoft\Edge\User Data")
    options.add_argument("--start-maximized")

    service = Service(driver_path)
    driver = webdriver.Edge(service=service, options=options)
    return driver

# === 3. Buscar a NF-e no site da Receita ===
def consultar_e_baixar(driver, chave):
    # Etapa 1: acessar página inicial (força cookies válidos)
    driver.get("https://www.nfe.fazenda.gov.br/portal/principal.aspx")
    time.sleep(1000)

    # Etapa 2: acessar diretamente a consulta completa (evita autodetect)
    driver.get("https://www.nfe.fazenda.gov.br/portal/consultaCompleta.aspx")
    time.sleep(3000)

    try:
        # Espera o campo da chave
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_txtChaveAcessoCompleta"))
        )
        input_chave = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtChaveAcessoCompleta")
        input_chave.clear()
        input_chave.send_keys(chave)
        print(f"🔑 Chave preenchida: {chave}")

        # Pausa para você resolver o CAPTCHA manualmente
        input("🤖 Resolva o CAPTCHA no navegador e pressione Enter aqui para continuar...")

        # Agora clica no botão de consultar
        botao_consultar = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btnConsultarCompleta")
        botao_consultar.click()

        # Espera a página carregar e encontrar o link de download
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Download do Documento"))
        )
        link_download = driver.find_element(By.LINK_TEXT, "Download do Documento")
        link_download.click()

        print(f"✅ XML solicitado com sucesso para {chave[-8:]}. Verifique os downloads.")
    except Exception as e:
        print(f"❌ Erro ao consultar ou baixar NF {chave[-8:]}: {e}")
# === Execução principal ===
if __name__ == "__main__":
    chaves = carregar_chaves(CSV_PATH)

    if not chaves:
        print("⚠️ Nenhuma chave encontrada para a empresa no arquivo.")
        exit()

    driver = iniciar_navegador(DRIVER_PATH)
    consultar_e_baixar(driver, chaves[0])  # Testa com a primeira chave

    input("⏳ Pressione Enter após resolver o CAPTCHA para encerrar...")
    driver.quit()
