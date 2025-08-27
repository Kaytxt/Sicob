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
pyautogui.PAUSE = 1.0
pyautogui.FAILSAFE = True

# Caminhos do projeto
BASE_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGENS_BOTOES_FOLDER = os.path.join(BASE_FOLDER, 'img_automacao', 'botoes')
IMAGENS_CONTAS_FOLDER = os.path.join(IMAGENS_BOTOES_FOLDER, 'contas')
IMAGENS_DIAS_FOLDER = os.path.join(BASE_FOLDER, 'img_automacao', 'dias')
DOWNLOAD_FOLDER = os.path.join(BASE_FOLDER, 'extratos_baixados')

# Garante que as pastas existem
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Lista das contas a serem processadas (CORRIGIDA)
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
        "nome_na_tela": "Conta 81117-3",  # CORRIGIDO: era 81171-3
        "nome_arquivo": "Sicoob_81117"  # CORRIGIDO: era Sicoob_81171
    }
]

# --- Funções Auxiliares ---
def verificar_arquivo_imagem(caminho_arquivo):
    """
    Verifica se o arquivo de imagem existe e pode ser carregado
    """
    if not os.path.exists(caminho_arquivo):
        logger.error(f"Arquivo não encontrado: {caminho_arquivo}")
        return False
    
    if not os.access(caminho_arquivo, os.R_OK):
        logger.error(f"Sem permissão para ler arquivo: {caminho_arquivo}")
        return False
    
    try:
        img = cv2.imread(caminho_arquivo)
        if img is None:
            logger.error(f"OpenCV não conseguiu carregar a imagem: {caminho_arquivo}")
            return False
        return True
    except Exception as e:
        logger.error(f"Erro ao carregar imagem: {e}")
        return False

def encontrar_imagem_conta(nome_conta_na_tela):
    """
    Procura pela imagem da conta, testando diferentes variações de nome
    """
    # Nome padrão baseado no código original
    image_name_principal = nome_conta_na_tela.replace("Conta ", "conta_").lower() + ".png"
    caminho_principal = os.path.join(IMAGENS_CONTAS_FOLDER, image_name_principal)
    
    if verificar_arquivo_imagem(caminho_principal):
        logger.info(f"Imagem principal encontrada: {image_name_principal}")
        return caminho_principal
    
    # Variações de nome para tentar
    numero_conta = nome_conta_na_tela.replace("Conta ", "")
    variações = [
        f"conta_{numero_conta}.png",
        f"conta_{numero_conta.replace('-', '_')}.png",
        f"conta_{numero_conta.replace('_', '-')}.png",
        f"{numero_conta}.png",
        f"Conta_{numero_conta}.png",
        f"conta{numero_conta}.png",
        f"conta{numero_conta.replace('-', '')}.png"
    ]
    
    logger.warning(f"Imagem principal não encontrada: {image_name_principal}")
    logger.info("Testando variações de nome...")
    
    for variacao in variações:
        caminho_variacao = os.path.join(IMAGENS_CONTAS_FOLDER, variacao)
        if verificar_arquivo_imagem(caminho_variacao):
            logger.info(f"Imagem alternativa encontrada: {variacao}")
            return caminho_variacao
    
    # Se não encontrou nenhuma variação, lista arquivos disponíveis
    logger.error(f"Nenhuma imagem encontrada para a conta: {nome_conta_na_tela}")
    
    if os.path.exists(IMAGENS_CONTAS_FOLDER):
        logger.info("Arquivos PNG disponíveis no diretório de contas:")
        for arquivo in os.listdir(IMAGENS_CONTAS_FOLDER):
            if arquivo.endswith('.png'):
                logger.info(f"  - {arquivo}")
    
    return None

