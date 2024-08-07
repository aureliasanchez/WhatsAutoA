import webbrowser
import time
import pandas as pd
import urllib.parse
import pyautogui
import os
import pyperclip
import random

# Función para enviar mensajes con imágenes usando un navegador específico
def enviar_mensajes(datos, browser_path, image_path_coords, drop_area_coords):
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
        time.sleep(20)
        
        # Si hay una imagen, se adjunta la imagen antes de enviar el mensaje de texto
        if pd.notna(imagen):
            # Hacer clic en el botón de adjuntar (clip)
            pyautogui.click(678, 984)
            tiempo_adjuntar = random.uniform(2, 4)
            print(f"Esperando {tiempo_adjuntar:.2f} segundos para adjuntar...")
            time.sleep(tiempo_adjuntar)
            # Hacer clic en el botón de adjuntar imagen
            pyautogui.click(685, 629)
            tiempo_adjuntari = random.uniform(2, 4)
            print(f"Esperando {tiempo_adjuntari:.2f} segundos para imagen...")
            time.sleep(tiempo_adjuntari)
            
            # Copiar la ruta de la imagen al portapapeles
            pyperclip.copy(imagen)
            time.sleep(3)
            
            # Pegar la ruta de la imagen en el diálogo de adjuntar archivo
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(2)
            
            # Presionar ENTER para seleccionar la imagen
            pyautogui.press('enter')
            time.sleep(2)  # Esperar a que la imagen se cargue en el chat
            
        # Presionar ENTER para enviar el mensaje de texto (y la imagen si existe)
        pyautogui.press('enter')
        time.sleep(10)  # Esperar a que el mensaje y la imagen se envíen
        print(f"Mensaje y imagen enviados a {movil}.")
        
        # Cierra la pestaña actual
        pyautogui.hotkey('ctrl', 'w')
        
        # Espera aleatoria antes de pasar al siguiente contacto
        tiempo_espera = random.uniform(6, 10)
        print(f"Esperando {tiempo_espera:.2f} segundos antes de pasar al siguiente contacto...")
        time.sleep(tiempo_espera)
        pyautogui.press('enter')


# Leer los datos del archivo de contactos, mensajes e imágenes
datos = pd.read_excel("rondaA.xlsx")
   
# Coordenadas del área de la ruta de la imagen (ajustar según sea necesario)
image_path_coords = (408, 165)  # Ajustar según la posición real de la imagen en tu sistema de archivos

# Coordenadas del área de drop en el chat de WhatsApp Web
drop_area_coords = (780, 663)  # Ajustar según la posición real del área de drop en el chat de WhatsApp Web

# Ruta al navegador específico
browser_path = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s'

# Enviar mensajes a todos los contactos
enviar_mensajes(datos, browser_path, image_path_coords, drop_area_coords)

print("Todos los mensajes han sido enviados")
