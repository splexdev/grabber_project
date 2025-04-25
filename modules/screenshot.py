import pyautogui
import base64
import io
import os

def take_screenshot(save_locally=False):
    """Capturar a tela e retornar como base64 ou salvar localmente."""
    print("[INFO] Iniciando captura de tela...")
    try:
        screenshot = pyautogui.screenshot()
        print("[INFO] Screenshot capturado com sucesso.")
        
        if save_locally:
            print("[INFO] Salvando screenshot localmente em 'output/screenshot.png'...")
            os.makedirs("output", exist_ok=True)
            screenshot_path = "output/screenshot.png"
            screenshot.save(screenshot_path)
            print(f"[INFO] Screenshot salvo em: {screenshot_path}")
            return screenshot_path
        else:
            print("[INFO] Convertendo screenshot para base64...")
            buffer = io.BytesIO()
            screenshot.save(buffer, format="PNG")
            screenshot_base64 = base64.b64encode(buffer.getvalue()).decode()
            print("[INFO] Screenshot convertido para base64 com sucesso.")
            return screenshot_base64
    except Exception as e:
        print(f"[ERRO] Falha ao capturar screenshot: {e}")
        return None