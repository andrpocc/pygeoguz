## PyGeoGUZ
Решение задач геодезии на языке Python. Пакет содержит 5 модулей:

- **simplegeo** - Основные и вспомогательные функции, используемые в геодезических вычислениях
- **adjustment** - Реализация общего параметрического метода уравнивания по методу наименьших квадратов в матричной форме
- **transform** - Преобразование координат между эллипсоидами ПЗ-90 и WGS84, пересчет в проекцию Гаусса-Крюгера
- **highergeo** - Реализация прямой геодезической задачи на сфере
- **objects** - Вспомогательный модуль с классами объектов точек, линий и углов

## Установка

	pip install pygeoguz

### Модуль simplegeo:

##### 1. Прямая геодезическая задача
```python
from pygeoguz.simplegeo import *
from pygeoguz.objects import *

p1 = Point2D(x=10, y=10)
line = Line2D(length=10, direction=45)
p2 = pgz(point=p1, line=line)

x = p2.x
y = p2.y
```
#### 2. Обратная геодезическая задача
```python
from pygeoguz.simplegeo import *
from pygeoguz.objects import *

p1 = Point2D(x=10, y=10)
p2 = Point2D(x=50, y=50)
line = ogz(point_a=p1, point_b=p2)

length = line.length
direction = line.direction
```
#### 3. Площадь полигона по формуле Гаусса
```python
from pygeoguz.simplegeo import *
from pygeoguz.objects import *

p1 = Point2D(x=10, y=10)
p2 = Point2D(x=20, y=20)
p3 = Point2D(x=15, y=30)

points = [p1, p2, p3]
square = polygon_square(points=points)
```
#### 4. Координаты точки пересечения двух линий
#### 5. Координаты середины отрезка
#### 6. degrees, minutes, seconds -> degrees
```python
from pygeoguz.simplegeo import *
from pygeoguz.objects import *

angle = Angle(degrees=54, minutes=14, seconds=16.5)
angle_degrees = to_degrees(angle=angle)
```
#### 7. degrees -> degrees, minutes, seconds
```python
from pygeoguz.simplegeo import *

angle_degrees = 34.66885435
angle = to_dms(degrees=angle_degrees, n_sec=1)

degrees = angle.degrees
minutes = angle.minutes
seconds = angle.seconds
```
#### 8. Вычисление верного значения угла
```python
from pygeoguz.simplegeo import *

angle_degrees = 367.66885435
true_ang = true_angle(angle=angle_degrees, max_value=360)
```
#### 9. hours -> degrees
```python
from pygeoguz.simplegeo import *

hours = 11.5
degrees = from_h_to_d(hours=hours)
```
#### 10. degrees -> hours
```python
from pygeoguz.simplegeo import *

degrees = 58.8431144
hours = from_d_to_h(degrees=degrees)
```
#### 11. Генерация псевдослучайных погрешностей измерений
```python
from pygeoguz.simplegeo import *

mu = 2  # Среднее квадратическое отклонение
count_of_errors = 15
errors = generate_errors(mu=mu, count=count_of_errors)
```
#### 12. Округление по Гауссу
```python
from pygeoguz.simplegeo import *

number = 2.345
n = ground(number=number, n=2)
#  print -> 2.34
```
#### 13. Вычисление левых горизонтальных углов хода

### Модуль adjustment:
1. Параметрический метод уравнивания с оценкой точности
2. Уравнивание теодолитного хода раздельным методом

### Модуль transform:
1. Преобразование координат ПЗ90 -> WGS84
2. Преобразование координат WGS84 -> ПЗ90 
3. Преобразование координат Геодезические -> Плоские в проекции Гаусса-Крюгера 
4. Преобразование координат Плоские в проекции Гаусса-Крюгера -> Геодезические

### Модуль higherGeo 
1. Прямая геодезическая задача на сфере