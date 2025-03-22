import socket

# Список IP-адресов
targets = ["192.168.1.1", "scanme.nmap.org"]  # Замени на реальные IP

# Порты, которые будем проверять
ports = [22, 80, 443]  # SSH, HTTP, HTTPS

for target in targets:
    print(f"Scanning {target}...")
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Тайм-аут 1 секунда
        result = sock.connect_ex((target, port))  # Проверяем порт
        if result == 0:
            print(f"  [OPEN] Port {port}")
        sock.close()
