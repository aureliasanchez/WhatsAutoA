import webbrowser
import time
import pandas as pd
import urllib.parse
import pyautogui
import pyperclip
import random

# Función para enviar mensajes con imágenes usando un navegador específico
def enviar_mensajes(datos, browser_path):
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
            pyautogui.click(498, 829)
            time.sleep(3)
            # Hacer clic en el botón de adjuntar imagen
            pyautogui.click(577, 465)
            time.sleep(3)
            
            # Copiar la ruta de la imagen al portapapeles
            pyperclip.copy(imagen)
            time.sleep(3)
            
            # Pegar la ruta de la imagen en el diálogo de adjuntar archivo
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(2)
            
            # Presionar ENTER para seleccionar la imagen
            pyautogui.press('enter')
            time.sleep(10)  # Esperar a que la imagen se cargue en el chat
            
        # Presionar ENTER para enviar el mensaje de texto (y la imagen si existe)
        pyautogui.press('enter')
        
        # Esperar hasta que el mensaje haya sido enviado
        enviado = False
        intentos = 0
        while not enviado and intentos < 10:  # Intentar hasta 10 veces
            time.sleep(5)  # Esperar antes de verificar
            # Capturar la región donde aparece el check de confirmación de envío
            screenshot = pyautogui.screenshot(region=(1787, 940, 50, 50))  # Ajustar según tu pantalla
            screenshot.save('screenshot.png')
            
            # Comprobar si el check de envío está presente
            enviado = pyautogui.locate('check_icon.png', 'screenshot.png') is not None
            
            if enviado:
                print(f"Mensaje y imagen enviados a {movil}.")
            else:
                print("El mensaje no se ha enviado todavía, esperando...")
                intentos += 1
        
        if not enviado:
            print(f"No se pudo confirmar el envío del mensaje a {movil} después de varios intentos.")
        
        # Cierra la pestaña actual
        pyautogui.hotkey('ctrl', 'w')
        
        # Espera aleatoria antes de pasar al siguiente contacto
        tiempo_espera = random.uniform(4, 8)
        print(f"Esperando {tiempo_espera:.2f} segundos antes de pasar al siguiente contacto...")
        time.sleep(tiempo_espera)

# Leer los datos del archivo de contactos, mensajes e imágenes
datos = pd.read_excel("listaContactos.xlsx")

# Ruta al navegador específico
browser_path = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s'

# Enviar mensajes a todos los contactos
enviar_mensajes(datos, browser_path)

print("Todos los mensajes han sido enviados")
