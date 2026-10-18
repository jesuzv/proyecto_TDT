import json
from pathlib import Path as Ruta

carpeta = Ruta(__file__).resolve().parent

def leer_json(nombre):
    return json.loads(
        (carpeta / nombre).read_text(encoding="utf-8")
    )

def serializar_seguro(valor):
    return (
        json.dumps(valor, ensure_ascii=False)
        .replace("<", "\\u003c")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )

datos_geograficos = leer_json("datos/barrios.geojson")
configuracion = leer_json("configuracion.json")
plantilla = (carpeta / "plantilla.html").read_text(
    encoding="utf-8"
)

pagina = (
    plantilla
    .replace("__GEOJSON__", serializar_seguro(datos_geograficos))
    .replace("__CAPTIONS__", serializar_seguro(configuracion["titulos"]))
    .replace("__RELEASES__", serializar_seguro(configuracion["versiones"]))
)

destino = carpeta / "salida" / "index.html"
destino.parent.mkdir(exist_ok=True)
destino.write_text(pagina, encoding="utf-8")
print("Mapa generado:", destino)
