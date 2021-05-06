# task_1
words = ["разработка", "сокет", "декоратор"]

words_unicode = [
    "\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430",
    "\u0441\u043e\u043a\u0435\u0442",
    "\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440",
]

for i in words:
    print(type(i), i)

for i in words_unicode:
    print(type(i), i)

print("И формат unicode и str имеют тип 'str'")

# task_2

b_type = [b"class", b"function", b"method"]
for i in b_type:
    print(f"ТИП: {type(i)} Содержимое: {i} Длина: {len(i)}")

# решение с помощью приведения типов
b_type = ["class", "function", "method"]
for i in b_type:
    print(bytes(i, encoding="utf-8"), len(bytes(i, encoding="utf-8")), type(bytes(i, encoding="utf-8")))

# task_3

# Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в
# байтовом типе.

# word_1 = b"attribute"
# word_2 = b"класс"    # SyntaxError: bytes can only contain ASCII literal characters
# word_3 = b"функция"  # SyntaxError: bytes can only contain ASCII literal characters
# word_4 = b"type"

# Синтаксическая ошибка: байты могут содержать только литеральные символы ASCII

# task_4

task_4 = ["разработка", "администрирование", "protocol", "standard"]
task_4_encode = [word.encode("utf-8") for word in task_4]
# print(task_4_encode)
task_4_decode = [word.decode("utf-8") for word in task_4_encode]
# print(task_4_decode)

# task_5

import subprocess

args = ["ping", "yandex.ru"]
subprocess_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
for line in subprocess_ping.stdout:
    l = line.decode("cp866").encode("utf-8")
    print(l.decode("utf-8"), end="")


args = ["ping", "youtube.com"]
subprocess_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
for line in subprocess_ping.stdout:
    l = line.decode("cp866").encode("utf-8")
    print(l.decode("utf-8"), end="")

# task_6

lines = ["сетевое программирование", "сокет", "декоратор"]
with open("test_file.txt", "w") as f:
    f.writelines("%s\n" % line for line in lines)

print(f"Тип кодировки по умолчанию: {f}")

with open("test_file.txt", "r", encoding="utf-8", errors="replace") as f:
    lines = f.readlines()
    for line in lines:
        print(line.strip())

# на win Тип кодировки по умолчанию: <_io.TextIOWrapper name='test_file.txt' mode='w' encoding='cp1251'>
# при открытии в utf-8 выводит ������� ���������������� такие знаки