def clicar_imagem(image_name, confidence=0.7, tries=3, delay=1, pasta_especifica=None):
    """
    Tenta encontrar e clicar em uma imagem na tela com melhor tratamento de erro.
    """
    # Define as pastas para procurar
    if pasta_especifica:
        caminhos_possíveis = [os.path.join(pasta_especifica, image_name)]
    else:
        caminhos_possíveis = [
            os.path.join(IMAGENS_BOTOES_FOLDER, image_name),
            os.path.join(IMAGENS_DIAS_FOLDER, image_name),
            os.path.join(IMAGENS_CONTAS_FOLDER, image_name)
        ]
    
    # Procura o arquivo de imagem
    image_path = None
    for caminho in caminhos_possíveis:
        if verificar_arquivo_imagem(caminho):
            image_path = caminho
            break
    
    if not image_path:
        logger.error(f"Arquivo de imagem '{image_name}' não encontrado em nenhum diretório")
        return False

    logger.info(f"Tentando clicar em '{image_name}' (caminho: {image_path})")
    
    for i in range(tries):
        try:
            button_location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            if button_location:
                pyautogui.click(button_location)
                time.sleep(delay)
                logger.info(f"Sucesso: Clicou em '{image_name}' na posição {button_location}")
                return True
        except pyautogui.ImageNotFoundException:
            logger.warning(f"Tentativa {i+1}/{tries}: Imagem '{image_name}' não encontrada na tela")
            if i == tries - 1:  # Na última tentativa, captura screenshot para debug
                screenshot_path = f"debug_erro_{image_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                pyautogui.screenshot(screenshot_path)
                logger.info(f"Screenshot de debug salvo: {screenshot_path}")
        except Exception as e:
            logger.error(f"Erro inesperado ao clicar em '{image_name}': {e}")
        
        if i < tries - 1:  # Não esperar na última tentativa
            time.sleep(delay)
    
    logger.error(f"Falha: Não foi possível encontrar e clicar em '{image_name}' após {tries} tentativas")
    return False
    
def selecionar_datas_no_calendario():
    """
    Seleciona o primeiro dia do mês e a data atual no calendário.
    """
    logger.info("Selecionando o período no calendário...")
    
    # Clica no dia 1 do mês
    if not clicar_imagem('1.jpg', confidence=0.9, tries=5, delay=2):
        logger.error("Falha ao selecionar o dia 1")
        return False
    
    # Clica no dia atual do mês
    dia_atual = datetime.date.today().day
    dia_atual_str = f"{dia_atual}.jpg"
    
    if not clicar_imagem(dia_atual_str, confidence=0.9, tries=5, delay=2):
        logger.error(f"Falha ao selecionar o dia atual ({dia_atual_str})")
        
        # Tenta variações do nome do dia
        variações_dia = [
            f"{dia_atual:02d}.jpg",  # Com zero à esquerda
            f"dia_{dia_atual}.jpg",
            f"dia{dia_atual}.jpg",
        ]
        
        logger.info("Tentando variações do nome do arquivo do dia...")
        encontrou_dia = False
        for variacao in variações_dia:
            if clicar_imagem(variacao, confidence=0.9, tries=2, delay=1):
                logger.info(f"Dia selecionado com nome alternativo: {variacao}")
                encontrou_dia = True
                break
        
        if not encontrou_dia:
            logger.error("Não foi possível selecionar o dia atual com nenhuma variação")
            return False

    logger.info("Período de extrato selecionado com sucesso")
    return True

