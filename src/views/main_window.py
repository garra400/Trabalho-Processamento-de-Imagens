import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image

from config.settings import APP_TITLE, APP_GEOMETRY
from config.constants import SUPPORTED_IMAGE_TYPES, EXPORT_TYPES, PREVIEW_MAX_SIZE
from models.image_model import ImageModel
from models.application_state import ApplicationState
from controllers.image_controller import ImageController
from models.pipeline import Pipeline
from controllers.pipeline_controller import PipelineController
from services.image_processing.color_service import convert_color as svc_convert_color
from services.image_processing.filter_service import apply_filter as svc_apply_filter
from services.image_processing.edge_service import detect_edges as svc_detect_edges
from services.image_processing.binary_service import binarize as svc_binarize
from services.image_processing.morphology_service import apply_morphology as svc_apply_morphology


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)

        # Modelos e controlador
        self.image_model = ImageModel()
        self.app_state = ApplicationState()
        self.controller = ImageController(self.image_model, self.app_state)
        self.pipeline = Pipeline()
        self.pipeline_controller = PipelineController(self.controller, self.pipeline)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "")
        try:
            from PIL import Image as PILImage
            self.logo_image = ctk.CTkImage(PILImage.open(os.path.join(image_path, "icone.png")), size=(26, 26))
        except Exception:
            self.logo_image = None

        # Frame de navegação
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0, width=180, fg_color=("gray75", "gray25"))
        self.navigation_frame.grid(row=0, column=0, sticky="ns")
        self.navigation_frame.grid_rowconfigure(8, weight=1)

        # Frame principal
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=("gray90", "gray15"))
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Cabeçalho
        self.nav_frame_label = ctk.CTkLabel(
            self.navigation_frame,
            text="  Processamento de Imagens  ",
            image=self.logo_image,
            compound="left",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.nav_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # Botões
        self.create_navigation_buttons()

        # Páginas
        self.create_all_pages()

        self.selected_frame_name = "import"
        self.select_frame_by_name("import")

    # Navegação
    def create_navigation_buttons(self):
        buttons_config = [
            ("import", "Importar Imagem", 1),
            ("pipeline", "Vetor de Modificações", 2),
            ("color", "Conversão de Cor", 3),
            ("filter", "Filtros", 4),
            ("edge", "Detector de Borda", 5),
            ("binary", "Binarização", 6),
            ("morphology", "Morfologia", 7),
        ]

        self.nav_buttons = {}
        for name, text, row in buttons_config:
            button = ctk.CTkButton(
                self.navigation_frame,
                corner_radius=0,
                height=40,
                border_spacing=10,
                text=text,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                anchor="w",
                command=lambda n=name: self.select_frame_by_name(n),
            )
            button.grid(row=row, column=0, sticky="ew", padx=5, pady=2)
            self.nav_buttons[name] = button

    def create_all_pages(self):
        self.import_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.color_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.filter_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.edge_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.binary_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.morphology_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.pipeline_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")

        self.setup_import_page()
        self.setup_color_page()
        self.setup_filter_page()
        self.setup_edge_page()
        self.setup_binary_page()
        self.setup_morphology_page()
        self.setup_pipeline_page()

    def setup_import_page(self):
        self.import_frame.grid_rowconfigure(0, weight=1)
        self.import_frame.grid_rowconfigure(1, weight=0)
        self.import_frame.grid_rowconfigure(2, weight=0)
        self.import_frame.grid_rowconfigure(3, weight=0)
        self.import_frame.grid_columnconfigure(0, weight=1)

        self.import_image_area = ctk.CTkFrame(self.import_frame, fg_color=("gray95", "gray10"))
        self.import_image_area.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        self.import_image_area.grid_rowconfigure(0, weight=1)
        self.import_image_area.grid_columnconfigure(0, weight=1)

        self.import_image_label = ctk.CTkLabel(
            self.import_image_area,
            text="Clique em 'Abrir' para selecionar uma imagem",
            font=ctk.CTkFont(size=16),
        )
        self.import_image_label.grid(row=0, column=0)

        toolbar = ctk.CTkFrame(self.import_frame, height=48, fg_color=("gray90", "gray15"))
        toolbar.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        toolbar.grid_columnconfigure(3, weight=1)

        ctk.CTkButton(toolbar, text="Abrir", command=self.open_image).grid(row=0, column=0, padx=(10, 6), pady=8)
        ctk.CTkButton(toolbar, text="Exportar", command=self.export_image).grid(row=0, column=1, padx=6, pady=8)

        self.import_files_strip = ctk.CTkScrollableFrame(self.import_frame, height=120, fg_color=("gray92", "gray18"))
        self.import_files_strip.grid(row=2, column=0, sticky="nsew", padx=10, pady=(5, 10))
        self.import_files_strip.grid_columnconfigure(0, weight=1)

    def setup_pipeline_page(self):
        def create_pipeline_controls(parent):
            parent.grid_columnconfigure(0, weight=1)
            # Lista de etapas
            self.pipeline_list = ctk.CTkScrollableFrame(parent, fg_color=("gray92", "gray18"))
            self.pipeline_list.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
            self.pipeline_list.grid_columnconfigure(0, weight=1)

            # Barra de ações
            actions = ctk.CTkFrame(parent, height=48, fg_color=("gray90", "gray15"))
            actions.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))
            actions.grid_columnconfigure((0, 1, 2), weight=1)

            ctk.CTkButton(actions, text="Salvar Vetor", command=self.on_pipeline_save).grid(row=0, column=0, padx=6, pady=8)
            ctk.CTkButton(actions, text="Reverter Vetor", command=self.on_pipeline_revert).grid(row=0, column=1, padx=6, pady=8)
            ctk.CTkLabel(actions, text="O resultado do vetor aparece acima.").grid(row=0, column=2, padx=6, pady=8)

        # Reutiliza o mesmo layout das outras páginas, porém com toolbar personalizada (sem 'Salvar Modificações')
        self.pipeline_image_area, self.pipeline_image_label = self.setup_processing_page(
            self.pipeline_frame, "Vetor de Modificações", create_pipeline_controls, include_default_toolbar=False
        )

        # Adiciona apenas os botões necessários na toolbar do pipeline
        toolbar = getattr(self.pipeline_frame, "_toolbar", None)
        if toolbar is not None:
            toolbar.grid_columnconfigure(10, weight=1)
            ctk.CTkButton(toolbar, text="Exportar", command=self.export_image).grid(row=0, column=0, padx=6, pady=8)
            ctk.CTkButton(toolbar, text="Resetar", command=self.on_pipeline_reset).grid(row=0, column=1, padx=6, pady=8)

    def create_intensity_toolbar(self, parent):
        # Mantido por compatibilidade, mas não é mais usado. Controles agora estão por técnica.
        pass

    def on_intensity_change(self, value):
        # Deprecated: intensidade global não é mais usada
        pass

    def on_iterations_change(self, value):
        # Deprecated: repetições globais não é mais usado
        pass

    def setup_processing_page(self, frame, title, controls_func, include_default_toolbar: bool = True):
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=0)
        frame.grid_rowconfigure(2, weight=0)
        frame.grid_rowconfigure(3, weight=0)
        frame.grid_columnconfigure(0, weight=1)

        image_area = ctk.CTkFrame(frame, fg_color=("gray95", "gray10"))
        image_area.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        image_area.grid_rowconfigure(0, weight=1)
        image_area.grid_columnconfigure(0, weight=1)

        image_label = ctk.CTkLabel(image_area, text=f"{title} - Prévia da imagem", font=ctk.CTkFont(size=16))
        image_label.grid(row=0, column=0)

        toolbar = ctk.CTkFrame(frame, height=48, fg_color=("gray90", "gray15"))
        toolbar.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        toolbar.grid_columnconfigure(10, weight=1)

        # Expor a toolbar no frame para customizações (ex.: página do pipeline)
        frame._toolbar = toolbar

        if include_default_toolbar:
            ctk.CTkButton(toolbar, text="Salvar Modificações", command=self.save_modifications).grid(row=0, column=0, padx=(10, 6), pady=8)
            ctk.CTkButton(toolbar, text="Exportar", command=self.export_image).grid(row=0, column=1, padx=6, pady=8)
            ctk.CTkButton(toolbar, text="Resetar", command=self.reset_image).grid(row=0, column=2, padx=6, pady=8)

        controls_frame = ctk.CTkFrame(frame, height=160, fg_color=("gray92", "gray18"))
        controls_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(5, 10))

        controls_func(controls_frame)

        return image_area, image_label

    def setup_color_page(self):
        def create_color_controls(parent):
            # 3 colunas para centralizar o seletor na coluna do meio
            parent.grid_columnconfigure((0, 1, 2), weight=1)
            ctk.CTkLabel(parent, text="Conversão de Cor:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=3, pady=(10, 5))

            self.color_method_var = ctk.StringVar(value="grayscale")
            self.color_method_option = ctk.CTkOptionMenu(parent, values=["grayscale", "hsv", "lab", "invert"], variable=self.color_method_var, command=lambda _: self.update_color_controls())
            self.color_method_option.grid(row=1, column=1, padx=5, pady=5)

            self.color_params_frame = ctk.CTkFrame(parent)
            self.color_params_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=10, pady=5)
            self.color_params_frame.grid_columnconfigure((0, 1, 2), weight=1)

            self.update_color_controls()

        self.color_image_area, self.color_image_label = self.setup_processing_page(self.color_frame, "Conversão de Cor", create_color_controls)

    def update_color_controls(self):
        for w in self.color_params_frame.winfo_children():
            w.destroy()
        method = self.color_method_var.get()
        # Sem parâmetros (determinístico). Não mostra mensagem; apenas mantém espaço limpo.
        pass

        self.on_color_param_change()

    def on_color_param_change(self):
        if not self.image_model.original:
            return
        method = self.color_method_var.get()
        try:
            base = self.get_pipeline_base()
            if base is None:
                return
            # Usar serviço puro para prévia baseada no vetor
            result = svc_convert_color(base, method, intensity=self.app_state.intensity, iterations=self.app_state.iterations)
            self.image_model.processed = result
            self.update_preview_image(self.color_image_label)
        except Exception:
            pass

    def setup_filter_page(self):
        def create_filter_controls(parent):
            parent.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
            # Título e centralização da técnica
            ctk.CTkLabel(parent, text="Filtros:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, columnspan=5, pady=(10, 5))

            ctk.CTkLabel(parent, text="Técnica:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
            self.filter_method_var = ctk.StringVar(value="blur")
            self.filter_method_option = ctk.CTkOptionMenu(parent, values=["blur", "sharpen", "emboss", "smooth"], variable=self.filter_method_var, command=lambda _: self.update_filter_controls())
            self.filter_method_option.grid(row=2, column=3, padx=5, pady=5, sticky="w")

            self.filter_params_frame = ctk.CTkFrame(parent)
            self.filter_params_frame.grid(row=3, column=0, columnspan=5, sticky="ew", padx=10, pady=5)
            self.filter_params_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

            self.update_filter_controls()

        self.filter_image_area, self.filter_image_label = self.setup_processing_page(self.filter_frame, "Filtros", create_filter_controls)

    def setup_edge_page(self):
        def create_edge_controls(parent):
            parent.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
            # Intensidade e repetições agora fazem parte dos controles abaixo

            ctk.CTkLabel(parent, text="Detector de Borda:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, columnspan=5, pady=(10, 5))

            # Seletor de técnica
            ctk.CTkLabel(parent, text="Técnica:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
            self.edge_method_var = ctk.StringVar(value="canny")
            self.edge_method_option = ctk.CTkOptionMenu(parent, values=["canny", "sobel", "laplacian"], variable=self.edge_method_var, command=lambda _: self.update_edge_controls())
            self.edge_method_option.grid(row=2, column=3, padx=5, pady=5, sticky="w")

            # Parâmetros dinâmicos
            self.edge_params_frame = ctk.CTkFrame(parent)
            self.edge_params_frame.grid(row=3, column=0, columnspan=5, sticky="ew", padx=10, pady=5)
            self.edge_params_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

            # Render inicial
            self.update_edge_controls()

        self.edge_image_area, self.edge_image_label = self.setup_processing_page(self.edge_frame, "Detector de Borda", create_edge_controls)

    def setup_binary_page(self):
        def create_binary_controls(parent):
            parent.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
            # Intensidade e repetições agora fazem parte dos controles abaixo
            ctk.CTkLabel(parent, text="Binarização:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, columnspan=5, pady=(10, 5))

            ctk.CTkLabel(parent, text="Técnica:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
            self.binary_method_var = ctk.StringVar(value="simple")
            self.binary_method_option = ctk.CTkOptionMenu(parent, values=["simple", "adaptive", "otsu"], variable=self.binary_method_var, command=lambda _: self.update_binary_controls())
            self.binary_method_option.grid(row=2, column=3, padx=5, pady=5, sticky="w")

            self.binary_params_frame = ctk.CTkFrame(parent)
            self.binary_params_frame.grid(row=3, column=0, columnspan=5, sticky="ew", padx=10, pady=5)
            self.binary_params_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

            self.update_binary_controls()

        self.binary_image_area, self.binary_image_label = self.setup_processing_page(self.binary_frame, "Binarização", create_binary_controls)

    # Edge dynamic controls and live update
    def update_edge_controls(self):
        for w in self.edge_params_frame.winfo_children():
            w.destroy()

        method = self.edge_method_var.get()

        if method == "canny":  # sem repetições
            ctk.CTkLabel(self.edge_params_frame, text="Low Threshold").grid(row=0, column=0, padx=5, pady=5)
            self.canny_low = ctk.IntVar(value=int(50 * self.app_state.intensity))
            low_slider = ctk.CTkSlider(self.edge_params_frame, from_=0, to=255, number_of_steps=255, variable=self.canny_low, command=lambda v: self.on_edge_param_change())
            low_slider.grid(row=0, column=1, sticky="ew", padx=5)

            ctk.CTkLabel(self.edge_params_frame, text="High Threshold").grid(row=0, column=2, padx=5, pady=5)
            self.canny_high = ctk.IntVar(value=int(150 * self.app_state.intensity))
            high_slider = ctk.CTkSlider(self.edge_params_frame, from_=0, to=255, number_of_steps=255, variable=self.canny_high, command=lambda v: self.on_edge_param_change())
            high_slider.grid(row=0, column=3, sticky="ew", padx=5)
        else:  # sobel/laplacian, sem repetições
            # Preparar 6 colunas para centralização quando aplicável
            for c in range(6):
                try:
                    self.edge_params_frame.grid_columnconfigure(c, weight=1)
                except Exception:
                    pass

            # Para Laplacian: um único parâmetro -> centralizar (col=2 e col=3)
            # Para Sobel: exibimos também dx/dy, então não será centralizado simples
            start_col = 2 if method == "laplacian" else 0
            label_col = start_col
            slider_col = start_col + 1

            ctk.CTkLabel(self.edge_params_frame, text="Kernel Size").grid(row=0, column=label_col, padx=5, pady=5)
            default_k = max(3, int(3 * self.app_state.intensity))
            if default_k % 2 == 0:
                default_k += 1
            self.edge_ksize = ctk.IntVar(value=default_k)
            k_slider = ctk.CTkSlider(self.edge_params_frame, from_=1, to=31, number_of_steps=30, variable=self.edge_ksize, command=lambda v: self.on_edge_param_change())
            k_slider.grid(row=0, column=slider_col, sticky="ew", padx=5)

            if method == "sobel":
                ctk.CTkLabel(self.edge_params_frame, text="dx").grid(row=0, column=2, padx=5, pady=5)
                self.sobel_dx = ctk.IntVar(value=1)
                dx_opt = ctk.CTkOptionMenu(self.edge_params_frame, values=["0", "1"], variable=self.sobel_dx, command=lambda _: self.on_edge_param_change())
                dx_opt.grid(row=0, column=3, padx=5, pady=5)

                ctk.CTkLabel(self.edge_params_frame, text="dy").grid(row=0, column=4, padx=5, pady=5)
                self.sobel_dy = ctk.IntVar(value=0)
                dy_opt = ctk.CTkOptionMenu(self.edge_params_frame, values=["0", "1"], variable=self.sobel_dy, command=lambda _: self.on_edge_param_change())
                dy_opt.grid(row=0, column=5, padx=5, pady=5)

        # Live update using current method and params
        self.on_edge_param_change()

    def on_edge_param_change(self):
        if not self.image_model.original:
            return
        method = self.edge_method_var.get()
        kwargs = {}
        if method == "canny":
            kwargs = {"low_threshold": int(self.canny_low.get()), "high_threshold": int(self.canny_high.get())}
        else:
            # Ensure odd kernel
            k = int(self.edge_ksize.get())
            if k % 2 == 0:
                k += 1
            kwargs = {"ksize": max(1, k)}
            if method == "sobel":
                try:
                    dx = int(self.sobel_dx.get())
                    dy = int(self.sobel_dy.get())
                except Exception:
                    dx, dy = 1, 0
                kwargs.update({"dx": dx, "dy": dy})
        try:
            base = self.get_pipeline_base()
            if base is None:
                return
            result = svc_detect_edges(base, method, intensity=self.app_state.intensity, **kwargs)
            self.image_model.processed = result
            self.update_preview_image(self.edge_image_label)
        except Exception:
            pass

    # Binary dynamic controls and live update
    def update_binary_controls(self):
        for w in self.binary_params_frame.winfo_children():
            w.destroy()

        method = self.binary_method_var.get()

        if method == "simple":
            # Centralizar único parâmetro
            for c in range(5):
                try:
                    self.binary_params_frame.grid_columnconfigure(c, weight=1)
                except Exception:
                    pass
            ctk.CTkLabel(self.binary_params_frame, text="Threshold").grid(row=0, column=2, padx=5, pady=5)
            self.binary_threshold = ctk.IntVar(value=int(127 * self.app_state.intensity))
            t_slider = ctk.CTkSlider(self.binary_params_frame, from_=0, to=255, number_of_steps=255, variable=self.binary_threshold, command=lambda v: self.on_binary_param_change())
            t_slider.grid(row=0, column=3, sticky="ew", padx=5)
        elif method == "adaptive":
            ctk.CTkLabel(self.binary_params_frame, text="Block Size").grid(row=0, column=0, padx=5, pady=5)
            default_bs = max(3, int(11 * self.app_state.intensity))
            if default_bs % 2 == 0:
                default_bs += 1
            self.binary_block = ctk.IntVar(value=default_bs)
            b_slider = ctk.CTkSlider(self.binary_params_frame, from_=3, to=51, number_of_steps=24, variable=self.binary_block, command=lambda v: self.on_binary_param_change())
            b_slider.grid(row=0, column=1, sticky="ew", padx=5)

            ctk.CTkLabel(self.binary_params_frame, text="C").grid(row=0, column=2, padx=5, pady=5)
            self.binary_C = ctk.IntVar(value=2)
            c_slider = ctk.CTkSlider(self.binary_params_frame, from_=-20, to=20, number_of_steps=40, variable=self.binary_C, command=lambda v: self.on_binary_param_change())
            c_slider.grid(row=0, column=3, sticky="ew", padx=5)
        else:
            ctk.CTkLabel(self.binary_params_frame, text="Sem parâmetros para Otsu").grid(row=0, column=0, padx=5, pady=5)

        self.on_binary_param_change()

    def on_binary_param_change(self):
        if not self.image_model.original:
            return
        method = self.binary_method_var.get()
        kwargs = {}
        if method == "simple":
            kwargs = {"threshold_value": int(self.binary_threshold.get())}
        elif method == "adaptive":
            bs = int(self.binary_block.get())
            if bs % 2 == 0:
                bs += 1
            kwargs = {"block_size": max(3, bs), "C": int(self.binary_C.get())}
        try:
            base = self.get_pipeline_base()
            if base is None:
                return
            result = svc_binarize(base, method, intensity=self.app_state.intensity, **kwargs)
            self.image_model.processed = result
            self.update_preview_image(self.binary_image_label)
        except Exception:
            pass

    def setup_morphology_page(self):
        def create_morphology_controls(parent):
            parent.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
            # Intensidade e repetições agora fazem parte dos controles abaixo
            ctk.CTkLabel(parent, text="Morfologia Matemática:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, columnspan=5, pady=(10, 5))

            ctk.CTkLabel(parent, text="Operação:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
            self.morph_method_var = ctk.StringVar(value="erosion")
            self.morph_method_option = ctk.CTkOptionMenu(parent, values=["erosion", "dilation", "opening", "closing"], variable=self.morph_method_var, command=lambda _: self.update_morphology_controls())
            self.morph_method_option.grid(row=2, column=3, padx=5, pady=5, sticky="w")

            self.morph_params_frame = ctk.CTkFrame(parent)
            self.morph_params_frame.grid(row=3, column=0, columnspan=5, sticky="ew", padx=10, pady=5)
            self.morph_params_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

            self.update_morphology_controls()

        self.morphology_image_area, self.morphology_image_label = self.setup_processing_page(self.morphology_frame, "Morfologia Matemática", create_morphology_controls)

    # Filter dynamic controls/live update
    def update_filter_controls(self):
        for w in self.filter_params_frame.winfo_children():
            w.destroy()
        method = self.filter_method_var.get()
        # Controles comuns onde faz sentido: repetições (para filtros faz sentido)
        ctk.CTkLabel(self.filter_params_frame, text="Repetições").grid(row=0, column=0, padx=5, pady=5)
        self.filter_iterations = ctk.IntVar(value=1)
        it_slider = ctk.CTkSlider(self.filter_params_frame, from_=1, to=10, number_of_steps=9, variable=self.filter_iterations, command=lambda v: self.on_filter_param_change())
        it_slider.grid(row=0, column=1, sticky="ew", padx=5)
        if method == "blur":
            ctk.CTkLabel(self.filter_params_frame, text="Raio").grid(row=0, column=2, padx=5, pady=5)
            self.blur_radius = ctk.IntVar(value=3)
            r_slider = ctk.CTkSlider(self.filter_params_frame, from_=1, to=50, number_of_steps=49, variable=self.blur_radius, command=lambda v: self.on_filter_param_change())
            r_slider.grid(row=0, column=3, sticky="ew", padx=5)
        else:
            # Centralizar quando só houver repetições
            for c in range(5):
                try:
                    self.filter_params_frame.grid_columnconfigure(c, weight=1)
                except Exception:
                    pass
            # mover repetições para o centro: colunas 2 e 3
            # relocar widgets criando novamente nesta posição
            for w in self.filter_params_frame.grid_slaves(row=0):
                w.grid_forget()
            ctk.CTkLabel(self.filter_params_frame, text="Repetições").grid(row=0, column=2, padx=5, pady=5)
            self.filter_iterations = ctk.IntVar(value=self.filter_iterations.get() if hasattr(self, 'filter_iterations') else 1)
            it_slider = ctk.CTkSlider(self.filter_params_frame, from_=1, to=10, number_of_steps=9, variable=self.filter_iterations, command=lambda v: self.on_filter_param_change())
            it_slider.grid(row=0, column=3, sticky="ew", padx=5)
        self.on_filter_param_change()

    def on_filter_param_change(self):
        if not self.image_model.original:
            return
        method = self.filter_method_var.get()
        kwargs = {}
        if method == "blur":
            kwargs = {"radius": int(self.blur_radius.get())}
        try:
            base = self.get_pipeline_base()
            if base is None:
                return
            result = svc_apply_filter(base, method, intensity=self.app_state.intensity, iterations=int(self.filter_iterations.get()), **kwargs)
            self.image_model.processed = result
            self.update_preview_image(self.filter_image_label)
        except Exception:
            pass

    # Morphology dynamic controls/live update
    def update_morphology_controls(self):
        for w in self.morph_params_frame.winfo_children():
            w.destroy()
        ctk.CTkLabel(self.morph_params_frame, text="Kernel Size").grid(row=0, column=0, padx=5, pady=5)
        self.morph_kernel = ctk.IntVar(value=5)
        ks_slider = ctk.CTkSlider(self.morph_params_frame, from_=1, to=51, number_of_steps=50, variable=self.morph_kernel, command=lambda v: self.on_morph_param_change())
        ks_slider.grid(row=0, column=1, sticky="ew", padx=5)

        ctk.CTkLabel(self.morph_params_frame, text="Repetições").grid(row=0, column=2, padx=5, pady=5)
        self.morph_iterations = ctk.IntVar(value=1)
        it_slider = ctk.CTkSlider(self.morph_params_frame, from_=1, to=10, number_of_steps=9, variable=self.morph_iterations, command=lambda v: self.on_morph_param_change())
        it_slider.grid(row=0, column=3, sticky="ew", padx=5)
        self.on_morph_param_change()

    def on_morph_param_change(self):
        if not self.image_model.original:
            return
        op = self.morph_method_var.get()
        ks = int(self.morph_kernel.get())
        try:
            base = self.get_pipeline_base()
            if base is None:
                return
            result = svc_apply_morphology(base, op, intensity=self.app_state.intensity, iterations=int(self.morph_iterations.get()), kernel_size=max(1, ks))
            self.image_model.processed = result
            self.update_preview_image(self.morphology_image_label)
        except Exception:
            pass

    def get_pipeline_base(self):
        if not self.image_model.original:
            return None
        try:
            if self.pipeline.steps:
                return self.pipeline_controller.run(self.image_model.original)
            return self.image_model.original.copy()
        except Exception:
            return self.image_model.original.copy()

    # Exibição e estado
    def select_frame_by_name(self, name: str):
        for btn_name, button in self.nav_buttons.items():
            if btn_name == name:
                button.configure(fg_color=("gray75", "gray25"))
            else:
                button.configure(fg_color="transparent")

        for frame in [self.import_frame, self.color_frame, self.filter_frame, self.edge_frame, self.binary_frame, self.morphology_frame, self.pipeline_frame]:
            frame.grid_forget()
        # Ao trocar de página, garantir que a imagem exibida reflita o vetor (se existir)
        # sem alterar o estado original. Assim evitamos "salvar" sem clicar.
        if self.image_model.original is not None and name != "pipeline":
            try:
                if self.pipeline.steps:
                    result = self.pipeline_controller.run(self.image_model.original)
                    self.image_model.processed = result.copy()
                else:
                    self.image_model.processed = self.image_model.original.copy()
            except Exception:
                self.image_model.processed = self.image_model.original.copy()

        if name == "pipeline":
            self.pipeline_frame.grid(row=0, column=0, sticky="nsew")
            self.refresh_pipeline_list()
            self.update_pipeline_preview()
        if name == "import":
            self.import_frame.grid(row=0, column=0, sticky="nsew")
        elif name == "color":
            self.color_frame.grid(row=0, column=0, sticky="nsew")
            self.update_preview_image(self.color_image_label)
        elif name == "filter":
            self.filter_frame.grid(row=0, column=0, sticky="nsew")
            self.update_preview_image(self.filter_image_label)
        elif name == "edge":
            self.edge_frame.grid(row=0, column=0, sticky="nsew")
            self.update_preview_image(self.edge_image_label)
        elif name == "binary":
            self.binary_frame.grid(row=0, column=0, sticky="nsew")
            self.update_preview_image(self.binary_image_label)
        elif name == "morphology":
            self.morphology_frame.grid(row=0, column=0, sticky="nsew")
            self.update_preview_image(self.morphology_image_label)

        self.selected_frame_name = name

    # ===== Pipeline helpers/actions =====
    def refresh_pipeline_list(self):
        for w in self.pipeline_list.winfo_children():
            w.destroy()
        if not self.pipeline.steps:
            ctk.CTkLabel(self.pipeline_list, text="Nenhuma etapa adicionada.").grid(row=0, column=0, padx=10, pady=10)
            return
        for i, step in enumerate(self.pipeline.steps):
            item = ctk.CTkFrame(self.pipeline_list, fg_color=("gray85", "gray25"))
            item.grid(row=i, column=0, sticky="ew", padx=6, pady=4)
            item.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(item, text=step.display_text(), anchor="w").grid(row=0, column=0, sticky="ew", padx=10, pady=6)
            ctk.CTkButton(item, text="↑", width=36, command=lambda idx=i: self.on_pipeline_move_up(idx)).grid(row=0, column=1, padx=4, pady=6)
            ctk.CTkButton(item, text="↓", width=36, command=lambda idx=i: self.on_pipeline_move_down(idx)).grid(row=0, column=2, padx=4, pady=6)
            ctk.CTkButton(item, text="Apagar", width=80, command=lambda idx=i: self.on_pipeline_delete(idx)).grid(row=0, column=3, padx=6, pady=6)

    def on_pipeline_move_up(self, idx: int):
        self.pipeline_controller.move_up(idx)
        self.refresh_pipeline_list()
        # Sincroniza a imagem processada com o vetor atual
        if self.image_model.original:
            try:
                result = self.pipeline_controller.run(self.image_model.original) if self.pipeline.steps else self.image_model.original.copy()
                self.image_model.processed = result
            except Exception:
                self.image_model.processed = self.image_model.original.copy()
        self.update_pipeline_preview()

    def on_pipeline_move_down(self, idx: int):
        self.pipeline_controller.move_down(idx)
        self.refresh_pipeline_list()
        # Sincroniza a imagem processada com o vetor atual
        if self.image_model.original:
            try:
                result = self.pipeline_controller.run(self.image_model.original) if self.pipeline.steps else self.image_model.original.copy()
                self.image_model.processed = result
            except Exception:
                self.image_model.processed = self.image_model.original.copy()
        self.update_pipeline_preview()

    def on_pipeline_delete(self, idx: int):
        self.pipeline_controller.delete_step(idx)
        self.refresh_pipeline_list()
        # Atualiza a imagem processada para refletir o novo estado do vetor
        if self.image_model.original:
            try:
                if self.pipeline.steps:
                    result = self.pipeline_controller.run(self.image_model.original)
                    self.image_model.processed = result
                else:
                    self.image_model.processed = self.image_model.original.copy()
            except Exception:
                self.image_model.processed = self.image_model.original.copy()
        self.update_pipeline_preview()

    def on_pipeline_save(self):
        # Salvar Vetor: salva apenas o snapshot das etapas (não altera a imagem original importada)
        if not self.image_model.original:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro!")
            return
        try:
            result = self.pipeline_controller.run(self.image_model.original)
            # Atualiza apenas a visualização processada com o resultado do vetor
            self.image_model.processed = result
            # Salva snapshot do vetor (para permitir reverter)
            self.pipeline_controller.save()
            # Atualiza a UI
            self.refresh_pipeline_list()
            self.update_pipeline_preview()
            messagebox.showinfo("Sucesso", "Vetor salvo! A imagem original permanece a mesma; o resultado será sempre calculado a partir dela.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar vetor: {str(e)}")

    def on_pipeline_revert(self):
        # Reverter Vetor = reverter etapas para o snapshot salvo e atualizar a prévia
        if not self.image_model.original:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro!")
            return
        try:
            self.pipeline_controller.revert()
            # Atualiza imagem processada com base no vetor revertido
            if self.pipeline.steps:
                result = self.pipeline_controller.run(self.image_model.original)
                self.image_model.processed = result
            else:
                self.image_model.processed = self.image_model.original.copy()
            self.refresh_pipeline_list()
            self.update_pipeline_preview()
            messagebox.showinfo("Revertido", "Vetor revertido para o último snapshot!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao reverter vetor: {str(e)}")

    def on_pipeline_reset(self):
        """Resetar (na aba do vetor) descarta alterações não salvas e volta ao snapshot."""
        if not self.image_model.original:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro!")
            return
        try:
            self.pipeline_controller.revert()
            # Atualizar a imagem processada conforme o vetor revertido
            if self.pipeline.steps:
                result = self.pipeline_controller.run(self.image_model.original)
                self.image_model.processed = result
            else:
                self.image_model.processed = self.image_model.original.copy()
            self.refresh_pipeline_list()
            self.update_pipeline_preview()
            messagebox.showinfo("Resetado", "Alterações do vetor nesta aba foram descartadas.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao resetar vetor: {str(e)}")

    # Removido: rodar vetor é intrínseco e a prévia já é atualizada automaticamente

    # ===== Add steps from pages =====
    def add_step_from_color(self):
        method = self.color_method_var.get()
        self.pipeline_controller.add_step("color", method, {})
        self.refresh_pipeline_list()
        self.update_pipeline_preview()

    def add_step_from_filter(self):
        method = self.filter_method_var.get()
        params = {}
        if method == "blur":
            params = {"radius": int(self.blur_radius.get()), "iterations": int(self.filter_iterations.get())}
        else:
            params = {"iterations": int(self.filter_iterations.get())}
        self.pipeline_controller.add_step("filter", method, params)
        self.refresh_pipeline_list()
        self.update_pipeline_preview()

    def add_step_from_edge(self):
        method = self.edge_method_var.get()
        params = {}
        if method == "canny":
            params = {"low_threshold": int(self.canny_low.get()), "high_threshold": int(self.canny_high.get())}
        else:
            k = int(self.edge_ksize.get())
            if k % 2 == 0:
                k += 1
            params = {"ksize": max(1, k)}
            if method == "sobel":
                try:
                    params.update({"dx": int(self.sobel_dx.get()), "dy": int(self.sobel_dy.get())})
                except Exception:
                    pass
        self.pipeline_controller.add_step("edge", method, params)
        self.refresh_pipeline_list()
        self.update_pipeline_preview()

    def add_step_from_binary(self):
        method = self.binary_method_var.get()
        params = {}
        if method == "simple":
            params = {"threshold_value": int(self.binary_threshold.get())}
        elif method == "adaptive":
            bs = int(self.binary_block.get())
            if bs % 2 == 0:
                bs += 1
            params = {"block_size": max(3, bs), "C": int(self.binary_C.get())}
        self.pipeline_controller.add_step("binary", method, params)
        self.refresh_pipeline_list()
        self.update_pipeline_preview()

    def add_step_from_morphology(self):
        op = self.morph_method_var.get()
        params = {"kernel_size": int(self.morph_kernel.get()), "iterations": int(self.morph_iterations.get())}
        self.pipeline_controller.add_step("morphology", op, params)
        self.refresh_pipeline_list()
        self.update_pipeline_preview()

    def update_pipeline_preview(self):
        if not self.image_model.original:
            # Se não houver imagem, apenas limpe o rótulo
            self.pipeline_image_label.configure(image=None, text="Nenhuma imagem carregada")
            return
        if not self.pipeline.steps:
            # Sem etapas, mostrar a imagem original
            display_image = self.image_model.original.copy()
            display_image.thumbnail(PREVIEW_MAX_SIZE, Image.Resampling.LANCZOS)
            self._pipeline_ctk_image = ctk.CTkImage(light_image=display_image, dark_image=display_image, size=(display_image.width, display_image.height))
            self.pipeline_image_label.configure(image=self._pipeline_ctk_image, text="")
            return
        try:
            result = self.pipeline_controller.run(self.image_model.original)
            # Renderiza no label do pipeline sem alterar o estado global processado
            display_image = result.copy()
            display_image.thumbnail(PREVIEW_MAX_SIZE, Image.Resampling.LANCZOS)
            self._pipeline_ctk_image = ctk.CTkImage(light_image=display_image, dark_image=display_image, size=(display_image.width, display_image.height))
            self.pipeline_image_label.configure(image=self._pipeline_ctk_image, text="")
        except Exception:
            # Em caso de erro, mantém a imagem atual
            pass

    def open_image(self):
        filename = filedialog.askopenfilename(title='Selecionar imagem', initialdir=os.getcwd(), filetypes=SUPPORTED_IMAGE_TYPES)
        if filename:
            try:
                self.controller.load(filename)
                if filename not in self.app_state.imported_files:
                    self.app_state.imported_files.append(filename)
                    self.update_files_list()
                self.update_preview_image(self.import_image_label)
                messagebox.showinfo("Sucesso", "Imagem carregada com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar imagem: {str(e)}")

    def update_files_list(self):
        for widget in self.import_files_strip.winfo_children():
            widget.destroy()
        if not self.app_state.imported_files:
            ctk.CTkLabel(self.import_files_strip, text="Nenhum arquivo importado", anchor="w").grid(row=0, column=0, sticky="ew", padx=10, pady=6)
        else:
            for i, filepath in enumerate(self.app_state.imported_files):
                filename = os.path.basename(filepath)
                file_frame = ctk.CTkFrame(self.import_files_strip, height=40, fg_color=("gray85", "gray25"))
                file_frame.grid(row=i, column=0, sticky="ew", padx=5, pady=2)
                file_frame.grid_columnconfigure(0, weight=1)
                ctk.CTkLabel(file_frame, text=filename, anchor="w").grid(row=0, column=0, sticky="ew", padx=10, pady=5)
                ctk.CTkButton(file_frame, text="Carregar", width=80, command=lambda f=filepath: self.load_file(f)).grid(row=0, column=1, padx=5, pady=5)

    def load_file(self, filepath):
        try:
            self.controller.load(filepath)
            self.update_preview_image(self.import_image_label)
            messagebox.showinfo("Sucesso", f"Imagem {os.path.basename(filepath)} carregada!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar arquivo: {str(e)}")

    def update_preview_image(self, label):
        if self.image_model.processed:
            display_image = self.image_model.processed.copy()
            display_image.thumbnail(PREVIEW_MAX_SIZE, Image.Resampling.LANCZOS)
            ctk_image = ctk.CTkImage(light_image=display_image, dark_image=display_image, size=(display_image.width, display_image.height))
            label.configure(image=ctk_image, text="")
        else:
            label.configure(image=None, text="Nenhuma imagem carregada")

    # Ações delegadas
    def on_convert_color(self, conversion_type: str):
        if not self.image_model.original:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro!")
            return
        try:
            self.controller.convert_color(conversion_type)
            self.update_preview_image(self.color_image_label)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na conversão: {str(e)}")

    def on_apply_filter(self, filter_type: str):
        if not self.image_model.original:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro!")
            return
        try:
            self.controller.apply_filter(filter_type)
            self.update_preview_image(self.filter_image_label)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no filtro: {str(e)}")

    def on_detect_edges(self, method: str):
        # Mantido para compatibilidade; agora usamos os controles dinâmicos
        if not self.image_model.original:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro!")
            return
        self.on_edge_param_change()

    def on_binarize(self, method: str):
        if not self.image_model.original:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro!")
            return
        self.on_binary_param_change()

    def on_apply_morphology(self, operation: str):
        if not self.image_model.original:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro!")
            return
        try:
            self.controller.apply_morphology(operation)
            self.update_preview_image(self.morphology_image_label)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na morfologia: {str(e)}")

    def save_modifications(self):
        if self.image_model.processed and self.image_model.original:
            # Antes de salvar, adiciona a etapa atual ao vetor
            try:
                if self.selected_frame_name == "color":
                    self.add_step_from_color()
                elif self.selected_frame_name == "filter":
                    self.add_step_from_filter()
                elif self.selected_frame_name == "edge":
                    self.add_step_from_edge()
                elif self.selected_frame_name == "binary":
                    self.add_step_from_binary()
                elif self.selected_frame_name == "morphology":
                    self.add_step_from_morphology()
            except Exception:
                # Mesmo se falhar ao adicionar, prossegue o salvamento
                pass
            # Atualiza visualização com base no resultado do vetor atualizado
            try:
                result = self.pipeline_controller.run(self.image_model.original)
                self.image_model.processed = result
            except Exception:
                # Se falhar, mantém o processado atual
                pass
            # Salva snapshot do vetor (não altera a imagem original carregada)
            try:
                self.pipeline_controller.save()
            except Exception:
                pass
            # Atualiza UI do vetor se estiver aberto
            if self.selected_frame_name == "pipeline":
                self.refresh_pipeline_list()
                self.update_pipeline_preview()
            messagebox.showinfo("Sucesso", "Modificação adicionada ao vetor e salva no snapshot. A imagem original permanece inalterada.")
        else:
            messagebox.showwarning("Aviso", "Nenhuma modificação para salvar!")

    def reset_image(self):
        if self.image_model.original:
            # Resetar volta a prévia para o resultado atual do vetor (ou original se vazio)
            try:
                base = self.get_pipeline_base()
                if base is not None:
                    self.image_model.processed = base.copy()
            except Exception:
                self.image_model.processed = self.image_model.original.copy()
            if self.selected_frame_name == "color":
                self.update_preview_image(self.color_image_label)
            elif self.selected_frame_name == "filter":
                self.update_preview_image(self.filter_image_label)
            elif self.selected_frame_name == "edge":
                self.update_preview_image(self.edge_image_label)
            elif self.selected_frame_name == "binary":
                self.update_preview_image(self.binary_image_label)
            elif self.selected_frame_name == "morphology":
                self.update_preview_image(self.morphology_image_label)
            messagebox.showinfo("Sucesso", "Visualização resetada ao resultado do vetor (ou original se o vetor estiver vazio).")

    def export_image(self):
        # Se estiver na aba do vetor, exporta o resultado do pipeline, sem mutar o estado global
        if self.selected_frame_name == "pipeline":
            if not self.image_model.original:
                messagebox.showwarning("Aviso", "Nenhuma imagem para exportar!")
                return
            try:
                result = self.pipeline_controller.run(self.image_model.original)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao calcular o vetor: {str(e)}")
                return
            export_source = result
        else:
            if not self.image_model.processed:
                messagebox.showwarning("Aviso", "Nenhuma imagem para exportar!")
                return
            export_source = self.image_model.processed
        filename = filedialog.asksaveasfilename(title='Salvar imagem', defaultextension='.png', filetypes=EXPORT_TYPES)
        if filename:
            try:
                # Exporta a imagem escolhida
                from services.file_management.image_exporter import export_image as export_image_service
                export_image_service(export_source, filename)
                messagebox.showinfo("Sucesso", f"Imagem salva como {filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
