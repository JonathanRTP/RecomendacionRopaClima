import requests
import json

# ================================================
# CLIMA + RECOMENDADOR DE OUTFIT
# ================================================
# Consulta el clima de cualquier ciudad con la
# API gratuita de OpenWeatherMap y recomienda
# qué ropa ponerte según la temperatura y lluvia.
#
# Requisitos:
#   pip install requests
#
# API key gratis en: openweathermap.org
# ================================================


# ------------------------------------------------
# CONFIGURACIÓN
# ------------------------------------------------
API_KEY  = "6ec04dc81eeb34a070ec0a139ef4dad2"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
LANG     = "es"                 # idioma de la descripción del clima
UNIDADES = "metric"             # metric = Celsius | imperial = Fahrenheit


# ------------------------------------------------
# COLORES EN TERMINAL
# ------------------------------------------------
class Color:
    ROJO    = "\033[91m"
    VERDE   = "\033[92m"
    AMARILLO= "\033[93m"
    AZUL    = "\033[94m"
    CYAN    = "\033[96m"
    BLANCO  = "\033[97m"
    RESET   = "\033[0m"
    BOLD    = "\033[1m"


# ------------------------------------------------
# OBTENER CLIMA — llamada a la API
# ------------------------------------------------
def obtener_clima(ciudad: str) -> dict | None:
    """
    Hace una petición GET a OpenWeatherMap.
    Retorna el JSON con los datos del clima,
    o None si hubo un error.
    """
    params = {
        "q":     ciudad,
        "appid": API_KEY,
        "lang":  LANG,
        "units": UNIDADES
    }

    try:
        # requests.get() hace la petición HTTP
        respuesta = requests.get(BASE_URL, params=params)

        # 200 = éxito, cualquier otro código es error
        if respuesta.status_code == 200:
            return respuesta.json()   # convierte el JSON a diccionario Python
        elif respuesta.status_code == 404:
            print(f"{Color.ROJO}  Ciudad no encontrada. Verifica el nombre.{Color.RESET}")
        elif respuesta.status_code == 401:
            print(f"{Color.ROJO}  API key inválida. Verifica tu clave.{Color.RESET}")
        else:
            print(f"{Color.ROJO}  Error {respuesta.status_code} al consultar el clima.{Color.RESET}")
        return None

    except requests.exceptions.ConnectionError:
        print(f"{Color.ROJO}  Sin conexión a internet.{Color.RESET}")
        return None


# ------------------------------------------------
# PROCESAR DATOS — extrae lo que necesitamos
# ------------------------------------------------
def procesar_clima(data: dict) -> dict:
    """
    Del JSON completo que devuelve la API,
    extraemos solo los campos que nos interesan.
    """
    return {
        "ciudad":      data["name"],
        "pais":        data["sys"]["country"],
        "temperatura": round(data["main"]["temp"], 1),
        "sensacion":   round(data["main"]["feels_like"], 1),
        "humedad":     data["main"]["humidity"],
        "descripcion": data["weather"][0]["description"].capitalize(),
        "lluvia":      "rain" in data or data["weather"][0]["main"].lower() == "rain",
        "nieve":       "snow" in data or data["weather"][0]["main"].lower() == "snow",
        "viento":      round(data["wind"]["speed"] * 3.6, 1),  # m/s → km/h
        "icono":       data["weather"][0]["main"].lower()
    }


# ------------------------------------------------
# ÍCONO DEL CLIMA
# ------------------------------------------------
def icono_clima(tipo: str) -> str:
    """Devuelve un emoji según el tipo de clima."""
    iconos = {
        "clear":        "☀️",
        "clouds":       "☁️",
        "rain":         "🌧️",
        "drizzle":      "🌦️",
        "thunderstorm": "⛈️",
        "snow":         "❄️",
        "mist":         "🌫️",
        "fog":          "🌫️",
        "haze":         "🌫️",
    }
    return iconos.get(tipo, "🌡️")


