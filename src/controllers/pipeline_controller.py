from typing import Dict, Any
from PIL import Image

from models.pipeline import Pipeline, PipelineStep
from controllers.image_controller import ImageController
from services.pipeline_executor import execute_pipeline


class PipelineController:
    def __init__(self, image_controller: ImageController, pipeline: Pipeline):
        self.image_controller = image_controller
        self.pipeline = pipeline

    def add_step(self, category: str, method: str, params: Dict[str, Any] | None = None) -> None:
        self.pipeline.add_step(PipelineStep(category=category, method=method, params=params or {}))

    def delete_step(self, index: int) -> None:
        self.pipeline.delete_step(index)

    def move_up(self, index: int) -> None:
        self.pipeline.move_up(index)

    def move_down(self, index: int) -> None:
        self.pipeline.move_down(index)

    def run(self, base_image: Image.Image) -> Image.Image:
        return execute_pipeline(self.image_controller, self.pipeline, base_image)

    def save(self) -> None:
        self.pipeline.save_snapshot()

    def revert(self) -> None:
        self.pipeline.revert_to_snapshot()
