import socket

def obtener_ip_local():
    try:
        # Truco para obtener la IP real conectada a la red (no localhost)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"