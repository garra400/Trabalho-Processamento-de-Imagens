import customtkinter as ctk
import os
from PIL import Image, ImageFilter, ImageEnhance, ImageTk
import cv2
import numpy as np
from tkinter import filedialog, messagebox
import copy

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Trabalho Bimestral do Pedro - Processamento de Imagens")
        self.geometry("900x650")

        # Estado da aplicação
        self.current_image = None  # Imagem original
        self.processed_image = None  # Imagem com modificações
        self.imported_files = []  # Lista de arquivos importados
        
        # Controles de intensidade e repetições
        self.intensity_var = ctk.DoubleVar(value=1.0)
        self.iterations_var = ctk.IntVar(value=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Carregar imagens dos ícones (usando placeholder se não existir)
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "")
        try:
            self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "icone.png")), size=(26, 26))
        except:
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

        # Cabeçalho da navegação
        self.nav_frame_label = ctk.CTkLabel(
            self.navigation_frame,
            text="  Processamento de Imagens  ",
            image=self.logo_image,
            compound="left",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.nav_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # Botões de navegação
        self.create_navigation_buttons()

        # Criar todas as páginas
        self.create_all_pages()

        # Página inicial
        self.selected_frame_name = "import"
        self.select_frame_by_name("import")

    def create_navigation_buttons(self):
        buttons_config = [
            ("import", "Importar Imagem", 1),
            ("color", "Conversão de Cor", 2),
            ("filter", "Filtros", 3),
            ("edge", "Detector de Borda", 4),
            ("binary", "Binarização", 5),
            ("morphology", "Morfologia", 6)
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
        # Criar todas as páginas
        self.import_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.color_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.filter_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.edge_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.binary_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.morphology_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")

        # Configurar layout para cada página
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

        # Área da imagem
        self.import_image_area = ctk.CTkFrame(self.import_frame, fg_color=("gray95", "gray10"))
        self.import_image_area.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        self.import_image_area.grid_rowconfigure(0, weight=1)
        self.import_image_area.grid_columnconfigure(0, weight=1)
        
        self.import_image_label = ctk.CTkLabel(
            self.import_image_area, 
            text="Clique em 'Abrir' para selecionar uma imagem",
            font=ctk.CTkFont(size=16)
        )
        self.import_image_label.grid(row=0, column=0)

        # Barra de ferramentas
        toolbar = ctk.CTkFrame(self.import_frame, height=48, fg_color=("gray90", "gray15"))
        toolbar.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        toolbar.grid_columnconfigure(3, weight=1)

        ctk.CTkButton(toolbar, text="Abrir", command=self.open_image).grid(row=0, column=0, padx=(10, 6), pady=8)
        ctk.CTkButton(toolbar, text="Exportar", command=self.export_image).grid(row=0, column=1, padx=6, pady=8)

        # Faixa de arquivos importados
        self.import_files_strip = ctk.CTkScrollableFrame(self.import_frame, height=120, fg_color=("gray92", "gray18"))
        self.import_files_strip.grid(row=2, column=0, sticky="nsew", padx=10, pady=(5, 10))
        self.import_files_strip.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.import_files_strip, text="Nenhum arquivo importado", anchor="w").grid(row=0, column=0, sticky="ew", padx=10, pady=6)

    def create_intensity_toolbar(self, parent):
        """Cria a toolbar com controles de intensidade e repetições"""
        # Frame para controles de intensidade
        intensity_frame = ctk.CTkFrame(parent, fg_color=("gray88", "gray20"))
        intensity_frame.grid(row=0, column=0, columnspan=4, sticky="ew", padx=5, pady=(5, 10))
        intensity_frame.grid_columnconfigure(1, weight=1)
        intensity_frame.grid_columnconfigure(3, weight=1)
        
        # Controle de Intensidade
        ctk.CTkLabel(intensity_frame, text="Intensidade:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=5)
        
        self.intensity_slider = ctk.CTkSlider(
            intensity_frame, 
            from_=0.1, 
            to=3.0, 
            number_of_steps=29,
            variable=self.intensity_var,
            command=self.on_intensity_change
        )
        self.intensity_slider.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        
        self.intensity_label = ctk.CTkLabel(intensity_frame, text="1.0")
        self.intensity_label.grid(row=0, column=2, padx=5, pady=5)
        
        # Controle de Repetições
        ctk.CTkLabel(intensity_frame, text="Repetições:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=3, padx=(20, 10), pady=5)
        
        self.iterations_slider = ctk.CTkSlider(
            intensity_frame, 
            from_=1, 
            to=10, 
            number_of_steps=9,
            variable=self.iterations_var,
            command=self.on_iterations_change
        )
        self.iterations_slider.grid(row=0, column=4, sticky="ew", padx=10, pady=5)
        
        self.iterations_label = ctk.CTkLabel(intensity_frame, text="1")
        self.iterations_label.grid(row=0, column=5, padx=5, pady=5)

    def on_intensity_change(self, value):
        """Callback para mudança de intensidade"""
        self.intensity_label.configure(text=f"{value:.1f}")

    def on_iterations_change(self, value):
        """Callback para mudança de repetições"""
        self.iterations_label.configure(text=f"{int(value)}")

    def setup_processing_page(self, frame, title, controls_func):
        """Configuração padrão para páginas de processamento"""
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=0)
        frame.grid_rowconfigure(2, weight=0)
        frame.grid_rowconfigure(3, weight=0)
        frame.grid_columnconfigure(0, weight=1)

        # Área da imagem
        image_area = ctk.CTkFrame(frame, fg_color=("gray95", "gray10"))
        image_area.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        image_area.grid_rowconfigure(0, weight=1)
        image_area.grid_columnconfigure(0, weight=1)
        
        image_label = ctk.CTkLabel(image_area, text=f"{title} - Prévia da imagem", font=ctk.CTkFont(size=16))
        image_label.grid(row=0, column=0)

        # Barra de ferramentas
        toolbar = ctk.CTkFrame(frame, height=48, fg_color=("gray90", "gray15"))
        toolbar.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        toolbar.grid_columnconfigure(10, weight=1)

        ctk.CTkButton(toolbar, text="Salvar Modificações", command=self.save_modifications).grid(row=0, column=0, padx=(10, 6), pady=8)
        ctk.CTkButton(toolbar, text="Exportar", command=self.export_image).grid(row=0, column=1, padx=6, pady=8)
        ctk.CTkButton(toolbar, text="Resetar", command=self.reset_image).grid(row=0, column=2, padx=6, pady=8)

        # Controles específicos
        controls_frame = ctk.CTkFrame(frame, height=160, fg_color=("gray92", "gray18"))
        controls_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(5, 10))
        
        controls_func(controls_frame)
        
        return image_area, image_label

    def setup_color_page(self):
        def create_color_controls(parent):
            parent.grid_columnconfigure((0, 1, 2, 3), weight=1)
            
            # Toolbar de intensidade
            self.create_intensity_toolbar(parent)
            
            ctk.CTkLabel(parent, text="Conversão de Cor:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, columnspan=4, pady=(10, 5))
            
            ctk.CTkButton(parent, text="RGB para Grayscale", command=lambda: self.convert_color("grayscale")).grid(row=2, column=0, padx=5, pady=5)
            ctk.CTkButton(parent, text="RGB para HSV", command=lambda: self.convert_color("hsv")).grid(row=2, column=1, padx=5, pady=5)
            ctk.CTkButton(parent, text="RGB para LAB", command=lambda: self.convert_color("lab")).grid(row=2, column=2, padx=5, pady=5)
            ctk.CTkButton(parent, text="Inverter Cores", command=lambda: self.convert_color("invert")).grid(row=2, column=3, padx=5, pady=5)
            
        self.color_image_area, self.color_image_label = self.setup_processing_page(self.color_frame, "Conversão de Cor", create_color_controls)

    def setup_filter_page(self):
        def create_filter_controls(parent):
            parent.grid_columnconfigure((0, 1, 2, 3), weight=1)
            
            # Toolbar de intensidade
            self.create_intensity_toolbar(parent)
            
            ctk.CTkLabel(parent, text="Filtros:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, columnspan=4, pady=(10, 5))
            
            ctk.CTkButton(parent, text="Blur", command=lambda: self.apply_filter("blur")).grid(row=2, column=0, padx=5, pady=5)
            ctk.CTkButton(parent, text="Sharpen", command=lambda: self.apply_filter("sharpen")).grid(row=2, column=1, padx=5, pady=5)
            ctk.CTkButton(parent, text="Emboss", command=lambda: self.apply_filter("emboss")).grid(row=2, column=2, padx=5, pady=5)
            ctk.CTkButton(parent, text="Smooth", command=lambda: self.apply_filter("smooth")).grid(row=2, column=3, padx=5, pady=5)
            
        self.filter_image_area, self.filter_image_label = self.setup_processing_page(self.filter_frame, "Filtros", create_filter_controls)

    def setup_edge_page(self):
        def create_edge_controls(parent):
            parent.grid_columnconfigure((0, 1, 2), weight=1)
            
            # Toolbar de intensidade
            self.create_intensity_toolbar(parent)
            
            ctk.CTkLabel(parent, text="Detector de Borda:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, columnspan=3, pady=(10, 5))
            
            ctk.CTkButton(parent, text="Canny", command=lambda: self.detect_edges("canny")).grid(row=2, column=0, padx=5, pady=5)
            ctk.CTkButton(parent, text="Sobel", command=lambda: self.detect_edges("sobel")).grid(row=2, column=1, padx=5, pady=5)
            ctk.CTkButton(parent, text="Laplacian", command=lambda: self.detect_edges("laplacian")).grid(row=2, column=2, padx=5, pady=5)
            
        self.edge_image_area, self.edge_image_label = self.setup_processing_page(self.edge_frame, "Detector de Borda", create_edge_controls)

    def setup_binary_page(self):
        def create_binary_controls(parent):
            parent.grid_columnconfigure((0, 1, 2), weight=1)
            
            # Toolbar de intensidade
            self.create_intensity_toolbar(parent)
            
            ctk.CTkLabel(parent, text="Binarização:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, columnspan=3, pady=(10, 5))
            
            ctk.CTkButton(parent, text="Threshold Simples", command=lambda: self.binarize("simple")).grid(row=2, column=0, padx=5, pady=5)
            ctk.CTkButton(parent, text="Threshold Adaptativo", command=lambda: self.binarize("adaptive")).grid(row=2, column=1, padx=5, pady=5)
            ctk.CTkButton(parent, text="Otsu", command=lambda: self.binarize("otsu")).grid(row=2, column=2, padx=5, pady=5)
            
        self.binary_image_area, self.binary_image_label = self.setup_processing_page(self.binary_frame, "Binarização", create_binary_controls)

    def setup_morphology_page(self):
        def create_morphology_controls(parent):
            parent.grid_columnconfigure((0, 1, 2, 3), weight=1)
            
            # Toolbar de intensidade
            self.create_intensity_toolbar(parent)
            
            ctk.CTkLabel(parent, text="Morfologia Matemática:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, columnspan=4, pady=(10, 5))
            
            ctk.CTkButton(parent, text="Erosão", command=lambda: self.apply_morphology("erosion")).grid(row=2, column=0, padx=5, pady=5)
            ctk.CTkButton(parent, text="Dilatação", command=lambda: self.apply_morphology("dilation")).grid(row=2, column=1, padx=5, pady=5)
            ctk.CTkButton(parent, text="Abertura", command=lambda: self.apply_morphology("opening")).grid(row=2, column=2, padx=5, pady=5)
            ctk.CTkButton(parent, text="Fechamento", command=lambda: self.apply_morphology("closing")).grid(row=2, column=3, padx=5, pady=5)
            
        self.morphology_image_area, self.morphology_image_label = self.setup_processing_page(self.morphology_frame, "Morfologia Matemática", create_morphology_controls)

    def select_frame_by_name(self, name: str):
        # Atualizar cores dos botões
        for btn_name, button in self.nav_buttons.items():
            if btn_name == name:
                button.configure(fg_color=("gray75", "gray25"))
            else:
                button.configure(fg_color="transparent")

        # Ocultar todas as páginas
        for frame in [self.import_frame, self.color_frame, self.filter_frame, 
                     self.edge_frame, self.binary_frame, self.morphology_frame]:
            frame.grid_forget()

        # Mostrar página selecionada
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
        filetypes = (
            ('Imagens', '*.png *.jpg *.jpeg *.gif *.bmp *.tiff'),
            ('Todos os arquivos', '*.*')
        )
        
        filename = filedialog.askopenfilename(
            title='Selecionar imagem',
            initialdir=os.getcwd(),
            filetypes=filetypes
        )
        
        if filename:
            try:
                # Carregar imagem
                self.current_image = Image.open(filename)
                self.processed_image = self.current_image.copy()
                
                # Adicionar à lista de arquivos importados
                if filename not in self.imported_files:
                    self.imported_files.append(filename)
                    self.update_files_list()
                
                # Atualizar preview
                self.update_preview_image(self.import_image_label)
                
                messagebox.showinfo("Sucesso", "Imagem carregada com sucesso!")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar imagem: {str(e)}")

    def update_files_list(self):
        # Limpar lista atual
        for widget in self.import_files_strip.winfo_children():
            widget.destroy()
            
        if not self.imported_files:
            ctk.CTkLabel(self.import_files_strip, text="Nenhum arquivo importado", anchor="w").grid(row=0, column=0, sticky="ew", padx=10, pady=6)
        else:
            for i, filepath in enumerate(self.imported_files):
                filename = os.path.basename(filepath)
                file_frame = ctk.CTkFrame(self.import_files_strip, height=40, fg_color=("gray85", "gray25"))
                file_frame.grid(row=i, column=0, sticky="ew", padx=5, pady=2)
                file_frame.grid_columnconfigure(0, weight=1)
                
                ctk.CTkLabel(file_frame, text=filename, anchor="w").grid(row=0, column=0, sticky="ew", padx=10, pady=5)
                ctk.CTkButton(file_frame, text="Carregar", width=80, 
                             command=lambda f=filepath: self.load_file(f)).grid(row=0, column=1, padx=5, pady=5)

    def load_file(self, filepath):
        try:
            self.current_image = Image.open(filepath)
            self.processed_image = self.current_image.copy()
            self.update_preview_image(self.import_image_label)
            messagebox.showinfo("Sucesso", f"Imagem {os.path.basename(filepath)} carregada!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar arquivo: {str(e)}")

    def update_preview_image(self, label):
        if self.processed_image:
            # Redimensionar para o preview
            display_image = self.processed_image.copy()
            display_image.thumbnail((400, 300), Image.Resampling.LANCZOS)
            
            # Converter para CTkImage
            ctk_image = ctk.CTkImage(light_image=display_image, dark_image=display_image, 
                                   size=(display_image.width, display_image.height))
            
            label.configure(image=ctk_image, text="")
        else:
            label.configure(image=None, text="Nenhuma imagem carregada")

    def convert_color(self, conversion_type):
        if not self.current_image:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro!")
            return
            
        try:
            intensity = self.intensity_var.get()
            iterations = int(self.iterations_var.get())
            
            result_image = self.current_image.copy()
            
            for i in range(iterations):
                if conversion_type == "grayscale":
                    gray_image = result_image.convert('L').convert('RGB')
                    if intensity < 1.0:
                        # Misturar com a imagem original
                        result_image = Image.blend(result_image, gray_image, intensity)
                    else:
                        result_image = gray_image
                        
                elif conversion_type == "hsv":
                    result_image = result_image.convert('HSV').convert('RGB')
                    
                elif conversion_type == "lab":
                    # Conversão LAB usando OpenCV
                    cv_image = cv2.cvtColor(np.array(result_image), cv2.COLOR_RGB2LAB)
                    result_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_LAB2RGB))
                    
                elif conversion_type == "invert":
                    np_image = np.array(result_image)
                    inverted = 255 - np_image
                    inverted_image = Image.fromarray(inverted)
                    if intensity < 1.0:
                        result_image = Image.blend(result_image, inverted_image, intensity)
                    else:
                        result_image = inverted_image
                        
            self.processed_image = result_image
            self.update_preview_image(self.color_image_label)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na conversão: {str(e)}")

    def apply_filter(self, filter_type):
        if not self.current_image:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro!")
            return
            
        try:
            intensity = self.intensity_var.get()
            iterations = int(self.iterations_var.get())
            
            result_image = self.current_image.copy()
            
            for i in range(iterations):
                if filter_type == "blur":
                    # Aplicar blur com intensidade variável
                    radius = max(1, int(intensity * 2))
                    filtered_image = result_image.filter(ImageFilter.GaussianBlur(radius=radius))
                    
                elif filter_type == "sharpen":
                    # Aplicar sharpen
                    filtered_image = result_image.filter(ImageFilter.SHARPEN)
                    if intensity != 1.0:
                        filtered_image = Image.blend(result_image, filtered_image, min(intensity, 1.0))
                        
                elif filter_type == "emboss":
                    filtered_image = result_image.filter(ImageFilter.EMBOSS)
                    if intensity != 1.0:
                        filtered_image = Image.blend(result_image, filtered_image, min(intensity, 1.0))
                        
                elif filter_type == "smooth":
                    filtered_image = result_image.filter(ImageFilter.SMOOTH_MORE if intensity > 1.5 else ImageFilter.SMOOTH)
                    
                result_image = filtered_image
                
            self.processed_image = result_image
            self.update_preview_image(self.filter_image_label)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no filtro: {str(e)}")

    def detect_edges(self, method):
        if not self.current_image:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro!")
            return
            
        try:
            intensity = self.intensity_var.get()
            
            # Converter para numpy array
            cv_image = cv2.cvtColor(np.array(self.current_image), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            if method == "canny":
                # Usar intensidade para ajustar os thresholds
                low_threshold = int(50 * intensity)
                high_threshold = int(150 * intensity)
                edges = cv2.Canny(gray, low_threshold, high_threshold)
                
            elif method == "sobel":
                ksize = max(3, int(3 * intensity))
                if ksize % 2 == 0:
                    ksize += 1  # Garantir que seja ímpar
                sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
                sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
                edges = np.sqrt(sobelx**2 + sobely**2)
                edges = np.uint8(edges * intensity)
                
            elif method == "laplacian":
                ksize = max(3, int(3 * intensity))
                if ksize % 2 == 0:
                    ksize += 1
                edges = cv2.Laplacian(gray, cv2.CV_64F, ksize=ksize)
                edges = np.uint8(np.absolute(edges) * intensity)
            
            # Converter de volta para PIL
            self.processed_image = Image.fromarray(edges).convert('RGB')
            self.update_preview_image(self.edge_image_label)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na detecção de bordas: {str(e)}")

    def binarize(self, method):
        if not self.current_image:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro!")
            return
            
        try:
            intensity = self.intensity_var.get()
            
            # Converter para escala de cinza
            gray = cv2.cvtColor(np.array(self.current_image), cv2.COLOR_RGB2GRAY)
            
            if method == "simple":
                # Usar intensidade para ajustar o threshold
                threshold_value = int(127 * intensity)
                _, binary = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
                
            elif method == "adaptive":
                # Usar intensidade para ajustar o block size
                block_size = max(3, int(11 * intensity))
                if block_size % 2 == 0:
                    block_size += 1
                binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, 2)
                
            elif method == "otsu":
                _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            self.processed_image = Image.fromarray(binary).convert('RGB')
            self.update_preview_image(self.binary_image_label)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na binarização: {str(e)}")

    def apply_morphology(self, operation):
        if not self.current_image:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro!")
            return
            
        try:
            intensity = self.intensity_var.get()
            iterations = int(self.iterations_var.get())
            
            # Converter para escala de cinza e depois binária
            gray = cv2.cvtColor(np.array(self.current_image), cv2.COLOR_RGB2GRAY)
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            
            # Definir kernel baseado na intensidade
            kernel_size = max(3, int(5 * intensity))
            kernel = np.ones((kernel_size, kernel_size), np.uint8)
            
            result = binary
            for i in range(iterations):
                if operation == "erosion":
                    result = cv2.erode(result, kernel, iterations=1)
                elif operation == "dilation":
                    result = cv2.dilate(result, kernel, iterations=1)
                elif operation == "opening":
                    result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)
                elif operation == "closing":
                    result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
            
            self.processed_image = Image.fromarray(result).convert('RGB')
            self.update_preview_image(self.morphology_image_label)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na morfologia: {str(e)}")

    def save_modifications(self):
        if self.processed_image and self.current_image:
            self.current_image = self.processed_image.copy()
            messagebox.showinfo("Sucesso", "Modificações salvas! Agora você pode aplicar outras transformações.")
        else:
            messagebox.showwarning("Aviso", "Nenhuma modificação para salvar!")

    def reset_image(self):
        if self.current_image:
            self.processed_image = self.current_image.copy()
            # Resetar controles
            self.intensity_var.set(1.0)
            self.iterations_var.set(1)
            self.intensity_label.configure(text="1.0")
            self.iterations_label.configure(text="1")
            
            # Atualizar preview da página atual
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
        if not self.processed_image:
            messagebox.showwarning("Aviso", "Nenhuma imagem para exportar!")
            return
            
        filetypes = (
            ('PNG', '*.png'),
            ('JPEG', '*.jpg'),
            ('Todos os arquivos', '*.*')
        )
        
        filename = filedialog.asksaveasfilename(
            title='Salvar imagem',
            defaultextension='.png',
            filetypes=filetypes
        )
        
        if filename:
            try:
                self.processed_image.save(filename)
                messagebox.showinfo("Sucesso", f"Imagem salva como {filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

if __name__ == "__main__":
    app = App()
    app.mainloop()