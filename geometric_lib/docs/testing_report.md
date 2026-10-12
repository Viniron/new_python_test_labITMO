# Отчёт о тестировании библиотеки geometric_lib

## 1. Цели и задачи тестирования

Цель — проверить, что функции библиотеки правильно считают площадь и периметр
фигур, и выяснить, как они ведут себя на некорректных входных данных.

Задачи:

- составить наборы входных данных для каждой функции и заранее вручную
  посчитать ожидаемые ответы;
- написать unit-тесты на `unittest` для всех четырёх фигур: круга, квадрата,
  прямоугольника и треугольника;
- запустить тесты, зафиксировать результаты и разобрать каждый упавший тест.

Исходный код фигур в ходе работы не менялся. Тесты писались как для готового
приложения: ожидаемое поведение бралось из документации (`docs/documentation.md`)
и из геометрии, а не из того, как устроены функции внутри.

## 2. Описание тестируемого продукта

geometric_lib — библиотека на Python для вычисления площади и периметра плоских
фигур. Каждая фигура лежит в своём модуле, в модуле две функции:

| Модуль         | Функция              | Что возвращает                          |
|----------------|----------------------|-----------------------------------------|
| `circle.py`    | `area(r)`            | площадь круга, πr²                      |
| `circle.py`    | `perimeter(r)`       | длину окружности, 2πr                   |
| `square.py`    | `area(a)`            | площадь квадрата, a²                    |
| `square.py`    | `perimeter(a)`       | периметр квадрата, 4a                   |
| `rectangle.py` | `area(a, b)`         | площадь прямоугольника, ab              |
| `rectangle.py` | `perimeter(a, b)`    | периметр прямоугольника, 2(a + b)       |
| `triangle.py`  | `area(a, h)`         | площадь треугольника, ah / 2            |
| `triangle.py`  | `perimeter(a, b, c)` | периметр треугольника, a + b + c        |

Требования к продукту, которые проверялись:

- для неотрицательных чисел (целых и дробных) функции возвращают верный результат;
- результат не зависит от порядка сторон там, где порядок не важен
  (прямоугольник);
- длины сторон и радиус не могут быть отрицательными, а у треугольника стороны
  должны удовлетворять неравенству треугольника — в таких случаях логично ждать
  ошибку `ValueError`, а не число;
- если вместо числа передана строка, должна возникать ошибка `TypeError`.

## 3. Область тестирования

Тестируются все восемь функций из таблицы выше. Каждой фигуре соответствует свой
файл с тестами:

```
geometric_lib
 └── tests
     ├── __init__.py
     ├── test_circle.py
     ├── test_square.py
     ├── test_rectangle.py
     └── test_triangle.py
```

В каждом файле два класса-наследника `unittest.TestCase`: один для `area`,
другой для `perimeter`.

Что не входит в область тестирования: производительность, безопасность,
совместная работа модулей (интеграционное тестирование) — библиотека состоит из
независимых функций без состояния, поэтому для неё это не имеет смысла.

## 4. Стратегия тестирования

Вид тестирования — функциональное модульное (unit) тестирование методом
«чёрного ящика». Инструмент — встроенный модуль `unittest`.

При подборе данных использовались такие техники:

- **классы эквивалентности.** Входные значения делятся на группы, внутри которых
  функция должна вести себя одинаково: целые положительные, дробные, ноль,
  отрицательные, нечисловые. Из каждой группы берётся одно-два значения;
- **граничные значения.** Отдельно проверяется ноль (граница между допустимыми
  и недопустимыми размерами) и единица;
- **большие значения** (сторона 10⁶, радиус 1000) — чтобы убедиться, что нет
  переполнения или потери точности;
- **проверка свойств.** Для прямоугольника проверяется, что перестановка сторон
  не меняет результат;
- **негативные тесты.** На отрицательные размеры, строки и несуществующий
  треугольник ожидается исключение (`assertRaises`).

Ответы с дробной частью сравниваются через `assertAlmostEqual` (точность — 7
знаков после запятой), потому что вычисления с `float` дают погрешность.
Например, `0.1 + 0.2` в Python равно `0.30000000000000004`, и сравнение через
`assertEqual` упало бы, хотя функция работает правильно. Ожидаемые значения для
круга записаны в тестах числами, посчитанными вручную, а не через `math.pi`,
чтобы тест не повторял формулу из проверяемого кода.

