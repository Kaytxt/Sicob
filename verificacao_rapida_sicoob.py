import os
from pathlib import Path
from PIL import Image

def verificacao_rapida_sicoob():
    """
    Verificação rápida do projeto Sicoob - identifica problemas comuns (APENAS PIL)
    """
    print("VERIFICACAO RAPIDA DO PROJETO SICOOB - VERSAO PIL")
    print("="*60)
    
    # Caminhos do projeto
    BASE_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    IMAGENS_CONTAS_FOLDER = os.path.join(BASE_FOLDER, 'img_automacao', 'botoes', 'contas')
    
    # Lista de contas esperadas (ATUALIZADA baseada no log)
    CONTAS_ESPERADAS = [
        "conta_41930-3.png",    # ou conta_41.930-3.png (baseado no log)
        "conta_41932-0.png",    # ou conta_41.932-0.png  
        "conta_53276-2.png",    # ou conta_53.276-2.png
        "conta_81117-3.png"     # ou conta_81.117-3.png (CORRIGIDO)
    ]
    
    # Variações possíveis (baseado no log que mostrou pontos)
    VARIACOES_ESPERADAS = [
        "conta_41.930-3.png", "conta_41930-3.png",
        "conta_41.932-0.png", "conta_41932-0.png", 
        "conta_53.276-2.png", "conta_53276-2.png",
        "conta_81.117-3.png", "conta_81117-3.png"
    ]
    
    problemas = []
    sucessos = []
    
    # 1. Verificar se a pasta existe
    print("1. Verificando pasta de imagens das contas...")
    if not os.path.exists(IMAGENS_CONTAS_FOLDER):
        problema = f"PROBLEMA CRITICO: Pasta nao existe: {IMAGENS_CONTAS_FOLDER}"
        print(problema)
        problemas.append(problema)
        
        # Tentar criar a pasta
        try:
            Path(IMAGENS_CONTAS_FOLDER).mkdir(parents=True, exist_ok=True)
            print(f"   Pasta criada automaticamente!")
        except Exception as e:
            print(f"   Erro ao criar pasta: {e}")
            
        return problemas, sucessos
    else:
        print(f"   Pasta existe: {IMAGENS_CONTAS_FOLDER}")
    
    # 2. Verificar arquivos - primeiro as variações do log
    print("\n2. Verificando arquivos de imagem das contas...")
    
    contas_encontradas = set()
    
    # Primeiro verificar se existem as variações do log (com pontos)
    for variacao in VARIACOES_ESPERADAS:
        caminho_completo = os.path.join(IMAGENS_CONTAS_FOLDER, variacao)
        
        if os.path.exists(caminho_completo):
            try:
                with Image.open(caminho_completo) as img:
                    tamanho = os.path.getsize(caminho_completo)
                    sucesso = f"OK: {variacao} - {img.size[0]}x{img.size[1]} ({tamanho} bytes)"
                    print(f"   {sucesso}")
                    sucessos.append(sucesso)
                    
                    # Marcar qual conta foi encontrada
                    if "41930" in variacao or "41.930" in variacao:
                        contas_encontradas.add("41930-3")
                    elif "41932" in variacao or "41.932" in variacao:
                        contas_encontradas.add("41932-0")
                    elif "53276" in variacao or "53.276" in variacao:
                        contas_encontradas.add("53276-2")
                    elif "81117" in variacao or "81.117" in variacao:
                        contas_encontradas.add("81117-3")
                        
            except Exception as e:
                problema = f"ARQUIVO CORROMPIDO: {variacao} - {str(e)}"
                print(f"   {problema}")
                problemas.append(problema)
    
    # Verificar quais contas ainda faltam
    contas_necessarias = ["41930-3", "41932-0", "53276-2", "81117-3"]
    contas_faltando = []
    
    for conta in contas_necessarias:
        if conta not in contas_encontradas:
            contas_faltando.append(conta)
            problema = f"CONTA FALTANDO: {conta} (nenhuma variacao encontrada)"
            print(f"   {problema}")
            problemas.append(problema)
    
    # 3. Verificar arquivos extras ou com nomes diferentes
    print("\n3. Verificando arquivos extras...")
    if os.path.exists(IMAGENS_CONTAS_FOLDER):
        arquivos_encontrados = [f for f in os.listdir(IMAGENS_CONTAS_FOLDER) if f.endswith('.png')]
        
        # Filtrar arquivos que não são variações conhecidas
        arquivos_extras = []
        for arquivo in arquivos_encontrados:
            if arquivo not in VARIACOES_ESPERADAS:
                arquivos_extras.append(arquivo)
        
        if arquivos_extras:
            print("   Arquivos extras encontrados:")
            for arquivo in arquivos_extras:
                print(f"      {arquivo}")
                # Verificar se pode ser útil
                for conta_faltando in contas_faltando:
                    numero_limpo = conta_faltando.replace('-', '').replace('_', '')
                    if numero_limpo in arquivo.replace('-', '').replace('_', '').replace('.', ''):
                        print(f"         Possivel arquivo para conta {conta_faltando}")
        else:
            print("   Nenhum arquivo extra encontrado")
    
    # 4. RESUMO E SOLUÇÕES ESPECÍFICAS
    print("\n" + "="*60)
    print("RESUMO DA VERIFICACAO")
    print("="*60)
    
    print(f"Contas encontradas: {len(contas_encontradas)}/4")
    print(f"Problemas: {len(problemas)}")
    
    if problemas:
        print(f"\nPROBLEMAS ENCONTRADOS:")
        for problema in problemas:
            print(f"   {problema}")
        
        print(f"\nSOLUCOES ESPECIFICAS:")
        
        if contas_faltando:
            print(f"   1. IMAGENS FALTANDO: Execute 'descobrir_contas_tkinter.py'")
            print(f"      para capturar as contas: {', '.join(contas_faltando)}")
        
        print(f"   2. BOTOES FALTANDO: Execute 'capturar_botoes_tkinter.py'")
        print(f"      especialmente o 'extrato.jpg' que causou erro")
        
        print(f"   3. TESTE: Use 'baixar_extratos_pil_only.py' opcao 2")
        print(f"      para testar uma conta especifica primeiro")
        
        print(f"\nTODOS OS SCRIPTS AGORA USAM APENAS PIL + TKINTER!")
        
    else:
        print(f"\nPARABENS! Projeto configurado corretamente!")
        print(f"   Execute 'baixar_extratos_pil_only.py' opcao 3 para automacao completa")
    
    print("\n" + "="*60)
    
    return problemas, sucessos

