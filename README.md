# Pedro Modularizado - Processamento de Imagens

## Estrutura do Projeto

Este projeto é uma versão modular do `codigofinal3.py`, organizando o código em uma arquitetura limpa e escalável.

### Organização das Pastas

```
PedroModularizado/
├── src/                                # Código fonte principal
│   ├── config/                        # Configurações da aplicação
│   │   ├── __init__.py
│   │   ├── settings.py                # Configurações gerais (cores, tamanhos, etc.)
│   │   └── constants.py               # Constantes da aplicação
│   │
│   ├── models/                        # Modelos de dados
│   │   ├── __init__.py
│   │   ├── image_model.py             # Modelo para representar imagens
│   │   └── application_state.py       # Estado da aplicação
│   │
│   ├── services/                      # Lógica de negócio
│   │   ├── __init__.py
│   │   ├── image_processing/          # Serviços de processamento
│   │   │   ├── __init__.py
│   │   │   ├── color_service.py       # Conversões de cor
│   │   │   ├── filter_service.py      # Aplicação de filtros
│   │   │   ├── edge_service.py        # Detecção de bordas
│   │   │   ├── binary_service.py      # Binarização
│   │   │   └── morphology_service.py  # Operações morfológicas
│   │   │
│   │   └── file_management/           # Gerenciamento de arquivos
│   │       ├── __init__.py
│   │       ├── image_loader.py        # Carregamento de imagens
│   │       └── image_exporter.py      # Exportação de imagens
│   │
│   ├── controllers/                   # Controladores (MVC)
│   │   ├── __init__.py
│   │   ├── main_controller.py         # Controlador principal
│   │   └── image_controller.py        # Controlador de imagens
│   │
│   ├── views/                         # Interface do usuário
│   │   ├── __init__.py
│   │   ├── components/                # Componentes reutilizáveis
│   │   │   ├── __init__.py
│   │   │   ├── navigation_frame.py    # Frame de navegação
│   │   │   ├── image_preview.py       # Preview de imagens
│   │   │   ├── intensity_toolbar.py   # Toolbar de intensidade
│   │   │   └── file_list.py           # Lista de arquivos
│   │   │
│   │   ├── pages/                     # Páginas da aplicação
│   │   │   ├── __init__.py
│   │   │   ├── import_page.py         # Página de importação
│   │   │   ├── color_page.py          # Página de cores
│   │   │   ├── filter_page.py         # Página de filtros
│   │   │   ├── edge_page.py           # Página de bordas
│   │   │   ├── binary_page.py         # Página de binarização
│   │   │   └── morphology_page.py     # Página de morfologia
│   │   │
│   │   └── main_window.py             # Janela principal
│   │
│   └── utils/                         # Utilitários
│       ├── __init__.py
│       ├── image_utils.py             # Utilitários para imagens
│       └── ui_utils.py                # Utilitários para UI
│
├── assets/                            # Recursos da aplicação
│   └── icons/                         # Ícones
│       ├── icone.png
│       └── icone.ico
│
├── tests/                             # Testes unitários
│   ├── __init__.py
│   ├── test_services/
│   ├── test_controllers/
│   └── test_utils/
│
├── docs/                              # Documentação
│   ├── README.md
│   └── API.md
│
├── main.py                            # Ponto de entrada da aplicação
└── requirements.txt                   # Dependências do projeto
```

### Funcionalidades por Módulo

#### Services (Serviços)
- **color_service.py**: Conversões RGB↔HSV, escala de cinza, etc.
- **filter_service.py**: Blur, sharpen, noise reduction, etc.
- **edge_service.py**: Canny, Sobel, Laplacian, Roberts
- **binary_service.py**: Threshold, Otsu, adaptativo
- **morphology_service.py**: Erosão, dilatação, abertura, fechamento

#### Views (Interface)
- **navigation_frame.py**: Menu lateral de navegação
- **image_preview.py**: Visualização de imagens
- **intensity_toolbar.py**: Controles de intensidade e iterações
- Páginas específicas para cada funcionalidade

#### Controllers (Controladores)
- **main_controller.py**: Coordena toda a aplicação
- **image_controller.py**: Gerencia estado das imagens

#### Models (Modelos)
- **image_model.py**: Representa uma imagem e suas propriedades
- **application_state.py**: Estado global da aplicação

### Como Desenvolver

1. **Configurações**: Modifique `src/config/settings.py`
2. **Processamento**: Adicione novos algoritmos em `src/services/image_processing/`
3. **Interface**: Crie novos componentes em `src/views/components/`
4. **Páginas**: Adicione novas páginas em `src/views/pages/`
5. **Utilitários**: Funções auxiliares em `src/utils/`

### Vantagens da Arquitetura Modular

- **Separação de Responsabilidades**: Cada módulo tem uma função específica
- **Reutilização**: Componentes podem ser reutilizados
- **Manutenibilidade**: Código mais fácil de manter e debuggar
- **Testabilidade**: Cada módulo pode ser testado independentemente
- **Escalabilidade**: Fácil adicionar novas funcionalidades# Trabalho-Processamento-de-Imagens
