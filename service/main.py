from src.web.page import web_page
from pathlib import Path


def main():
    app = web_page(Path('./').resolve())
    app.run(debug=True)


if __name__ == "__main__":
    main()