import pyautogui
import time
import os
import datetime
import logging
from pathlib import Path
from PIL import Image

# --- Configurações de Logging (SEM EMOJIS) ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automacao_sicoob.log', encoding='utf-8'),
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

# Lista das contas (VERIFICAR NOMES EXATOS)
CONTAS = [
    {
        "nome_empresa": "SERTANEZINA COMERCIO DE PEDRAS",
        "nome_na_tela": "Conta 41930-3",  # SEM pontos
        "nome_arquivo": "Sicoob_41930"
    },
    {
        "nome_empresa": "F C F - COMERCIO DE MARMORE E GRANITOS LTDA",
        "nome_na_tela": "Conta 41932-0",  # SEM pontos
        "nome_arquivo": "Sicoob_41932"
    },
    {
        "nome_empresa": "BOUTIQUE DA PEDRA COMERCIO DE MARMORE E GRANITOS",
        "nome_na_tela": "Conta 53276-2",  # SEM pontos
        "nome_arquivo": "Sicoob_53276"
    },
    {
        "nome_empresa": "MARMORARIA SERTANEZINA - COMERCIO DE PEDRAS LTDA",
        "nome_na_tela": "Conta 81117-3",  # SEM pontos (CORRIGIDO)
        "nome_arquivo": "Sicoob_81117"
    }
]

# Lista de botões necessários para verificar
BOTOES_NECESSARIOS = [
    'extrato.jpg',
    'periodo.jpg',
    'exportar-extrato.jpg',
    'radio-button-xls.jpg',
    'exportar-extrato-final.jpg',
    'trocar-conta.jpg'
]

# --- Funções Auxiliares ---
def verificar_arquivo_imagem(caminho_arquivo):
    """
    Verifica se o arquivo de imagem existe e pode ser carregado
    """
    if not os.path.exists(caminho_arquivo):
        logger.error(f"Arquivo nao encontrado: {caminho_arquivo}")
        return False
    
    if not os.access(caminho_arquivo, os.R_OK):
        logger.error(f"Sem permissao para ler arquivo: {caminho_arquivo}")
        return False
    
    try:
        with Image.open(caminho_arquivo) as img:
            return True
    except Exception as e:
        logger.error(f"Erro ao carregar imagem: {e}")
        return False

def verificar_todos_botoes():
    """
    Verifica se todas as imagens de botões existem
    """
    logger.info("Verificando imagens de botoes...")
    botoes_faltando = []
    
    for botao in BOTOES_NECESSARIOS:
        caminho_botao = os.path.join(IMAGENS_BOTOES_FOLDER, botao)
        if not verificar_arquivo_imagem(caminho_botao):
            botoes_faltando.append(botao)
            logger.error(f"Botao faltando: {botao}")
        else:
            logger.info(f"Botao OK: {botao}")
    
    if botoes_faltando:
        logger.error(f"CRITICO: {len(botoes_faltando)} botoes faltando!")
        logger.error("Execute primeiro um script para capturar essas imagens")
        return False
    
    logger.info("Todos os botoes estao disponiveis")
    return True

def encontrar_imagem_conta(nome_conta_na_tela):
    """
    Procura pela imagem da conta, testando diferentes variações de nome
    """
    # Variações possíveis do nome
    variacoes_nome = [
        nome_conta_na_tela.replace("Conta ", "conta_").lower() + ".png",  # conta_41930-3.png
        nome_conta_na_tela.replace("Conta ", "conta_").replace("-", ".").lower() + ".png",  # conta_41930.3.png  
        nome_conta_na_tela.replace("Conta ", "conta_").replace("-", "_").lower() + ".png",  # conta_41930_3.png
    ]
    
    logger.info(f"Procurando imagem para: {nome_conta_na_tela}")
    
    for i, variacao in enumerate(variacoes_nome):
        caminho = os.path.join(IMAGENS_CONTAS_FOLDER, variacao)
        logger.info(f"Tentativa {i+1}: {variacao}")
        
        if verificar_arquivo_imagem(caminho):
            logger.info(f"Imagem encontrada: {variacao}")
            return caminho
    
    # Se não encontrou nenhuma variação, lista arquivos disponíveis
    logger.error(f"Nenhuma imagem encontrada para: {nome_conta_na_tela}")
    
    if os.path.exists(IMAGENS_CONTAS_FOLDER):
        logger.info("Arquivos PNG disponiveis:")
        for arquivo in os.listdir(IMAGENS_CONTAS_FOLDER):
            if arquivo.endswith('.png'):
                logger.info(f"  - {arquivo}")
    
    return None

def capturar_screenshot_debug(nome_arquivo):
    """
    Captura screenshot para debug
    """
    try:
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        caminho = f"debug_{nome_arquivo}_{timestamp}.png"
        pyautogui.screenshot(caminho)
        logger.info(f"Screenshot debug salvo: {caminho}")
        return caminho
    except Exception as e:
        logger.error(f"Erro ao capturar screenshot: {e}")
        return None

