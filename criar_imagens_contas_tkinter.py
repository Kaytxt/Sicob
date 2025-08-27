import pyautogui
import os
import time
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import threading
from pathlib import Path

# Caminhos do projeto
BASE_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGENS_CONTAS_FOLDER = os.path.join(BASE_FOLDER, 'img_automacao', 'botoes', 'contas')

# Lista das contas
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

class CapturaImagemGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏦 Captura de Imagens das Contas - Sicoob")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Variáveis
        self.screenshot = None
        self.imagem_selecionada = None
        self.coordenadas = None
        
        # Garantir que a pasta existe
        Path(IMAGENS_CONTAS_FOLDER).mkdir(parents=True, exist_ok=True)
        
        self.criar_interface()
        
    def criar_interface(self):
        """Cria a interface principal"""
        # Título
        titulo = tk.Label(
            self.root, 
            text="🏦 Criador de Imagens das Contas Sicoob", 
            font=("Arial", 16, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        titulo.pack(pady=20)
        
        # Frame de instruções
        frame_instrucoes = tk.LabelFrame(
            self.root, 
            text="📋 Instruções",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            fg='#34495e'
        )
        frame_instrucoes.pack(fill="x", padx=20, pady=10)
        
        instrucoes_texto = """
1. 🖥️  Abra o sistema Sicoob no navegador
2. 🏦 Navegue até a tela que mostra a lista das contas  
3. 👀 Deixe a conta visível na tela (sem clicar em nada)
4. 📸 Clique em "Capturar Tela" aqui neste programa
5. ✂️  Selecione apenas a área do texto da conta
6. 💾 A imagem será salva automaticamente
        """
        
        instrucoes_label = tk.Label(
            frame_instrucoes,
            text=instrucoes_texto,
            font=("Arial", 10),
            bg='#f0f0f0',
            fg='#2c3e50',
            justify='left'
        )
        instrucoes_label.pack(padx=10, pady=10)
        
        # Frame de seleção de conta
        frame_contas = tk.LabelFrame(
            self.root,
            text="🏪 Selecionar Conta",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            fg='#34495e'
        )
        frame_contas.pack(fill="x", padx=20, pady=10)
        
        # Lista de contas
        self.conta_var = tk.StringVar()
        self.conta_var.set(CONTAS[0]["nome_na_tela"])  # Valor padrão
        
        for i, conta in enumerate(CONTAS):
            rb = tk.Radiobutton(
                frame_contas,
                text=f"{conta['nome_na_tela']} ({conta['nome_empresa']})",
                variable=self.conta_var,
                value=conta["nome_na_tela"],
                font=("Arial", 10),
                bg='#f0f0f0',
                fg='#2c3e50',
                wraplength=700
            )
            rb.pack(anchor="w", padx=10, pady=2)
        
        # Frame de botões
        frame_botoes = tk.Frame(self.root, bg='#f0f0f0')
        frame_botoes.pack(fill="x", padx=20, pady=20)
        
        # Botão verificar
        btn_verificar = tk.Button(
            frame_botoes,
            text="🔍 Verificar Imagens Existentes",
            command=self.verificar_imagens,
            font=("Arial", 12),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=10
        )
        btn_verificar.pack(side="left", padx=10)
        
        # Botão capturar
        btn_capturar = tk.Button(
            frame_botoes,
            text="📸 Capturar Tela",
            command=self.iniciar_captura,
            font=("Arial", 12),
            bg='#27ae60',
            fg='white',
            padx=20,
            pady=10
        )
        btn_capturar.pack(side="left", padx=10)
        
        # Botão sair
        btn_sair = tk.Button(
            frame_botoes,
            text="❌ Sair",
            command=self.root.quit,
            font=("Arial", 12),
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=10
        )
        btn_sair.pack(side="right", padx=10)
        
        # Área de status
        self.status_text = tk.Text(
            self.root,
            height=8,
            font=("Courier", 10),
            bg='#2c3e50',
            fg='#ecf0f1',
            wrap=tk.WORD
        )
        self.status_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Scrollbar para o status
        scrollbar = tk.Scrollbar(self.status_text)
        scrollbar.pack(side="right", fill="y")
        self.status_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.status_text.yview)
        
        self.log("🚀 Sistema iniciado! Selecione uma conta e siga as instruções.")
        
    def log(self, mensagem):
        """Adiciona mensagem ao log de status"""
        timestamp = time.strftime("%H:%M:%S")
        self.status_text.insert(tk.END, f"[{timestamp}] {mensagem}\n")
        self.status_text.see(tk.END)
        self.root.update()
        
    def verificar_imagens(self):
        """Verifica quais imagens já existem"""
        self.log("🔍 Verificando imagens existentes...")
        
        existentes = 0
        faltando = 0
        
        for conta in CONTAS:
            image_name = conta["nome_na_tela"].replace("Conta ", "conta_").lower() + ".png"
            caminho_completo = os.path.join(IMAGENS_CONTAS_FOLDER, image_name)
            
            if os.path.exists(caminho_completo):
                try:
                    # Verifica se pode abrir a imagem
                    with Image.open(caminho_completo) as img:
                        tamanho = os.path.getsize(caminho_completo)
                        self.log(f"✅ {image_name} - {img.size[0]}x{img.size[1]} ({tamanho} bytes)")
                        existentes += 1
                except Exception as e:
                    self.log(f"⚠️  {image_name} - Arquivo corrompido: {e}")
                    faltando += 1
            else:
                self.log(f"❌ {image_name} - Não existe")
                faltando += 1
        
        self.log(f"📊 Resumo: {existentes} existentes, {faltando} faltando")
        
    def iniciar_captura(self):
        """Inicia o processo de captura"""
        conta_selecionada = self.conta_var.get()
        conta_info = next(c for c in CONTAS if c["nome_na_tela"] == conta_selecionada)
        
        self.log(f"📸 Iniciando captura para: {conta_selecionada}")
        self.log("🎯 Posicione a janela do Sicoob com a conta visível...")
        
        # Minimizar esta janela temporariamente
        self.root.iconify()
        
        # Aguardar um pouco
        self.root.after(2000, lambda: self.capturar_tela(conta_info))
        
    def capturar_tela(self, conta_info):
        """Captura a tela e abre janela de seleção"""
        try:
            self.log("📸 Capturando tela...")
            
            # Capturar tela
            screenshot = pyautogui.screenshot()
            
            # Restaurar janela principal
            self.root.deiconify()
            
            # Salvar screenshot temporário
            temp_path = os.path.join(IMAGENS_CONTAS_FOLDER, "temp_screenshot.png")
            screenshot.save(temp_path)
            
            self.log("✅ Tela capturada! Abrindo seletor de área...")
            
            # Abrir janela de seleção de área
            self.abrir_seletor_area(temp_path, conta_info)
            
        except Exception as e:
            self.log(f"❌ Erro na captura: {e}")
            messagebox.showerror("Erro", f"Erro ao capturar tela: {e}")
            
    def abrir_seletor_area(self, screenshot_path, conta_info):
        """Abre janela para selecionar área da imagem"""
        janela_selecao = tk.Toplevel(self.root)
        janela_selecao.title(f"Selecionar área - {conta_info['nome_na_tela']}")
        janela_selecao.state('zoomed')  # Maximizar no Windows
        
        # Carregar imagem
        img_original = Image.open(screenshot_path)
        
        # Redimensionar se necessário (para caber na tela)
        largura_tela = janela_selecao.winfo_screenwidth()
        altura_tela = janela_selecao.winfo_screenheight()
        
        fator_escala = min(
            (largura_tela - 100) / img_original.width,
            (altura_tela - 100) / img_original.height,
            1.0
        )
        
        if fator_escala < 1.0:
            nova_largura = int(img_original.width * fator_escala)
            nova_altura = int(img_original.height * fator_escala)
            img_display = img_original.resize((nova_largura, nova_altura), Image.Resampling.LANCZOS)
        else:
            img_display = img_original
            fator_escala = 1.0
        
        # Converter para PhotoImage
        photo = ImageTk.PhotoImage(img_display)
        
        # Frame para instruções
        frame_instrucoes = tk.Frame(janela_selecao, bg='#34495e', height=60)
        frame_instrucoes.pack(fill="x")
        frame_instrucoes.pack_propagate(False)
        
        label_instrucoes = tk.Label(
            frame_instrucoes,
            text=f"🎯 Clique e arraste para selecionar apenas o texto: '{conta_info['nome_na_tela']}' | Pressione ESC para cancelar",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='white'
        )
        label_instrucoes.pack(expand=True)
        
        # Canvas para a imagem
        canvas = tk.Canvas(
            janela_selecao,
            width=img_display.width,
            height=img_display.height,
            bg='white'
        )
        canvas.pack(expand=True, fill='both')
        
        # Mostrar imagem no canvas
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.image = photo  # Manter referência
        
        # Variáveis para seleção
        start_x = start_y = end_x = end_y = 0
        rect_id = None
        
        def on_mouse_down(event):
            nonlocal start_x, start_y, rect_id
            start_x, start_y = event.x, event.y
            if rect_id:
                canvas.delete(rect_id)
                
        def on_mouse_drag(event):
            nonlocal rect_id, end_x, end_y
            end_x, end_y = event.x, event.y
            if rect_id:
                canvas.delete(rect_id)
            rect_id = canvas.create_rectangle(
                start_x, start_y, end_x, end_y,
                outline='red', width=3
            )
            
        def on_mouse_up(event):
            nonlocal end_x, end_y
            end_x, end_y = event.x, event.y
            
        def salvar_selecao():
            nonlocal start_x, start_y, end_x, end_y
            
            if abs(end_x - start_x) < 10 or abs(end_y - start_y) < 10:
                messagebox.showwarning("Aviso", "Por favor, selecione uma área maior!")
                return
                
            try:
                # Ajustar coordenadas para a imagem original
                x1 = int(min(start_x, end_x) / fator_escala)
                y1 = int(min(start_y, end_y) / fator_escala)
                x2 = int(max(start_x, end_x) / fator_escala)
                y2 = int(max(start_y, end_y) / fator_escala)
                
                # Extrair área selecionada
                area_selecionada = img_original.crop((x1, y1, x2, y2))
                
                # Salvar imagem
                image_name = conta_info["nome_na_tela"].replace("Conta ", "conta_").lower() + ".png"
                caminho_final = os.path.join(IMAGENS_CONTAS_FOLDER, image_name)
                
                area_selecionada.save(caminho_final, "PNG")
                
                janela_selecao.destroy()
                
                # Log de sucesso
                tamanho = os.path.getsize(caminho_final)
                self.log(f"✅ Imagem salva: {image_name}")
                self.log(f"   📏 Dimensões: {area_selecionada.size[0]}x{area_selecionada.size[1]}")
                self.log(f"   💾 Tamanho: {tamanho} bytes")
                self.log(f"   📁 Local: {caminho_final}")
                
                messagebox.showinfo(
                    "Sucesso!",
                    f"Imagem capturada e salva com sucesso!\n\n"
                    f"Arquivo: {image_name}\n"
                    f"Dimensões: {area_selecionada.size[0]}x{area_selecionada.size[1]}\n"
                    f"Tamanho: {tamanho} bytes"
                )
                
            except Exception as e:
                self.log(f"❌ Erro ao salvar: {e}")
                messagebox.showerror("Erro", f"Erro ao salvar imagem: {e}")
                
        def cancelar():
            janela_selecao.destroy()
            self.log("❌ Captura cancelada pelo usuário")
        
        # Bind dos eventos
        canvas.bind("<Button-1>", on_mouse_down)
        canvas.bind("<B1-Motion>", on_mouse_drag)
        canvas.bind("<ButtonRelease-1>", on_mouse_up)
        
        # Bind das teclas
        janela_selecao.bind("<Escape>", lambda e: cancelar())
        janela_selecao.bind("<Return>", lambda e: salvar_selecao())
        
        # Frame de botões
        frame_botoes = tk.Frame(janela_selecao, bg='#34495e', height=50)
        frame_botoes.pack(fill="x")
        frame_botoes.pack_propagate(False)
        
        btn_salvar = tk.Button(
            frame_botoes,
            text="✅ Salvar Seleção (Enter)",
            command=salvar_selecao,
            font=("Arial", 11),
            bg='#27ae60',
            fg='white',
            padx=20
        )
        btn_salvar.pack(side="left", padx=20, pady=10)
        
        btn_cancelar = tk.Button(
            frame_botoes,
            text="❌ Cancelar (Esc)",
            command=cancelar,
            font=("Arial", 11),
            bg='#e74c3c',
            fg='white',
            padx=20
        )
        btn_cancelar.pack(side="left", padx=10, pady=10)
        
        # Focar na janela
        janela_selecao.focus_set()
        janela_selecao.grab_set()
        
        # Limpar arquivo temporário quando a janela for fechada
        def on_closing():
            if os.path.exists(screenshot_path):
                try:
                    os.remove(screenshot_path)
                except:
                    pass
            janela_selecao.destroy()
            
        janela_selecao.protocol("WM_DELETE_WINDOW", on_closing)
        
    def executar(self):
        """Executa a interface"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.log("👋 Programa interrompido pelo usuário")
        except Exception as e:
            self.log(f"❌ Erro inesperado: {e}")

def main():
    """Função principal"""
    print("🏦 CRIADOR DE IMAGENS DE CONTAS SICOOB")
    print("="*50)
    print("🚀 Iniciando interface gráfica...")
    print("💡 Use a interface gráfica que irá abrir!")
    print()
    
    try:
        app = CapturaImagemGUI()
        app.executar()
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        input("⏸️  Pressione ENTER para sair...")

if __name__ == "__main__":
    main()
