from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pyautogui
import pyperclip
import openpyxl
from openpyxl import Workbook
import os

class EconetScrapper:
    def __init__(self):
        # Configurar o driver para conectar a uma instância existente do navegador
        self.driver = None
        self.dados_coletados = []
        
    def conectar_navegador_existente(self):
        """Conecta a uma instância existente do Chrome/Edge"""
        try:
            # Opções para conectar ao navegador já aberto
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            
            # Tentar conectar ao Chrome primeiro
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
                print("✓ Conectado ao Chrome existente")
                return True
            except:
                # Se falhar, tentar Edge
                try:
                    edge_options = webdriver.EdgeOptions()
                    edge_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
                    self.driver = webdriver.Edge(options=edge_options)
                    print("✓ Conectado ao Edge existente")
                    return True
                except:
                    print("❌ Não foi possível conectar ao navegador existente")
                    return False
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            return False
    
    def alternar_entre_abas(self):
        """Alterna entre as abas abertas do navegador"""
        abas = self.driver.window_handles
        print(f"📋 Encontradas {len(abas)} abas abertas")
        return abas
    
    def extrair_dados_da_aba(self, aba_handle):
        """Extrai dados dos elementos especificados de uma aba"""
        self.driver.switch_to.window(aba_handle)
        time.sleep(2)
        
        dados_aba = {
            'url': self.driver.current_url,
            'titulo': self.driver.title,
            'truncate_text': [],
            'datas_validade': [],
            'inputs_desabilitados': []
        }
        
        try:
            # 1. Extrair elementos com classe "truncate-text"
            elementos_truncate = self.driver.find_elements(By.CLASS_NAME, "truncate-text")
            for elemento in elementos_truncate:
                try:
                    texto = elemento.text.strip()
                    if texto:
                        dados_aba['truncate_text'].append(texto)
                        print(f"📝 Truncate-text: {texto}")
                except:
                    pass
            
            # 2. Extrair parágrafos com data de validade (data-v-183ffdf0)
            paragrafos_data = self.driver.find_elements(By.CSS_SELECTOR, "p[data-v-183ffdf0]")
            for p in paragrafos_data:
                try:
                    texto = p.text.strip()
                    if "Válido até" in texto or "válido até" in texto.lower():
                        dados_aba['datas_validade'].append(texto)
                        print(f"📅 Data de validade: {texto}")
                except:
                    pass
            
            # 3. Extrair valores de inputs desabilitados
            inputs_desabilitados = self.driver.find_elements(By.CSS_SELECTOR, "div[data-v-183ffdf0] input[disabled]")
            for input_elem in inputs_desabilitados:
                try:
                    valor = input_elem.get_attribute('value') or input_elem.text
                    if valor and valor.strip():
                        dados_aba['inputs_desabilitados'].append(valor.strip())
                        print(f"🔒 Input desabilitado: {valor}")
                except:
                    pass
            
        except Exception as e:
            print(f"❌ Erro ao extrair dados: {e}")
        
        return dados_aba
    
    def coletar_todos_dados(self):
        """Coleta dados de todas as abas"""
        if not self.conectar_navegador_existente():
            return False
        
        abas = self.alternar_entre_abas()
        
        for i, aba in enumerate(abas):
            print(f"\n🔍 Processando aba {i+1}/{len(abas)}")
            dados = self.extrair_dados_da_aba(aba)
            self.dados_coletados.append(dados)
        
        return True
    
    def criar_planilha(self, nome_arquivo="dados_extraidos.xlsx"):
        """Cria uma planilha Excel com os dados coletados"""
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Dados Extraídos"
            
            # Cabeçalhos
            headers = ['Aba', 'URL', 'Título', 'Truncate Text', 'Data Validade', 'Input Desabilitado']
            for col, header in enumerate(headers, 1):
                ws.cell(row=1, column=col, value=header)
            
            # Dados
            linha_atual = 2
            for i, dados in enumerate(self.dados_coletados):
                # Para cada tipo de dado, criar uma linha
                max_items = max(
                    len(dados['truncate_text']),
                    len(dados['datas_validade']),
                    len(dados['inputs_desabilitados']),
                    1
                )
                
                for j in range(max_items):
                    ws.cell(row=linha_atual, column=1, value=f"Aba {i+1}")
                    ws.cell(row=linha_atual, column=2, value=dados['url'])
                    ws.cell(row=linha_atual, column=3, value=dados['titulo'])
                    
                    # Truncate text
                    if j < len(dados['truncate_text']):
                        ws.cell(row=linha_atual, column=4, value=dados['truncate_text'][j])
                    
                    # Data validade
                    if j < len(dados['datas_validade']):
                        ws.cell(row=linha_atual, column=5, value=dados['datas_validade'][j])
                    
                    # Input desabilitado
                    if j < len(dados['inputs_desabilitados']):
                        ws.cell(row=linha_atual, column=6, value=dados['inputs_desabilitados'][j])
                    
                    linha_atual += 1
            
            # Salvar arquivo
            caminho_completo = os.path.join(os.getcwd(), nome_arquivo)
            wb.save(caminho_completo)
            print(f"✅ Planilha salva em: {caminho_completo}")
            return caminho_completo
            
        except Exception as e:
            print(f"❌ Erro ao criar planilha: {e}")
            return None
    
    def abrir_planilha_existente_e_colar(self):
        """Abre uma planilha existente e cola os dados"""
        try:
            # Simular Alt+Tab para alternar para a planilha
            print("🔄 Alternando para a planilha...")
            pyautogui.hotkey('alt', 'tab')
            time.sleep(1)
            
            # Preparar dados para colar
            dados_para_colar = []
            for i, dados in enumerate(self.dados_coletados):
                dados_para_colar.append(f"=== ABA {i+1} ===")
                dados_para_colar.append(f"URL: {dados['url']}")
                dados_para_colar.append(f"Título: {dados['titulo']}")
                
                if dados['truncate_text']:
                    dados_para_colar.append("Truncate Text:")
                    dados_para_colar.extend([f"  - {item}" for item in dados['truncate_text']])
                
                if dados['datas_validade']:
                    dados_para_colar.append("Datas de Validade:")
                    dados_para_colar.extend([f"  - {item}" for item in dados['datas_validade']])
                
                if dados['inputs_desabilitados']:
                    dados_para_colar.append("Inputs Desabilitados:")
                    dados_para_colar.extend([f"  - {item}" for item in dados['inputs_desabilitados']])
                
                dados_para_colar.append("")  # Linha em branco
            
            # Copiar para área de transferência
            texto_final = "\n".join(dados_para_colar)
            pyperclip.copy(texto_final)
            
            # Colar na planilha
            time.sleep(0.5)
            pyautogui.hotkey('ctrl', 'v')
            print("✅ Dados colados na planilha!")
            
        except Exception as e:
            print(f"❌ Erro ao colar na planilha: {e}")
    
    def executar_automacao(self):
        """Executa toda a automação"""
        print("🚀 Iniciando automação EconetScrapper...")
        
        # Coletar dados
        if self.coletar_todos_dados():
            print(f"\n📊 Coletados dados de {len(self.dados_coletados)} abas")
            
            # Criar planilha Excel
            arquivo_excel = self.criar_planilha()
            
            # Colar em planilha existente
            self.abrir_planilha_existente_e_colar()
            
            # Mostrar resumo
            print("\n📋 RESUMO DOS DADOS COLETADOS:")
            for i, dados in enumerate(self.dados_coletados):
                print(f"\n📄 Aba {i+1}: {dados['titulo']}")
                print(f"   🔗 URL: {dados['url']}")
                print(f"   📝 Truncate texts: {len(dados['truncate_text'])}")
                print(f"   📅 Datas validade: {len(dados['datas_validade'])}")
                print(f"   🔒 Inputs desabilitados: {len(dados['inputs_desabilitados'])}")
        
        else:
            print("❌ Falha ao coletar dados")
        
        # Fechar driver
        if self.driver:
            self.driver.quit()

# Executar a automação
if __name__ == "__main__":
    scrapper = EconetScrapper()
    scrapper.executar_automacao()