def clicar_imagem_com_debug(image_name, confidence=0.7, tries=3, delay=1):
    """
    Versão melhorada com mais debugging
    """
    # Procura o arquivo
    caminhos_possíveis = [
        os.path.join(IMAGENS_BOTOES_FOLDER, image_name),
        os.path.join(IMAGENS_DIAS_FOLDER, image_name),
        os.path.join(IMAGENS_CONTAS_FOLDER, image_name)
    ]
    
    image_path = None
    for caminho in caminhos_possíveis:
        if verificar_arquivo_imagem(caminho):
            image_path = caminho
            break
    
    if not image_path:
        logger.error(f"Imagem nao encontrada: {image_name}")
        logger.info("Capturando screenshot para debug...")
        capturar_screenshot_debug(f"imagem_nao_encontrada_{image_name}")
        return False

    logger.info(f"Tentando clicar: {image_name}")
    logger.info(f"Caminho: {image_path}")
    logger.info(f"Confianca: {confidence}")
    
    for tentativa in range(tries):
        logger.info(f"Tentativa {tentativa+1}/{tries}")
        
        try:
            # Procurar na tela
            logger.info("Procurando imagem na tela...")
            locations = list(pyautogui.locateAllOnScreen(image_path, confidence=confidence))
            
            if locations:
                logger.info(f"Imagem encontrada! {len(locations)} ocorrencia(s)")
                
                # Usar a primeira ocorrência
                button_location = pyautogui.center(locations[0])
                logger.info(f"Clicando na posicao: {button_location}")
                
                pyautogui.click(button_location)
                time.sleep(delay)
                
                logger.info(f"Sucesso: Clicou em {image_name}")
                return True
            else:
                logger.warning(f"Imagem nao encontrada na tela (tentativa {tentativa+1})")
                
        except Exception as e:
            logger.error(f"Erro na tentativa {tentativa+1}: {e}")
        
        # Capturar screenshot de debug na última tentativa
        if tentativa == tries - 1:
            logger.info("Capturando screenshot de debug...")
            capturar_screenshot_debug(f"erro_{image_name}")
        
        if tentativa < tries - 1:
            time.sleep(delay)
    
    logger.error(f"FALHA: Nao foi possivel clicar em {image_name}")
    return False

def testar_clique_manual():
    """
    Modo de teste manual para verificar se os cliques estão funcionando
    """
    print("\n" + "="*60)
    print("MODO TESTE MANUAL")
    print("="*60)
    print("Este modo permite testar cada botão individualmente")
    print("Pressione ENTER para cada teste ou 'q' para pular\n")
    
    for botao in BOTOES_NECESSARIOS:
        resposta = input(f"Testar '{botao}'? (ENTER=sim, q=pular): ").strip()
        if resposta.lower() == 'q':
            continue
            
        print(f"Testando {botao}...")
        sucesso = clicar_imagem_com_debug(botao, confidence=0.8, tries=1)
        
        if sucesso:
            print(f"SUCESSO: {botao} encontrado e clicado!")
        else:
            print(f"FALHA: {botao} nao encontrado")
        
        input("Pressione ENTER para continuar...")

def baixar_extrato_sicoob_debug(nome_conta_na_tela):
    """
    Versão com debug intensivo
    """
    logger.info(f"INICIANDO: {nome_conta_na_tela}")
    
    # 1. Encontrar imagem da conta
    caminho_imagem_conta = encontrar_imagem_conta(nome_conta_na_tela)
    if not caminho_imagem_conta:
        logger.error(f"Imagem da conta nao encontrada: {nome_conta_na_tela}")
        return False

    # 2. Procurar conta na tela
    logger.info("Procurando conta na tela...")
    
    try:
        # Tentar diferentes níveis de confiança
        confiancas = [0.9, 0.8, 0.7, 0.6]
        conta_location = None
        
        for conf in confiancas:
            logger.info(f"Tentando confianca {conf}")
            try:
                conta_location = pyautogui.locateCenterOnScreen(caminho_imagem_conta, confidence=conf)
                if conta_location:
                    logger.info(f"Conta encontrada com confianca {conf}: {conta_location}")
                    break
            except:
                continue
        
        if not conta_location:
            logger.error("Conta nao encontrada na tela")
            logger.info("Capturando screenshot...")
            capturar_screenshot_debug(f"conta_nao_encontrada_{nome_conta_na_tela}")
            return False

        # 3. Clicar em "Acessar conta"
        logger.info("Clicando no botao Acessar conta...")
        acessar_x = conta_location.x + 400  # Ajustar se necessário
        acessar_y = conta_location.y
        
        logger.info(f"Posicao do clique: ({acessar_x}, {acessar_y})")
        pyautogui.click(acessar_x, acessar_y)
        logger.info("Clicou no botao Acessar conta")
        
        # 4. Aguardar carregamento da página
        logger.info("Aguardando carregamento da pagina...")
        time.sleep(5)
        
        # 5. Capturar screenshot após clicar
        logger.info("Capturando screenshot apos acessar conta...")
        capturar_screenshot_debug(f"apos_acessar_{nome_conta_na_tela}")
        
        # 6. Sequência de botões
        passos = [
            ('extrato.jpg', 'botao Extrato'),
            ('periodo.jpg', 'botao Periodo'),
        ]
        
        for imagem, descricao in passos:
            logger.info(f"Tentando clicar: {descricao}")
            
            if not clicar_imagem_com_debug(imagem, confidence=0.8, tries=5, delay=2):
                logger.error(f"FALHA em {descricao}")
                return False
            
            logger.info(f"Sucesso: {descricao}")
            time.sleep(2)  # Aguardar entre cliques
        
        # Continuar com o resto do fluxo...
        logger.info("Fluxo basico completado")
        return True
        
    except Exception as e:
        logger.error(f"Erro durante processo: {e}")
        capturar_screenshot_debug(f"erro_geral_{nome_conta_na_tela}")
        return False

