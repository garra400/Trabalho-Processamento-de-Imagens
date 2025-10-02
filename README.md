# Processamento de Imagens (App Modular + Vetor de Modificações)

Aplicativo de processamento de imagens com interface em CustomTkinter, arquitetura modular e um Vetor de Modificações (pipeline) que encadeia transformações de forma pura a partir da imagem original.

## Organização das Pastas (real)

```
Trabalho-Processamento-de-Imagens/
├── main.py
├── requirements.txt
├── README.md
├── cofigofinal3.py
└── src/
	├── config/
	├── controllers/
	├── models/
	├── services/
	├── utils/
	└── views/
```

Diretórios principais:
- src/config: settings e constants
- src/models: image_model, application_state, pipeline
- src/controllers: image_controller e pipeline_controller
- src/services: image_processing/*, file_management/* e pipeline_executor (execução pura do vetor)
- src/views: main_window (UI principal) e basic_app (fallback)

## Como executar

```powershell
python -m venv venv
./venv/Scripts/Activate.ps1
pip install -r requirements.txt
python .\main.py
```

## Fluxo e Semântica do Vetor

- O Vetor de Modificações é uma lista ordenada de etapas que SEMPRE é aplicada sobre a imagem original (execução pura, sem efeitos colaterais).
- A cada mudança no vetor (adicionar, remover, reordenar), o resultado é recalculado imediatamente.
- Se o vetor estiver vazio, a base exibida é a imagem original.

Na aba Vetor:
- Salvar Vetor: salva um snapshot das etapas para uso do “Reverter Vetor”. Não altera a imagem original importada.
- Reverter Vetor: volta ao snapshot salvo e recalcula o resultado.
- Exportar: exporta o resultado atual do vetor.

Nas abas de operação (Cor, Filtros, Bordas, Binarização, Morfologia):
- O seletor começa em “Selecione…”. Enquanto estiver assim, a prévia exibe apenas a base atual (vetor → ou original se vetor vazio).
- Ao escolher a técnica, a prévia aplica a transformação sobre a base.
- Salvar Modificações: adiciona a técnica atual ao vetor e salva snapshot (para reverter depois). O original não é alterado.
- Resetar: volta a prévia para a base do momento (resultado do vetor, ou original quando vazio).

## Funcionalidades por Módulo

#### Services (Serviços)
- **color_service.py**: Conversões RGB↔HSV, escala de cinza, etc.
- **filter_service.py**: Blur, sharpen, noise reduction, etc.
- **edge_service.py**: Canny, Sobel, Laplacian, Roberts
- **binary_service.py**: Threshold, Otsu, adaptativo
- **morphology_service.py**: Erosão, dilatação, abertura, fechamento

#### Views (Interface)
- `main_window.py`: navegação, prévias, controles dinâmicos e aba do vetor
- `basic_app.py`: fallback simples

#### Controllers (Controladores)
- **image_controller.py**: Gerencia estado das imagens
- **pipeline_controller.py**: Gerencia etapas do vetor, snapshots e execução

#### Models (Modelos)
- **image_model.py**: Representa uma imagem e suas propriedades
- **application_state.py**: Estado global da aplicação
 - **pipeline.py**: Passos do vetor, snapshot/revert

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
- **Escalabilidade**: Fácil adicionar novas funcionalidades
