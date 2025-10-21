# Task5_Map_Python — генерирует map.html с Leaflet и открывает в браузере
# Не требует сторонних библиотек (использует CDN Leaflet).

import webbrowser
from pathlib import Path
from string import Template

TEMPLATE = Template(r"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Карта (Leaflet)</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
  <style>
    html, body { margin: 0; padding: 0; background: #0b0b0f; color: #e6e6f0; font-family: system-ui; }
    #map { height: ${height}px; width: ${width}px; margin: 16px auto; border-radius: 12px; }
    .panel { max-width: ${width}px; margin: 0 auto 12px; padding: 12px 16px; background: #0f0f14; border: 1px solid #202022; border-radius: 12px; }
    .panel h1 { margin: 0 0 8px 0; font-size: 18px; }
    .panel .meta { opacity: 0.85; font-size: 14px; }
  </style>
  <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
</head>
<body>
  <div class="panel">
    <h1>🗺️ Сгенерированная карта</h1>
    <div class="meta">Центр: ${lat}, ${lon} · Масштаб: ${zoom} · Размер: ${width}×${height}</div>
  </div>
  <div id="map"></div>
  <script>
    var map = L.map('map', { zoomControl: true }).setView([${lat}, ${lon}], ${zoom});
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    var marker = L.marker([${lat}, ${lon}]).addTo(map);
    marker.bindPopup('Lat: ${lat}<br>Lon: ${lon}<br>Zoom: ${zoom}').openPopup();
  </script>
</body>
</html>
""")

def ask_float(prompt, default=None):
    raw = input(prompt).strip()
    if raw == "":
        if default is None:
            raise ValueError("Пустое значение недопустимо")
        return float(default)
    return float(raw.replace(",", "."))

def ask_int(prompt, default=None):
    raw = input(prompt).strip()
    if raw == "":
        if default is None:
            raise ValueError("Пустое значение недопустимо")
        return int(default)
    return int(raw)

def main():
    print("=== Task5_Map_Python ===")
    print("Подсказка: оставь поле пустым и нажми Enter — подставятся значения по умолчанию.\n")

    # Значения по умолчанию (Павлодар, Казахстан)
    default_lat = 52.2873
    default_lon = 76.9674
    default_zoom = 13
    default_width = 1000
    default_height = 600

    try:
        lat = ask_float(f"Широта (например, {default_lat}) [Enter = {default_lat}]: ", default=default_lat)
        lon = ask_float(f"Долгота (например, {default_lon}) [Enter = {default_lon}]: ", default=default_lon)
        zoom = ask_int("Зум (1-19) [Enter = 13]: ", default=default_zoom)
        width = ask_int("Ширина карты в пикселях [Enter = 1000]: ", default=default_width)
        height = ask_int("Высота карты в пикселях [Enter = 600]: ", default=default_height)
    except Exception as e:
        print("Ошибка ввода:", e)
        return

    # Валидация зума
    if zoom < 1: zoom = 1
    if zoom > 19: zoom = 19

    html = TEMPLATE.safe_substitute(lat=lat, lon=lon, zoom=zoom, width=width, height=height)

    out_path = Path("map.html").resolve()
    out_path.write_text(html, encoding="utf-8")
    print(f"\n✅ Файл успешно создан: {out_path}")
    try:
        webbrowser.open(str(out_path))
        print("🌐 Открываю карту в браузере...")
    except Exception as e:
        print("Не удалось автоматически открыть браузер:", e)

if __name__ == "__main__":
    main()