### Тестовые случаи

**Круг (`test_circle.py`)**

| Тест                                         | Вход            | Ожидание            |
|----------------------------------------------|-----------------|---------------------|
| CircleAreaTestCase.test_unit_radius          | `area(1)`       | ≈ 3.1415926536      |
| CircleAreaTestCase.test_integer_radius       | `area(5)`       | ≈ 78.5398163397     |
| CircleAreaTestCase.test_fractional_radius    | `area(0.5)`     | ≈ 0.7853981634      |
| CircleAreaTestCase.test_zero_radius          | `area(0)`       | 0                   |
| CircleAreaTestCase.test_big_radius           | `area(1000)`    | ≈ 3141592.6535898   |
| CircleAreaTestCase.test_string_radius        | `area('5')`     | `TypeError`         |
| CircleAreaTestCase.test_negative_radius      | `area(-1)`      | `ValueError`        |
| CirclePerimeterTestCase.test_unit_radius     | `perimeter(1)`  | ≈ 6.2831853072      |
| CirclePerimeterTestCase.test_integer_radius  | `perimeter(5)`  | ≈ 31.4159265359     |
| CirclePerimeterTestCase.test_fractional_radius | `perimeter(2.5)` | ≈ 15.7079632679  |
| CirclePerimeterTestCase.test_zero_radius     | `perimeter(0)`  | 0                   |
| CirclePerimeterTestCase.test_string_radius   | `perimeter('5')`| `TypeError`         |
| CirclePerimeterTestCase.test_negative_radius | `perimeter(-1)` | `ValueError`        |

**Квадрат (`test_square.py`)**

| Тест                                      | Вход                | Ожидание     |
|-------------------------------------------|---------------------|--------------|
| SquareAreaTestCase.test_integer_side      | `area(3)`           | 9            |
| SquareAreaTestCase.test_unit_side         | `area(1)`           | 1            |
| SquareAreaTestCase.test_fractional_side   | `area(2.5)`         | 6.25         |
| SquareAreaTestCase.test_zero_side         | `area(0)`           | 0            |
| SquareAreaTestCase.test_big_side          | `area(10**6)`       | 10¹²         |
| SquareAreaTestCase.test_string_side       | `area('3')`         | `TypeError`  |
| SquareAreaTestCase.test_negative_side     | `area(-3)`          | `ValueError` |
| SquarePerimeterTestCase.test_integer_side | `perimeter(3)`      | 12           |
| SquarePerimeterTestCase.test_fractional_side | `perimeter(2.5)` | 10.0         |
| SquarePerimeterTestCase.test_zero_side    | `perimeter(0)`      | 0            |
| SquarePerimeterTestCase.test_big_side     | `perimeter(10**6)`  | 4·10⁶        |
| SquarePerimeterTestCase.test_string_side  | `perimeter('3')`    | `TypeError`  |
| SquarePerimeterTestCase.test_negative_side| `perimeter(-3)`     | `ValueError` |

**Прямоугольник (`test_rectangle.py`)**

| Тест                                             | Вход                  | Ожидание                    |
|--------------------------------------------------|-----------------------|-----------------------------|
| RectangleAreaTestCase.test_integer_sides         | `area(4, 5)`          | 20                          |
| RectangleAreaTestCase.test_zero_mul              | `area(10, 0)`         | 0                           |
| RectangleAreaTestCase.test_square_mul            | `area(10, 10)`        | 100                         |
| RectangleAreaTestCase.test_fractional_sides      | `area(2.5, 4)`        | 10.0                        |
| RectangleAreaTestCase.test_swap_sides            | `area(3, 7)`          | равно `area(7, 3)`          |
| RectangleAreaTestCase.test_string_side           | `area('4', 5)`        | `TypeError`                 |
| RectangleAreaTestCase.test_negative_side         | `area(-4, 5)`         | `ValueError`                |
| RectangleAreaTestCase.test_both_negative_sides   | `area(-4, -5)`        | `ValueError`                |
| RectanglePerimeterTestCase.test_integer_sides    | `perimeter(4, 5)`     | 18                          |
| RectanglePerimeterTestCase.test_square_sides     | `perimeter(10, 10)`   | 40                          |
| RectanglePerimeterTestCase.test_zero_sides       | `perimeter(0, 0)`     | 0                           |
| RectanglePerimeterTestCase.test_fractional_sides | `perimeter(0.1, 0.2)` | ≈ 0.6                       |
| RectanglePerimeterTestCase.test_swap_sides       | `perimeter(3, 7)`     | равно `perimeter(7, 3)`     |
| RectanglePerimeterTestCase.test_negative_side    | `perimeter(-4, 5)`    | `ValueError`                |

