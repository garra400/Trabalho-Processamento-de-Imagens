from PIL import Image

from models.pipeline import Pipeline
from controllers.image_controller import ImageController
from services.image_processing.color_service import convert_color as svc_convert_color
from services.image_processing.filter_service import apply_filter as svc_apply_filter
from services.image_processing.edge_service import detect_edges as svc_detect_edges
from services.image_processing.binary_service import binarize as svc_binarize
from services.image_processing.morphology_service import apply_morphology as svc_apply_morphology


def execute_pipeline(controller: ImageController, pipeline: Pipeline, base_image: Image.Image) -> Image.Image:
    """Executa o pipeline de forma pura, sem mutar o estado do controller.

    - Usa a imagem base fornecida como ponto de partida
    - Aplica cada etapa em sequência atualizando uma variável local
    - Retorna a imagem final sem alterar image_model.original/processado
    """
    current = base_image.copy()
    intensity = controller.state.intensity
    iterations = controller.state.iterations

    for step in pipeline.steps:
        category = step.category
        method = step.method
        params = step.params or {}

        if category == "color":
            current = svc_convert_color(current, method, intensity=intensity, iterations=iterations)
        elif category == "filter":
            current = svc_apply_filter(current, method, intensity=intensity, iterations=params.get("iterations", iterations), radius=params.get("radius"))
        elif category == "edge":
            current = svc_detect_edges(current, method, intensity=intensity, **params)
        elif category == "binary":
            current = svc_binarize(current, method, intensity=intensity, **params)
        elif category == "morphology":
            current = svc_apply_morphology(current, method, intensity=intensity, iterations=params.get("iterations", iterations), kernel_size=params.get("kernel_size"))
        else:
            # Categoria desconhecida: ignorar
            continue

    return current
