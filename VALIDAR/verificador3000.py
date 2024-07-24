import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import webbrowser
import time
import pandas as pd
import pyautogui
import random
import os

# Configura la ruta a Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Función para verificar si los números tienen cuenta de WhatsApp
def verificar_cuentas(datos, browser_path):
    moviles = datos['TELEFONO']
    resultados = []

    for movil in moviles:
        print(f"Verificando cuenta de WhatsApp para el número: {movil}")
        time.sleep(3)
        url = f"https://web.whatsapp.com/send?phone={movil}"
        
        webbrowser.get(browser_path).open(url)
        
        # Tiempo para que la página cargue completamente
        time.sleep(11)
        
        try:
            # Capturar una porción específica de la pantalla donde aparece el mensaje de advertencia
            x, y, width, height = 655, 477, 621, 204
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            screen_path = 'D:/yoe11/Documents/TESEO/Mensajes/WhatsAutoA/VALIDAR/screenshot.png'
            screenshot.save(screen_path)

            # Preprocesamiento de la imagen
            image = Image.open(screen_path)
            image = image.convert('L')  # Convertir a escala de grises
            image = image.filter(ImageFilter.SHARPEN)  # Aplicar un filtro de nitidez
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2)  # Aumentar el contraste
            preprocessed_path = 'D:/yoe11/Documents/TESEO/Mensajes/WhatsAutoA/VALIDAR/preprocessed_screenshot.png'
            image.save(preprocessed_path)  # Guardar la imagen preprocesada

            # Utilizar OCR para leer el texto de la imagen
            texto = pytesseract.image_to_string(image, config='--psm 6')
            
            # Verificar si el texto contiene el mensaje de advertencia
            if "El número de teléfono compartido a través de la dirección URL no es válido." in texto:
                print(f"{movil} no tiene cuenta de WhatsApp.")
                resultados.append(False)
            else:
                print(f"{movil} tiene cuenta de WhatsApp.")
                resultados.append(True)
        except Exception as e:
            print(f"Error al verificar el número {movil}: {e}")
            resultados.append(False)
        
        # Cierra la pestaña actual
        pyautogui.hotkey('ctrl', 'w')
        
        # Espera aleatoria antes de pasar al siguiente contacto
        tiempo_espera = random.uniform(1, 2)
        print(f"Esperando {tiempo_espera:.2f} segundos antes de verificar el siguiente número...")
        time.sleep(tiempo_espera)
    
    datos['HAS_WHATSAPP'] = resultados
    datos.to_excel('resultado_verificacion_whatsapp.xlsx', index=False)
    print("Verificación completada y resultados guardados.")

# Leer los datos del archivo de contactos
datos = pd.read_excel("D:/yoe11/Documents/TESEO/Mensajes/WhatsAutoA/VALIDAR/contactos.xlsx")

# Ruta al navegador específico
browser_path = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s'

# Verificar cuentas de WhatsApp
verificar_cuentas(datos, browser_path)

print("Todas las verificaciones han sido completadas")
