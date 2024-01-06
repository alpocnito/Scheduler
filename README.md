# Оптимизация расписания работы сервиса для множества входящих очередей

[methods.py](scheduler/methods.py) - главный файл проекта. Содержит в себе код принятия решения

[scripts.py](scheduler/scripts.py) - скрипты для запуска

[solver.py](scheduler/solver.py) - Класс. Содержит код обработки событий

[input_parser.py](scheduler/input_parser.py) - класс для парсинга входных файлов и генерации входных данных

[events.py](scheduler/events.py) - классы для работы с событиями

[logging_utils.py](scheduler/logging_utils.py) - классы для работы с логами

## Доступные алгоритмы

- MRandom - На каждой итерации выбирает случайную очередь и выгружает из нее задачу
- MSmart - На каждой итерации продолжает выгружать задачу из последней очереди. Если очередь пуста, выбирает очередь с минимальным временем изменения
- MBrainLike - адаптивная машина с памятью

## Запуск

Необходимо скачать poetry!

Скачивание библиотек для проекта:
```bash
poetry install
```

#### Генерация входных данных
```bash
poetry run gen_data --prob_step=<prob_step> --prob_queues=<prob_queues> --num_samples=<num_samples> --read_tag=<read_tag> --write_tag=<write_tag>
```
- prob_step - вероятность того, что запрос будет сгенерирован в одной временной метке. Например, prob_step = 0,5 означает, что в среднем один запрос будет генерироваться за два временных шага
- prob_queues - список с вероятностями. prob_queues[i] содержит вероятность того, что запрос поступит в очередь i. сумма (prob_queues) должна быть == 1
- num_samples - количество запросов, которое необходимо сгенерировать
- read_tag - Тэг входных файлов с таблицами change_times и work_times
- write_tag - Тэг выходных файлов с таблицами change_times, work_times и arrivals

Пример:
```bash
poetry run gen_data --prob_step=0.5 --prob_queues="0.1, 0.9" --num_samples=10000 --read_tag=3 --write_tag=3
```

#### Запуск алгоритма
```bash
poetry run run_algo --algo_name=<algo_name> --file_tag=<file_tag>
```
- algo_name - название алгоритма. См "Доступные алгоритмы"
- file_tag - Тэг входных файлов с таблицами change_times, work_times и arrivals

Пример:
```bash
poetry run run_algo --algo_name=MBrainLike --file_tag=1
```