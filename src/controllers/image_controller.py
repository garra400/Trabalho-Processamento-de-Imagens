from tkinter import messagebox
from PIL import Image
from typing import Optional

from models.image_model import ImageModel
from models.application_state import ApplicationState
from services.file_management.image_loader import load_image
from services.file_management.image_exporter import export_image as export_image_service
from services.image_processing.color_service import convert_color as svc_convert_color
from services.image_processing.filter_service import apply_filter as svc_apply_filter
from services.image_processing.edge_service import detect_edges as svc_detect_edges
from services.image_processing.binary_service import binarize as svc_binarize
from services.image_processing.morphology_service import apply_morphology as svc_apply_morphology


class ImageController:
    def __init__(self, image_model: ImageModel, app_state: ApplicationState):
        self.image_model = image_model
        self.state = app_state

    # Arquivos
    def load(self, path: str) -> None:
        self.image_model.original = load_image(path)
        self.image_model.processed = self.image_model.original.copy()

    def export(self, path: str) -> None:
        if self.image_model.processed is None:
            raise ValueError("Nenhuma imagem para exportar")
        export_image_service(self.image_model.processed, path)

    # Transformações
    def convert_color(self, conversion_type: str) -> None:
        if self.image_model.original is None:
            raise ValueError("Nenhuma imagem carregada")
        self.image_model.processed = svc_convert_color(
            self.image_model.original.copy(),
            conversion_type,
            self.state.intensity,
            self.state.iterations,
        )

    def apply_filter(self, filter_type: str, **kwargs) -> None:
        if self.image_model.original is None:
            raise ValueError("Nenhuma imagem carregada")
        self.image_model.processed = svc_apply_filter(
            self.image_model.original.copy(),
            filter_type,
            self.state.intensity,
            self.state.iterations,
            **kwargs,
        )

    def detect_edges(self, method: str, **kwargs) -> None:
        if self.image_model.original is None:
            raise ValueError("Nenhuma imagem carregada")
        self.image_model.processed = svc_detect_edges(
            self.image_model.original.copy(),
            method,
            self.state.intensity,
            **kwargs,
        )

    def binarize(self, method: str, **kwargs) -> None:
        if self.image_model.original is None:
            raise ValueError("Nenhuma imagem carregada")
        self.image_model.processed = svc_binarize(
            self.image_model.original.copy(),
            method,
            self.state.intensity,
            **kwargs,
        )

    def apply_morphology(self, operation: str, **kwargs) -> None:
        if self.image_model.original is None:
            raise ValueError("Nenhuma imagem carregada")
        self.image_model.processed = svc_apply_morphology(
            self.image_model.original.copy(),
            operation,
            self.state.intensity,
            self.state.iterations,
            **kwargs,
        )

    # Estado
    def save_modifications(self) -> None:
        if self.image_model.processed is not None:
            self.image_model.original = self.image_model.processed.copy()

    def reset_image(self) -> None:
        if self.image_model.original is not None:
            self.image_model.processed = self.image_model.original.copy()
