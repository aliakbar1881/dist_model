import time

from src.core.generator import QwenGenerator


def main():
    model = QwenGenerator()
    print(model.generate(['hello, this is a test'], 'this is test please send me a answer about this.'))


if __name__ == "__main__":
    time_laps = []
    for i in range(20):
        t1 = time.time()
        main()
        t2 = time.time()
        time_laps.append(t2 - t1)
    print("Time to spend on mean: ", sum(time_laps) / 20)