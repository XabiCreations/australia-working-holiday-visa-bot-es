import logging

import requests
from twilio.rest import Client as TwilioClient

from config import CHAT_ID, TELEGRAM_TOKEN, TWILIO_FROM, TWILIO_SID, TWILIO_TO, TWILIO_TOKEN

logger = logging.getLogger(__name__)

_PLACEHOLDERS = {
    "", "YOUR_TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_CHAT_ID",
    "YOUR_TWILIO_ACCOUNT_SID", "YOUR_TWILIO_AUTH_TOKEN", "+XXXXXXXXXXX",
}


def _telegram_configurado():
    return (
        TELEGRAM_TOKEN not in _PLACEHOLDERS
        and str(CHAT_ID) not in _PLACEHOLDERS
    )


def _twilio_configurado():
    return (
        TWILIO_SID not in _PLACEHOLDERS
        and TWILIO_TOKEN not in _PLACEHOLDERS
        and TWILIO_FROM not in _PLACEHOLDERS
        and TWILIO_TO not in _PLACEHOLDERS
    )


def enviar_telegram(mensaje):
    if not _telegram_configurado():
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    try:
        respuesta = requests.post(url, data=payload, timeout=10)
        if respuesta.status_code == 200:
            logger.info("📩 Mensaje enviado a Telegram.")
        else:
            logger.error(f"❌ Error Telegram ({respuesta.status_code}): {respuesta.text}")
    except requests.RequestException as e:
        logger.error(f"❌ Error de red al enviar Telegram: {e}")


def hacer_llamada(mensaje_voz):
    if not _twilio_configurado():
        return
    try:
        cliente = TwilioClient(TWILIO_SID, TWILIO_TOKEN)
        twiml = (
            f"<Response>"
            f'<Say language="es-ES" voice="alice">{mensaje_voz}</Say>'
            f'<Pause length="1"/>'
            f'<Say language="es-ES" voice="alice">{mensaje_voz}</Say>'
            f"</Response>"
        )
        cliente.calls.create(twiml=twiml, to=TWILIO_TO, from_=TWILIO_FROM)
        logger.info("📞 Llamada realizada.")
    except Exception as e:
        logger.error(f"❌ Error al realizar la llamada Twilio: {e}")
        enviar_telegram(f"❌ No se pudo realizar la llamada Twilio: `{e}`")
