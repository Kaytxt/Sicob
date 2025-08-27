import tkinter as tk
from tkinter import messagebox, simpledialog
import pyautogui
import os
import time
from pathlib import Path
from PIL import Image, ImageTk
import threading

# Caminhos do projeto
BASE_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGENS_BOTOES_FOLDER = os.path.join(BASE_FOLDER, 'img_automacao', 'botoes')

# Lista de botões necessários
BOTOES_NECESSARIOS = [
    {
        "nome": "extrato.jpg",
        "descricao": "Botão 'Extrato' na página da conta",
        "instrucoes": "Acesse uma conta e localize o botão/link 'Extrato' ou 'Consultar Extrato'"
    },
    {
        "nome": "periodo.jpg", 
        "descricao": "Botão 'Período' na página de extrato",
        "instrucoes": "Na página de extrato, localize onde escolher o período (pode ser um calendário ou dropdown)"
    },
    {
        "nome": "exportar-extrato.jpg",
        "descricao": "Botão 'Exportar' ou 'Download' do extrato",
        "instrucoes": "Botão para baixar/exportar o extrato (depois de selecionar o período)"
    },
    {
        "nome": "radio-button-xls.jpg",
        "descricao": "Opção XLS/Excel no formato de export",
        "instrucoes": "Radio button ou checkbox para escolher formato XLS/Excel"
    },
    {
        "nome": "exportar-extrato-final.jpg",
        "descricao": "Botão final de confirmação do export",
        "instrucoes": "Botão final 'Exportar', 'Download', 'Confirmar' para baixar o arquivo"
    },
    {
        "nome": "trocar-conta.jpg",
        "descricao": "Botão para voltar à lista de contas",
        "instrucoes": "Botão 'Voltar', 'Trocar Conta', 'Sair' ou similar para voltar à tela inicial"
    }
]

class CapturaBootoesGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Capturar Botões - Sicoob")
        self.root.geometry("900x700")
        self.root.configure(bg='#2c3e50')
        
        # Garantir que a pasta existe
        Path(IMAGENS_BOTOES_FOLDER).mkdir(parents=True, exist_ok=True)
        
        self.criar_interface()
        
    def criar_interface(self):
        """Cria interface principal"""
        # Título
        titulo = tk.Label(
            self.root,
            text="Capturador de Botões - Sistema Sicoob",
            font=("Arial", 18, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        titulo.pack(pady=20)
        
        # Frame de instruções
        frame_instrucoes = tk.LabelFrame(
            self.root,
            text="Instruções",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        )
        frame_instrucoes.pack(fill="x", padx=20, pady=10)
        
        instrucoes = """
1. Abra o sistema Sicoob no navegador
2. Navegue até encontrar o botão que você quer capturar
3. Clique em "Capturar Tela" aqui
4. Selecione apenas a área do botão
5. A imagem será salva automaticamente
        """
        
        label_instrucoes = tk.Label(
            frame_instrucoes,
            text=instrucoes,
            font=("Arial", 11),
            bg='#34495e',
            fg='#ecf0f1',
            justify='left'
        )
        label_instrucoes.pack(padx=15, pady=15)
        
        # Frame de botões
        frame_botoes_acao = tk.Frame(self.root, bg='#2c3e50')
        frame_botoes_acao.pack(fill="x", padx=20, pady=10)
        
        btn_verificar = tk.Button(
            frame_botoes_acao,
            text="Verificar Botões Existentes",
            command=self.verificar_botoes,
            font=("Arial", 12),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=8
        )
        btn_verificar.pack(side="left", padx=10)
        
        btn_capturar_todos = tk.Button(
            frame_botoes_acao,
            text="Capturar Todos Faltando",
            command=self.capturar_todos_faltando,
            font=("Arial", 12),
            bg='#27ae60',
            fg='white',
            padx=20,
            pady=8
        )
        btn_capturar_todos.pack(side="left", padx=10)
        
        # Lista de botões
        frame_lista = tk.LabelFrame(
            self.root,
            text="Selecionar Botão Individual",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        )
        frame_lista.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Scrollable frame para botões
        canvas_botoes = tk.Canvas(frame_lista, bg='#34495e')
        scrollbar = tk.Scrollbar(frame_lista, orient="vertical", command=canvas_botoes.yview)
        scrollable_frame = tk.Frame(canvas_botoes, bg='#34495e')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas_botoes.configure(scrollregion=canvas_botoes.bbox("all"))
        )
        
        canvas_botoes.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas_botoes.configure(yscrollcommand=scrollbar.set)
        
        # Adicionar botões para cada imagem
        for i, botao in enumerate(BOTOES_NECESSARIOS):
            frame_botao = tk.Frame(scrollable_frame, bg='#34495e')
            frame_botao.pack(fill="x", padx=10, pady=5)
            
            # Status do botão
            caminho = os.path.join(IMAGENS_BOTOES_FOLDER, botao["nome"])
            status_cor = '#27ae60' if os.path.exists(caminho) else '#e74c3c'
            status_texto = 'Existe' if os.path.exists(caminho) else 'Faltando'
            
            status_label = tk.Label(
                frame_botao,
                text=status_texto,
                bg=status_cor,
                fg='white',
                font=("Arial", 9, "bold"),
                width=10
            )
            status_label.pack(side="left", padx=5)
            
            # Nome e descrição
            info_frame = tk.Frame(frame_botao, bg='#34495e')
            info_frame.pack(side="left", fill="x", expand=True, padx=10)
            
            nome_label = tk.Label(
                info_frame,
                text=botao["nome"],
                font=("Arial", 11, "bold"),
                bg='#34495e',
                fg='#ecf0f1',
                anchor="w"
            )
            nome_label.pack(fill="x")
            
            desc_label = tk.Label(
                info_frame,
                text=botao["descricao"],
                font=("Arial", 9),
                bg='#34495e',
                fg='#bdc3c7',
                anchor="w",
                wraplength=400
            )
            desc_label.pack(fill="x")
            
            # Botão de capturar
            btn_capturar = tk.Button(
                frame_botao,
                text="Capturar",
                command=lambda b=botao: self.capturar_botao_individual(b),
                font=("Arial", 10),
                bg='#f39c12',
                fg='white',
                padx=15
            )
            btn_capturar.pack(side="right", padx=5)
        
        canvas_botoes.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Área de status
        self.status_text = tk.Text(
            self.root,
            height=8,
            font=("Courier", 10),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        self.status_text.pack(fill="x", padx=20, pady=(0, 20))
        
        self.log("Sistema iniciado! Verifique os botões ou capture os que estão faltando.")
        
    def log(self, mensagem):
        """Adiciona mensagem ao log"""
        timestamp = time.strftime("%H:%M:%S")
        self.status_text.insert(tk.END, f"[{timestamp}] {mensagem}\n")
        self.status_text.see(tk.END)
        self.root.update()
        
    def verificar_botoes(self):
        """Verifica status de todos os botões"""
        self.log("Verificando status dos botões...")
        
        existentes = 0
        faltando = 0
        
        for botao in BOTOES_NECESSARIOS:
            caminho = os.path.join(IMAGENS_BOTOES_FOLDER, botao["nome"])
            
            if os.path.exists(caminho):
                try:
                    with Image.open(caminho) as img:
                        tamanho = os.path.getsize(caminho)
                        self.log(f"OK: {botao['nome']} - {img.size[0]}x{img.size[1]} ({tamanho} bytes)")
                        existentes += 1
                except Exception as e:
                    self.log(f"ERRO: {botao['nome']} - arquivo corrompido: {e}")
                    faltando += 1
            else:
                self.log(f"FALTANDO: {botao['nome']}")
                faltando += 1
        
        self.log(f"RESUMO: {existentes} existentes, {faltando} faltando")
        
        # Atualizar interface
        self.criar_interface()
        
    def capturar_todos_faltando(self):
        """Captura todos os botões que estão faltando"""
        faltando = []
        
        for botao in BOTOES_NECESSARIOS:
            caminho = os.path.join(IMAGENS_BOTOES_FOLDER, botao["nome"])
            if not os.path.exists(caminho):
                faltando.append(botao)
        
        if not faltando:
            messagebox.showinfo("Sucesso", "Todos os botões já existem!")
            return
        
        self.log(f"Iniciando captura de {len(faltando)} botões faltando...")
        
        for i, botao in enumerate(faltando):
            resposta = messagebox.askyesno(
                f"Capturar {i+1}/{len(faltando)}",
                f"Capturar '{botao['nome']}'?\n\n{botao['descricao']}\n\n{botao['instrucoes']}"
            )
            
            if resposta:
                self.capturar_botao(botao)
            else:
                self.log(f"Pulado: {botao['nome']}")
        
        self.log("Processo de captura concluído!")
        self.verificar_botoes()
        
    def capturar_botao_individual(self, botao_info):
        """Captura um botão específico"""
        resposta = messagebox.askyesno(
            f"Capturar {botao_info['nome']}",
            f"Instruções:\n{botao_info['instrucoes']}\n\nProsseguir com a captura?"
        )
        
        if resposta:
            self.capturar_botao(botao_info)
            self.verificar_botoes()
        
    def capturar_botao(self, botao_info):
        """Realiza a captura do botão"""
        self.log(f"Iniciando captura: {botao_info['nome']}")
        
        # Minimizar janela temporariamente
        self.root.iconify()
        
        # Aguardar posicionamento
        time.sleep(2)
        
        try:
            # Capturar tela
            screenshot = pyautogui.screenshot()
            
            # Restaurar janela
            self.root.deiconify()
            
            # Salvar temporariamente
            temp_path = os.path.join(IMAGENS_BOTOES_FOLDER, "temp_captura.png")
            screenshot.save(temp_path)
            
            self.log("Tela capturada! Abrindo seletor...")
            
            # Abrir seletor
            self.abrir_seletor_area(temp_path, botao_info)
            
        except Exception as e:
            self.log(f"Erro na captura: {e}")
            messagebox.showerror("Erro", f"Erro ao capturar tela: {e}")
    
    def abrir_seletor_area(self, screenshot_path, botao_info):
        """Abre janela para selecionar área"""
        janela_selecao = tk.Toplevel(self.root)
        janela_selecao.title(f"Selecionar área - {botao_info['nome']}")
        janela_selecao.state('zoomed')
        
        # Carregar imagem
        img_original = Image.open(screenshot_path)
        
        # Redimensionar se necessário
        largura_tela = janela_selecao.winfo_screenwidth()
        altura_tela = janela_selecao.winfo_screenheight()
        
        fator_escala = min(
            (largura_tela - 100) / img_original.width,
            (altura_tela - 150) / img_original.height,
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
        
        # Frame de instruções
        frame_instrucoes = tk.Frame(janela_selecao, bg='#34495e', height=80)
        frame_instrucoes.pack(fill="x")
        frame_instrucoes.pack_propagate(False)
        
        label_titulo = tk.Label(
            frame_instrucoes,
            text=f"Capturando: {botao_info['nome']}",
            font=("Arial", 14, "bold"),
            bg='#34495e',
            fg='white'
        )
        label_titulo.pack(pady=(10, 5))
        
        label_instrucoes = tk.Label(
            frame_instrucoes,
            text=f"Clique e arraste para selecionar apenas: {botao_info['descricao']} | ESC=Cancelar",
            font=("Arial", 10),
            bg='#34495e',
            fg='#ecf0f1'
        )
        label_instrucoes.pack()
        
        # Canvas para a imagem
        canvas = tk.Canvas(
            janela_selecao,
            width=img_display.width,
            height=img_display.height,
            bg='white'
        )
        canvas.pack(expand=True, fill='both')
        
        # Mostrar imagem
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.image = photo
        
        # Variáveis de seleção
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
                messagebox.showwarning("Aviso", "Selecione uma área maior!")
                return
                
            try:
                # Ajustar coordenadas
                x1 = int(min(start_x, end_x) / fator_escala)
                y1 = int(min(start_y, end_y) / fator_escala)
                x2 = int(max(start_x, end_x) / fator_escala)
                y2 = int(max(start_y, end_y) / fator_escala)
                
                # Extrair área
                area_selecionada = img_original.crop((x1, y1, x2, y2))
                
                # Salvar
                caminho_final = os.path.join(IMAGENS_BOTOES_FOLDER, botao_info["nome"])
                area_selecionada.save(caminho_final, "JPEG" if botao_info["nome"].endswith('.jpg') else "PNG")
                
                janela_selecao.destroy()
                
                # Log sucesso
                tamanho = os.path.getsize(caminho_final)
                self.log(f"SUCESSO: {botao_info['nome']} salvo - {area_selecionada.size[0]}x{area_selecionada.size[1]} ({tamanho} bytes)")
                
                messagebox.showinfo(
                    "Sucesso!",
                    f"Botão capturado!\n\n{botao_info['nome']}\n{area_selecionada.size[0]}x{area_selecionada.size[1]} pixels"
                )
                
            except Exception as e:
                self.log(f"Erro ao salvar: {e}")
                messagebox.showerror("Erro", f"Erro ao salvar: {e}")
                
        def cancelar():
            janela_selecao.destroy()
            self.log(f"Cancelado: {botao_info['nome']}")
        
        # Eventos
        canvas.bind("<Button-1>", on_mouse_down)
        canvas.bind("<B1-Motion>", on_mouse_drag)
        canvas.bind("<ButtonRelease-1>", on_mouse_up)
        
        janela_selecao.bind("<Escape>", lambda e: cancelar())
        janela_selecao.bind("<Return>", lambda e: salvar_selecao())
        
        # Botões de ação
        frame_botoes = tk.Frame(janela_selecao, bg='#34495e', height=60)
        frame_botoes.pack(fill="x")
        frame_botoes.pack_propagate(False)
        
        btn_salvar = tk.Button(
            frame_botoes,
            text="Salvar Seleção (Enter)",
            command=salvar_selecao,
            font=("Arial", 12),
            bg='#27ae60',
            fg='white',
            padx=30
        )
        btn_salvar.pack(side="left", padx=20, pady=15)
        
        btn_cancelar = tk.Button(
            frame_botoes,
            text="Cancelar (Esc)",
            command=cancelar,
            font=("Arial", 12),
            bg='#e74c3c',
            fg='white',
            padx=30
        )
        btn_cancelar.pack(side="left", padx=10, pady=15)
        
        janela_selecao.focus_set()
        janela_selecao.grab_set()
        
        # Limpeza
        def on_closing():
            if os.path.exists(screenshot_path):
                try:
                    os.remove(screenshot_path)
                except:
                    pass
            janela_selecao.destroy()
            
        janela_selecao.protocol("WM_DELETE_WINDOW", on_closing)
    
    def executar(self):
        """Executa a aplicação"""
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Erro: {e}")

def main():
    """Função principal"""
    print("Capturador de Botões Sicoob - Interface Gráfica")
    print("Abrindo janela...")
    
    try:
        app = CapturaBootoesGUI()
        app.executar()
    except Exception as e:
        print(f"Erro crítico: {e}")
        input("Pressione ENTER para sair...")

if __name__ == "__main__":
    main()