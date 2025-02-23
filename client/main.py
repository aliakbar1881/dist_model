from src.web.page import web_page
from pathlib import Path
import multiprocessing

from src.core.retriever import Retriver


def main():
    generator = Retriver(Path('./').resolve())
    p1 = multiprocessing.Process(target=web_page, args=(generator,))
    p1.start()


if __name__ == "__main__":
    main()