# ------------------------------------------------
# RECOMENDADOR DE OUTFIT
# ------------------------------------------------
def recomendar_outfit(clima: dict) -> list[str]:
    """
    Analiza el clima y retorna una lista de
    recomendaciones de ropa según temperatura,
    lluvia, nieve y viento.
    """
    temp    = clima["temperatura"]
    lluvia  = clima["lluvia"]
    nieve   = clima["nieve"]
    viento  = clima["viento"]
    outfit  = []

    # ── Temperatura ──────────────────────────────
    if temp >= 30:
        outfit += ["👕 Camiseta ligera o sin mangas", "🩳 Shorts o ropa muy ligera"]
    elif temp >= 22:
        outfit += ["👕 Camiseta manga corta", "👖 Pantalón ligero o jeans"]
    elif temp >= 15:
        outfit += ["👔 Camisa manga larga o sudadera ligera", "👖 Pantalón largo"]
    elif temp >= 8:
        outfit += ["🧥 Chaqueta o abrigo mediano", "👖 Pantalón grueso"]
    else:
        outfit += ["🧥 Abrigo de invierno grueso", "🧣 Bufanda y guantes", "🧤 Ropa térmica interior"]

    # ── Lluvia ───────────────────────────────────
    if lluvia:
        outfit += ["☂️ Paraguas o impermeable", "👟 Zapatos impermeables"]

    # ── Nieve ────────────────────────────────────
    if nieve:
        outfit += ["🥾 Botas de nieve", "🧣 Bufanda, gorro y guantes"]

    # ── Viento fuerte ────────────────────────────
    if viento > 40:
        outfit.append("💨 Chaqueta cortavientos")

    # ── Sol fuerte ───────────────────────────────
    if temp >= 25 and not lluvia:
        outfit += ["🕶️ Gafas de sol", "🧴 Protector solar"]

    return outfit


# ------------------------------------------------
# MOSTRAR RESULTADO
# ------------------------------------------------
def mostrar_resultado(clima: dict):
    """Imprime el clima y las recomendaciones con formato."""

    icono = icono_clima(clima["icono"])

    print(f"\n{Color.BOLD}{Color.CYAN}{'═' * 45}{Color.RESET}")
    print(f"  {icono}  {Color.BOLD}{clima['ciudad']}, {clima['pais']}{Color.RESET}")
    print(f"{Color.CYAN}{'═' * 45}{Color.RESET}\n")

    # Color de la temperatura según frío/calor
    if clima["temperatura"] >= 28:
        color_temp = Color.ROJO
    elif clima["temperatura"] >= 15:
        color_temp = Color.AMARILLO
    else:
        color_temp = Color.AZUL

    print(f"  🌡️  Temperatura:  {color_temp}{Color.BOLD}{clima['temperatura']}°C{Color.RESET}  (sensación {clima['sensacion']}°C)")
    print(f"  📋  Condición:   {clima['descripcion']}")
    print(f"  💧  Humedad:     {clima['humedad']}%")
    print(f"  💨  Viento:      {clima['viento']} km/h")

    if clima["lluvia"]:
        print(f"  🌧️  {Color.AZUL}Hay lluvia — ¡lleva paraguas!{Color.RESET}")
    if clima["nieve"]:
        print(f"  ❄️  {Color.CYAN}Hay nieve — ¡abrígate bien!{Color.RESET}")

    # Recomendaciones de outfit
    outfit = recomendar_outfit(clima)
    print(f"\n{Color.BOLD}{Color.AMARILLO}  👗 Recomendación de outfit:{Color.RESET}")
    print(f"{Color.AMARILLO}  {'─' * 40}{Color.RESET}")
    for prenda in outfit:
        print(f"    {Color.VERDE}✓{Color.RESET} {prenda}")

    print(f"\n{Color.CYAN}{'═' * 45}{Color.RESET}\n")


# ------------------------------------------------
# PUNTO DE ENTRADA
# ------------------------------------------------
def main():
    print(f"\n{Color.BOLD}{Color.CYAN}")
    print("  ╔══════════════════════════════════════╗")
    print("  ║   🌤️  CLIMA + RECOMENDADOR OUTFIT     ║")
    print("  ╚══════════════════════════════════════╝")
    print(Color.RESET)

    while True:
        ciudad = input("  Ingresa una ciudad (o 'salir'): ").strip()

        if ciudad.lower() == "salir":
            print(f"\n  {Color.AMARILLO}¡Hasta luego! 👋{Color.RESET}\n")
            break

        if not ciudad:
            print(f"  {Color.ROJO}Escribe el nombre de una ciudad.{Color.RESET}")
            continue

        print(f"\n  Consultando clima de {Color.BOLD}{ciudad}{Color.RESET}...")

        # Llamada a la API
        data = obtener_clima(ciudad)

        if data:
            clima = procesar_clima(data)
            mostrar_resultado(clima)

        # Preguntar si quiere consultar otra ciudad
        otra = input("  ¿Consultar otra ciudad? (s/n): ").strip().lower()
        if otra != "s":
            print(f"\n  {Color.AMARILLO}¡Hasta luego! 👋{Color.RESET}\n")
            break


if __name__ == "__main__":
    main()
