#Bibliotecas Utilizadas 
import time
import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


logging.basicConfig(level= logging.INFO, filename="serve.log", format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.basicConfig(level= logging.ERROR, filename="serve.log", format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
#Aqui é onde o Pandas ler o CSV

tabela = pd.read_excel("documento.xlsx")
tabela = pd.read_excel("documento.xlsx", dtype={'cns': str, 'cpf': str, 'conselho': str, 'matricula': str, 'naturalidade': str, 'nacionalidade': str, 'inicio do vinculo': str, 'inicio': str, 'ano inicio': str, 'ano fim': str, 'cbo': str})
tabela_values_list = tabela.values.tolist()

#--------------------------------------------------------------------------------------------------------------------------

class main():

    def __init__ (self, email, senha):
        self.email = email
        self.senha = senha
        
        servico = Service(GeckoDriverManager().install())
        self.navegador = webdriver.Firefox(service=servico)

    def login(self):

        #Aqui é onde a URL do Ambiente é adicionada
        self.navegador.get("http://172.16.99.238/aghu/pages/casca/casca.xhtml")
        logging.info('Url acessada com Sucesso')
        #Efetuado login e senha ele entra no sistema 
        self.navegador.find_element('xpath', '//*[@id="usuario:usuario:inputId"]').send_keys(self.email)
        logging.info('Login Preenchido com sucesso')
        self.navegador.find_element('xpath', '//*[@id="password:inputId"]').send_keys(self.senha)
        time.sleep (1)
        logging.info('Senha Preenchido com sucesso')
    
        self.navegador.find_element('xpath', '/html/body/div[1]/div/div/div/div/form/fieldset/div[4]/button/span').click()
        logging.info('Clicou no Botao Entrar com Sucesso')
        return self.navegador
  
    def scroll_to_element(self, element):
        self.navegador.execute_script("arguments[0].scrollIntoView(true);", element)
    #--------------------------------------------------------------------------------------------------------------------------

    #Condição de como a lista vai ser chamada, dentro do CSV e os value que vão ser preenchidos.
    def cadastra_sistema(self, lista):

        nome = lista [0]
        mae = lista [1]
        sexo = lista [2]
        data_de_nacimento = lista [3]
        nacionalidade = lista [4] 
        naturalidade = lista [5]
        email = lista [6]
        rg = lista [7]
        orgao_emissor = lista [8]  # Corrigindo a nomenclatura da coluna
        uf = lista [9]
        cpf = lista [10]
        vinculo = lista [11]
        conselho = lista [12]
        matricula = lista [13]
        inicio_do_vinculo = lista [14]
        cbo = lista [15]
        inicio = lista [16]
        cns = lista [17]
        curso = lista [18]
        ano_inicio = lista [19]
        ano_fim = lista [20]
        perfil = lista [21]
        
        #Acessar o menu do modulo pessoas
        self.navegador.find_element('xpath', '/html/body/header/div[2]/ul/li[14]/a/span').click()
        time.sleep(0.3)
        logging.info('Clicou em Outros Modulos com Sucesso')

        self.navegador.switch_to.default_content()

        self.navegador.find_element('xpath', '/html/body/header/div[2]/ul/li[14]/ul/li[3]/a/span').click()
        logging.info('Clicou em Colaborador com Sucesso')
        time.sleep(0.3)
        self.navegador.switch_to.default_content()

        self.navegador.find_element('xpath', '/html/body/header/div[2]/ul/li[14]/ul/li[3]/ul/li[1]/a/span').click()
        logging.info('Clicou em Administrar Servidores com Sucesso')
        time.sleep(0.3)
        self.navegador.switch_to.default_content()

        self.navegador.find_element('xpath', '/html/body/header/div[2]/ul/li[14]/ul/li[3]/ul/li[1]/ul/li[1]/a/span').click()
        logging.info('Clicou em Pessoas com Sucesso')
        time.sleep(0.3)
        self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------


        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))

        self.navegador.switch_to.frame(iframe)
        #Clica dentro do elemento pesquisa
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/form[3]/div/button[1]/span[2]')))
        elemento_dentro_do_iframe.click()
        logging.info('Clicou no Botao de Pesquisar com sucesso')
        #Após interagir com o iframe, você pode voltar ao contexto padrão
        self.navegador.switch_to.default_content()
        
        #--------------------------------------------------------------------------------------------------------------------------

        #Clicar no botão Novo
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))

        self.navegador.switch_to.frame(iframe)
        #Clica dentro do elemento novo
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/form[3]/div/span/button/span[2]')))
        elemento_dentro_do_iframe.click()
        logging.info('Clicou no Botao de Novo com sucesso')
        #Após interagir com o iframe, você pode voltar ao contexto padrão
        self.navegador.switch_to.default_content()


        #--------------------------------------------------------------------------------------------------------------------------
    

        try:
            # Verifica se o nome é válido (não nulo e não NaN)
            if not nome or str(nome).lower() == 'nan':
                logging.error(f"ERRO: NOME NAO ENCONTRADO NA PLANILHA. Nome: {nome}")
                time.sleep(5)
                self.navegador.refresh()
                
                # Faz o refresh se o nome não é válido
                return

            # Clicar no elemento Nome, e preenche o nome puxando da planilha
           
            
            iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
            
            self.navegador.switch_to.frame(iframe)

            # Encontra o elemento dentro do Frame
            elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="nomePessoa:nomePessoa:inputId"]')))
            elemento_dentro_do_iframe.click()
            elemento_dentro_do_iframe.send_keys(nome)

            logging.info(f"Preencheu Nome '{nome}' com sucesso")
            self.navegador.switch_to.default_content()

            # Após interagir com o iframe, você pode voltar ao contexto padrão

        except Exception as e:
            logging.error(f"ERRO AO PREENCHER NOME '{nome}': {str(e)}")

            self.navegador.refresh()
            time.sleep(3)

            self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------
        
        try:
             # Verifica se o mae é válido (não nulo e não NaN)
            if not mae or str(mae).lower() == 'nan':
                logging.error(f"ERRO: NOME DA MAE NAO ENCONTRADO NA PLANILHA. mae: {mae}")
                time.sleep(3)
                self.navegador.refresh()
                
                # Faz o refresh se o nome não é válido
                return
                
            #Clicar no elemento Mãe, e preenche puxando da planilha
            iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))

            self.navegador.switch_to.frame(iframe)
            #Encontra o elemento dentro do Frame
            elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="nomeMae:nomeMae:inputId"]')))
            elemento_dentro_do_iframe.click()
            iframe.send_keys(mae)

            logging.info(f"Preencheu Nome da Mae '{mae}' com sucesso")
            self.navegador.switch_to.default_content()
        except Exception as e:
            logging.error(f"ERRO AO PREENCHER NOME DA'{mae}': {str(e)}")
            time.sleep(3)

            self.navegador.refresh()
            time.sleep(3)
            self.navegador.switch_to.defaut_content()
            #-----------------------------------------------------------------------------------------------
        try:
             # Verifica se o mae é válido (não nulo e não NaN)
            if not sexo or str(sexo).lower() == 'nan':
                logging.error(f"ERRO: SEXO NAO ENCONTRADO NA PLANILHA. mae: {mae}")
                time.sleep(3)
                self.navegador.refresh()

                return
            #Encontra o elemento dentro do iframe
            iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
            #Muda para o iframe
            self.navegador.switch_to.frame(iframe)

            #Clica direto no elemento e preenche puxando da planilha
            elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sexo:sexo:inputId_label"]')))
            elemento_dentro_do_iframe.click()

            #Após preencher o sexo ele clicar na tecla ENTER
            iframe.send_keys(sexo)
            iframe.send_keys(Keys.ENTER)
            logging.info(f"Preencheu Sexo '{sexo}' com sucesso")
            
            self.navegador.switch_to.default_content()

        except Exception as e:
            logging.error(f"ERRO AO PREENCHER SEXO'{sexo}': {str(e)}")
            time.sleep(3)
            self.navegador.refresh()
            self.navegador.switch_to.default_content()
        #Após interagir com o iframe, você pode voltar ao contexto padrão
        #--------------------------------------------------------------------------------------------------------------------------
        try:
             # Verifica se o mae é válido (não nulo e não NaN)
            if not data_de_nacimento or str(data_de_nacimento).lower() == 'nan':
                logging.error(f"ERRO: DATA DE NASCIMENTO NAO ENCONTRADA NA PLANILHA. data_de_nacimento: {data_de_nacimento}")
                time.sleep(3)
                self.navegador.refresh()
                
                # Faz o refresh se o nome não é válido
                return

            #Encontra o elemento dentro do iframe
            iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
            
            #Muda para o iframe
            self.navegador.switch_to.frame(iframe)

            #Encontra o elemento dentro do Iframe e preenche a Data de Nacimento
            elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dataNascimento:dataNascimento:inputId_input"]')))
            elemento_dentro_do_iframe.click()
            elemento_dentro_do_iframe.send_keys(str(data_de_nacimento))
            logging.info(f"Preencheu data de nascimento '{data_de_nacimento}' com sucesso")

            self.navegador.switch_to.default_content()

        except Exception as e:
            logging.error(f"ERRO AO PREENCHER '{data_de_nacimento}': {str(e)}")
            time.sleep(3)

            self.navegador.refresh()
            time.sleep(3)
            self.navegador.switch_to.defaut_content()

        #--------------------------------------------------------------------------------------------------------------------------
        
        try:
             # Verifica se o mae é válido (não nulo e não NaN)
            if not nacionalidade or str(nacionalidade).lower() == 'nan':
                logging.error(f"ERRO: NACIONALIDADE NAO ENCONTRADO NA PLANILHA. nacionalidade: {nacionalidade}")
                time.sleep(3)
                self.navegador.refresh()
                
                # Faz o refresh se o nome não é válido
                return
            
            # Localiza o iframe
            iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
            
            # Muda para o iframe
            self.navegador.switch_to.frame(iframe)
            time.sleep(1)
            
            # Clica no elemento e preenche o valor 10, Código BRASILEIRO
            elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="suggestionNacionalidade:suggestionNacionalidade:suggestion_input"]')))
            elemento_dentro_do_iframe.click()
            time.sleep(1)
            # Preenche o valor TEXTO
            elemento_dentro_do_iframe.send_keys(str(nacionalidade))
            time.sleep(1)
            
            elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[18]/table/tbody/tr/td[1]')))
            elemento_dentro_do_iframe.click()
            
            logging.info(f"Preencheu nacionalidade '{nacionalidade}' com sucesso")

            self.navegador.switch_to.default_content()


            # Após interagir com o iframe, volta ao contexto padrão
        except Exception as e:
            logging.error(f"ERRO AO PREENCHER '{nacionalidade}': {str(e)}")
            time.sleep(3)

            self.navegador.refresh()
            time.sleep(3)
            self.navegador.switch_to.defaut_content()

        #--------------------------------------------------------------------------------------------------------------------------
        try:
             # Verifica se o mae é válido (não nulo e não NaN)
            if not naturalidade or str(naturalidade).lower() == 'nan':
                logging.error(f"ERRO: NATURALIDADE NAO ENCONTRADO NA PLANILHA. naturalidade: {naturalidade}")
                time.sleep(3)
                self.navegador.refresh()
                
                return
            #Encontra o iframe da naturalidade
        
            iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
            #Muda para o iframe
            self.navegador.switch_to.frame(iframe)
            time.sleep(1)
            #Usando WebdriverWait espera 10 seg para o elemento aparecer
            elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="naturalidade:naturalidade:suggestion_input"]')))
            elemento_dentro_do_iframe.click()
            
            #Preenche a Naturalidade puxando da planilha
            elemento_dentro_do_iframe.send_keys(str(naturalidade))

            time.sleep(1)
            elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[57]/table/tbody/tr/td[2]')))
            elemento_dentro_do_iframe.click()

            logging.info(f"Preencheu naturalidade '{naturalidade}' com sucesso")
            self.navegador.switch_to.default_content()

        except Exception as e:
            logging.error(f"ERRO AO PREENCHER '{naturalidade}': {str(e)}")
            time.sleep(3)

            self.navegador.refresh()
            time.sleep(3)
            self.navegador.switch_to.defaut_content()
       
        #--------------------------------------------------------------------------------------------------------------------------
        
        #Espera o elemento do iframe carregar
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))

        #Muda para o iframe
        self.navegador.switch_to.frame(iframe)

        #Clicar no elemento, e preencher a Graduação Ensino Superior      
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="grauInstrucao:grauInstrucao:inputId_label"]')))
        elemento_dentro_do_iframe.click()
        time.sleep(1)
        elemento_li = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[18]/div/ul/li[13]")))
        elemento_li.click()
        logging.info('Preencheu Grau de Instrucao com sucesso')

        #Após interagir com o iframe, você pode voltar ao contexto padrão
        self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------
        try:
             # Verifica se o mae é válido (não nulo e não NaN)
            if not email or str(email).lower() == 'nan':
                logging.error(f"ERRO: EMAIL NAO ENCONTRADO NA PLANILHA. email: {email}")
                time.sleep(3)
                self.navegador.refresh()
                
                # Faz o refresh se o nome não é válido
                return
            #Espera o elemento do iframe carregar
            iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))

            # Muda para o iframe
            self.navegador.switch_to.frame(iframe)

            #Clicar no elemento, e preencher o Email do colaborador puxando da planilha
            elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="email:email:inputId"]')))
            elemento_dentro_do_iframe.click()
            elemento_dentro_do_iframe.send_keys(str(email))
            logging.info(f"Preencheu Email '{email}' com sucesso")
            self.navegador.switch_to.default_content()
            # Após interagir com o iframe, você pode voltar ao contexto padrão
        except Exception as e:
            logging.error(f"ERRO AO PREENCHER '{email}': {str(e)}")
            time.sleep(3)

            self.navegador.refresh()
            time.sleep(3)
            self.navegador.switch_to.defaut_content()

        #--------------------------------------------------------------------------------------------------------------------------
        try:
             # Verifica se o mae é válido (não nulo e não NaN)
            if not rg or str(rg).lower() == 'nan':
                logging.error(f"ERRO: NOME DA MAE NAO ENCONTRADO NA PLANILHA. rg: {rg}")
                time.sleep(3)
                self.navegador.refresh()
                
                # Faz o refresh se o nome não é válido
                return
            #Espera o elemento do iframe carregar
            iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))

            #Muda para o iframe
            self.navegador.switch_to.frame(iframe)

            #Clicar no elemento e preencher o RG do Colaborador
            elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="rg:rg:inputId"]')))
            elemento_dentro_do_iframe.click()
            iframe.send_keys(rg)
            logging.info(f"Preencheu RG '{rg}' com sucesso")
            self.navegador.switch_to.default_content()

        #Após interagir com o iframe, você pode voltar ao contexto padrão
        except Exception as e:
            logging.error(f"ERRO AO PREENCHER '{rg}': {str(e)}")
            time.sleep(3)

            self.navegador.refresh()
            time.sleep(3)
            self.navegador.switch_to.defaut_content()

        #--------------------------------------------------------------------------------------------------------------------------
        try:
             # Verifica se o mae é válido (não nulo e não NaN)
            if not orgao_emissor or str(orgao_emissor).lower() == 'nan':
                logging.error(f"ERRO: NOME DA MAE NAO ENCONTRADO NA PLANILHA. orgao_emissor: {orgao_emissor}")
                time.sleep(3)
                self.navegador.refresh()
                
                # Faz o refresh se o nome não é válido
                return

            #Espera o elemento do iframe carregar
            iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]'))) 
            
            #Muda para o iframe
            self.navegador.switch_to.frame(iframe)

            #Clicar no elemento dentro do Iframe, e preencher o Orgão Emissor do colaborador
            elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="orgao:orgao:suggestion_input"]')))
            elemento_dentro_do_iframe.click()
            iframe.send_keys(orgao_emissor)

            #Aparecendo o preenchimento ele clicar no valor retornado
            elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[59]/table/tbody/tr/td')))
            elemento_dentro_do_iframe.click()
            
            logging.info(f"Preencheu Orgao emissor '{orgao_emissor}' com sucesso")
            self.navegador.switch_to.default_content()
            
            #Após interagir com o iframe, você pode voltar ao contexto padrão
            self.navegador.switch_to.default_content()
        except Exception as e:
            logging.error(f"ERRO AO PREENCHER '{orgao_emissor}': {str(e)}")
            time.sleep(3)

            self.navegador.refresh()
            time.sleep(3)
            self.navegador.switch_to.defaut_content()
    
        try:
             # Verifica se o mae é válido (não nulo e não NaN)
            if not uf or str(uf).lower() == 'nan':
                logging.error(f"ERRO: UF NAO ENCONTRADO NA PLANILHA. uf: {uf}")
                time.sleep(3)
                self.navegador.refresh()
                
                # Faz o refresh se o nome não é válido
                return
        #--------------------------------------------------------------------------------------------------------------------------

            #Espera o elemento do iframe carregar
            iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
            time.sleep(1)
            # Muda para o iframe
            self.navegador.switch_to.frame(iframe)
            
            #Clicar no elemento, e preencher o UF do Colaborador puxando da planilha
            elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ufRgPessoa:ufRgPessoa:suggestion_input"]')))
            elemento_dentro_do_iframe.click()
            iframe.send_keys(uf)
            #Elemento <li>
            elemento_li = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "tr.ui-autocomplete-item:nth-child(1) > td:nth-child(1)")))
            #Clica no elemento <li>
            elemento_li.click()
            logging.info(f"Preencheu UF '{uf}' com sucesso")
            
            self.navegador.switch_to.default_content()
            

            #Após interagir com o iframe, você pode voltar ao contexto padrão
            self.navegador.switch_to.default_content()
        except Exception as e:
            logging.error(f"ERRO AO PREENCHER '{uf}': {str(e)}")
            time.sleep(3)

            self.navegador.refresh()
            time.sleep(3)
            self.navegador.switch_to.defaut_content()
    
        #--------------------------------------------------------------------------------------------------------------------------
        try:
             # Verifica se o mae é válido (não nulo e não NaN)
            if not cpf or str(cpf).lower() == 'nan':
                logging.error(f"ERRO: CPF NAO ENCONTRADO NA PLANILHA. cpf: {cpf}")
                time.sleep(3)
                self.navegador.refresh()
                
                # Faz o refresh se o nome não é válido
                return

            #Espera o elemento do iframe carregar
            iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
            
            #Muda para o iframe
            self.navegador.switch_to.frame(iframe)
            
            #Clica no elemento, e preenche o CPF do colaborador
            elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cpf:cpf:inputId"]')))
            elemento_dentro_do_iframe.click()    
            elemento_dentro_do_iframe.send_keys(str(cpf))             
            elemento_dentro_do_iframe.click()
            logging.info(f"Preencheu CPF '{cpf}' com sucesso")
            self.navegador.switch_to.default_content()

        except Exception as e:
            logging.error(f"ERRO AO PREENCHER '{cpf}': {str(e)}")
            time.sleep(3)

            self.navegador.refresh()
            time.sleep(3)
            self.navegador.switch_to.defaut_content()

        #--------------------------------------------------------------------------------------------------------------------------
        
        #Espera o elemento do iframe carregar
        
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
    
        #Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        
        #Clica no Botão de Grava
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/form[3]/div[3]/button[1]/span[1]')))
        elemento_dentro_do_iframe.click()
        
        try:
            time.sleep(4)
            try:
                elemento = self.navegador.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/div/div/ul/li/span')
                elemento = elemento.text
                print(f'Texto do elemento {elemento}')
                if 'já cadastrado' in elemento:
                    self.navegador.refresh()
                    time.sleep(3)
                    return 'Pessoa incluída com sucesso'
            except:
                pass     
        except:
            print("Caixa de cliente não cadastrado não apareceu")
            pass

        #Após interagir com o iframe, você pode voltar ao contexto padrão
        self.navegador.switch_to.default_content()

        #Espera o elemento do iframe carregar
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))

        #Muda para o iframe
        self.navegador.switch_to.frame(iframe)

        #Vai aparece um POP informando que o cadastro foi realizado, ele clica no Fecha do POP
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[4]/div[1]/a[1]/span')))
        elemento_dentro_do_iframe.click()
        
        #Após interagir com o iframe, você pode voltar ao contexto padrão
        self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------

        #Espera o elemento do iframe carregar
        
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
        #Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        #Clica no elemento de busca, e preenche o CPF do colaborador
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cpf:cpf:inputId"]')))
        elemento_dentro_do_iframe.click()
        elemento_dentro_do_iframe.send_keys(str(cpf))
        elemento_dentro_do_iframe.click()
        #Após interagir com o iframe, você pode voltar ao contexto padrão
        self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------
        
        #Espera o elemento do iframe carregar
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
        #Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        #Clica no Botão de Pesquisar
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/form[3]/div/button[1]/span[2]')))
        elemento_dentro_do_iframe.click()
        #Após interagir com o iframe, você pode voltar ao contexto padrão
        self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------
        time.sleep(1)
        #Espera o elemento do iframe carregar
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
        #Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        time.sleep(1)
        #Passando esse um Seg ele Clica no Icone do Servidor                                                       
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tabelaPessoaFisica\:resultList\:0\:j_idt109\:link")))
        elemento_dentro_do_iframe.click()
        
        #Após interagir com o iframe, você pode voltar ao contexto padrão
        self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------
        time.sleep(1)
        #Espera o elemento do iframe carregar
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))

        #Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        
        #Clica no Botão de Novo
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/form[3]/div/span[1]/button/span[2]')))
        elemento_dentro_do_iframe.click()
        
        #Após interagir com o iframe, você pode voltar ao contexto padrão
        self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------

        #Espera o elemento do iframe carregar
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
        #Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        
        #Clicar no elemento, e Preenche o Vinculo
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="suggestionVinculo:suggestionVinculo:suggestion_input"]')))
        elemento_dentro_do_iframe.click()
        elemento_dentro_do_iframe.send_keys(str(vinculo))
        elemento_dentro_do_iframe.click

        #Após interagir com o iframe, você pode voltar ao contexto padrão
        self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------

        #Espera o elemento do iframe carregar
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))

        #Muda para o iframe
        self.navegador.switch_to.frame(iframe)

        #Preenchendo o Vinculo, ele aparece a opção e aqui clicamos dentro dela
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[8]/table/tbody/tr/td[2]')))
        elemento_dentro_do_iframe.click()
        
        #Após interagir com o iframe, você pode voltar ao contexto padrão
        self.navegador.switch_to.default_content() 
        #--------------------------------------------------------------------------------------------------------------------------

        #Espera o elemento do iframe carregar
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
        #Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        
        #Clicando dentro do ele preenche o dado de matricula do colaborador
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="matricula:matricula:inputId_input"]')))
        elemento_dentro_do_iframe.click()
        elemento_dentro_do_iframe.send_keys(str(matricula))
        elemento_dentro_do_iframe.click()

        #Após interagir com o iframe, você pode voltar ao contexto padrão
        self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------

        #Espera o elemento do iframe carregar
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
        #Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        
        #Clicar no elemento dentro do iframe e preencher o inicio do vinculo do colaborador
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dataInicioVinculo:dataInicioVinculo:inputId_input"]')))
        elemento_dentro_do_iframe.click()
        elemento_dentro_do_iframe.send_keys(str(inicio_do_vinculo))
        elemento_dentro_do_iframe.click()

        #Após interagir com o iframe, você pode voltar ao contexto padrão
        self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------

        #Espera o elemento do iframe carregar
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))

        #Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        
        #Clicando dentro do elemento, e preenchendo o codigo ("1") Centro de Custo 1
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="suggestionCCLotacao:suggestionCCLotacao:suggestion_input"]')))
        elemento_dentro_do_iframe.click()
        iframe.send_keys("1")
        time.sleep(1)
        #Após preencher o codigo, clicar dentro do valor retonado
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[14]/table/tbody/tr/td[2]')))
        # Após interagir com o iframe, você pode voltar ao contexto padrão
        elemento_dentro_do_iframe.click()
        
        #Após interagir com o iframe, você pode voltar ao contexto padrão
        self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------

        #Espera o elemento do iframe carregar
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))

        #Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        
        #Clicar dentro do elemento e coloca o codigo 1, Assim que ele preenche Centro Custo 1
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="suggestionCCAtuacao:suggestionCCAtuacao:suggestion_input"]')))
        elemento_dentro_do_iframe.click()
        iframe.send_keys("1")
        time.sleep(1)

        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[14]/table/tbody/tr/td[2]')))
        #Após interagir com o iframe, você pode voltar ao contexto padrão
        elemento_dentro_do_iframe.click()
        #Após interagir com o iframe, você pode voltar ao contexto padrão
        self.navegador.switch_to.default_content()

        #--------------------------------------------------------------------------------------------------------------------------

        #Esperado o elemento do iframe carregar
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
        #Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        #Clicar no valor retornado Centro Custo 1
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/form[3]/div/button[1]/span[2]')))
        elemento_dentro_do_iframe.click()
        self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------

        #Esperado o elemento do iframe carregar
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
        #Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        #clicar em grava a informação
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/form[3]/div/button[3]/span[2]')))
        elemento_dentro_do_iframe.click()
        #Após interagir com o iframe, você pode voltar ao contexto padrão
        self.navegador.switch_to.default_content() 
        #--------------------------------------------------------------------------------------------------------------------------

        #Clicar dentro do elemento e preencher o codigo 2, e clica dentro do valor retornado 
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="linkModalTipoInformacoes:linkModalTipoInformacoes:suggestion_input"]')))
        elemento_dentro_do_iframe.click()
        iframe.send_keys("2")
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/table/tbody/tr/td[2]')))
        # Após interagir com o iframe, você pode voltar ao contexto padrão
        elemento_dentro_do_iframe.click()

        self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------
        #Espera o frame carregar 
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        time.sleep(1)
        #clicar dentro do elemento Cbo, esperar um seg
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cbo:cbo:suggestion_input"]')))
        elemento_dentro_do_iframe.click()
        elemento_dentro_do_iframe.send_keys(str(cbo))
        elemento_dentro_do_iframe.click()

        self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------
        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        time.sleep(1)

        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[14]/table/tbody/tr/td[1]')))
        elemento_dentro_do_iframe.click()

        self.navegador.switch_to.default_content() 
        #--------------------------------------------------------------------------------------------------------------------------
        
        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)

        time.sleep(1)

        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dtInicio:dtInicio:inputId_input"]')))
        elemento_dentro_do_iframe.click()
        elemento_dentro_do_iframe.send_keys(str(inicio_do_vinculo))
        elemento_dentro_do_iframe.click()

        self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------
        
        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))

        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)

        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/form[3]/div/button[1]/span[2]')))
        elemento_dentro_do_iframe.click()

        self.navegador.switch_to.default_content() 
        #--------------------------------------------------------------------------------------------------------------------------

        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))

        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/form[3]/div/button[3]/span[2]')))
        elemento_dentro_do_iframe.click()

        self.navegador.switch_to.default_content() 
        #--------------------------------------------------------------------------------------------------------------------------

        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))

        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="linkModalTipoInformacoes:linkModalTipoInformacoes:suggestion_input"]')))
        elemento_dentro_do_iframe.click()
        iframe.send_keys("7")
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/table/tbody/tr/td[1]')))
        # Após interagir com o iframe, você pode voltar ao contexto padrão
        elemento_dentro_do_iframe.click()

        self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------
    
        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dtInicio:dtInicio:inputId_input"]')))
        elemento_dentro_do_iframe.click()

        elemento_dentro_do_iframe.send_keys(str(inicio_do_vinculo))
        elemento_dentro_do_iframe.click() 

        self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------
        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        time.sleep(1)
                
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="campoValorId:campoValorId:textArea"]')))
        elemento_dentro_do_iframe.click()
        elemento_dentro_do_iframe.send_keys(str(cns))
        elemento_dentro_do_iframe.click()
        self.navegador.switch_to.default_content()
       
        #--------------------------------------------------------------------------------------------------------------------------
        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))

        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)

        try:
            elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="salvar:button"]')))
            self.scroll_to_element(elemento_dentro_do_iframe)
            time.sleep(0.5)
            elemento_dentro_do_iframe.click()
        except:
            pass

        self.navegador.switch_to.default_content() 
       
        #--------------------------------------------------------------------------------------------------------------------------
    # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
        
        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
                                                                                                                
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/form[3]/div/button[4]/span[1]')))
        
        elemento_dentro_do_iframe.click()
        self.navegador.switch_to.default_content() 

        #--------------------------------------------------------------------------------------------------------------------------
        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))

        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
                                                                                                                
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tabelaServidor\:resultList\:0\:j_idt307\:link")))
        
        elemento_dentro_do_iframe.click()

        self.navegador.switch_to.default_content()                                                                    
        #--------------------------------------------------------------------------------------------------------------------------
        
        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))

        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)

        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/form[3]/div/button[3]/span[2]')))
        elemento_dentro_do_iframe.click()

        self.navegador.switch_to.default_content() 
        #--------------------------------------------------------------------------------------------------------------------------

        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)

        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="curso:curso:suggestion_input"]')))
        elemento_dentro_do_iframe.click()

        elemento_dentro_do_iframe.send_keys(str(curso))
        elemento_dentro_do_iframe.click()

        self.navegador.switch_to.default_content()

        #--------------------------------------------------------------------------------------------------------------------------

        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))

        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/table/tbody/tr/td[2]')))
        elemento_dentro_do_iframe.click()

        self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------
    
        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))

        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="situacao:situacao:inputId_label"]')))
        elemento_dentro_do_iframe.click()

        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/ul/li[3]')))
        # Após interagir com o iframe, você pode voltar ao contexto padrão
        elemento_dentro_do_iframe.click()

        self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------

        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dtInicio:dtInicio:inputId_input"]')))
        elemento_dentro_do_iframe.click()

        elemento_dentro_do_iframe.send_keys(str(ano_inicio))
        elemento_dentro_do_iframe.click()

        self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------

        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dtFim:dtFim:inputId_input"]')))
        elemento_dentro_do_iframe.click()

        elemento_dentro_do_iframe.send_keys(str(ano_fim))
        elemento_dentro_do_iframe.click()

        self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------

        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))
        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#nroRegConselho\:nroRegConselho\:inputId")))
        elemento_dentro_do_iframe.click()
        time.sleep(1)
        elemento_dentro_do_iframe.send_keys(str(conselho))
        elemento_dentro_do_iframe.click()
        self.navegador.switch_to.default_content()

        #--------------------------------------------------------------------------------------------------------------------------

        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))

        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/form[3]/fieldset/div/div[4]/div/div[2]/div[1]/span/button/span[1]')))
        elemento_dentro_do_iframe.click()
        time.sleep(2)
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[12]/table/tbody/tr/td[2]')))
        # Após interagir com o iframe, você pode voltar ao contexto padrão
        elemento_dentro_do_iframe.click()

        self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------
        
        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))

        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        time.sleep(1)
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/form[3]/div/button[1]/span[2]')))
        elemento_dentro_do_iframe.click()
        #----------------------
        self.navegador.switch_to.default_content() 
        #--------------------------------------------------------------------------------------------------------------------------

        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_pessoas"]')))

        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/form[3]/div/button[4]/span[2]')))
        elemento_dentro_do_iframe.click()

        self.navegador.switch_to.default_content() 
        #--------------------------------------------------------------------------------------------------------------------------

        self.navegador.find_element('xpath', '/html/body/header/div[2]/ul/li[14]/ul/li[3]/a').click()
        self.navegador.find_element('xpath', '/html/body/header/div[2]/ul/li[14]/ul/li[5]/a').click()
        self.navegador.find_element('xpath', '/html/body/header/div[2]/ul/li[14]/ul/li[5]/ul/li[3]/a/span').click()
        self.navegador.find_element('xpath', '/html/body/header/div[2]/ul/li[14]/ul/li[5]/ul/li[3]/ul/li[1]/a/span').click()
        self.navegador.switch_to.default_content()
        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_usuario"]')))

        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/form[3]/div[1]/button[1]/span[2]')))
        elemento_dentro_do_iframe.click()

        self.navegador.switch_to.default_content() 
        #--------------------------------------------------------------------------------------------------------------------------

        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_usuario"]')))
        
        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        time.sleep(1)
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/form[3]/div[1]/span/button/span[2]')))
        elemento_dentro_do_iframe.click()

        self.navegador.switch_to.default_content() 
        #--------------------------------------------------------------------------------------------------------------------------
    
        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_usuario"]')))
        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pessoaFisicaNome:pessoaFisicaNome:suggestion_input"]')))
        elemento_dentro_do_iframe.click()
        
        elemento_dentro_do_iframe.send_keys(str(cpf))
        time.sleep(1)
        elemento_dentro_do_iframe.click()

        self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------

        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_usuario"]')))
    
        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        time.sleep(1)
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/table/tbody/tr/td[2]')))
        elemento_dentro_do_iframe.click()

        self.navegador.switch_to.default_content() 
        #--------------------------------------------------------------------------------------------------------------------------

        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_usuario"]')))

        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/form[3]/div/button[1]/span[2]')))
        elemento_dentro_do_iframe.click()

        self.navegador.switch_to.default_content() 
        #--------------------------------------------------------------------------------------------------------------------------

        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_usuario"]')))
        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="nomeOuLogin:nomeOuLogin:inputId"]')))
        elemento_dentro_do_iframe.click()
        time.sleep(1)
        elemento_dentro_do_iframe.send_keys(str(cpf))

        self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------

        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_usuario"]')))

        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        time.sleep(1)
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/form[3]/div[1]/button[1]/span[2]')))
        elemento_dentro_do_iframe.click()

        self.navegador.switch_to.default_content() 
        #--------------------------------------------------------------------------------------------------------------------------
        
        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_usuario"]')))
        time.sleep(1)
        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)                                                               
        
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#tabelaUsuarios\:resultList\:0\:j_idt80\:link")))
        elemento_dentro_do_iframe.click()

        self.navegador.switch_to.default_content() 
        #--------------------------------------------------------------------------------------------------------------------------

        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_usuario"]')))
        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        time.sleep(1)
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="selecionaPerfil:selecionaPerfil:suggestion_input"]')))
        elemento_dentro_do_iframe.click()
        time.sleep(1)                                                                                            
        elemento_dentro_do_iframe.send_keys(str(perfil))
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="selecionaPerfil:selecionaPerfil:suggestion_panel"]/table/tbody/tr/td')))
        
        cont = 0
        while True:
            cont += 1
            if cont == 60:
                print(f'Não foi possível cadastrar a pessoa: {lista[0]}')
                input('\nDigite qualquer coisa para fechar o programa:')
                exit()
            try:
                elemento_dentro_do_iframe.click()
            except Exception as e:
                time.sleep(1)
                pass
            else:
                break

        self.navegador.switch_to.default_content()
        #--------------------------------------------------------------------------------------------------------------------------

        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_usuario"]')))

        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/form[3]/fieldset[2]/div/div[1]/div[2]/button/span[2]')))
        elemento_dentro_do_iframe.click()

        self.navegador.switch_to.default_content() 
        #--------------------------------------------------------------------------------------------------------------------------

        # Espera pelo seletor do iframe
        iframe = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i_frame_usuario"]')))
        
        # Muda para o iframe
        self.navegador.switch_to.frame(iframe)
        
        elemento_dentro_do_iframe = WebDriverWait(self.navegador, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/form[3]/div[1]/button[1]/span[2]')))
        elemento_dentro_do_iframe.click()
        
        self.navegador.switch_to.default_content()

        try:
            self.navegador.find_element('xpath', '//*[@id="usuario:usuario:inputId"]').send_keys(self.email)
            logging.info('Login Preenchido com sucesso')
            self.navegador.find_element('xpath', '//*[@id="password:inputId"]').send_keys(self.senha)
            time.sleep (1)
            logging.info('Senha Preenchido com sucesso')
            self.navegador.find_element('xpath', '/html/body/div[1]/div/div/div/div/form/fieldset/div[4]/button/span').click()
            logging.info('Clicou no Botao Entrar com Sucesso')
        except Exception as e:
            pass

    def executa_cadastro(self):
        cont = 0
        for i in range(len(tabela_values_list)):
            try:
                dados = tabela_values_list[i]
                cont += 1
                print(f'cadastrando a pessoa: {tabela_values_list[i][0]}')
                print (tabela_values_list[i])
                content = self.cadastra_sistema(tabela_values_list[i])
            except Exception as e:
                msg = f'Erro ao cadastrar a pessoa da linha {i+1} cujos dados são: {tabela_values_list[i]}. Erro: {e}'
                print(msg)
                pass