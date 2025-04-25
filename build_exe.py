import os
import PyInstaller.__main__

def build_executable():
    """Gerar o executável com PyInstaller."""
    executable_name = "nitrogift"
    icon_path = os.path.join("icons", "custom_icon.ico")  # Caminho relativo
    
    print(f"[INFO] Iniciando geração do executável '{executable_name}'...")
    
    # Verificar se o main.py existe
    if not os.path.isfile("main.py"):
        print("[ERRO] Arquivo 'main.py' não encontrado no diretório atual.")
        return
    
    # Verificar se a pasta modules existe
    if not os.path.isdir("modules"):
        print("[ERRO] Pasta 'modules' não encontrada no diretório atual.")
        return
    
    # Argumentos do PyInstaller
    pyinstaller_args = [
        "main.py",
        f"--name={executable_name}",
        "--onefile",
        # "--noconsole",  # Comentado para depuração (exibe terminal)
        "--clean",
        "--hidden-import=pyautogui",
        "--hidden-import=PIL",
        "--hidden-import=requests",
        "--hidden-import=pyautogui._pyautogui_win",
        "--hidden-import=PIL.Image",
        "--hidden-import=base64",
        "--hidden-import=io",
        "--hidden-import=sqlite3",
        "--hidden-import=subprocess"
    ]
    
    # Adicionar ícone, se existir
    if os.path.isfile(icon_path):
        print(f"[INFO] Ícone encontrado: {icon_path}")
        pyinstaller_args.append(f"--icon={icon_path}")
    else:
        print(f"[AVISO] Ícone '{icon_path}' não encontrado. Gerando executável sem ícone.")
    
    try:
        print("[INFO] Executando PyInstaller...")
        PyInstaller.__main__.run(pyinstaller_args)
        print(f"[INFO] Executável gerado com sucesso em: dist/{executable_name}{'.exe' if os.name == 'nt' else ''}")
    except Exception as e:
        print(f"[ERRO] Falha ao gerar executável: {e}")
        print("[INFO] Verifique se todas as dependências estão instaladas (pip install -r requirements.txt).")
        print("[INFO] Certifique-se de que o PyInstaller está instalado (pip install pyinstaller).")

if __name__ == "__main__":
    build_executable()