import pyautogui
import os
from pathlib import Path
import time

# Caminhos do projeto
BASE_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGENS_CONTAS_FOLDER = os.path.join(BASE_FOLDER, 'img_automacao', 'botoes', 'contas')

def descobrir_nome_conta_exato():
    """
    Ajuda a descobrir o nome exato das contas na tela
    """
    print("🔍 DESCOBRIDOR DE NOMES DE CONTAS")
    print("="*50)
    print("""
Este script ajuda a descobrir o nome EXATO das contas como aparecem na tela.

PROCESSO:
1. Abra o sistema Sicoob 
2. Vá para a tela que mostra a lista de contas
3. Para cada conta, vamos capturar uma imagem pequena
4. Você vai dizer qual conta é essa
5. O script vai salvar com o nome correto

IMPORTANTE: Capture apenas o TEXTO da conta (ex: "Conta 41930-3")
""")
    
    input("Pressione ENTER quando estiver na tela com as contas visíveis...")
    
    # Garantir que a pasta existe
    Path(IMAGENS_CONTAS_FOLDER).mkdir(parents=True, exist_ok=True)
    
    conta_numero = 1
    
    while True:
        print(f"\n📸 CAPTURANDO CONTA #{conta_numero}")
        print("-" * 30)
        
        continuar = input(f"Capturar mais uma conta? (ENTER=sim, 'n'=terminar): ").strip().lower()
        if continuar == 'n':
            break
        
        print(f"\nPASSOO 1: Posicione o mouse no CANTO SUPERIOR ESQUERDO do texto da conta")
        input("Pressione ENTER quando posicionado...")
        
        x1, y1 = pyautogui.position()
        print(f"Posição 1: ({x1}, {y1})")
        
        print(f"\nPASSOO 2: Mova o mouse para o CANTO INFERIOR DIREITO do texto da conta")
        input("Pressione ENTER quando posicionado...")
        
        x2, y2 = pyautogui.position()
        print(f"Posição 2: ({x2}, {y2})")
        
        # Validar área
        largura = abs(x2 - x1)
        altura = abs(y2 - y1)
        
        if largura < 20 or altura < 10:
            print(f"⚠️  Área pequena ({largura}x{altura}). Continuar?")
            if input("s/N: ").lower() != 's':
                continue
        
        print(f"Área: {largura}x{altura} pixels")
        
        # Capturar
        print("Capturando em 2 segundos...")
        time.sleep(2)
        
        try:
            x_min = min(x1, x2)
            y_min = min(y1, y2)
            
            screenshot = pyautogui.screenshot(region=(x_min, y_min, largura, altura))
            
            # Mostrar a imagem capturada
            try:
                screenshot.show()
                print("👁️  Imagem capturada mostrada")
            except:
                pass
            
            # Perguntar qual conta é essa
            print(f"\n❓ QUAL CONTA FOI CAPTURADA?")
            print("Digite o nome EXATO como aparece na imagem:")
            print("Exemplos:")
            print("  - Conta 41930-3")
            print("  - Conta 41.930-3") 
            print("  - CONTA 41930-3")
            print("  - 41930-3")
            
            nome_conta = input("\nNome da conta: ").strip()
            
            if not nome_conta:
                print("❌ Nome vazio, pulando...")
                continue
            
            # Gerar nome do arquivo
            nome_arquivo = nome_conta.lower().replace(" ", "_") + ".png"
            # Limpar caracteres especiais
            nome_arquivo = nome_arquivo.replace(".", "").replace("-", "_")
            
            print(f"Arquivo será salvo como: {nome_arquivo}")
            
            confirmar = input("Confirmar? (ENTER=sim): ").strip()
            if confirmar.lower() not in ['', 's', 'sim']:
                print("❌ Não salvo")
                continue
            
            # Salvar
            caminho_final = os.path.join(IMAGENS_CONTAS_FOLDER, nome_arquivo)
            screenshot.save(caminho_final)
            
            tamanho = os.path.getsize(caminho_final)
            print(f"✅ Salvo: {nome_arquivo} ({tamanho} bytes)")
            
            # Também salvar com nome padrão para compatibilidade
            if "conta" in nome_conta.lower():
                nome_padrao = nome_conta.replace("Conta ", "conta_").lower() + ".png"
                caminho_padrao = os.path.join(IMAGENS_CONTAS_FOLDER, nome_padrao)
                screenshot.save(caminho_padrao)
                print(f"✅ Também salvo como: {nome_padrao}")
            
            conta_numero += 1
            
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    print(f"\n🎉 Processo concluído!")
    print(f"📁 Imagens salvas em: {IMAGENS_CONTAS_FOLDER}")

