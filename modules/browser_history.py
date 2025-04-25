import os
import sqlite3
import platform
import subprocess

def get_browser_history():
    """Coletar todo o histórico do Chrome e salvar em um arquivo .txt."""
    print("[INFO] Iniciando coleta do histórico do navegador...")
    
    # Caminho do arquivo de histórico do Chrome
    history_path = os.path.join(
        os.getenv("LOCALAPPDATA"),
        "Google",
        "Chrome",
        "User Data",
        "Default",
        "History"
    ) if platform.system() == "Windows" else os.path.expanduser("~/Library/Application Support/Google/Chrome/Default/History")
    
    print(f"[INFO] Caminho do histórico: {history_path}")
    
    # Verificar se o arquivo existe
    if not os.path.exists(history_path):
        print(f"[ERRO] Arquivo de histórico não encontrado: {history_path}")
        return ["Arquivo de histórico não encontrado"]
    
    # Tentar fechar o Chrome para liberar o arquivo
    print("[INFO] Tentando fechar o Chrome para liberar o banco de dados...")
    try:
        if platform.system() == "Windows":
            subprocess.run(["taskkill", "/IM", "chrome.exe", "/F"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            subprocess.run(["pkill", "Google Chrome"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("[INFO] Chrome fechado com sucesso.")
    except Exception as e:
        print(f"[AVISO] Falha ao fechar o Chrome: {e}")
        print("[INFO] Continuando mesmo assim...")
    
    # Criar a pasta output, se não existir
    os.makedirs("output", exist_ok=True)
    output_file = "output/browser_history.txt"
    
    try:
        # Conectar ao banco de dados do Chrome
        print("[INFO] Conectando ao banco de dados do Chrome...")
        conn = sqlite3.connect(f"file:{history_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        
        # Coletar todo o histórico
        print("[INFO] Coletando todo o histórico do navegador...")
        cursor.execute("SELECT url, title, visit_count, last_visit_time FROM urls ORDER BY last_visit_time DESC")
        history = cursor.fetchall()
        
        if not history:
            print("[INFO] Nenhum histórico encontrado.")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("Nenhum histórico encontrado.")
            return output_file
        
        # Salvar o histórico em um arquivo .txt
        print(f"[INFO] Salvando histórico em {output_file}...")
        with open(output_file, "w", encoding="utf-8") as f:
            for entry in history:
                url, title, visit_count, last_visit_time = entry
                f.write(f"URL: {url}\n")
                f.write(f"Título: {title or 'Sem título'}\n")
                f.write(f"Contagem de Visitas: {visit_count}\n")
                f.write(f"Última Visita (timestamp): {last_visit_time}\n")
                f.write("-" * 50 + "\n")
        
        print(f"[INFO] Histórico salvo com sucesso em {output_file}.")
        conn.close()
        return output_file
    
    except Exception as e:
        print(f"[ERRO] Erro ao acessar histórico: {e}")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"Erro ao acessar histórico: {e}")
        return output_file