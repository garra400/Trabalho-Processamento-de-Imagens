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

    def on_iterations_change(self, value):
        self.app_state.iterations = int(value)
        self.iterations_label.configure(text=f"{int(value)}")

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
            parent.grid_columnconfigure((0, 1, 2, 3), weight=1)
            self.create_intensity_toolbar(parent)
            ctk.CTkLabel(parent, text="Filtros:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, columnspan=4, pady=(10, 5))
            ctk.CTkButton(parent, text="Blur", command=lambda: self.on_apply_filter("blur")).grid(row=2, column=0, padx=5, pady=5)
            ctk.CTkButton(parent, text="Sharpen", command=lambda: self.on_apply_filter("sharpen")).grid(row=2, column=1, padx=5, pady=5)
            ctk.CTkButton(parent, text="Emboss", command=lambda: self.on_apply_filter("emboss")).grid(row=2, column=2, padx=5, pady=5)
            ctk.CTkButton(parent, text="Smooth", command=lambda: self.on_apply_filter("smooth")).grid(row=2, column=3, padx=5, pady=5)

        self.filter_image_area, self.filter_image_label = self.setup_processing_page(self.filter_frame, "Filtros", create_filter_controls)

    def setup_edge_page(self):
        def create_edge_controls(parent):
            parent.grid_columnconfigure((0, 1, 2), weight=1)
            self.create_intensity_toolbar(parent)
            ctk.CTkLabel(parent, text="Detector de Borda:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, columnspan=3, pady=(10, 5))
            ctk.CTkButton(parent, text="Canny", command=lambda: self.on_detect_edges("canny")).grid(row=2, column=0, padx=5, pady=5)
            ctk.CTkButton(parent, text="Sobel", command=lambda: self.on_detect_edges("sobel")).grid(row=2, column=1, padx=5, pady=5)
            ctk.CTkButton(parent, text="Laplacian", command=lambda: self.on_detect_edges("laplacian")).grid(row=2, column=2, padx=5, pady=5)

        self.edge_image_area, self.edge_image_label = self.setup_processing_page(self.edge_frame, "Detector de Borda", create_edge_controls)

    def setup_binary_page(self):
        def create_binary_controls(parent):
            parent.grid_columnconfigure((0, 1, 2), weight=1)
            self.create_intensity_toolbar(parent)
            ctk.CTkLabel(parent, text="Binarização:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, columnspan=3, pady=(10, 5))
            ctk.CTkButton(parent, text="Threshold Simples", command=lambda: self.on_binarize("simple")).grid(row=2, column=0, padx=5, pady=5)
            ctk.CTkButton(parent, text="Threshold Adaptativo", command=lambda: self.on_binarize("adaptive")).grid(row=2, column=1, padx=5, pady=5)
            ctk.CTkButton(parent, text="Otsu", command=lambda: self.on_binarize("otsu")).grid(row=2, column=2, padx=5, pady=5)

        self.binary_image_area, self.binary_image_label = self.setup_processing_page(self.binary_frame, "Binarização", create_binary_controls)

    def setup_morphology_page(self):
        def create_morphology_controls(parent):
            parent.grid_columnconfigure((0, 1, 2, 3), weight=1)
            self.create_intensity_toolbar(parent)
            ctk.CTkLabel(parent, text="Morfologia Matemática:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, columnspan=4, pady=(10, 5))
            ctk.CTkButton(parent, text="Erosão", command=lambda: self.on_apply_morphology("erosion")).grid(row=2, column=0, padx=5, pady=5)
            ctk.CTkButton(parent, text="Dilatação", command=lambda: self.on_apply_morphology("dilation")).grid(row=2, column=1, padx=5, pady=5)
            ctk.CTkButton(parent, text="Abertura", command=lambda: self.on_apply_morphology("opening")).grid(row=2, column=2, padx=5, pady=5)
            ctk.CTkButton(parent, text="Fechamento", command=lambda: self.on_apply_morphology("closing")).grid(row=2, column=3, padx=5, pady=5)

        self.morphology_image_area, self.morphology_image_label = self.setup_processing_page(self.morphology_frame, "Morfologia Matemática", create_morphology_controls)

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
        if not self.image_model.original:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro!")
            return
        try:
            self.controller.detect_edges(method)
            self.update_preview_image(self.edge_image_label)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na detecção de bordas: {str(e)}")

    def on_binarize(self, method: str):
        if not self.image_model.original:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro!")
            return
        try:
            self.controller.binarize(method)
            self.update_preview_image(self.binary_image_label)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na binarização: {str(e)}")

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
