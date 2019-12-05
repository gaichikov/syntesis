Test task for Syntesis company.

Запуск скрипта установки через python install.py  - создастся виртуальное окружение и установятся пакеты из requirements.txt

Сделал два варианта краулеров.

1) Scrapy.

Для запуска необходимо перейти в папку parse_cruises и запустить краулер.

# cd parse_cruises

# scrapy crawl cruises -o cruises.json

Результат будет выгружен в файл в формате json.

Для подмены user-agent`ов используется middleware  scrapy_useragents, настроено в parse_cruises/parse_cruises/settings.py .


2) Beautiful soup.

Скрипт находится в папке parse_cruises_bs , запуск через python parse_cruises_bs.py  в том же виртуальном окружении. Скрипт выведет результат в стандартный вывод.  Агенты выставляются рандомом в аргументе header при запросе url`ов библиотекой request.

Для ускорения парсинга использую треды, возможно использовать asyncio для асинхронного запуска тасков.
