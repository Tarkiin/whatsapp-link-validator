import requests
from colorama import Fore, init

# Inicializar colorama para que funcione correctamente en todas las plataformas
init(autoreset=True)


def is_valid_group_link_updated(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    # Si la URL de la imagen genérica está presente en la respuesta, el enlace es inválido
    generic_img_url = "https://static.whatsapp.net/rsrc.php/v3/yB/r/_0dVljceIA5.png"
    if generic_img_url in response.text:
        return False
    return True


def process_and_sort_links_from_file(file_path):
    print("Iniciando el procesamiento de enlaces...")  # Mensaje de depuración

    # Leer el archivo y obtener todos los enlaces
    with open(file_path, "r") as file:
        links = file.readlines()

    if not links:
        print("El archivo no contiene enlaces.")  # Mensaje de depuración
        return

    # Listas para acumular los enlaces válidos e inválidos
    valid_links = []
    invalid_links = []

    # Procesar cada enlace y agregarlo a la lista correspondiente
    for link in links:
        link = link.strip()  # Eliminar espacios y saltos de línea
        if is_valid_group_link_updated(link):
            valid_links.append(link)
        else:
            invalid_links.append(link)

    # Imprimir los enlaces válidos
    for link in valid_links:
        print(Fore.GREEN + link + " - Válido")

    # Imprimir los enlaces inválidos
    for link in invalid_links:
        print(Fore.RED + link + " - Inválido")


process_and_sort_links_from_file("links.txt")