def resolver_problema_especifico_conta_41930():
    """
    Solução específica para o erro da conta 41930-3 (APENAS PIL)
    """
    print("\nVERIFICACAO ESPECIFICA - CONTA 41930-3")
    print("-"*50)
    
    BASE_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    IMAGENS_CONTAS_FOLDER = os.path.join(BASE_FOLDER, 'img_automacao', 'botoes', 'contas')
    
    # Baseado no log, pode ser com pontos
    arquivos_possiveis = [
        "conta_41930-3.png",
        "conta_41.930-3.png",  # Baseado no log
        "conta_41930_3.png",
        "41930-3.png"
    ]
    
    print(f"Verificando conta 41930-3...")
    print(f"Pasta: {IMAGENS_CONTAS_FOLDER}")
    
    arquivo_encontrado = None
    
    for arquivo in arquivos_possiveis:
        caminho = os.path.join(IMAGENS_CONTAS_FOLDER, arquivo)
        print(f"Testando: {arquivo}")
        
        if os.path.exists(caminho):
            print(f"   Arquivo existe!")
            
            # Verificar permissões
            if os.access(caminho, os.R_OK):
                print(f"   Pode ser lido")
            else:
                print(f"   SEM PERMISSAO para ler")
                continue
            
            # Verificar tamanho
            tamanho = os.path.getsize(caminho)
            print(f"   Tamanho: {tamanho} bytes")
            
            if tamanho == 0:
                print(f"   PROBLEMA: Arquivo vazio!")
                continue
            elif tamanho < 100:
                print(f"   SUSPEITO: Muito pequeno")
            
            # Tentar carregar com PIL
            try:
                with Image.open(caminho) as img:
                    print(f"   PIL carregou OK! Dimensoes: {img.size}")
                    arquivo_encontrado = arquivo
                    break
            except Exception as e:
                print(f"   ERRO ao carregar com PIL: {e}")
        else:
            print(f"   Nao existe")
    
    if arquivo_encontrado:
        print(f"\nSUCESSO: Encontrada imagem valida: {arquivo_encontrado}")
        print(f"O problema pode ser no script principal ou nos botoes")
        
        print(f"\nPROXIMOS PASSOS:")
        print(f"1. Verifique se botoes existem: execute 'capturar_botoes_tkinter.py'")
        print(f"2. Teste script principal: 'baixar_extratos_pil_only.py' opcao 2")
        
    else:
        print(f"\nNENHUMA IMAGEM VALIDA ENCONTRADA!")
        
        # Verificar arquivos similares
        if os.path.exists(IMAGENS_CONTAS_FOLDER):
            print(f"\nArquivos na pasta:")
            for arquivo in os.listdir(IMAGENS_CONTAS_FOLDER):
                if arquivo.endswith('.png'):
                    if '41930' in arquivo or '930' in arquivo:
                        print(f"   SIMILAR: {arquivo}")
                    else:
                        print(f"   {arquivo}")
        
        print(f"\nSOLUCAO:")
        print(f"1. Execute 'descobrir_contas_tkinter.py'")
        print(f"2. Capture a imagem da conta 41930-3")
        print(f"3. Digite o nome EXATO como aparece na tela")

def main():
    """
    Função principal
    """
    try:
        problemas, sucessos = verificacao_rapida_sicoob()
        
        # Verificação específica para o erro reportado
        if any("conta_41930-3.png" in p for p in problemas):
            resolver_problema_especifico_conta_41930()
        
        print(f"\n🏁 Verificação concluída!")
        
        if problemas:
            print(f"⚠️  Encontrados {len(problemas)} problema(s) que precisam ser resolvidos")
        else:
            print(f"🎉 Projeto está funcionando perfeitamente!")
            
    except Exception as e:
        print(f"\n❌ Erro durante verificação: {e}")
    
    input(f"\n⏸️  Pressione ENTER para sair...")

if __name__ == "__main__":
    main()
