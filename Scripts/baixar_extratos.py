
import pyautogui
import time
import os
import datetime
import cv2
import logging
from pathlib import Path

# --- Configurações de Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automacao_sicoob.log'),
        logging.StreamHandler()
]
)
logger = logging.getLogger(__name__)

# --- Configurações Iniciais ---
pyautogui.PAUSE = 1.0 # Pausa entre cada comando
pyautogui.FAILSAFE = True # Mova o mouse para o canto superior esquerdo para interromper

# Caminhos do projeto
BASE_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGENS_BOTOES_FOLDER = os.path.join(BASE_FOLDER, 'img_automacao', 'botoes')
IMAGENS_CONTAS_FOLDER = os.path.join(IMAGENS_BOTOES_FOLDER, 'contas')
IMAGENS_DIAS_FOLDER = os.path.join(BASE_FOLDER, 'img_automacao', 'dias')
DOWNLOAD_FOLDER = os.path.join(BASE_FOLDER, 'extratos_baixados')

# Garante que as pastas existem
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Lista das contas a serem processadas
CONTAS = [
    {
    "nome_empresa": "SERTANEZINA COMERCIO DE PEDRAS",
    "nome_na_tela": "Conta 41930-3",
    "nome_arquivo": "Sicoob_41930"
    },
    {
    "nome_empresa": "F C F - COMERCIO DE MARMORE E GRANITOS LTDA",
    "nome_na_tela": "Conta 41932-0",
    "nome_arquivo": "Sicoob_41932"
    },
    {
    "nome_empresa": "BOUTIQUE DA PEDRA COMERCIO DE MARMORE E GRANITOS",
    "nome_na_tela": "Conta 53276-2",
    "nome_arquivo": "Sicoob_53276"
    },
    {
    "nome_empresa": "MARMORARIA SERTANEZINA - COMERCIO DE PEDRAS LTDA",
    "nome_na_tela": "Conta 81117-3",
    "nome_arquivo": "Sicoob_81117"
    }
]

# --- Funções Auxiliares ---

def clicar_imagem(image_name, confidence=0.7, tries=3, delay=1):
    """
    Tenta encontrar e clicar em uma imagem na tela, verificando vários caminhos de pasta.
    """
    # Define a lista de pastas para procurar
    pastas_a_procurar = [IMAGENS_BOTOES_FOLDER, IMAGENS_DIAS_FOLDER, IMAGENS_CONTAS_FOLDER]
    image_path = None

    for pasta in pastas_a_procurar:
        caminho_completo = os.path.join(pasta, image_name)
        if os.path.exists(caminho_completo):
            image_path = caminho_completo
            break
        
    if not image_path:
        logger.error(f"Erro: Arquivo de imagem '{image_name}' não encontrado em nenhum diretório.")
        return False

    for i in range(tries):
        try:
            button_location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            if button_location:
                pyautogui.click(button_location)
            time.sleep(delay)
            logger.info(f"Sucesso: Clicou em '{image_name}' na posição {button_location}.")
            return True
        except pyautogui.ImageNotFoundException:
            logger.warning(f"Tentativa {i+1}/{tries}: Imagem '{image_name}' não encontrada na tela.")
            if i == tries - 1:
                screenshot_path = f"debug_erro_{image_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                pyautogui.screenshot(screenshot_path)
                logger.info(f"Screenshot de debug salvo: {screenshot_path}")
        except Exception as e:
            logger.error(f"Erro inesperado ao clicar em '{image_name}': {e}")
            break

    logger.error(f"Falha: Não foi possível encontrar e clicar em '{image_name}' após {tries} tentativas.")
    return False

def selecionar_datas_no_calendario():
    """
    Seleciona o primeiro dia do mês e a data atual no calendário.
    """
    logger.info("Selecionando o período no calendário...")
    if not clicar_imagem('1.jpg', confidence=0.9, tries=5, delay=2):
        logger.error("Falha ao selecionar o dia 1.")
        return False

    dia_atual = datetime.date.today().day
    dia_atual_str = f"{dia_atual}.jpg"
    if not clicar_imagem(dia_atual_str, confidence=0.9, tries=5, delay=2):
        logger.error(f"Falha ao selecionar o dia atual ({dia_atual_str}).")
        return False

    logger.info("Período de extrato selecionado com sucesso.")
    return True

