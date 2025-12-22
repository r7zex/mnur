"""Простой сервер для предпросмотра интерфейса МНУР."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    """Запускает локальный сервер для каталога web."""
    web_root = Path(__file__).resolve().parents[1] / "web"
    if not web_root.exists():
        raise FileNotFoundError(f"Каталог {web_root} не найден")

    handler = partial(SimpleHTTPRequestHandler, directory=str(web_root))

    with ThreadingHTTPServer((host, port), handler) as httpd:
        print(f"Сервер запущен: http://{host}:{port}")
        httpd.serve_forever()


if __name__ == "__main__":
    run()
