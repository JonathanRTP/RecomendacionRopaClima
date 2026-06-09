# 🌤️ Clima + Recomendador de Outfit

Consulta el clima de cualquier ciudad del mundo y recibe recomendaciones de ropa según la temperatura, lluvia, nieve y viento. Construido con Python y la API gratuita de OpenWeatherMap.

---

## 🖥️ Demo

```
  ╔══════════════════════════════════════╗
  ║   🌤️  CLIMA + RECOMENDADOR OUTFIT     ║
  ╚══════════════════════════════════════╝

  Ingresa una ciudad: Medellín

  ═════════════════════════════════════════════
  ☀️  Medellín, CO
  ═════════════════════════════════════════════

  🌡️  Temperatura:  26.3°C  (sensación 28.1°C)
  📋  Condición:   Cielo despejado
  💧  Humedad:     65%
  💨  Viento:      12.6 km/h

  👗 Recomendación de outfit:
  ────────────────────────────────────────
    ✓ 👕 Camiseta manga corta
    ✓ 👖 Pantalón ligero o jeans
    ✓ 🕶️ Gafas de sol
    ✓ 🧴 Protector solar
```

---

## 🚀 Cómo ejecutarlo

**1. Clona el repositorio**
```bash
git clone https://github.com/JonathanRTP/clima-outfit.git
cd clima-outfit
```

**2. Instala la dependencia**
```bash
pip install requests
```

**3. Consigue tu API key gratis**
- Regístrate en [openweathermap.org](https://openweathermap.org)
- Ve a **API Keys** y copia tu clave
- En `clima.py`, reemplaza `TU_API_KEY_AQUI` con tu clave

**4. Ejecuta**
```bash
python clima.py
```

---

## 👗 Lógica de recomendación

| Temperatura | Outfit sugerido |
|---|---|
| 30°C o más | Camiseta ligera, shorts |
| 22°C – 29°C | Camiseta manga corta, pantalón ligero |
| 15°C – 21°C | Manga larga o sudadera |
| 8°C – 14°C | Chaqueta o abrigo mediano |
| Menos de 8°C | Abrigo grueso, ropa térmica |

Además detecta: 🌧️ lluvia, ❄️ nieve, 💨 viento fuerte y ☀️ sol intenso.

---

## 📁 Estructura

```
clima-outfit/
└── clima.py      # Código principal
└── README.md     # Este archivo
```

---

## 🧠 Conceptos de Python utilizados

- Consumo de API REST con `requests`
- Manejo de JSON
- Funciones con type hints
- Manejo de errores HTTP (404, 401, etc.)
- Formato de terminal con códigos ANSI

---

## 👤 Autor

**Jonathan Restrepo** — [github.com/tu-usuario](https://github.com/JonathanRTP)
