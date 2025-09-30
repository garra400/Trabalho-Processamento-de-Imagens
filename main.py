#!/usr/bin/env python3
"""
Ponto de entrada da aplicação modular de processamento de imagens
Trabalho Bimestral do Pedro
"""

import sys
import os
from pathlib import Path

def main():
    """Função principal da aplicação"""
    # Adicionar o diretório src ao path
    current_dir = Path(__file__).parent
    src_dir = current_dir / "src"
    sys.path.insert(0, str(src_dir))
    
    try:
        # Configurar customtkinter antes de importar a aplicação
        import customtkinter as ctk
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        
        # Importar e executar a aplicação principal
        # Primeiro, vamos tentar importar de views se existir
        try:
            from views.main_window import MainWindow
            app = MainWindow()
        except ImportError:
            # Se não existir, criar uma aplicação básica
            print("Módulo views.main_window não encontrado.")
            print("Criando aplicação básica...")
            from src.views.basic_app import BasicImageApp
            app = BasicImageApp()
        
        app.mainloop()
    
    except ImportError as e:
        print(f"Erro ao importar módulos necessários: {e}")
        print("Verifique se todas as dependências estão instaladas:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Erro na execução da aplicação: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()