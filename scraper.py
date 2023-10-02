import os
import re

def extract_links_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Una expresión regular para detectar enlaces de grupos de WhatsApp
    pattern = re.compile(r'https:\/\/chat\.whatsapp\.com\/[a-zA-Z0-9]+')
    links = pattern.findall(content)

    return links

def extract_links_from_directory(directory_path):
    all_links = []

    # Recorrer cada archivo en el directorio
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            links_from_file = extract_links_from_file(file_path)
            all_links.extend(links_from_file)

    return all_links

# Extraer todos los enlaces de los archivos .txt en la carpeta "chats"
all_links = extract_links_from_directory('chats')

# Determinar y mostrar los enlaces duplicados eliminados
duplicates_count = len(all_links) - len(set(all_links))

# Eliminar duplicados
unique_links = list(set(all_links))

# Guardar los enlaces en links_chats.txt
with open('links_chats.txt', 'w', encoding='utf-8') as f:
    for link in unique_links:
        f.write(link + '\n')

# Imprimir el total de enlaces únicos encontrados y los duplicados eliminados
print(f"Total de enlaces únicos encontrados: {len(unique_links)}")
print(f"Total de duplicados eliminados: {duplicates_count}")
