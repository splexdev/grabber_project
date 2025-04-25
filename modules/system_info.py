import getpass
import socket
import platform
from datetime import datetime

def get_system_info():
    """Coletar informações básicas do sistema."""
    return {
        "Username": getpass.getuser(),
        "Hostname": socket.gethostname(),
        "IP Address": socket.gethostbyname(socket.gethostname()),
        "OS": f"{platform.system()} {platform.release()}",
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }