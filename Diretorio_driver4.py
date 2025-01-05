import os
import re
import shutil
from tkinter import Tk, filedialog, Button, Text, Scrollbar
from datetime import datetime

def search_keywords_in_filename(filename):
    normalized_filename = filename.lower().replace(' ', '').replace('_', '').replace('-', '')
    if 'unica' in normalized_filename:
        return 'unica'
    elif 'sup' in normalized_filename:
        return 'sup'
    else:
        return None

def extract_date_from_filename(filename):
    match = re.search(r'\b\d{8}\b', filename)
    if match:
        return match.group()
    else:
        return None

def get_month_from_date(date_string):
    date = datetime.strptime(date_string, '%Y%m%d')
    month = date.strftime('%B').lower()
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

def create_month_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def select_pdf_files_manually():
    root = Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(title="Selecione os arquivos PDF para processar")
    root.destroy()
    return file_paths

def display_message(message):
    text_area.insert("end", message + "\n")
    text_area.see("end")

def move_selected_files():
    selected_files = select_pdf_files_manually()
    if selected_files:
        process_selected_files(selected_files)
    else:
        display_message("Nenhum arquivo selecionado.")

def process_selected_files(files):
    for file_path in files:
        if file_path.lower().endswith('.pdf'):
            filename = os.path.basename(file_path)
            date = extract_date_from_filename(filename)
            if date:
                month = get_month_from_date(date)
                year = date[:4]  # Extrair o ano da data no formato YYYYMMDD
                keyword = search_keywords_in_filename(filename)

                # Definir os diretórios base de forma dinâmica com o ano extraído
                if "TCEMG" in filename.upper():
                    base_directory = fr"F:\Work\Diarios\MG\Diário do Tribunal de Contas de Minas Gerais\Unica\{year}"
                elif "TCEPI" in filename.upper():
                    base_directory = fr"F:\Work\Diarios\PI\Diário do Tribunal de Contas do Piauí\Unica\{year}"
                elif "TCETO" in filename.upper():
                    base_directory = fr"F:\\Work\\Diarios\\TO\\Diário do Tribunal de Contas do Tocantins\\Unica\\{year}"
                elif "DOEPB" in filename.upper():
                    base_directory = fr"F:\\Work\\Diarios\\PB\\Diário Oficial da Paraíba\\Cadernos\\{year}"

                if base_directory:
                    # Garantir que o diretório do mês seja criado
                    month_directory = os.path.join(base_directory, month)
                    create_month_directory(month_directory)

                    # Verificar se a palavra-chave existe e mover o arquivo
                    if keyword:
                        destination_directory = os.path.join(month_directory, keyword)
                        create_month_directory(destination_directory)

                        destination_file_path = os.path.join(destination_directory, filename)
                        if not os.path.exists(destination_file_path):
                            shutil.move(file_path, destination_file_path)
                            display_message(f"Arquivo '{filename}' movido com sucesso para '{destination_directory}'.")
                        else:
                            display_message(f"O arquivo '{filename}' já existe na pasta de destino. Ignorando.")
                    else:
                        display_message(f"Arquivo '{filename}' não contém as palavras-chave 'unica' ou 'sup'. Ignorando.")
                else:
                    display_message(f"Diretório base não encontrado para o arquivo '{filename}'. Ignorando.")
            else:
                display_message(f"Data não encontrada no nome do arquivo '{filename}'. Ignorando.")
        else:
            display_message(f"Arquivo '{file_path}' não é um arquivo PDF. Ignorando.")



root = Tk()
root.title("Selecionar e Mover Arquivos")

select_button = Button(root, text="Selecionar Arquivos", command=move_selected_files)
select_button.pack(pady=10)

text_area = Text(root, height=10, width=50)
text_area.pack(padx=10, pady=10)

scrollbar = Scrollbar(root, command=text_area.yview)
scrollbar.pack(side="right", fill="y")
text_area.config(yscrollcommand=scrollbar.set)

root.mainloop()