def menu_debug():
    """
    Menu para debug e testes
    """
    while True:
        print("\n" + "="*60)
        print("MENU DEBUG - SICOOB")
        print("="*60)
        print("1. Verificar todas as imagens")
        print("2. Testar cliques manuais")
        print("3. Processar uma conta (debug completo)")
        print("4. Capturar screenshot atual")
        print("5. Listar arquivos de imagem")
        print("6. Executar automacao normal")
        print("7. Sair")
        print("="*60)
        
        opcao = input("Escolha (1-7): ").strip()
        
        if opcao == "1":
            verificar_todos_botoes()
            for conta in CONTAS:
                encontrar_imagem_conta(conta["nome_na_tela"])
            
        elif opcao == "2":
            testar_clique_manual()
            
        elif opcao == "3":
            print("\nContas disponíveis:")
            for i, conta in enumerate(CONTAS, 1):
                print(f"{i}. {conta['nome_na_tela']}")
            
            try:
                escolha = int(input("Qual conta testar? (1-4): ")) - 1
                if 0 <= escolha < len(CONTAS):
                    baixar_extrato_sicoob_debug(CONTAS[escolha]["nome_na_tela"])
                else:
                    print("Opcao invalida!")
            except ValueError:
                print("Digite um numero!")
                
        elif opcao == "4":
            capturar_screenshot_debug("manual")
            
        elif opcao == "5":
            print(f"\nImagens em: {IMAGENS_CONTAS_FOLDER}")
            if os.path.exists(IMAGENS_CONTAS_FOLDER):
                for arquivo in os.listdir(IMAGENS_CONTAS_FOLDER):
                    if arquivo.endswith('.png'):
                        caminho = os.path.join(IMAGENS_CONTAS_FOLDER, arquivo)
                        tamanho = os.path.getsize(caminho)
                        print(f"  - {arquivo} ({tamanho} bytes)")
            
            print(f"\nImagens em: {IMAGENS_BOTOES_FOLDER}")
            if os.path.exists(IMAGENS_BOTOES_FOLDER):
                for arquivo in os.listdir(IMAGENS_BOTOES_FOLDER):
                    if arquivo.endswith('.jpg') or arquivo.endswith('.png'):
                        caminho = os.path.join(IMAGENS_BOTOES_FOLDER, arquivo)
                        tamanho = os.path.getsize(caminho)
                        print(f"  - {arquivo} ({tamanho} bytes)")
                        
        elif opcao == "6":
            # Executar automação normal
            if not verificar_todos_botoes():
                print("Corrija os problemas antes de executar!")
                continue
                
            print("Executando automacao...")
            input("Pressione ENTER quando estiver pronto...")
            
            for conta in CONTAS:
                print(f"\nProcessando: {conta['nome_na_tela']}")
                if not baixar_extrato_sicoob_debug(conta["nome_na_tela"]):
                    print(f"Falha na conta: {conta['nome_na_tela']}")
                    break
                time.sleep(3)
            
        elif opcao == "7":
            break
            
        else:
            print("Opcao invalida!")
        
        input("\nPressione ENTER para continuar...")

# --- Execução Principal ---
if __name__ == "__main__":
    logger.info("INICIANDO MODO DEBUG")
    
    try:
        menu_debug()
    except KeyboardInterrupt:
        logger.info("Programa interrompido pelo usuario")
    except Exception as e:
        logger.error(f"Erro critico: {e}")
    
    logger.info("Programa finalizado")
    input("Pressione ENTER para sair...")