def baixar_extrato_sicoob(nome_conta_na_tela):
    """
    Executa a sequência de ações para baixar o extrato de uma única conta.
    """
    logger.info(f"Iniciando processo para a conta: {nome_conta_na_tela}")
    
    # Encontra a imagem da conta
    caminho_imagem_conta = encontrar_imagem_conta(nome_conta_na_tela)
    if not caminho_imagem_conta:
        logger.error(f"Não foi possível encontrar imagem para a conta: {nome_conta_na_tela}")
        return False

    # Encontra o texto da conta e clica no botão "Acessar conta" ao lado
    try:
        logger.info(f"Procurando pela conta na tela: {nome_conta_na_tela}")
        conta_text_location = pyautogui.locateCenterOnScreen(caminho_imagem_conta, confidence=0.7)

        if conta_text_location:
            # Clica no botão "Acessar conta" (assumindo que está à direita do texto)
            acessar_conta_x = conta_text_location.x + 400
            pyautogui.click(x=acessar_conta_x, y=conta_text_location.y)
            logger.info(f"Clicou no botão 'Acessar conta' para {nome_conta_na_tela}")
            time.sleep(5)
        else:
            logger.error(f"Texto da conta '{nome_conta_na_tela}' não encontrado na tela")
            # Tenta com confiança menor
            logger.info("Tentando com confiança menor (0.6)...")
            conta_text_location = pyautogui.locateCenterOnScreen(caminho_imagem_conta, confidence=0.6)
            
            if conta_text_location:
                acessar_conta_x = conta_text_location.x + 400
                pyautogui.click(x=acessar_conta_x, y=conta_text_location.y)
                logger.info(f"Clicou no botão 'Acessar conta' para {nome_conta_na_tela} (confiança baixa)")
                time.sleep(5)
            else:
                logger.error(f"Não foi possível encontrar a conta '{nome_conta_na_tela}' mesmo com confiança baixa")
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

    # Selecionar datas no calendário
    if not selecionar_datas_no_calendario():
        logger.error("Falha ao selecionar datas no calendário")
        return False

    # Rolar a página e continuar
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

    logger.info("Download concluído. Voltando para a tela de seleção de contas")
    if not clicar_imagem('trocar-conta.jpg', confidence=0.9, tries=5, delay=3):
        logger.warning("Falha ao voltar para a tela inicial")
        # Não retorna False aqui pois o download pode ter sido bem-sucedido

    logger.info(f"Processo para a conta {nome_conta_na_tela} finalizado com sucesso")
    return True

def verificar_prerequisitos():
    """
    Verifica se todos os arquivos necessários existem antes de iniciar
    """
    logger.info("Verificando pré-requisitos...")
    
    # Verificar se as pastas existem
    pastas_necessarias = [
        IMAGENS_BOTOES_FOLDER,
        IMAGENS_CONTAS_FOLDER,
        IMAGENS_DIAS_FOLDER
    ]
    
    for pasta in pastas_necessarias:
        if not os.path.exists(pasta):
            logger.error(f"Pasta necessária não encontrada: {pasta}")
            return False
    
    # Verificar se as imagens das contas existem
    contas_sem_imagem = []
    for conta in CONTAS:
        if not encontrar_imagem_conta(conta["nome_na_tela"]):
            contas_sem_imagem.append(conta["nome_na_tela"])
    
    if contas_sem_imagem:
        logger.error("Contas sem imagem de referência:")
        for conta in contas_sem_imagem:
            logger.error(f"  - {conta}")
        logger.error("Execute o script de criação de imagens antes de continuar")
        return False
    
    logger.info("Todos os pré-requisitos foram atendidos")
    return True

# --- Execução Principal do Script ---
if __name__ == "__main__":
    logger.info("="*60)
    logger.info("INICIANDO AUTOMAÇÃO DE DOWNLOAD DE EXTRATOS SICOOB")
    logger.info("="*60)
    
    # Verificar pré-requisitos
    if not verificar_prerequisitos():
        logger.error("Pré-requisitos não atendidos. Encerrando...")
        input("Pressione ENTER para sair...")
        exit(1)
    
    logger.info("Posicione a tela com as contas visível")
    logger.info("A automação começará em 10 segundos...")
    logger.info("Pressione Ctrl+C para cancelar")
    
    try:
        for i in range(10, 0, -1):
            print(f"Iniciando em {i} segundos...", end='\r')
            time.sleep(1)
        print(" " * 30, end='\r')  # Limpa a linha
        
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
                    
                # Pequena pausa entre contas
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