**Треугольник (`test_triangle.py`)**

| Тест                                              | Вход                    | Ожидание     |
|---------------------------------------------------|-------------------------|--------------|
| TriangleAreaTestCase.test_integer_values          | `area(6, 4)`            | 12           |
| TriangleAreaTestCase.test_odd_product             | `area(3, 5)`            | 7.5          |
| TriangleAreaTestCase.test_fractional_values       | `area(2.5, 2)`          | 2.5          |
| TriangleAreaTestCase.test_zero_height             | `area(5, 0)`            | 0            |
| TriangleAreaTestCase.test_string_side             | `area('6', 4)`          | `TypeError`  |
| TriangleAreaTestCase.test_negative_side           | `area(-6, 4)`           | `ValueError` |
| TrianglePerimeterTestCase.test_right_triangle     | `perimeter(3, 4, 5)`    | 12           |
| TrianglePerimeterTestCase.test_equilateral        | `perimeter(2, 2, 2)`    | 6            |
| TrianglePerimeterTestCase.test_fractional_sides   | `perimeter(1.5, 2.5, 3)`| 7.0          |
| TrianglePerimeterTestCase.test_string_side        | `perimeter('3', 4, 5)`  | `TypeError`  |
| TrianglePerimeterTestCase.test_negative_side      | `perimeter(-3, 4, 5)`   | `ValueError` |
| TrianglePerimeterTestCase.test_impossible_triangle| `perimeter(1, 2, 10)`   | `ValueError` |

Всего 52 теста: 13 для круга, 13 для квадрата, 14 для прямоугольника и 12 для
треугольника.

### Запуск тестов

Из каталога `geometric_lib` все тесты сразу:

```
python -m unittest -v
```

Тесты одной фигуры:

```
python -m unittest tests/test_square.py
```

## 5. Критерии приемки

Тестирование считается завершённым, если:

- для каждой из 8 функций есть тесты на корректные данные, на ноль и на
  некорректные данные;
- все тесты запущены, результат каждого зафиксирован;
- по каждому упавшему тесту понятна причина и сделан вывод.

Продукт можно считать принятым, если проходят все тесты на корректных данных
(правильность формул) и библиотека сообщает об ошибке на некорректных данных,
а не возвращает число, похожее на правильный ответ.

## 6. Ожидаемые результаты

- Все тесты с корректными входными данными должны пройти — формулы в
  документации простые и известные.
- Тесты с отрицательными размерами и несуществующим треугольником, скорее
  всего, упадут: в документации ничего не сказано про проверку входных данных.
- Тесты со строками должны пройти там, где строку нельзя умножить или сложить
  с числом, и могут упасть там, где Python умеет повторять строку (`'3' * 4`).
- По итогам — список найденных дефектов и статистика: сколько тестов прошло и
  сколько упало.

## 7. Актуальные результаты тестирования

Запуск `python -m unittest -v` (Python 3.13):

```
Ran 52 tests in 0.028s

FAILED (failures=12)
```

| Фигура         | Всего | Прошло | Упало |
|----------------|-------|--------|-------|
| Круг           | 13    | 11     | 2     |
| Квадрат        | 13    | 10     | 3     |
| Прямоугольник  | 14    | 10     | 4     |
| Треугольник    | 12    | 9      | 3     |
| **Итого**      | 52    | 40     | 12    |

Все тесты на корректных данных (целые, дробные, ноль, большие значения,
перестановка сторон) прошли.

Упавшие тесты:

