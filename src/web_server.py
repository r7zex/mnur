"""Простой сервер для предпросмотра интерфейса МНУР."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

alarm = False


class AppHandler(SimpleHTTPRequestHandler):
    """Отдаёт статические файлы и конфигурацию интерфейса."""

    def do_GET(self) -> None:
        if self.path.rstrip("/") == "/config.js":
            payload = f"window.APP_CONFIG = {{ alarm: {str(alarm).lower()} }};"
            self.send_response(200)
            self.send_header("Content-Type", "application/javascript; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload.encode("utf-8"))
            return
        super().do_GET()


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    """Запускает локальный сервер для каталога web."""
    web_root = Path(__file__).resolve().parents[1] / "web"
    if not web_root.exists():
        raise FileNotFoundError(f"Каталог {web_root} не найден")

    handler = partial(AppHandler, directory=str(web_root))

    with ThreadingHTTPServer((host, port), handler) as httpd:
        print(f"Сервер запущен: http://{host}:{port}")
        httpd.serve_forever()


if __name__ == "__main__":
    run()
