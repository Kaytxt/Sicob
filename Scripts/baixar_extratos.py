import pyautogui
import time
import os

# --- Configurações Iniciais ---
# Tempo de pausa entre as ações do mouse/teclado.
# Isso é crucial para que o script não seja mais rápido que o carregamento da página.
pyautogui.PAUSE = 1.0

# Define o caminho base do projeto
BASE_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGENS_BOTOES_FOLDER = os.path.join(BASE_FOLDER, 'img_automacao', 'botoes')

# --- Funções Auxiliares ---
def clicar_imagem(image_name, confidence=0.9, tries=3, delay=1):
    """
    Tenta encontrar e clicar em uma imagem na tela.
    Args:
        image_name (str): Nome do arquivo da imagem (ex: 'acessar-conta.jpg').
        confidence (float): Nível de confiança para encontrar a imagem (0.0 a 1.0).
        tries (int): Número de tentativas para encontrar e clicar na imagem.
        delay (int): Atraso em segundos entre as tentativas.
    Returns:
        bool: True se a imagem foi clicada, False caso contrário.
    """
    image_path = os.path.join(IMAGENS_BOTOES_FOLDER, image_name)

    for i in range(tries):
        try:
            button_location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            if button_location:
                pyautogui.click(button_location)
                time.sleep(delay)
                print(f"Sucesso: Clicou em '{image_name}'.")
                return True
        except pyautogui.ImageNotFoundException:
            print(f"Tentativa {i+1}: Imagem '{image_name}' não encontrada.")
        time.sleep(delay)
    print(f"Erro: Não foi possível encontrar e clicar em '{image_name}' após {tries} tentativas.")
    return False

# --- Execução Principal do Script ---
if __name__ == "__main__":
    print("Iniciando a automação: Acessando a primeira conta.")

    # Certifique-se de que a tela com as contas (Image 1) esteja visível
    # antes de rodar este script.

    # Dá um tempo para você mudar para a janela do navegador
    print("Você tem 5 segundos para mudar para a tela das contas...")
    time.sleep(5) 

    # Tenta clicar no botão "Acessar conta"
    if clicar_imagem('acessar-conta.jpg'):
        print("Automação concluída para a primeira etapa.")
    else:
        print("Falha na automação da primeira etapa.")