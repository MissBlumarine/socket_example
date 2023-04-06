import socket
from views import blog, index

URLS = {
    '/': index,
    '/blog': blog
}


def parse_request(request):
    parsed = request.split(' ')
    method = parsed[0]
    url = parsed[1]
    return (method, url)


def generate_headers(method, url):
    if not method == 'GET':
        return ('HTTP/1.1 405 method not allowedn\n\n', 405)

    if not url in URLS:
        return ('HTTP/1.1 404 not found\n\n', 404)

    return ('HTTP/1.1 200 OK\n\n', 200)


def generate_content(code, url):
    if code == 404:
        return '<h1>404</h1><p>Not Found</p>'
    if code == 405:
        return '<h1>405</h1><p>Method Not Allowed</p>'
    return URLS[url]()


def generate_response(request):
    method, url = parse_request(request)
    headers, code = generate_headers(method, url)
    body = generate_content(code, url)

    return (headers + body).encode()


def run():
    # принимает запросы субьект server_socker
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # нужно связать субъекта с конкретным адресом (например, localhost) и портом
    server_socket.bind(('localhost', 5000))

    # даем серверу указанию для начала прослушивания вышеуказанного порта
    server_socket.listen()

    while True:
        # сервер получает что-то от клиента, исп-ся метод accept
        # наш сервер получает в методе accept кортеж, в котором указан клиент и его адрес
        client_socket, addr = server_socket.accept()

        # чтобы увидеть созданный клиентом запрос
        request = client_socket.recv(1024)
        # print(request.decode('utf-8'))
        print(request)
        print(f'address: {addr}')

        response = generate_response(request.decode('utf-8'))

        client_socket.sendall(response)
        client_socket.close()


if __name__ == '__main__':
    run()
