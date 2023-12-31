import requests
from lxml import html
from colorama import Fore, init
import time

# Inicializar colorama para que funcione correctamente en todas las plataformas
init(autoreset=True)

def is_valid_group_link_updated(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    content = response.text

    tree = html.fromstring(content)
    group_name = tree.xpath('/html/body/div[1]/div[1]/div[2]/div/section/div/div/div/div/div[2]/h3/text()')

    # Si el nombre del grupo está vacío o no se encuentra, el enlace es inválido
    if not group_name or not group_name[0].strip():
        return False, content

    return True, content

def get_group_name_from_content(content):
    tree = html.fromstring(content)
    group_name = tree.xpath('/html/body/div[1]/div[1]/div[2]/div/section/div/div/div/div/div[2]/h3/text()')
    return group_name[0] if group_name else "Nombre desconocido"

def process_and_sort_links_from_file(file_path):
    # Leer el archivo y obtener todos los enlaces
    with open(file_path, "r") as file:
        links = file.readlines()

    if not links:
        print("El archivo no contiene enlaces.")  # Mensaje de depuración
        return

    # Listas para acumular los enlaces válidos e inválidos
    valid_links = []
    invalid_links = []

    print("Iniciando el procesamiento de enlaces...")  # Mensaje de depuración

    total_links = len(links)
    start_time = time.time()

    # Procesar cada enlace y agregarlo a la lista correspondiente
    for index, link in enumerate(links, start=1):
        link = link.strip()  # Eliminar espacios y saltos de línea
        is_valid, content = is_valid_group_link_updated(link)
        elapsed_time = time.time() - start_time
        estimated_total_time = (elapsed_time / index) * total_links
        time_left = estimated_total_time - elapsed_time

        group_name = get_group_name_from_content(content)
        link_info = f"{link} - {group_name} - Válido"
        if is_valid:
            valid_links.append(link_info)
        else:
            link_info = f"{link} - {group_name} - Inválido"
            invalid_links.append(link_info)

        # Mostrar el progreso y el tiempo estimado
        minutes_left, seconds_left = divmod(time_left, 60)
        print(f"\rProcesando enlaces... {Fore.GREEN}{index}{Fore.RESET}/"f"{total_links}. Tiempo estimado restante: {Fore.GREEN}{int(minutes_left)} minutos, {int(seconds_left)} segundos{Fore.RESET}",end='')

    print("\nFinalizado el procesamiento de enlaces.")

    # Leer los enlaces válidos previamente guardados
    with open("links_validos.txt", "r", encoding="utf-8") as infile:
        existing_valid_links = [line.strip() for line in infile.readlines()]

    # Combinar los enlaces válidos previos con los nuevos y eliminar duplicados
    all_valid_links = list(set(existing_valid_links + valid_links))

    # Guardar los enlaces válidos en el archivo sin duplicados
    with open("links_validos.txt", "w", encoding="utf-8") as outfile:
        for link_info in all_valid_links:
            outfile.write(link_info + "\n")

    # Imprimir los enlaces válidos
    for link_info in valid_links:
        print(Fore.GREEN + link_info)

    # Imprimir los enlaces inválidos
    for link_info in invalid_links:
        print(Fore.RED + link_info)

process_and_sort_links_from_file("links.txt")