| Тест                                             | Вход                  | Ожидалось    | Получено                          |
|--------------------------------------------------|-----------------------|--------------|-----------------------------------|
| CircleAreaTestCase.test_negative_radius          | `area(-1)`            | `ValueError` | 3.141592653589793                 |
| CirclePerimeterTestCase.test_negative_radius     | `perimeter(-1)`       | `ValueError` | -6.283185307179586                |
| SquareAreaTestCase.test_negative_side            | `area(-3)`            | `ValueError` | 9                                 |
| SquarePerimeterTestCase.test_negative_side       | `perimeter(-3)`       | `ValueError` | -12                               |
| SquarePerimeterTestCase.test_string_side         | `perimeter('3')`      | `TypeError`  | `'3333'`                          |
| RectangleAreaTestCase.test_negative_side         | `area(-4, 5)`         | `ValueError` | -20                               |
| RectangleAreaTestCase.test_both_negative_sides   | `area(-4, -5)`        | `ValueError` | 20                                |
| RectangleAreaTestCase.test_string_side           | `area('4', 5)`        | `TypeError`  | `'44444'`                         |
| RectanglePerimeterTestCase.test_negative_side    | `perimeter(-4, 5)`    | `ValueError` | 2                                 |
| TriangleAreaTestCase.test_negative_side          | `area(-6, 4)`         | `ValueError` | -12.0                             |
| TrianglePerimeterTestCase.test_negative_side     | `perimeter(-3, 4, 5)` | `ValueError` | 6                                 |
| TrianglePerimeterTestCase.test_impossible_triangle | `perimeter(1, 2, 10)` | `ValueError` | 13                              |

Во всех случаях unittest выдал одно и то же сообщение, например:

```
FAIL: test_negative_radius (tests.test_circle.CircleAreaTestCase.test_negative_radius)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "...\geometric_lib\tests\test_circle.py", line 28, in test_negative_radius
    with self.assertRaises(ValueError):
AssertionError: ValueError not raised
```

## 8. Выводы из результатов тестирования

1. Формулы во всех четырёх модулях реализованы правильно. Для допустимых
   входных данных все 40 тестов прошли, в том числе на дробных и больших
   значениях.
2. В библиотеке нет проверки входных данных. Это главный найденный дефект,
   из-за него упали все 12 тестов. Функции молча возвращают число даже тогда,
   когда фигуры с такими размерами не существует.
3. Особенно опасны случаи, когда ответ выглядит правдоподобно. `circle.area(-1)`,
   `square.area(-3)` и `rectangle.area(-4, -5)` возвращают положительные числа,
   потому что минус на минус даёт плюс. По результату нельзя понять, что на вход
   пришли неверные данные. `triangle.perimeter(1, 2, 10)` возвращает 13, хотя
   треугольника со сторонами 1, 2 и 10 не бывает.
4. При передаче строки поведение зависит от формулы. Где строка умножается на
   целое число, Python повторяет её: `square.perimeter('3')` возвращает `'3333'`,
   а `rectangle.area('4', 5)` — `'44444'`. В остальных функциях возникает
   `TypeError`, но это заслуга самого Python, а не библиотеки.
5. Рекомендация разработчикам: добавить в начало каждой функции проверку, что
   аргументы — числа (`int` или `float`) и что они неотрицательные, а в
   `triangle.perimeter` — проверку неравенства треугольника. В случае ошибки
   выбрасывать `TypeError` или `ValueError`. После такой доработки написанные
   тесты можно запустить повторно без изменений, и они покажут, исправлен ли
   дефект.
6. Сравнивать дробные результаты нужно приближённо (`assertAlmostEqual`).
   Например, `rectangle.perimeter(0.1, 0.2)` возвращает `0.6000000000000001`,
   и это особенность чисел с плавающей точкой, а не ошибка библиотеки.

## История изменений

| Хеш коммита | Описание изменения |
|-------------|--------------------|
| c55e91b | Добавлен новый файл rectangle.py с функциями площади и периметра прямоугольника |
| e37d566 | Исправлена ошибка в вычислении периметра в rectangle.py, добавлен файл triangle.py |
| d874a56 | Ко всем функциям библиотеки добавлены комментарии с описанием и примером вызова |
| 57988e0 | Добавлена документация проекта в каталог docs |
| b6cdcae | Добавлены unit-тесты для круга, квадрата, прямоугольника и треугольника (каталог tests) |
| —       | Добавлен отчёт о тестировании (этот файл) |
