from browser import navegador
from arquivos_de_dados import arquivos_de_dados
from janela import JanelaInterativa
from reconhecimentoDeImagem import reconhecerImagem
from extracao_dados import extracao
from time import sleep
import pyautogui
import threading

senha = None
compet = None

# Ações do Navegador

# Preencher informação em um Campo OBS: Definido pelo XPATH
def preencher_campo(selector, value):
    navegador_instancia.escreverElemento(selector, value)
    sleep(0.5)

# Clicar no Elemento pelo ID do CSS
def clicar_elemento_ID(id):
    navegador_instancia.clicarElementoID(id, Browser)



# Função para clicar em um elemento do navegador
def clicar_elemento(selector):
    navegador_instancia.clicarElemento(selector, Browser)

# Thread para Selecionar o 1 certificado
def thread_selecao_certificado():
    clicar_elemento('/html/body/div[1]/main/form/div/div[5]/button')

# Chamar e destruir Janela
def solicitarInfamcoesJanela(titulo, texto):
    janela_interacao_user = JanelaInterativa()
    informacoes = janela_interacao_user.solicitar_entrada(titulo, texto)
    janela_interacao_user.destuirJanela()
    return informacoes

# Função para encontrar e clicar no centro da Imagem
def encontrarClicarImg(caminho):
    instancia_imagem.encontrar_e_clicar_no_centro(caminho)

#Função de Login
def realizar_login(navegador):
    global senha, cnpj
 
    # Seleciona a caixa entrar
    clicar_elemento('/html/body/div[2]/div[3]/form/fieldset/div[1]/div[2]/p/button')

    # Inicie a thread para selecionar o certificado em segundo plano
    thread = threading.Thread(target=thread_selecao_certificado)
    thread.start()
    sleep(6)
    # Clica no Botação Ok para Abrir a tela de Assinatura do Certificadi
    pyautogui.hotkey('enter')
    encontrarClicarImg(r'imagens\caixaLoginGov.png')
    sleep(0.5)
    pyautogui.typewrite(senha)
    sleep(0.7)
    pyautogui.hotkey('enter')
    

# Função para Realizar Relogin no sistema do E-Social.        
def  realizar_relogin(Browser):
    navegador_instancia.encerrarNavegador(Browser)
    sleep(25)
    



def incluirInformacoes(cpf, dtPgto, ideDmDev, vrLiq, perApur, tppag):
    global compet
    if testeInclusao == 1:
        Browser.get(f'https://www.esocial.gov.br/portal/FolhaPagamento/PagamentoCompleto?cpf={cpf}&competencia={compet}&possuiDae=False&tipo=1210')
    
    navegador_instancia.esperarPaginaCarregar()
    clicar_elemento_ID("btn-incluir-pagto")
    sleep(0.6)
    
    # Usando a variável 'tppag' na string JavaScript
    script_js = f"""
function selecionarValorNoSelect(valor) {{
  var selectElement = document.querySelector('select[caminho-completo="eSocial/evtPgtos/ideBenef/infoPgto/tpPgto"]');
  
  if (selectElement) {{
    // Define o valor no select
    selectElement.value = valor;

    // Dispara o evento de mudança (change) no select
    var eventoMudanca = new Event('change', {{ bubbles: true }});
    selectElement.dispatchEvent(eventoMudanca);
  }} else {{
    console.error('Select não encontrado');
  }}
}}

// Chama a função para selecionar o valor desejado no select
selecionarValorNoSelect('{tppag}'); // Isso selecionará o valor definido na variável 'tppag'
"""

# Executando o script no navegador usando Browser.execute_script()
    Browser.execute_script(script_js)
    sleep(0.5)
    # Preencher Data De Pagamento
    preencher_campo("/html/body/div[3]/div[5]/div/form/div[2]/div[1]/div[2]/div[1]/div[2]/span/input", dtPgto)
    sleep(0.5)
    # Preencher a que competencia se refere  o Pagamento
    preencher_campo("/html/body/div[3]/div[5]/div/form/div[2]/div[1]/div[2]/div[1]/div[3]/span/input",perApur)
    sleep(0.5)
    # Identificador do Demostrativo
    preencher_campo("/html/body/div[3]/div[5]/div/form/div[2]/div[1]/div[2]/div[2]/div[1]/span/input", ideDmDev)
    sleep(0.5)
    # Preencher campo do Valor
    preencher_campo("/html/body/div[3]/div[5]/div/form/div[2]/div[1]/div[2]/div[2]/div[2]/span/input", vrLiq)
    sleep(0.5)
    # Clicar em Incluir
    Browser.execute_script("""
// Obtém uma referência ao botão pelo id
var botao = document.getElementById('incluir-informacao-pagamento');
// Verifica se o botão foi encontrado
if (botao) {
  // Aciona o botão (clique programaticamente)
  botao.click();
} else {
  console.log('Botão não encontrado');
}
""")
    sleep(2.4)

    