def analisar_imagens_existentes():
    """
    Analisa as imagens existentes e tenta deduzir os nomes corretos
    """
    print("\n🔍 ANALISANDO IMAGENS EXISTENTES")
    print("="*40)
    
    if not os.path.exists(IMAGENS_CONTAS_FOLDER):
        print("❌ Pasta de contas não existe!")
        return
    
    arquivos = [f for f in os.listdir(IMAGENS_CONTAS_FOLDER) if f.endswith('.png')]
    
    if not arquivos:
        print("❌ Nenhuma imagem encontrada!")
        return
    
    print("Imagens encontradas:")
    print("-" * 40)
    
    for arquivo in arquivos:
        caminho = os.path.join(IMAGENS_CONTAS_FOLDER, arquivo)
        tamanho = os.path.getsize(caminho)
        
        # Tentar deduzir o nome da conta
        nome_base = arquivo.replace('.png', '')
        
        # Possíveis nomes baseados no arquivo
        possiveis_nomes = []
        
        if nome_base.startswith('conta_'):
            numero = nome_base.replace('conta_', '').replace('_', '-')
            possiveis_nomes.append(f"Conta {numero}")
        
        if nome_base.replace('.', '').replace('_', '').replace('-', '').isdigit():
            # É só número
            numero = nome_base
            possiveis_nomes.append(f"Conta {numero}")
            possiveis_nomes.append(f"{numero}")
        
        print(f"📁 {arquivo:<25} ({tamanho:,} bytes)")
        if possiveis_nomes:
            for nome in possiveis_nomes:
                print(f"   💡 Possível nome na tela: '{nome}'")
        print()

def menu_descobrir():
    """Menu principal"""
    while True:
        print(f"\n{'='*60}")
        print("DESCOBRIDOR DE NOMES DE CONTAS - SICOOB")
        print(f"{'='*60}")
        print("1. 🔍 Analisar imagens existentes")
        print("2. 📸 Capturar e descobrir nomes das contas")
        print("3. 📋 Listar arquivos na pasta")
        print("4. ❌ Sair")
        print(f"{'='*60}")
        
        opcao = input("Escolha (1-4): ").strip()
        
        if opcao == "1":
            analisar_imagens_existentes()
            
        elif opcao == "2":
            descobrir_nome_conta_exato()
            
        elif opcao == "3":
            print(f"\n📁 PASTA: {IMAGENS_CONTAS_FOLDER}")
            if os.path.exists(IMAGENS_CONTAS_FOLDER):
                arquivos = os.listdir(IMAGENS_CONTAS_FOLDER)
                if arquivos:
                    print("-" * 50)
                    for arquivo in sorted(arquivos):
                        if arquivo.endswith(('.png', '.jpg', '.jpeg')):
                            caminho = os.path.join(IMAGENS_CONTAS_FOLDER, arquivo)
                            tamanho = os.path.getsize(caminho)
                            print(f"📄 {arquivo:<30} ({tamanho:,} bytes)")
                else:
                    print("Pasta vazia")
            else:
                print("Pasta não existe")
                
        elif opcao == "4":
            print("👋 Até logo!")
            break
            
        else:
            print("❌ Opção inválida!")
        
        input("\n⏸️  Pressione ENTER para continuar...")

if __name__ == "__main__":
    try:
        menu_descobrir()
    except KeyboardInterrupt:
        print("\n👋 Programa interrompido. Até logo!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        input("Pressione ENTER para sair...")
