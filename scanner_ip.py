import os
import platform
import socket
import concurrent.futures
import time 

def exibir_aviso_legal():
    aviso = """
╔══════════════════════════════════════════════════════════════════╗
║ ⚠️  AVISO LEGAL - USO INDEVIDO É CRIME                            ║
╠══════════════════════════════════════════════════════════════════╣
║ Este script é fornecido apenas para fins educacionais, testes    ║
║ em redes autorizadas ou ambientes de laboratório.                ║
║                                                                  ║
║ ❌ Invadir redes sem permissão é crime no Brasil:                ║
║    • Art. 154-A do Código Penal (Invasão de dispositivo)         ║
║    • Pode resultar em multa e até prisão.                        ║
║    • Não me responsabilizo, pelo mau uso deste script            ║
║                                                                  ║
║ ✅ Use este código apenas em redes que você tem autorização!     ║
╚══════════════════════════════════════════════════════════════════╝
"""
    print(aviso)
    time.sleep(2)

def obter_ip_local():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)) 
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return None

def construir_comando_ping(ip):
    if platform.system() == "Windows":
        return f"ping -n 1 -w 1000 {ip} > nul"
    else:
        return f"ping -c 1 -W 1 {ip} > /dev/null"

def verificar_ip(ip):
    comando = construir_comando_ping(ip)
    resposta = os.system(comando)
    if resposta == 0:
        return ip
    return None

def escanear_subrede(subrede_base, inicio=1, fim=254):
    ativos = []
    print(f"Escaneando sub-rede {subrede_base}.x de {inicio} a {fim}...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futuros = [executor.submit(verificar_ip, f"{subrede_base}.{i}") for i in range(inicio, fim + 1)]
        for futuro in concurrent.futures.as_completed(futuros):
            resultado = futuro.result()
            if resultado:
                ativos.append(resultado)
                print(f"Ativo: {resultado}")
    return ativos

def testar_porta(ip, port):
    try:
        s = socket.socket()
        s.settimeout(0.5)
        s.connect((ip, port))
        print(f"[+] {ip}:{port} PORTA ABERTA")
        s.close()
    except:
      
        #print(f"{ip}:{port} FECHADA")
        pass  

if __name__ == "__main__":
    exibir_aviso_legal()
    ip_local = obter_ip_local()
    if not ip_local:
        print("Não foi possível detectar o IP local.")
        exit(1)

    subrede_base = ".".join(ip_local.split(".")[:3])  
    ativos = escanear_subrede(subrede_base)

    print("\nIPs Ativos Encontrados:")
    for ip in ativos:
        print(ip)

    # Teste as portas
    portas = [80, 81, 554, 8000, 8080, 8888, 5000, 37777]

    for ip in ativos:
        print(f"\n🔍 Testando IP: {ip}...")
        for porta in portas:
            testar_porta(ip, porta)