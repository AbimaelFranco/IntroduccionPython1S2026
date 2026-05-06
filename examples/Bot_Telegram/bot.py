import pandas as pd
import logging
import ssl
import certifi
import os

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)
from telegram.request import HTTPXRequest

# ==============================
# 🔧 FIX SSL (Python 3.13)
# ==============================
ssl._create_default_https_context = ssl._create_unverified_context
os.environ['SSL_CERT_FILE'] = certifi.where()

# ==============================
# 🪵 LOGS
# ==============================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ==============================
# 📌 Estados
# ==============================
MENU, DPI = range(2)

# ==============================
# 📊 Cargar Excel
# ==============================
archivo = "examples/Bot_Telegram/notas.xlsx"

try:
    df = pd.read_excel(archivo)

    # Limpiar columnas
    df.columns = df.columns.str.strip()

    # 🔥 LIMPIEZA CLAVE DEL DPI
    df["Usuario"] = (
        df["Usuario"]
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.strip()
    )

    print("✅ Excel cargado correctamente")
    print("Ejemplo DPI:", df["Usuario"].head().tolist())

except Exception as e:
    print("❌ Error cargando Excel:", e)
    df = pd.DataFrame()

# ==============================
# 🚀 START
# ==============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Nota Parcial"]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False  # 👈 mantiene visible el menú
    )

    await update.message.reply_text(
        "Bienvenido 👋\nSelecciona una opción:",
        reply_markup=reply_markup
    )
    return MENU

# ==============================
# 📋 MENÚ
# ==============================
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()

    if text == "nota parcial":
        await update.message.reply_text("Ingresa tu DPI:")
        return DPI

    await update.message.reply_text("❌ Opción no válida. Usa el menú.")
    return MENU

# ==============================
# 🔍 BUSCAR DPI
# ==============================
async def buscar_dpi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dpi = update.message.text.strip()

    print("🔍 DPI ingresado:", dpi)

    try:
        # 🔥 BÚSQUEDA ROBUSTA
        resultado = df[df["Usuario"].str.contains(dpi, na=False)]

        if not resultado.empty:
            nombre = resultado.iloc[0]["Nombre"]
            nota = resultado.iloc[0]["Calificación/30.00"]

            await update.message.reply_text(
                f"👤 Nombre: {nombre}\n📊 Nota Parcial: {nota}"
            )
        else:
            await update.message.reply_text("❌ DPI no encontrado")

    except Exception as e:
        await update.message.reply_text("⚠️ Error procesando datos")
        print("Error:", e)

    return await start(update, context)

# ==============================
# ⚠️ MANEJO DE ERRORES GLOBAL
# ==============================
async def error_handler(update, context):
    print(f"⚠️ Error global: {context.error}")

# ==============================
# 🧠 MAIN
# ==============================
def main():
    TOKEN = "TOKEN_AQUI"  # 👈 coloca tu token

    request = HTTPXRequest(
        connect_timeout=10,
        read_timeout=10,
        write_timeout=10,
        pool_timeout=10
    )

    app = ApplicationBuilder().token(TOKEN).request(request).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, menu)],
            DPI: [MessageHandler(filters.TEXT & ~filters.COMMAND, buscar_dpi)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    app.add_handler(conv_handler)
    app.add_error_handler(error_handler)

    print("🤖 Bot corriendo...")
    app.run_polling()

# ==============================
# ▶️ RUN
# ==============================
if __name__ == "__main__":
    main()