# --- Função Principal de Automação ---
def baixar_extrato_sicoob(nome_conta_na_tela):
    """
    Executa a sequência de ações para baixar o extrato de uma única conta.
    """
    logger.info(f"Iniciando o processo para a conta: {nome_conta_na_tela}")

    # Constrói o nome do arquivo da imagem da conta
    image_name_conta = nome_conta_na_tela.replace("Conta ", "conta_").lower() + ".png"

    # Encontra o texto da conta e clica no botão "Acessar conta" ao lado
    try:
        # Procura pela imagem da conta com uma confiança menor para ser mais robusto
        image_path_conta = os.path.join(IMAGENS_CONTAS_FOLDER, image_name_conta)
        conta_text_location = pyautogui.locateCenterOnScreen(image_path_conta, confidence=0.7)

        if conta_text_location:
             # Clica no botão "Acessar conta" (assumindo que está à direita do texto)
            acessar_conta_x = conta_text_location.x + 400
            pyautogui.click(x=acessar_conta_x, y=conta_text_location.y)
            logger.info(f"Clicou no botão 'Acessar conta' para {nome_conta_na_tela}")
            time.sleep(5)
        else:
            logger.error(f"Erro: Imagem do texto da conta '{nome_conta_na_tela}' não encontrada na tela.")
            return False
    except Exception as e:
        logger.error(f"Erro ao procurar pela conta '{nome_conta_na_tela}': {e}")
        return False
 
    # Sequência de cliques para baixar o extrato
    passos = [
        ('extrato.jpg', 'botão Extrato'),
        ('periodo.jpg', 'botão Período'),
]
 
    for imagem, descricao in passos:
        if not clicar_imagem(imagem, confidence=0.9):
            logger.error(f"Falha ao clicar em {descricao}")
            return False

    if not selecionar_datas_no_calendario():
        logger.error("Falha ao selecionar datas no calendário")
        return False

    logger.info("Rolando a página...")
    pyautogui.scroll(-500)
    time.sleep(2)
    
    passos_finais = [
        ('exportar-extrato.jpg', 'botão Exportar Extrato'),
        ('radio-button-xls.jpg', 'radio button XLS'),
        ('exportar-extrato-final.jpg', 'botão final Exportar')
]
 
    for imagem, descricao in passos_finais:
        if not clicar_imagem(imagem, confidence=0.9):
            logger.error(f"Falha ao clicar em {descricao}")
            return False
 
    logger.info("Aguardando download...")
    time.sleep(5)

    logger.info("Download concluído. Voltando para a tela de seleção de contas.")
    if not clicar_imagem('trocar-conta.jpg', confidence=0.9, tries=5, delay=3):
        logger.warning("Falha ao voltar para a tela inicial.")
        return False

    logger.info(f"Processo para a conta {nome_conta_na_tela} finalizado com sucesso.")
    return True

# --- Execução Principal do Script ---
if __name__ == "__main__":
    logger.info("="*60)
    logger.info("INICIANDO AUTOMAÇÃO DE DOWNLOAD DE EXTRATOS SICOOB")
    logger.info("="*60)

    logger.info("Posicione a tela com as contas visível")
    logger.info("A automação começará em 10 segundos...")
    logger.info("Pressione Ctrl+C para cancelar")
 
    try:
        for i in range(10, 0, -1):
            print(f"Iniciando em {i} segundos...", end='\r')
            time.sleep(1)
        print(" " * 30, end='\r')

        sucessos = 0
        falhas = 0

        for i, conta in enumerate(CONTAS, 1):
            logger.info(f"Processando conta {i}/{len(CONTAS)}: {conta['nome_na_tela']}")

            try:
                if baixar_extrato_sicoob(conta["nome_na_tela"]):
                    sucessos += 1
                    logger.info(f"✅ Conta {conta['nome_na_tela']} processada com sucesso")
                else:
                    falhas += 1
                    logger.error(f"❌ Falha ao processar conta {conta['nome_na_tela']}")
                if i < len(CONTAS):
                    logger.info("Aguardando antes da próxima conta...")
                    time.sleep(3)
            except KeyboardInterrupt:
                logger.warning("Automação interrompida pelo usuário")
                break
            except Exception as e:
                falhas += 1
                logger.error(f"Erro inesperado na conta {conta['nome_na_tela']}: {e}")

        logger.info("="*60)
        logger.info("RESUMO DA AUTOMAÇÃO")
        logger.info("="*60)
        logger.info(f"Total de contas: {len(CONTAS)}")
        logger.info(f"Sucessos: {sucessos}")
        logger.info(f"Falhas: {falhas}")
        
        if falhas == 0:
            logger.info("🎉 Todos os extratos foram baixados com sucesso!")
        else:
            logger.warning(f"⚠️  {falhas} conta(s) apresentaram problemas")
    except KeyboardInterrupt:
        logger.warning("Automação cancelada pelo usuário")
    except Exception as e:
        logger.error(f"Erro crítico na automação: {e}")
        
    logger.info("Automação finalizada")
    input("Pressione ENTER para sair...")
