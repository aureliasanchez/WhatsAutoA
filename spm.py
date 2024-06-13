from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def send_message(driver, number, message):
    try:
        # Incluir el código de país de México (+52)
        number_with_code = f"+52{number}"
        url = f"https://web.whatsapp.com/send?phone={number_with_code}&text={message}"
        driver.get(url)
        print(f"Abriendo URL: {url}")
        time.sleep(random.uniform(8, 12))  # Espera para cargar la página

        try:
            # Esperar hasta que el campo de entrada de mensaje esté presente
            message_box = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true" and @data-tab="6"]'))
            )
            message_box.send_keys(message)
            print(f"Escribiendo mensaje en {number_with_code}")

            # Esperar hasta que el botón de enviar esté presente y hacer clic en él
            send_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="compose-btn-send"]'))
            )
            send_button.click()
            print(f"Mensaje enviado a {number_with_code}")
        except Exception as e:
            print(f"Error al enviar mensaje a {number_with_code}: {e}")
    except Exception as e:
        print(f"Error general en send_message: {e}")

def human_like_wait(driver):
    try:
        # Simula tiempos de espera humanos y acciones adicionales
        time.sleep(random.uniform(1, 3))
        actions = [
            lambda: driver.execute_script("window.scrollTo(0, document.body.scrollHeight);"),
            lambda: driver.execute_script("window.scrollTo(0, 0);")
        ]
        random.choice(actions)()
        print("Realizando una acción humana simulada (scroll).")
        time.sleep(random.uniform(1, 3))
    except Exception as e:
        print(f"Error en human_like_wait: {e}")

def main():
    try:
        # Configurar el webdriver
        driver = webdriver.Chrome()
        print("Webdriver configurado.")

        # Abrir WhatsApp Web
        driver.get("https://web.whatsapp.com")
        print("WhatsApp Web abierto.")
        input("Presiona Enter después de escanear el código QR")

        # Lista de números de teléfono y mensajes
        numbers = [
            "772112615" "7713529855" "7733429397", "7751634657", "7751636128", "7751635533", "7751676807", "7751676656"
        ]
        
        messages = [
            "Hola, ¿cómo estás?",
            "¡Saludos! Espero que tengas un buen día.",
            "Este es un mensaje repetitivo de prueba."
        ]

        # Enviar un mensaje aleatorio a cada número en intervalos aleatorios
        for number in numbers:
            print(f"Enviando mensaje a {number}.")
            message = random.choice(messages)
            send_message(driver, number, message)
            human_like_wait(driver)
            sleep_time = random.randint(5, 10)  # Aumenta el tiempo de espera
            print(f"Esperando {sleep_time} segundos antes de enviar el siguiente mensaje.")
            time.sleep(sleep_time)
        
        print("Todos los mensajes han sido enviados.")
        # Cerrar el navegador
        driver.quit()
    except Exception as e:
        print(f"Error en main: {e}")

if __name__ == "__main__":
    main()
