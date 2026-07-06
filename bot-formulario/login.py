import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import IMMI_EMAIL, IMMI_PASSWORD, TIMEOUT_BOTON, URL_POST_LOGIN

logger = logging.getLogger(__name__)


def iniciar_sesion(driver):
    logger.info("🔐 Iniciando sesión automáticamente...")

    WebDriverWait(driver, TIMEOUT_BOTON).until(
        EC.presence_of_element_located((By.ID, "username"))
    )

    driver.find_element(By.ID, "username").send_keys(IMMI_EMAIL)
    driver.find_element(By.ID, "password").send_keys(IMMI_PASSWORD)
    driver.find_element(By.XPATH, "//button[@name='login' and not(@tabindex='-1')]").click()

    logger.info("✅ Credenciales enviadas.")
    time.sleep(0.1)

    driver.get(URL_POST_LOGIN)
    logger.info(f"🌐 Redirigido a {URL_POST_LOGIN}")
