import os
import re
import shutil
from tkinter import Tk, filedialog, Button, Text, Scrollbar
from datetime import datetime

def search_keywords_in_filename(filename):
    # Lista de palavras-chave adicionais
    keywords = ['unica', 'sup', 'suplementos', 'doemgexec', 'doemgpubterc', 'admin', 'admsup', 'doemganx', 'doemgmuniminei']
    # Verifica se o nome do arquivo contém alguma das palavras-chave, independentemente da formatação
    for keyword in keywords:
        if keyword in filename.lower():
            return keyword
    return None


def extract_date_from_filename(filename):
    match = re.search(r'\b\d{8}\b', filename)  # Procura por uma sequência de 8 dígitos (yyyymmdd) no nome do arquivo
    if match:
        return match.group()
    else:
        return None


def get_month_from_date(date_string):
    date = datetime.strptime(date_string, '%Y%m%d')
    month = date.strftime('%B').lower()  # Obtém o nome do mês em minúsculo
    # Mapeia os nomes dos meses para o português
    month_names = {
        'january': 'janeiro',
        'february': 'fevereiro',
        'march': 'março',
        'april': 'abril',
        'may': 'maio',
        'june': 'junho',
        'july': 'julho',
        'august': 'agosto',
        'september': 'setembro',
        'october': 'outubro',
        'november': 'novembro',
        'december': 'dezembro'
    }
    return month_names[month]


def create_month_directory(month_directory, date):
    if not os.path.exists(month_directory):
        os.makedirs(month_directory)
        return month_directory
    else:
        return None


def select_pdf_files_manually():
    root = Tk()
    root.withdraw()  # Esconde a janela principal
    file_paths = filedialog.askopenfilenames(title="Selecione os arquivos PDF para processar")
    root.destroy()  # Fecha a janela após a seleção
    return file_paths


def display_message(message):
    text_area.insert("end", message + "\n")
    text_area.see("end")  # Mantém a área de texto rolando automaticamente


def move_selected_files():
    selected_files = select_pdf_files_manually()
    if selected_files:
        process_selected_files(selected_files)
    else:
        display_message("Nenhum arquivo selecionado.")
    display_message("Processo concluído.")


def process_selected_files(files):
    for file_path in files:
        if file_path.lower().endswith('.pdf'):
            filename = os.path.basename(file_path)
            date = extract_date_from_filename(filename)
            if date:
                month = get_month_from_date(date)
                keyword = search_keywords_in_filename(filename)
                base_directory = None

                # Verifica o nome do arquivo e atribui o diretório base correspondente
                if "DEOAB unica" in filename:
                    base_directory = r"F:\Work\Diarios\DF\Diário Ordem dos Advogados do Brasil\Unica\2025"
                elif "DOEAC Unica" in filename:
                    base_directory = r"F:\Work\Diarios\AC\Diário Oficial do Acre\Unica\2025"
                elif "DOEALUnica" in filename:
                    base_directory = r"F:\Work\Diarios\AL\Diário Oficial de Alagoas\Unica\2025"
                elif "doees unica" in filename:
                    base_directory = r"F:\Work\Diarios\ES\Diário Oficial do Espírito Santo\Secoes\2025"
                elif "DOEMG doemgexec" in filename or "DOEMG doemgpubterc" in filename:
                    base_directory = r"F:\Work\Diarios\MG\Diário Oficial de Minas Gerais\Cadernos\2025"
                elif "doemg doemganx" in filename.lower():
                    base_directory = r"F:\Work\Diarios\MG\Diário Oficial de Minas Gerais\Cadernos\2025"
                elif "doemg doemgmuniminei" in filename.lower():
                    base_directory = r"F:\Work\Diarios\MG\Diário Oficial de Minas Gerais\Cadernos\2025"
                elif "DOEPI SUP - doepisup" in filename:
                    base_directory = r"F:\Work\Diarios\PI\Diário Oficial do Piauí\Cadernos\2025"
                    keyword = "doepisup"
                elif "DOEPI Unica" in filename:
                    base_directory = r"F:\Work\Diarios\PI\Diário Oficial do Piauí\Cadernos\2025"
                elif "DOESC unica" in filename:
                    base_directory = r"F:\Work\Diarios\SC\Diário Oficial de Santa Catarina\Unica\2025"
                elif "doescsup" in filename:
                    base_directory = r"F:\Work\Diarios\SC\Diário Oficial de Santa Catarina\Unica\2025"
                    keyword = "doescsup"
                elif "doeto Unica" in filename:
                    base_directory = r"F:\Work\Diarios\TO\Diário Oficial do Tocantins\Unica\2025"
                elif "TCEAM unica" in filename:
                    base_directory = r"F:\Work\Diarios\AM\Diário do Tribunal de Contas do Amazonas\Unica\2025"
                elif "TCECE Unica" in filename:
                    base_directory = r"F:\Work\Diarios\CE\Diário do Tribunal de Contas do Ceará\Unica\2025"
                elif "TRF4 trf4admin" in filename:
                    base_directory = r"F:\Work\Diarios\DF\Diário do TRF4\Cadernos\2025"
                    keyword = "trf4admin"
                elif "TRF4 trf4admsup" in filename:
                    base_directory = r"F:\Work\Diarios\DF\Diário do TRF4\Cadernos\2025"
                    keyword = "trf4admsup"
                elif "TRF4 trf4jud" in filename:
                    base_directory = r"F:\Work\Diarios\DF\Diário do TRF4\Cadernos\2025"
                    keyword = "trf4jud"
                # Adicione mais condições para outros diretórios aqui
                if base_directory:
                    if keyword:
                        # Cria a pasta com a data e move o arquivo para dentro dela
                        destination_directory = os.path.join(base_directory, month, keyword, date)
                        os.makedirs(destination_directory, exist_ok=True)
                        destination_file_path = os.path.join(destination_directory, filename)
                        # Verifica se o arquivo já existe na pasta de destino antes de mover
                        if not os.path.exists(destination_file_path):
                            shutil.move(file_path, destination_file_path)
                            display_message(
                                f"Arquivo '{filename}' movido com sucesso para '{destination_directory}'.")
                        else:
                            display_message(
                                f"O arquivo '{filename}' já existe na pasta de destino. Ignorando.")
                    else:
                        display_message(
                            f"Arquivo '{filename}' não contém as palavras-chave. Ignorando.")
                else:
                    display_message(f"Diretório base não encontrado para o arquivo '{filename}'. Ignorando.")
            else:
                display_message(f"Data não encontrada no nome do arquivo '{filename}'. Ignorando.")
        else:
            display_message(f"Arquivo '{file_path}' não é um arquivo PDF. Ignorando.")


# Criar a janela principal
root = Tk()
root.title("Selecionar e Mover Arquivos")

# Botão para selecionar arquivos
select_button = Button(root, text="Selecionar Arquivos", command=move_selected_files)
select_button.pack(pady=10)

# Área de texto para exibir mensagens
text_area = Text(root, height=10, width=50)
text_area.pack(padx=10, pady=10)

# Adicionar barra de rolagem à área de texto
scrollbar = Scrollbar(root, command=text_area.yview)
scrollbar.pack(side="right", fill="y")
text_area.config(yscrollcommand=scrollbar.set)

# Executar o loop principal da janela
root.mainloop()
