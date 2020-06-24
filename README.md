# py-meters

### Основные функции:
* опрос счётчиков электроэнергии по стандарту МЭК 61107-2001 (СЕ805M);
* хранение получасовых профилей мощностей в БД (sqlite);
* интеграция с ПК "Энергосфера"

station.communicate.Comm - класс взаимодействия с COM-портом

station.communicate.Counter - класс взаимодействия со счётчиком

Counter.get_profile(self, date, energy_type) - считывание со счётчика профиля энергии [PE, PI, QE, QI] за сутки <date>

Построения Графиков Google Charts:
https://developers.google.com/chart/interactive/docs/gallery

UI-Фреймворк Metro 4 Документация:
https://metroui.org.ua/intro.html

### Страница профиля нагрузки
![Профиль](https://github.com/babazhanov/py-meters/blob/master/blob/profiles.png?raw=true)
