import requests
from bs4 import BeautifulSoup
import time
import random
from fake_useragent import UserAgent
from telegram import Bot

# Datos del bot de Telegram
TELEGRAM_TOKEN = "7770800424:AAGhwn_LgjHrL2L_2po0e0kHMhRvCsliffI"
TELEGRAM_CHAT_ID = 1677368106
bot = Bot(token=TELEGRAM_TOKEN)

# URL del producto en Amazon (¡cámbiala!)
PRODUCT_URL = "https://www.amazon.com.mx/dp/B0DLPL7LC5"

# Lista de User-Agents para evitar detección
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
]


def get_headers():
    """Genera un User-Agent aleatorio para cada petición."""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9"
    }


def send_notification(message):
    """Envía una notificación a Telegram usando GET."""
    # url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={message}"


    response = requests.get(url)  # Usamos GET en lugar de POST

    print(f"Código de respuesta: {response.status_code}")
    print(f"Respuesta de Telegram: {response.text}")  # Mostrará la respuesta exacta de Telegram


def check_availability():
    """Verifica si el producto está disponible en Amazon."""
    try:
        response = requests.get(PRODUCT_URL, headers=get_headers(), timeout=10)

        if response.status_code != 200:
            print(f"⚠ Error {response.status_code}. Amazon podría estar bloqueando la IP.")
            return False

        soup = BeautifulSoup(response.text, "lxml")

        # Buscar disponibilidad
        availability = soup.find("div", {"id": "availability"})

        if availability:
            availability_text = availability.get_text(strip=True)

            if "In Stock" in availability_text:
                print("✅ ¡El producto está disponible!")
                send_notification(f"✅ ¡El producto está disponible en Amazon! 🎉\n🔗 {PRODUCT_URL}")
                return True
            else:
                print("❌ El producto aún no está disponible.")
                send_notification("❌ El producto aún no está disponible.")
                return False
        else:
            print("❌ No se encontró información de disponibilidad.")
            send_notification("❌ No se encontró información de disponibilidad.")
            return False
    except Exception as e:
        print(f"❌ Error al verificar disponibilidad: {e}")
        send_notification(f"❌ Error al verificar disponibilidad: {e}")
        return False


# Monitorear cada 5 a 15 minutos (intervalo aleatorio)
while True:
    if check_availability():
        break  # Detiene el monitoreo si está disponible

    wait_time = random.randint(300, 900)  # Entre 5 y 15 minutos
    print(f"⌛ Esperando {wait_time // 60} minutos antes de la siguiente verificación...")
    time.sleep(wait_time)
#https://api.telegram.org/bot7770800424:AAGhwn_LgjHrL2L_2po0e0kHMhRvCsliffI/getUpdates
#https://api.telegram.org/bot7770800424:AAGhwn_LgjHrL2L_2po0e0kHMhRvCsliffI/sendMessage?chat_id=1677368106&text=Prueba+desde+navegador