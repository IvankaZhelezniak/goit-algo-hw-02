# імітуання роботи сервісного центру (приймає і обробляє заявки). Програма має автоматично
# генерувати нові заявки (ідентифіковані унікальним номером або іншими даними),
# додавати їх до черги, а потім послідовно видаляти з черги для "обробки"

from queue import Queue, Empty
from dataclasses import dataclass, field
from itertools import count
from time import sleep, time
import random


#  модель заявки 
@dataclass
class Request:
    id: int
    created_at: float = field(default_factory=time)
    payload: str = ""


#  черга та операції з нею 
class ServiceCenter:
    def __init__(self, maxsize: int | None = None):
        self.queue = Queue(maxsize=maxsize or 0)  # 0 = без обмежень
        self._ids = count(1)

    # generate_request(): створює нову заявку 1 або більше і додає в чергу
    def generate_request(self):
        # скільки заявок з’явиться цього "тіку" (0..2)
        n = random.randint(0, 2)
        for _ in range(n):
            req = Request(id=next(self._ids),
                          payload=f"data-{random.randint(100, 999)}")
            self.queue.put(req)
            print(f"[NEW ] додано заявку #{req.id} (у черзі: {self.queue.qsize()})")

    # process_request(): бере з черги і "обробити"
    def process_request(self):
        try:
            req = self.queue.get_nowait()
        except Empty:
            print("[INFO] черга порожня — нема що обробляти")
            return
        print(f"[PROC] обробка #{req.id} ...")
        sleep(random.uniform(0.2, 0.6))  # імітація роботи
        print(f"[DONE] завершено #{req.id}")
        self.queue.task_done()


# --------- головний цикл програми ---------
def main():
    center = ServiceCenter()
    try:
        # працює фіксовану кількість кроків; треба натиснути Ctrl+C, щоб перервати
        for tick in range(1, 21):
            print(f"\n— Тік {tick} —")
            center.generate_request()  # створення нових заявок
            center.process_request()   # обробка однієї заявки (якщо є)
            sleep(0.4)
    except KeyboardInterrupt:
        print("\nЗупинка користувачем.")
    finally:
        # доробляє все, що залишилося в черзі
        while not center.queue.empty():
            center.process_request()
        center.queue.join()
        print("\nУсі заявки опрацьовано. Готово.")


if __name__ == "__main__":
    main()
