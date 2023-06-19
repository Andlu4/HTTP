import socket
import os
from sys import argv

ip = argv[1]
port = int(argv[2])
directory = argv[3]

def respostaDiretorio():
    files = os.listdir(directory)
    html = '<html><body>'
    for filesName in files:
        filesPath = os.path.join(directory, filesName)
        if os.path.isfile(filesPath):
            html += f'<a href="/{filesName}">{filesName}</a><br>'
    html += '</body></html>'
    return f'HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n{html}'.encode('utf-8')

def respostaHeader(header):
    html = '<html><body><p>' 
    html += header
    html += '</p></body></html>'
    return f'HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n{html}'.encode('utf-8')

def respostaArquivo(filesPath):
    if os.path.isfile(filesPath):
        with open(filesPath, 'rb') as file:
            fileData = file.read()
        filesName = os.path.basename(filesPath)
        headers = f'HTTP/1.1 200 OK\r\nContent-type: application/octet-stream\r\nContent-Disposition: attachment; filename="{filesName}"\r\n\r\n'
        return headers.encode('utf-8') + fileData
    else:
        return 'HTTP/1.1 404 Not Found\r\n\r\n Pagina não encontrada.'.encode('utf-8')

def acessoIP(socketReceptor):
    pedidoData = socketReceptor.recv(1024)
    pedido0 = pedidoData.decode('utf-8')
    pedido1 = pedido0.split('\r\n')
    _ , caminhoPedido, _ = pedido1[0].split(' ')
    print(caminhoPedido)
    print(caminhoPedido == '/')
    if caminhoPedido == '/':
        response = respostaDiretorio()
    elif caminhoPedido == '/HEADER':
        response = respostaHeader(pedido0)
    else:
        filesPath = os.path.join(directory, caminhoPedido[1:])
        response = respostaArquivo(filesPath)
    
    if type(response) is str:
        response = response.encode()
    print(type(response))
    socketReceptor.sendall(response)
    socketReceptor.close()

socketOrigem = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketOrigem.bind((ip, port))
socketOrigem.listen(1)
print(f'Servidor rodando na porta {port}')

while True:
    socketReceptor, _ = socketOrigem.accept()
    acessoIP(socketReceptor)
