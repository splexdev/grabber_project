# Grabber Project

Um grabber educacional para coletar informações do sistema, tokens do Discord, histórico do navegador e capturas de tela em um ambiente controlado (máquina virtual). É configurável via um script interativo, permitindo escolher quais dados coletar, se salvar a captura de tela localmente, e personalizar o executável (nome e ícone). Todos os dados são enviados a um webhook do Discord em formato de texto (ou anexo para a captura de tela). **Uso exclusivo para testes éticos.**

## Pré-requisitos
- Python 3.x
- Máquina virtual (ex.: VirtualBox, VMware)
- Conta de teste do Discord
- Navegador Chrome instalado
- Arquivo de ícone `.ico` para o executável (opcional)

## Instalação
1. Clone o projeto ou crie a estrutura de pastas.
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```