# Solicitar Informações sobre 
def recolherInformações():
    global compet, senha, cnpj
    #Solicitar informações para o usuario.
    compet = solicitarInfamcoesJanela('Competência', 'Digite a competência (Ano e Mês): ')
    #Solicita a Senha
    senha = solicitarInfamcoesJanela('Senha do Certificado', 'Digite a senha do Certificado: ')


# Chama função para Assinar Inclusao
def assinarInclusao():
    Browser.execute_script("""document.querySelector('input[name="salvar:evento"]').click();""")
    assinarJava()
    navegador_instancia.esperarPaginaCarregar()
    resposta = instancia_extracao.extrcaoWebListaDeElementos(Browser.page_source, [{'class': 'fade-alert alert alert-danger'}, {'class': 'fade-alert alert alert-success retornoServidor'}, {'class': "fade-alert alert alert-warning"}, {'class': "fade-alert alert alert-success"}])
    return resposta


# Chama Função para assina o Arquivo .Java
def assinarJava():
    # Chama a função para clicar no Assinador Java
    encontrarClicarImg(r'imagens\AbrirAssinadorJava.png')
    # Chama a função para clicar dentro do arquivo Java e depois seleciona Enter no Teclado.
    encontrarClicarImg(r'imagens\ClicarEmExecutar.png')
    pyautogui.hotkey('enter')
    # Chama a função para clicar no Botão Assinar Dentro da Janela do assinador Java
    encontrarClicarImg(r'imagens\ClicarBotaoAssinar.png')
    # Chama a função para Clicar na Caixa de inserir a Senha no Assinador Java
    encontrarClicarImg(r'imagens\ClicarCaixaDeSennha.png')
    pyautogui.typewrite(senha)
    sleep(0.7)
    pyautogui.hotkey('enter')
    sleep(0.5)
    # Chama a função para Clicar no Botão Ok
    encontrarClicarImg(r'imagens\ClicarBotaoOk.png')
    sleep(0.8)

if __name__ == "__main__":

    # Instancia as Classes do Navegador, Janela, e Arquivos
    navegador_instancia = navegador()
    instancia_dados = arquivos_de_dados()
    instancia_imagem = reconhecerImagem()
    instancia_extracao = extracao()
    janela_exibir_menssagem = JanelaInterativa()


    # Chama função para Solicitar Informações que serão usandas para acessar as 
    recolherInformações()
    df = instancia_dados.lendo_base_de_dados()

    #Começo da Interação com o Navegador
    Browser = navegador_instancia.criarNavegador(True, False)
    navegador_instancia.denirTempo_Elemt(Browser)
    Browser.get('https://login.esocial.gov.br/login.aspx')
    realizar_login(Browser)

    num = 0
    testeInclusao = 1
    contVezes = 0
    contagem = 0
    cont = 0

    for index, row in df.iterrows():
        
        incluirInformacoes(row['CPF'], row['Data do Pagamento'], row['Id do demostrativo'], row['Valor'], row['Comp Ref o Pagamento'], row['Tipo de Pagamento'])
        testeInclusao += 1
        num += 1
        
        

        if (num < len(df) and row['CPF'] != df['CPF'].iloc[num]):
            resposta = assinarInclusao()
            row['html'] = str(resposta)
            row['html2'] = instancia_extracao.extrair_texto_html(row['html'])
            instancia_dados.GravLog(row['CPF'], row['html2'])
            testeInclusao = 1
            contVezes += 1


            
        if  contagem == (len(df)-1):
            resposta = assinarInclusao()
            row['html'] = str(resposta)
            row['html2'] = instancia_extracao.extrair_texto_html(row['html'])
            instancia_dados.GravLog(row['CPF'], row['html2'])
   

        
        # Relogin de 14 em 14 Execuções
        if cont == 13:
            realizar_relogin(Browser)
            #Começo da Interação com o Navegador
            Browser = navegador_instancia.criarNavegador(True, False)
            navegador_instancia.denirTempo_Elemt(Browser)
            Browser.get('https://login.esocial.gov.br/login.aspx')
            realizar_login(Browser)
            cont = 0
        else:
            cont += 1
       
        contagem += 1

    janela_exibir_menssagem.exibir_informacoes('Fim da Lista.', 'A Lista foi finalizada!')
    navegador_instancia.encerrarNavegador(Browser)  
