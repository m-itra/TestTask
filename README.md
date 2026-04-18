# Поиск минимальной IP-сети

Утилита определяет наименьшую общую сеть для двух IP-адресов.
Поддерживаются адреса форматов IPv4 и IPv6.

## Запуск

#### С аргументами командной строки:

IPv4:

```bash
python main.py 192.168.1.1 192.168.1.254
```

Результат:

```text
Network: 192.168.1.0/24
Mask:    255.255.255.0
```

IPv6:

```bash
python main.py 2001:db8::1 2001:db8::ff
```

Результат:

```text
Network: 2001:db8::/120
Mask:    ffff:ffff:ffff:ffff:ffff:ffff:ffff:ff00
```

IPv4-mapped IPv6:

```bash
python main.py ::ffff:192.168.1.1 ::ffff:192.168.1.254
```

Результат:

```text
Network: ::ffff:192.168.1.0/120
Mask:    ffff:ffff:ffff:ffff:ffff:ffff:ffff:ff00
```

#### Адреса с портом

Если адрес передан с портом, порт отбрасывается перед расчетом:

```bash
python main.py 192.168.1.1:8080 192.168.1.254:8080
python main.py [2001:db8::1]:443 [2001:db8::ff]:443
python main.py [::ffff:192.168.1.1]:443 [::ffff:192.168.1.254]:443
```

#### Если аргументы не переданы, адреса можно ввести во время работы программы

## Тесты

```bash
python -m pip install -r requirements.txt
python -m pytest -v
```
