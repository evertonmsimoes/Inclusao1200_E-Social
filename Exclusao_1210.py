from browser import navegador
from arquivos_de_dados import arquivos_de_dados
from janela import JanelaInterativa
from reconhecimentoDeImagem import reconhecerImagem
from extracao_dados import extracao
import pandas as pd
from time import sleep
import pyautogui
import threading

compet = None


# Ações do Navegador
def preencher_campo(selector, value):
    navegador_instancia.escreverElemento(selector, value)
    sleep(0.5)


def clicar_elemento(selector):
    navegador_instancia.clicarElemento(selector, Browser)


def thread_selecao_certificado():
    clicar_elemento('/html/body/div[1]/main/form/div/div[5]/button')


# Chamar e destruir Janela
def solicitarInfamcoesJanela(titulo, texto):
    janela_interacao_user = JanelaInterativa()
    # janela_interacao_user.__init__()
    informacoes = janela_interacao_user.solicitar_entrada(titulo, texto)
    janela_interacao_user.destuirJanela()
    return informacoes


# Função de Login
def realizar_login(navegador):
    # Seleciona a caixa entrar
    clicar_elemento('/html/body/div[2]/div[3]/form/fieldset/div[1]/div[2]/p/button')

    # Inicie a thread para selecionar o certificado em segundo plano
    thread = threading.Thread(target=thread_selecao_certificado)
    thread.start()
    sleep(6)
    # Clica no Botação Ok
    pyautogui.hotkey('enter')


def incluirInformacoes():
    return None


# Solicitar informações para o usuario.
def recolherInformações():
    global compet
    # Solicitar Ano da Competencia para o Usuario
    compet = solicitarInfamcoesJanela('Competência', 'Digite a competência (Ano e Mês): ')

def excluirArquivo(Browser):
    sleep(3)
    try:
        clicar_elemento('/html/body/div[3]/div[5]/div/div[2]/div[3]/table/tbody/tr/td[3]/div/button')
        clicar_elemento('/html/body/div[3]/div[5]/div/div[2]/div[3]/table/tbody/tr/td[3]/div/ul/li[4]/a')
        clicar_elemento('/html/body/div[13]/div[2]/div/button[2]')
        sleep(4)
        assinar(Browser)
        sleep(6)
        resposta = instancia_extracao.extrcaoWeb(Browser.page_source,{'class': 'fade-alert alert alert-success retornoServidor'})
        return resposta
    except:
        resposta = "Erro desconhecido"
        return resposta


def assinar(Browser):
    #execute_script("arguments[0].scrollIntoView(true);")
    sleep(0.5)
    Browser.execute_script("""
        // Encontre o botão pelo atributo "name"
        const botaoSalvar = document.querySelector('input[name="salvar:evento"]');

        // Verifique se o botão foi encontrado
        if (botaoSalvar) {
            // Simule um clique no botão
            botaoSalvar.click();
        } else {
            console.log("Botão 'Salvar' não encontrado.");
        }
    """)
    instancia_imagem.encontrar_e_clicar_no_centro(r'C:\Users\ccba\Pictures\Imagens\AbrirAssinador.png')
    instancia_imagem.encontrar_e_clicar_no_centro(r'C:\Users\ccba\Pictures\Imagens\ExecultarJava.png')
    pyautogui.hotkey('enter')
    instancia_imagem.encontrar_e_clicar_no_centro(r'C:\Users\ccba\Pictures\Imagens\Assinar.png')
    instancia_imagem.encontrar_e_clicar_no_centro(r'C:\Users\ccba\Pictures\Imagens\ok.png')





if __name__ == "__main__":

    # Instancia as Classes do Navegador, Janela, e Arquivos
    navegador_instancia = navegador()
    instancia_dados = arquivos_de_dados()
    instancia_imagem = reconhecerImagem()
    instancia_extracao = extracao()

    recolherInformações()
    df = pd.DataFrame()
    df = instancia_dados.lendo_base_de_dados()
    # Começo da Interação com o Navegador
    Browser = navegador_instancia.criarNavegador(True, False)
    navegador_instancia.denirTempo_Elemt(Browser)
    Browser.get('https://login.esocial.gov.br/login.aspx')
    realizar_login(Browser)

    num = 0
    testeInclusao = 1

    for index, row in df.iterrows():
        sleep(300)
        link = f"https://www.esocial.gov.br/portal/FolhaPagamento/ListaRemuneracao?competencia={compet}&tipo=1210&PossuiDae=False&pagina=e1-o0&ehBeneficiario=false&cpf={row['CPF-RPA']}"
        Browser.get(link)
        resposta = excluirArquivo(Browser)
        instancia_dados.GravLog(row['CPF-RPA'], resposta)
        sleep(0.8)
# Link Correto : https://www.esocial.gov.br/portal/FolhaPagamento/PagamentoCompleto?cpf=22532964812&competencia=202101&tipo=1210&visualizar=true

