import threading
import customtkinter as ctk
from Wall_E import main
from PIL import Image, ImageTk, ImageDraw, ImageFont

# Configurações iniciais do customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Constantes
WINDOW_WIDTH = 750
WINDOW_HEIGHT = 450
IMG_WIDTH = 500
IMG_HEIGHT = 800
FONT_LARGE = ("Arial", 24, "bold")
FONT_MEDIUM = ("Arial", 20)
FONT_SMALL = ("Arial", 14)
FONT_TINY = ("Arial", 10)
IMG_PATH = "Wall-E.jpg"
WATERMARK_TEXT = "WALL-E"
WATERMARK_FONT_SIZE = 36
WATERMARK_FONT_PATH = "arial.ttf"

# Função que será executada ao pressionar o botão
def executar_funcao(email, senha):
    instancia = main(email, senha)
    instancia.login()
    instancia.executa_cadastro()

# Função para iniciar o loop em uma thread separada e fechar a janela
def iniciar_loop():
    email = email_entry.get()
    senha = senha_entry.get()
    print(f"Iniciando thread com Email={email}, Senha={senha}")  # Mensagem de depuração
    thread = threading.Thread(target=executar_funcao, args=(email, senha))
    thread.start()
    janela.destroy()

# Função para carregar e processar a imagem
def carregar_imagem(caminho):
    img = Image.open(caminho)
    img = img.resize((IMG_WIDTH, IMG_HEIGHT), Image.BILINEAR)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(WATERMARK_FONT_PATH, WATERMARK_FONT_SIZE)
    draw.text((10, 10), WATERMARK_TEXT, fill="white", font=font)
    return ImageTk.PhotoImage(img)

# Configuração da janela principal
janela = ctk.CTk()
janela.title("WALL-E")
janela.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
janela.resizable(False, False)

# Frame principal para organizar os elementos
main_frame = ctk.CTkFrame(janela, corner_radius=10)
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Carregamento e exibição da imagem do robô
photo = carregar_imagem(IMG_PATH)
robot_image = ctk.CTkLabel(main_frame, image=photo, text="")  # Defina o texto como vazio
robot_image.image = photo  # Mantém uma referência para evitar a coleta de lixo
robot_image.pack(side="left", padx=(0, 20))

# Título
titulo = ctk.CTkLabel(main_frame, text="Acesse o sistema\n", font=FONT_LARGE)
titulo.pack(pady=10, padx=20, fill="x")

# Frame para o campo de email (CPF)
email_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color=None)
email_frame.pack(pady=10, padx=20, fill="x")

email_icon = ctk.CTkLabel(email_frame, text="👤", font=FONT_MEDIUM)
email_icon.grid(row=0, column=0, padx=(0, 10))

email_entry = ctk.CTkEntry(email_frame, placeholder_text='Digite seu CPF', font=FONT_SMALL, width=287, corner_radius=5)
email_entry.grid(row=0, column=1, sticky="ew")

# Frame para o campo de senha
senha_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color=None)
senha_frame.pack(pady=20, padx=20, fill="x")

senha_icon = ctk.CTkLabel(senha_frame, text="🔒", font=FONT_MEDIUM)
senha_icon.grid(row=0, column=0, padx=(0, 10))

senha_entry = ctk.CTkEntry(senha_frame, placeholder_text='Digite sua senha', show="*", font=FONT_SMALL, width=287, corner_radius=5)
senha_entry.grid(row=0, column=1, sticky="ew")

# Botão para iniciar o loop de verificação de e-mails
botao = ctk.CTkButton(main_frame, text="Entrar", command=iniciar_loop, font=("Arial", 16, "bold"), width=200)
botao.pack(pady=20, padx=(20, 0))

# Informações adicionais próximas ao botão
rodape_texto = (
    "Automatização de Cadastro - Wall-E\n"
    "Versão do Sistema: 1.0.0\n\n"
    "Descrição: Desenvolvido para agilizar o processo de cadastro de colaboradores. Aumentando a eficiência e reduzindo o tempo gasto em tarefas administrativas.\n\n"
    "Data da última atualização em: 31/05/2024\n\n"
)

rodape = ctk.CTkLabel(main_frame, text=rodape_texto, font=FONT_TINY, justify="left", wraplength=300)
rodape.pack(pady=20, padx=(20, 0), fill="both", expand=True)

# Inicia o loop da aplicação
janela.mainloop()
