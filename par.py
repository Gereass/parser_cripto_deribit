

import subprocess

# Список файлов, которые нужно запустить
# files = ['parser_1_v2_0.py', 'parser_1_v2_1.py', 'parser_1_v2_2.py', 'parser_1_v2_3.py']
files = [ 'parser_1_v2_2.py', 'parser_1_v2_3.py']

# Создаем список процессов
processes = []

for file in files:
    # Запускаем каждый файл в своем процессе
    process = subprocess.Popen(['python', file])
    processes.append(process)

# Ждем завершения всех процессов
for process in processes:
    process.wait()
