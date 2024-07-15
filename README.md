import webbrowser
import time
import pandas as pd
import urllib.parse
import pyautogui
import os
import pyperclip
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Función para enviar mensajes con imágenes usando un navegador específico
def enviar_mensajes(datos, browser_path, image_path_coords, drop_area_coords):
    moviles = datos['Movil']
    mensajes = datos['Mensaje']
    imagenes = datos['Imagen']
    
    # Configurar WebDriver para el navegador específico
    driver = webdriver.Edge(executable_path='C:/Program Files (x86)/Microsoft/Edge/Application/msedgedriver.exe')
    
    for movil, mensaje, imagen in zip(moviles, mensajes, imagenes):
        print(f"Enviando mensaje al número: {movil}")
        
        mensaje_codificado = urllib.parse.quote(mensaje)
        url = f"https://web.whatsapp.com/send?phone={movil}&text={mensaje_codificado}"
        
        driver.get(url)
        
        # Esperar a que el campo de texto de WhatsApp Web esté disponible
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')))
        
        # Si hay una imagen, se adjunta la imagen antes de enviar el mensaje de texto
        if pd.notna(imagen):
            # Hacer clic en el botón de adjuntar (clip)
            pyautogui.click(477, 668)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div[1]/div[2]/div')))
            
            # Hacer clic en el botón de adjuntar imagen
            pyautogui.click(521, 328)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/span[2]/div/div[2]/div/div/div[1]/div/ul/li[1]/button/input')))
            
            # Copiar la ruta de la imagen al portapapeles
            pyperclip.copy(imagen)
            time.sleep(1)
            
            # Pegar la ruta de la imagen en el diálogo de adjuntar archivo
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1)
            
            # Presionar ENTER para seleccionar la imagen
            pyautogui.press('enter')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/span[2]/div/div[2]/span/div/div/div/div/div[2]/span/div')))
            
        # Presionar ENTER para enviar el mensaje de texto (y la imagen si existe)
        pyautogui.press('enter')
        print(f"Mensaje y imagen enviados a {movil}.")
        time.sleep(5)  # Esperar a que el mensaje y la imagen se envíen
        
        # Cerrar la pestaña actual
        driver.execute_script("window.close()")
        
        # Esperar antes de pasar al siguiente contacto
        tiempo_espera = random.uniform(4, 8)
        print(f"Esperando {tiempo_espera:.2f} segundos antes de pasar al siguiente contacto...")
        time.sleep(tiempo_espera)

    driver.quit()

# Leer los datos del archivo de contactos, mensajes e imágenes
datos = pd.read_excel("listaContactos.xlsx")

# Coordenadas del área de la ruta de la imagen (ajustar según sea necesario)
image_path_coords = (408, 165)  # Ajustar según la posición real de la imagen en tu sistema de archivos

# Coordenadas del área de drop en el chat de WhatsApp Web
drop_area_coords = (780, 663)  # Ajustar según la posición real del área de drop en el chat de WhatsApp Web

# Ruta al navegador específico
browser_path = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s'

# Enviar mensajes a todos los contactos
enviar_mensajes(datos, browser_path, image_path_coords, drop_area_coords)

print("Todos los mensajes han sido enviados")
