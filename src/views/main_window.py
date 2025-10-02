import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image

from config.settings import APP_TITLE, APP_GEOMETRY
from config.constants import SUPPORTED_IMAGE_TYPES, EXPORT_TYPES, PREVIEW_MAX_SIZE
from models.image_model import ImageModel
from models.application_state import ApplicationState
from controllers.image_controller import ImageController


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)

        # Modelos e controlador
        self.image_model = ImageModel()
        self.app_state = ApplicationState()
        self.controller = ImageController(self.image_model, self.app_state)

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
        self.navigation_frame.grid_rowconfigure(7, weight=1)

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
            ("color", "Conversão de Cor", 2),
            ("filter", "Filtros", 3),
            ("edge", "Detector de Borda", 4),
            ("binary", "Binarização", 5),
            ("morphology", "Morfologia", 6),
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

        self.setup_import_page()
        self.setup_color_page()
        self.setup_filter_page()
        self.setup_edge_page()
        self.setup_binary_page()
        self.setup_morphology_page()

    def setup_import_page(self):
        self.import_frame.grid_rowconfigure(0, weight=1)
        self.import_frame.grid_rowconfigure(1, weight=0)
        self.import_frame.grid_rowconfigure(2, weight=0)
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

        ctk.CTkLabel(self.import_files_strip, text="Nenhum arquivo importado", anchor="w").grid(
            row=0, column=0, sticky="ew", padx=10, pady=6
        )

    def create_intensity_toolbar(self, parent):
        intensity_frame = ctk.CTkFrame(parent, fg_color=("gray88", "gray20"))
        intensity_frame.grid(row=0, column=0, columnspan=4, sticky="ew", padx=5, pady=(5, 10))
        intensity_frame.grid_columnconfigure(1, weight=1)
        intensity_frame.grid_columnconfigure(3, weight=1)

        ctk.CTkLabel(intensity_frame, text="Intensidade:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=5)

        self.intensity_var = ctk.DoubleVar(value=self.app_state.intensity)
        self.iterations_var = ctk.IntVar(value=self.app_state.iterations)

        self.intensity_slider = ctk.CTkSlider(
            intensity_frame,
            from_=0.1,
            to=3.0,
            number_of_steps=29,
            variable=self.intensity_var,
            command=self.on_intensity_change,
        )
        self.intensity_slider.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

        self.intensity_label = ctk.CTkLabel(intensity_frame, text=f"{self.app_state.intensity:.1f}")
        self.intensity_label.grid(row=0, column=2, padx=5, pady=5)

        ctk.CTkLabel(intensity_frame, text="Repetições:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=3, padx=(20, 10), pady=5)

        self.iterations_slider = ctk.CTkSlider(
            intensity_frame,
            from_=1,
            to=10,
            number_of_steps=9,
            variable=self.iterations_var,
            command=self.on_iterations_change,
        )
        self.iterations_slider.grid(row=0, column=4, sticky="ew", padx=10, pady=5)

        self.iterations_label = ctk.CTkLabel(intensity_frame, text=str(self.app_state.iterations))
        self.iterations_label.grid(row=0, column=5, padx=5, pady=5)

    def on_intensity_change(self, value):
        self.app_state.intensity = float(value)
        self.intensity_label.configure(text=f"{value:.1f}")
        # Live refresh for pages with dynamic params
        if getattr(self, 'selected_frame_name', None) == "edge":
            self.on_edge_param_change()
        elif getattr(self, 'selected_frame_name', None) == "binary":
            self.on_binary_param_change()
        elif getattr(self, 'selected_frame_name', None) == "filter":
            self.on_filter_param_change()
        elif getattr(self, 'selected_frame_name', None) == "morphology":
            self.on_morph_param_change()

    def on_iterations_change(self, value):
        self.app_state.iterations = int(value)
        self.iterations_label.configure(text=f"{int(value)}")
        # Some techniques respond to iteration changes (filters/morphology)
        if getattr(self, 'selected_frame_name', None) == "filter":
            self.on_filter_param_change()
        elif getattr(self, 'selected_frame_name', None) == "morphology":
            self.on_morph_param_change()

    def setup_processing_page(self, frame, title, controls_func):
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

        ctk.CTkButton(toolbar, text="Salvar Modificações", command=self.save_modifications).grid(row=0, column=0, padx=(10, 6), pady=8)
        ctk.CTkButton(toolbar, text="Exportar", command=self.export_image).grid(row=0, column=1, padx=6, pady=8)
        ctk.CTkButton(toolbar, text="Resetar", command=self.reset_image).grid(row=0, column=2, padx=6, pady=8)

        controls_frame = ctk.CTkFrame(frame, height=160, fg_color=("gray92", "gray18"))
        controls_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(5, 10))

        controls_func(controls_frame)

        return image_area, image_label

    def setup_color_page(self):
        def create_color_controls(parent):
            parent.grid_columnconfigure((0, 1, 2, 3), weight=1)
            self.create_intensity_toolbar(parent)
            ctk.CTkLabel(parent, text="Conversão de Cor:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, columnspan=4, pady=(10, 5))
            ctk.CTkButton(parent, text="RGB para Grayscale", command=lambda: self.on_convert_color("grayscale")).grid(row=2, column=0, padx=5, pady=5)
            ctk.CTkButton(parent, text="RGB para HSV", command=lambda: self.on_convert_color("hsv")).grid(row=2, column=1, padx=5, pady=5)
            ctk.CTkButton(parent, text="RGB para LAB", command=lambda: self.on_convert_color("lab")).grid(row=2, column=2, padx=5, pady=5)
            ctk.CTkButton(parent, text="Inverter Cores", command=lambda: self.on_convert_color("invert")).grid(row=2, column=3, padx=5, pady=5)

        self.color_image_area, self.color_image_label = self.setup_processing_page(self.color_frame, "Conversão de Cor", create_color_controls)

    def setup_filter_page(self):
        def create_filter_controls(parent):
            parent.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
            self.create_intensity_toolbar(parent)
            ctk.CTkLabel(parent, text="Filtros:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, columnspan=5, pady=(10, 5))

            ctk.CTkLabel(parent, text="Técnica:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
            self.filter_method_var = ctk.StringVar(value="blur")
            self.filter_method_option = ctk.CTkOptionMenu(parent, values=["blur", "sharpen", "emboss", "smooth"], variable=self.filter_method_var, command=lambda _: self.update_filter_controls())
            self.filter_method_option.grid(row=2, column=1, padx=5, pady=5, sticky="w")

            self.filter_params_frame = ctk.CTkFrame(parent)
            self.filter_params_frame.grid(row=3, column=0, columnspan=5, sticky="ew", padx=10, pady=5)
            self.filter_params_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

            self.update_filter_controls()

        self.filter_image_area, self.filter_image_label = self.setup_processing_page(self.filter_frame, "Filtros", create_filter_controls)

    def setup_edge_page(self):
        def create_edge_controls(parent):
            parent.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
            self.create_intensity_toolbar(parent)

            ctk.CTkLabel(parent, text="Detector de Borda:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, columnspan=5, pady=(10, 5))

            # Seletor de técnica
            ctk.CTkLabel(parent, text="Técnica:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
            self.edge_method_var = ctk.StringVar(value="canny")
            self.edge_method_option = ctk.CTkOptionMenu(parent, values=["canny", "sobel", "laplacian"], variable=self.edge_method_var, command=lambda _: self.update_edge_controls())
            self.edge_method_option.grid(row=2, column=1, padx=5, pady=5, sticky="w")

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
            self.create_intensity_toolbar(parent)
            ctk.CTkLabel(parent, text="Binarização:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, columnspan=5, pady=(10, 5))

            ctk.CTkLabel(parent, text="Técnica:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
            self.binary_method_var = ctk.StringVar(value="simple")
            self.binary_method_option = ctk.CTkOptionMenu(parent, values=["simple", "adaptive", "otsu"], variable=self.binary_method_var, command=lambda _: self.update_binary_controls())
            self.binary_method_option.grid(row=2, column=1, padx=5, pady=5, sticky="w")

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

        if method == "canny":
            ctk.CTkLabel(self.edge_params_frame, text="Low Threshold").grid(row=0, column=0, padx=5, pady=5)
            self.canny_low = ctk.IntVar(value=int(50 * self.app_state.intensity))
            low_slider = ctk.CTkSlider(self.edge_params_frame, from_=0, to=255, number_of_steps=255, variable=self.canny_low, command=lambda v: self.on_edge_param_change())
            low_slider.grid(row=0, column=1, sticky="ew", padx=5)

            ctk.CTkLabel(self.edge_params_frame, text="High Threshold").grid(row=0, column=2, padx=5, pady=5)
            self.canny_high = ctk.IntVar(value=int(150 * self.app_state.intensity))
            high_slider = ctk.CTkSlider(self.edge_params_frame, from_=0, to=255, number_of_steps=255, variable=self.canny_high, command=lambda v: self.on_edge_param_change())
            high_slider.grid(row=0, column=3, sticky="ew", padx=5)
        else:
            ctk.CTkLabel(self.edge_params_frame, text="Kernel Size").grid(row=0, column=0, padx=5, pady=5)
            default_k = max(3, int(3 * self.app_state.intensity))
            if default_k % 2 == 0:
                default_k += 1
            self.edge_ksize = ctk.IntVar(value=default_k)
            k_slider = ctk.CTkSlider(self.edge_params_frame, from_=1, to=31, number_of_steps=30, variable=self.edge_ksize, command=lambda v: self.on_edge_param_change())
            k_slider.grid(row=0, column=1, sticky="ew", padx=5)

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
        try:
            self.controller.detect_edges(method, **kwargs)
            self.update_preview_image(self.edge_image_label)
        except Exception:
            pass

    # Binary dynamic controls and live update
    def update_binary_controls(self):
        for w in self.binary_params_frame.winfo_children():
            w.destroy()

        method = self.binary_method_var.get()

        if method == "simple":
            ctk.CTkLabel(self.binary_params_frame, text="Threshold").grid(row=0, column=0, padx=5, pady=5)
            self.binary_threshold = ctk.IntVar(value=int(127 * self.app_state.intensity))
            t_slider = ctk.CTkSlider(self.binary_params_frame, from_=0, to=255, number_of_steps=255, variable=self.binary_threshold, command=lambda v: self.on_binary_param_change())
            t_slider.grid(row=0, column=1, sticky="ew", padx=5)
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
            self.controller.binarize(method, **kwargs)
            self.update_preview_image(self.binary_image_label)
        except Exception:
            pass

    def setup_morphology_page(self):
        def create_morphology_controls(parent):
            parent.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
            self.create_intensity_toolbar(parent)
            ctk.CTkLabel(parent, text="Morfologia Matemática:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, columnspan=5, pady=(10, 5))

            ctk.CTkLabel(parent, text="Operação:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
            self.morph_method_var = ctk.StringVar(value="erosion")
            self.morph_method_option = ctk.CTkOptionMenu(parent, values=["erosion", "dilation", "opening", "closing"], variable=self.morph_method_var, command=lambda _: self.update_morphology_controls())
            self.morph_method_option.grid(row=2, column=1, padx=5, pady=5, sticky="w")

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
        if method == "blur":
            ctk.CTkLabel(self.filter_params_frame, text="Raio").grid(row=0, column=0, padx=5, pady=5)
            self.blur_radius = ctk.IntVar(value=max(1, int(self.app_state.intensity * 2)))
            r_slider = ctk.CTkSlider(self.filter_params_frame, from_=1, to=50, number_of_steps=49, variable=self.blur_radius, command=lambda v: self.on_filter_param_change())
            r_slider.grid(row=0, column=1, sticky="ew", padx=5)
        else:
            ctk.CTkLabel(self.filter_params_frame, text="Sem parâmetros").grid(row=0, column=0, padx=5, pady=5)
        self.on_filter_param_change()

    def on_filter_param_change(self):
        if not self.image_model.original:
            return
        method = self.filter_method_var.get()
        kwargs = {}
        if method == "blur":
            kwargs = {"radius": int(self.blur_radius.get())}
        try:
            self.controller.apply_filter(method, **kwargs)
            self.update_preview_image(self.filter_image_label)
        except Exception:
            pass

    # Morphology dynamic controls/live update
    def update_morphology_controls(self):
        for w in self.morph_params_frame.winfo_children():
            w.destroy()
        ctk.CTkLabel(self.morph_params_frame, text="Kernel Size").grid(row=0, column=0, padx=5, pady=5)
        default_ks = max(3, int(5 * self.app_state.intensity))
        self.morph_kernel = ctk.IntVar(value=default_ks)
        ks_slider = ctk.CTkSlider(self.morph_params_frame, from_=1, to=51, number_of_steps=50, variable=self.morph_kernel, command=lambda v: self.on_morph_param_change())
        ks_slider.grid(row=0, column=1, sticky="ew", padx=5)
        self.on_morph_param_change()

    def on_morph_param_change(self):
        if not self.image_model.original:
            return
        op = self.morph_method_var.get()
        ks = int(self.morph_kernel.get())
        try:
            self.controller.apply_morphology(op, kernel_size=max(1, ks))
            self.update_preview_image(self.morphology_image_label)
        except Exception:
            pass

    # Exibição e estado
    def select_frame_by_name(self, name: str):
        for btn_name, button in self.nav_buttons.items():
            if btn_name == name:
                button.configure(fg_color=("gray75", "gray25"))
            else:
                button.configure(fg_color="transparent")

        for frame in [self.import_frame, self.color_frame, self.filter_frame, self.edge_frame, self.binary_frame, self.morphology_frame]:
            frame.grid_forget()

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
            self.controller.save_modifications()
            messagebox.showinfo("Sucesso", "Modificações salvas! Agora você pode aplicar outras transformações.")
        else:
            messagebox.showwarning("Aviso", "Nenhuma modificação para salvar!")

    def reset_image(self):
        if self.image_model.original:
            self.controller.reset_image()
            self.intensity_var.set(1.0)
            self.iterations_var.set(1)
            self.on_intensity_change(1.0)
            self.on_iterations_change(1)
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
            messagebox.showinfo("Sucesso", "Imagem resetada para o estado original!")

    def export_image(self):
        if not self.image_model.processed:
            messagebox.showwarning("Aviso", "Nenhuma imagem para exportar!")
            return
        filename = filedialog.asksaveasfilename(title='Salvar imagem', defaultextension='.png', filetypes=EXPORT_TYPES)
        if filename:
            try:
                self.controller.export(filename)
                messagebox.showinfo("Sucesso", f"Imagem salva como {filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
