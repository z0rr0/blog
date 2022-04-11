# Храните деньги в… #blog

## Немного истории

### Как десятичные числа хранятся в компьютерах


## Как же хранить деньги

## Типичные ошибки с деньгами

## Выводы


IEEE754 1985

Примеры

```python
>>> 0.1+0.11
0.21000000000000002

>>> 1.3+1.6
2.9000000000000004
```

На Go

```go
fmt.Printf("%.6f", float32(1.3+1.6)) // 2.9000000
fmt.Printf("%.9f", float32(1.3+1.6)) // 2.900000095
fmt.Printf("%.15f", float32(1.3+1.6)) // 2.900000095367432
fmt.Printf("%.25f", float32(1.3+1.6)) // 2.9000000953674316406250000

// ещё немного "магии"
fmt.Printf("%f", float32(16777217.0)) // 16777216.000000
```

## Ссылки


1. [754-2019 - IEEE Standard for Floating-Point Arithmetic](https://ieeexplore.ieee.org/document/8766229)
2. [The IEEE 754 Format](http://mathcenter.oxford.emory.edu/site/cs170/ieee754/)
3. [Single-precision floating-point format](https://en.wikipedia.org/wiki/Single-precision_floating-point_format)
4. Журал "Хакер" статья ["Всё, точка, приплыли! Учимся работать с числами с плавающей точкой и разрабатываем альтернативу с фиксированной точностью десятичной дроби"](https://xakep.ru/2015/01/01/vsyo-tochka-priplyli/). [Версия](https://habr.com/ru/company/xakep/blog/257897/) для Хабра.
5. Генри С. Уоррен ["Алгоритмические трюки для программистов"](http://www.williamspublishing.com/Books/978-5-8459-1838-3.html), 2-е издание (Henry Warren ["Hacker's Delight, 2nd Edition"](https://www.amazon.com/Hackers-Delight-2nd-Henry-Warren/dp/0321842685))
6. YouTube ["Как работают числа с плавающей точкой"](https://www.youtube.com/watch?v=U0U8Ddx4TgE)
7. [github.com/shopspring/decimal](https://github.com/shopspring/decimal)
