import webbrowser
import time
import pandas as pd
import urllib.parse
import pyautogui
import pyperclip
import random

# Función para enviar mensajes con imágenes usando un navegador específico
def enviar_mensajes(datos, browser_path, clip_coords, image_coords):
    moviles = datos['Movil']
    mensajes = datos['Mensaje']
    imagenes = datos['Imagen']
    
    for movil, mensaje, imagen in zip(moviles, mensajes, imagenes):
        print(f"Enviando mensaje al número: {movil}")
        time.sleep(5)
        mensaje_codificado = urllib.parse.quote(mensaje)
        url = f"https://web.whatsapp.com/send?phone={movil}&text={mensaje_codificado}"
        
        webbrowser.get(browser_path).open(url)
        
        # Tiempo para que la página cargue completamente
        time.sleep(15)
        
        # Si hay una imagen, se adjunta la imagen antes de enviar el mensaje de texto
        if pd.notna(imagen):
            # Hacer clic en el botón de adjuntar (clip)
            pyautogui.click(*clip_coords)
            time.sleep(3)
            # Hacer clic en el botón de adjuntar imagen
            pyautogui.click(*image_coords)
            time.sleep(3)
            
            # Copiar la ruta de la imagen al portapapeles
            pyperclip.copy(imagen)
            time.sleep(3)
            
            # Pegar la ruta de la imagen en el diálogo de adjuntar archivo
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(2)
            
            # Presionar ENTER para seleccionar la imagen
            pyautogui.press('enter')
            time.sleep(3)  # Esperar a que la imagen se cargue en el chat
            
        # Presionar ENTER para enviar el mensaje de texto (y la imagen si existe)
        pyautogui.press('enter')
        print(f"Mensaje y imagen enviados a {movil}.")
        time.sleep(10)  # Esperar a que el mensaje y la imagen se envíen
        
        # Cierra la pestaña actual
        pyautogui.hotkey('ctrl', 'w')
        
        # Espera aleatoria antes de pasar al siguiente contacto
        tiempo_espera = random.uniform(4, 8)
        print(f"Esperando {tiempo_espera:.2f} segundos antes de pasar al siguiente contacto...")
        time.sleep(tiempo_espera)

# Leer los datos del archivo de contactos, mensajes e imágenes
datos = pd.read_excel("listaContactos.xlsx")

# Coordenadas del área de la ruta de la imagen (ajustar según sea necesario)
image_path_coords = (408, 165)  # Ajustar según la posición real de la imagen en tu sistema de archivos

# Coordenadas de los botones de adjuntar (clip) e imagen para cada navegador
coords = {
    'edge': {
        'clip_coords': (468, 676),
        'image_coords': (478, 443)
    },
    'chrome': {
        'clip_coords': (484, 671),  # Ajusta según sea necesario
        'image_coords': (480, 498)  # Ajusta según sea necesario
    },
    'opera': {
        'clip_coords': (515, 667),  # Ajusta según sea necesario
        'image_coords': (524, 446)  # Ajusta según sea necesario
    }
}

# Rutas a los navegadores específicos
browser_paths = {
    'edge': 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s',
    'chrome': 'C:/Program Files/Google/Chrome/Application/chrome.exe %s',
    'opera': 'C:/Users/Administrator/AppData/Local/Programs/Opera/launcher.exe %s'  # Ajustar la ruta a Opera según sea necesario

}

# Parámetros de segmentación
total_contacts = len(datos)
batch_size = total_contacts // 3  # Dividir la lista de contactos en 3 partes

browser_order = ['edge', 'chrome', 'opera']

for i, browser_name in enumerate(browser_order):
    browser_path = browser_paths[browser_name]
    clip_coords = coords[browser_name]['clip_coords']
    image_coords = coords[browser_name]['image_coords']
    start_index = i * batch_size
    end_index = (i + 1) * batch_size if i < 2 else total_contacts  # Asegurar que el último segmento incluya todos los restantes
    segment = datos.iloc[start_index:end_index]
    enviar_mensajes(segment, browser_path, clip_coords, image_coords)
    print(f"Segmento de mensajes desde {start_index} hasta {end_index} completado.")
    if i < 2:
        tiempo_espera_segmento = random.uniform(10, 15)
        print(f"Esperando {tiempo_espera_segmento:.2f} segundos antes de continuar con el siguiente segmento...")
        time.sleep(tiempo_espera_segmento)

print("Todos los mensajes han sido enviados")