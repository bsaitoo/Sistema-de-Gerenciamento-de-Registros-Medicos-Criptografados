import customtkinter as ctk
from pymongo.mongo_client import MongoClient
from bcrypt import hashpw, gensalt, checkpw
from cryptography.fernet import Fernet

def gerar_chave_criptografia():
    return Fernet.generate_key()

chave_secreta = gerar_chave_criptografia()
cipher_suite = Fernet(chave_secreta)

mongo_client = MongoClient("mongodb+srv://paolet:123@cluster0.tj2me.mongodb.net/sistema?retryWrites=true&w=majority")
db = mongo_client["sistema"]

def criptografar(texto):
    return cipher_suite.encrypt(texto.encode()).decode()


def descriptografar(texto_criptografado):
    return cipher_suite.decrypt(texto_criptografado.encode()).decode()


def adicionar_registro():
    id = entry_id.get()
    nomePaciente = criptografar(entry_nomePaciente.get())
    tratamento = criptografar(entry_tratamento.get())
    historico_medico = criptografar(entry_historico_medico.get())

    db["registros"].insert_one({
        "id": id,
        "nomePaciente": nomePaciente,
        "tratamento": tratamento,
        "historico_medico": historico_medico,
    })
    label_resultado.configure(text="Registro adicionado com sucesso!")

def visualizar_paciente():
    id = entry_id.get()
    registros = db["registros"].find_one({"id": id})

    if registros:
        try:
            nome = descriptografar(registros["Nome"])
            tratamento = descriptografar(registros["tratamento"])
            historico_medico = descriptografar(registros["Historico"])
            label_resultado.configure(text=f"nomePaciente: {nome}\ntratamento: {tratamento}\nhistorico_medico: {historico_medico}")
        except:
            label_resultado.configure(text="Erro na descriptografia dos dados.")
    else:
        label_resultado.configure(text="Registro não encontrado.")

def adicionar_medico():
    id_medico = entry_id_medico.get()
    nomeMedico = criptografar(entry_nomeMedico2.get())
    senha = entry_senha.get().encode('utf-8')
    senha_criptografada = hashpw(senha, gensalt())

    db["medicos"].insert_one({
        "IdentificacaoMedica": id_medico,
        "Nome": nomeMedico,
        "Senha": senha_criptografada
    })
    label_resultado.configure(text="Médico adicionado com sucesso!")


app = ctk.CTk()
app.title("Sistema de Gestão Hospitalar")
app.geometry("500x500")

telaRegistro = ctk.CTkFrame(app)
telaMedico = ctk.CTkFrame(app)
telaRegistro.pack(pady=10)
telaMedico.pack(pady=10)

ctk.CTkLabel(telaRegistro, text="Adicionar/Ver Paciente", font=("Arial", 16)).pack(pady=5)
entry_id = ctk.CTkEntry(telaRegistro, placeholder_text="ID do Paciente")
entry_id.pack(pady=5)
entry_nomePaciente = ctk.CTkEntry(telaRegistro, placeholder_text="Nome do Paciente")
entry_nomePaciente.pack(pady=5)
entry_tratamento = ctk.CTkEntry(telaRegistro, placeholder_text="Tratamento")
entry_tratamento.pack(pady=5)
entry_historico_medico = ctk.CTkEntry(telaRegistro, placeholder_text="Histórico Médico")
entry_historico_medico.pack(pady=5)
ctk.CTkButton(telaRegistro, text="Adicionar Registro", command=adicionar_registro).pack(pady=5)
ctk.CTkButton(telaRegistro, text="Ver Registro", command=visualizar_paciente).pack(pady=5)

ctk.CTkLabel(telaMedico, text="Adicionar Médico", font=("Arial", 16)).pack(pady=5)
entry_id_medico = ctk.CTkEntry(telaMedico, placeholder_text="ID do Médico")
entry_id_medico.pack(pady=5)
entry_nomeMedico2 = ctk.CTkEntry(telaMedico, placeholder_text="Nome do Médico")
entry_nomeMedico2.pack(pady=5)
entry_senha = ctk.CTkEntry(telaMedico, placeholder_text="Senha", show="*")
entry_senha.pack(pady=5)
ctk.CTkButton(telaMedico, text="Adicionar Médico", command=adicionar_medico).pack(pady=5)

# Resultado da operação
label_resultado = ctk.CTkLabel(app, text="")
label_resultado.pack(pady=10)

app.mainloop()
