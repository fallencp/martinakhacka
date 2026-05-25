import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import os
from ctypes import windll, create_unicode_buffer

class CustomAmateurUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Martinhack")
        self.root.geometry("850x550") 
        self.root.configure(bg="#4a4a4a") 
        
        # Remove standard Windows border framing
        self.root.overrideredirect(True)
        
        self.is_fullscreen = False
        self.is_muted = False
        self.drag_x = 0
        self.drag_y = 0
        
        # --- PATH RESOLUTION ENGINE ---
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_path = os.path.join(self.script_dir, "icons")
        
        self.font_name = "Arial" 
        
        # --- PORTABLE WIN32 FONT EMBEDDING ---
        font_filename = "papyrus.ttf"  
        full_font_path = os.path.join(self.assets_path, font_filename)
        
        if os.path.exists(full_font_path):
            try:
                path_buffer = create_unicode_buffer(full_font_path)
                num_fonts_added = windll.gdi32.AddFontResourceExW(path_buffer, 0x10 | 0x20, 0)
                if num_fonts_added > 0:
                    self.font_name = "Papyrus"
            except Exception:
                pass
            
        self.font_papyrus_bold = (self.font_name, 12, "bold")
        self.font_papyrus_regular = (self.font_name, 11)
        
        self.img_cache = {} 
        self.load_all_icons()
        
        # Start background music loop at startup
        self.play_background_music()
        
        # Pre-load loading screen GIF sequences so it's ready to show instantly
        self.loading_frame = None
        self.gif_frames = []
        self.gif_frame_index = 0
        self.preload_loading_gif()
        
        # --- BUILD BASE MAIN UI ---
        self.build_ui()
        
        # --- KEYBOARD TRIGGER BINDINGS ---
        self.root.bind("<KeyPress-space>", self.show_loading_screen)
        self.root.bind("<KeyRelease-space>", self.hide_loading_screen)

    def load_all_icons(self):
        """Pre-loads, scales, and locks asset images securely in memory."""
        icon_files = {
            "background": ("background.png", (610, 360)),
            "close": ("close.png", (24, 24)),
            "execute": ("execute.png", (30, 30)),     # Made slightly bigger (from 20 to 30)
            "fullscreen": ("fullscreen.png", (24, 24)),
            "inject": ("inject.png", (140, 140)), 
            "load": ("load.png", (30, 30)),           # Made slightly bigger (from 20 to 30)
            "logo": ("logo.png", (140, 35)),
            "minimize": ("minimize.png", (24, 24)),
            "save": ("save.png", (30, 30)),           # Made slightly bigger (from 20 to 30)
            "mute": ("mute.png", (24, 24)) 
        }
        
        for key, (filename, size) in icon_files.items():
            full_path = os.path.join(self.assets_path, filename)
            if os.path.exists(full_path):
                try:
                    img = Image.open(full_path)
                    img = img.resize(size, Image.Resampling.LANCZOS)
                    self.img_cache[key] = ImageTk.PhotoImage(img)
                except Exception:
                    self.img_cache[key] = self.create_fallback(size)
            else:
                self.img_cache[key] = self.create_fallback(size)

    def create_fallback(self, size):
        img = Image.new("RGBA", size, color="#ffffff")
        return ImageTk.PhotoImage(img)

    # --- WIN32 AUDIO DEVICE SUBSYSTEM CONTROL ---
    def play_background_music(self):
        music_path = os.path.join(self.assets_path, "music.mp3")
        if os.path.exists(music_path):
            try:
                buffer_size = 256
                short_path_buffer = create_unicode_buffer(buffer_size)
                windll.kernel32.GetShortPathNameW(music_path, short_path_buffer, buffer_size)
                short_path = short_path_buffer.value
                
                windll.winmm.mciSendStringW(f"open {short_path} type mpegvideo alias bgmusic", None, 0, 0)
                windll.winmm.mciSendStringW("play bgmusic repeat", None, 0, 0)
            except Exception:
                pass

    def toggle_mute(self):
        """Mutes and unmutes the application music stream on command click."""
        try:
            if not self.is_muted:
                windll.winmm.mciSendStringW("pause bgmusic", None, 0, 0)
                self.is_muted = True
            else:
                windll.winmm.mciSendStringW("resume bgmusic", None, 0, 0)
                self.is_muted = False
        except Exception:
            pass

    def play_click_sound(self):
        """Plays the brief mechanical button interface sound asset on user interactions."""
        click_path = os.path.join(self.assets_path, "click.mp3")
        if os.path.exists(click_path):
            try:
                buffer_size = 256
                short_path_buffer = create_unicode_buffer(buffer_size)
                windll.kernel32.GetShortPathNameW(click_path, short_path_buffer, buffer_size)
                short_path = short_path_buffer.value
                
                # Use a specific handle tracking alias sequence to play multiple times without collision stalls
                windll.winmm.mciSendStringW(f"open {short_path} type mpegvideo alias clicksound", None, 0, 0)
                windll.winmm.mciSendStringW("seek clicksound to start", None, 0, 0)
                windll.winmm.mciSendStringW("play clicksound", None, 0, 0)
            except Exception:
                pass

    # --- CONDITIONAL SPACEBAR LOADING ENGINE ---
    def preload_loading_gif(self):
        """Caches GIF sequence data frames in advance to avoid memory lag on keypress spikes."""
        gif_path = os.path.join(self.assets_path, "gif.gif")
        if os.path.exists(gif_path):
            try:
                pil_gif = Image.open(gif_path)
                for frame in ImageSequence.Iterator(pil_gif):
                    resized_frame = frame.resize((200, 200), Image.Resampling.LANCZOS).convert("RGBA")
                    self.gif_frames.append(ImageTk.PhotoImage(resized_frame))
            except Exception:
                pass

    def show_loading_screen(self, event=None):
        """Instantly covers the UI interface container with the loading panel while Space is held."""
        if self.loading_frame is not None:
            return
            
        # Pause background track completely during loading event sequence handles
        try:
            windll.winmm.mciSendStringW("pause bgmusic", None, 0, 0)
        except Exception:
            pass

        # Trigger standalone localized loading loop track sequence audio context assets
        load_track_path = os.path.join(self.assets_path, "loading.mp3")
        if os.path.exists(load_track_path):
            try:
                buffer_size = 256
                short_path_buffer = create_unicode_buffer(buffer_size)
                windll.kernel32.GetShortPathNameW(load_track_path, short_path_buffer, buffer_size)
                short_path = short_path_buffer.value
                
                windll.winmm.mciSendStringW(f"open {short_path} type mpegvideo alias loadingmusic", None, 0, 0)
                windll.winmm.mciSendStringW("seek loadingmusic to start", None, 0, 0)
                windll.winmm.mciSendStringW("play loadingmusic repeat", None, 0, 0)
            except Exception:
                pass

        self.loading_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.loading_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        if self.gif_frames:
            self.gif_label = tk.Label(self.loading_frame, image=self.gif_frames[0], bg="#1e1e1e")
            self.gif_label.pack(expand=True, pady=(40, 0))
            self.gif_frame_index = 0
            self.animate_loading_gif()
        else:
            self.gif_label = tk.Label(self.loading_frame, text="[GIF LAYERING ACTIVE]", fg="#ffffff", bg="#1e1e1e")
            self.gif_label.pack(expand=True)
            
        self.loading_text = tk.Label(
            self.loading_frame, 
            text="loading...", 
            font=(self.font_name, 14, "italic"), 
            fg="#ffffff", 
            bg="#1e1e1e"
        )
        self.loading_text.pack(pady=(0, 60))

    def animate_loading_gif(self):
        """Advances GIF frames inside the temporary overlay panel container."""
        if self.loading_frame and self.gif_frames:
            self.gif_frame_index = (self.gif_frame_index + 1) % len(self.gif_frames)
            self.gif_label.configure(image=self.gif_frames[self.gif_frame_index])
            self.root.after(50, self.animate_loading_gif)

    def hide_loading_screen(self, event=None):
        """Destroys the loading layer immediately upon lifting the key trigger."""
        if self.loading_frame:
            # Terminate running loading animation audio streams cleanly
            try:
                windll.winmm.mciSendStringW("stop loadingmusic", None, 0, 0)
                windll.winmm.mciSendStringW("close loadingmusic", None, 0, 0)
            except Exception:
                pass

            # Resume original music loop context streams securely if layout states aren't manually muted
            if not self.is_muted:
                try:
                    windll.winmm.mciSendStringW("resume bgmusic", None, 0, 0)
                except Exception:
                    pass

            self.loading_frame.destroy()
            self.loading_frame = None

    # --- CUSTOM WINDOW DRAGGING ENGINE ---
    def start_window_drag(self, event):
        self.drag_x = event.x
        self.drag_y = event.y

    def execute_window_drag(self, event):
        deltax = event.x - self.drag_x
        deltay = event.y - self.drag_y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def toggle_fullscreen(self):
        if not self.is_fullscreen:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            self.root.geometry(f"{screen_width}x{screen_height}+0+0")
            self.is_fullscreen = True
        else:
            self.root.geometry("850x550+100+100")
            self.is_fullscreen = False

    def build_ui(self):
        # --- TOP TITLE BAR ---
        top_bar = tk.Frame(self.root, bg="#ffffff", height=45, bd=0)
        top_bar.pack(fill="x", side="top")
        top_bar.pack_propagate(False)

        top_bar.bind("<Button-1>", self.start_window_drag)
        top_bar.bind("<B1-Motion>", self.execute_window_drag)

        if "logo" in self.img_cache:
            logo_label = tk.Label(top_bar, image=self.img_cache["logo"], bg="#ffffff")
            logo_label.pack(side="left", padx=10, pady=5)
            logo_label.bind("<Button-1>", self.start_window_drag)
            logo_label.bind("<B1-Motion>", self.execute_window_drag)

        # --- WINDOW CONTROL UTILITY BUTTON PACK ---
        btn_close = tk.Button(top_bar, image=self.img_cache["close"], bg="#ffffff", bd=0, 
                              activebackground="#ffffff", command=self.root.destroy)
        btn_close.pack(side="right", padx=5)
        
        btn_full = tk.Button(top_bar, image=self.img_cache["fullscreen"], bg="#ffffff", bd=0, 
                              activebackground="#ffffff", command=self.toggle_fullscreen)
        btn_full.pack(side="right", padx=5)
        
        btn_min = tk.Button(top_bar, image=self.img_cache["minimize"], bg="#ffffff", bd=0, 
                             activebackground="#ffffff", command=self.root.iconify)
        btn_min.pack(side="right", padx=5)

        btn_mute = tk.Button(top_bar, image=self.img_cache["mute"], bg="#ffffff", bd=0, 
                             activebackground="#ffffff", command=self.toggle_mute)
        btn_mute.pack(side="right", padx=5)

        # --- MAIN INNER CONTENT WRAPPER ---
        main_body = tk.Frame(self.root, bg="#4a4a4a")
        main_body.pack(fill="both", expand=True, padx=15, pady=15)

        # LEFT COLUMN SIDEBAR
        sidebar = tk.Frame(main_body, bg="#ffffff", width=160, bd=0)
        sidebar.pack(side="left", fill="y", padx=(0, 15))
        sidebar.pack_propagate(False)

        lbl_all_scripts = tk.Label(sidebar, text="all scripts", font=self.font_papyrus_bold, fg="#cc2929", bg="#ffffff")
        lbl_all_scripts.pack(anchor="nw", padx=10, pady=10)

        list_container = tk.Frame(sidebar, bg="#ffffff")
        list_container.pack(fill="both", expand=True, padx=10)

        # RIGHT COLUMN PANEL
        right_content = tk.Frame(main_body, bg="#4a4a4a")
        right_content.pack(side="right", fill="both", expand=True)

        self.display_canvas = tk.Canvas(right_content, bg="#ffffff", bd=0, highlightthickness=0)
        self.display_canvas.pack(fill="both", expand=True)

        if "background" in self.img_cache:
            self.display_canvas.create_image(0, 0, image=self.img_cache["background"], anchor="nw")

        self.code_editor = tk.Text(
            self.display_canvas,
            font=("Courier New", 12, "bold"),
            fg="#000000",
            insertbackground="#000000",
            bg="#ffffff", 
            bd=0,
            relief="flat",
            undo=True
        )
        self.display_canvas.create_window(0, 0, window=self.code_editor, anchor="nw", width=610, height=360)
        self.code_editor.insert("1.0", "-- Paste your executable code here...\nprint('Hello World')")

        # --- HORIZONTAL TOOLBAR PANEL ---
        button_row = tk.Frame(right_content, bg="#4a4a4a")
        button_row.pack(fill="x", side="bottom", pady=(15, 0))

        btn_center_tray = tk.Frame(button_row, bg="#4a4a4a")
        btn_center_tray.pack(anchor="center")

        # Configuration dictionary rearranged left-to-right (pinned inject explicitly on the right)
        btn_config = [
            ("execute", self.img_cache["execute"], "#00ff00"),
            ("open", self.img_cache["load"], "#ffaa00"),
            ("save", self.img_cache["save"], "#ffffff"),
            ("inject", self.img_cache["inject"], "#00ff00")
        ]

        for text, icon, fg_color in btn_config:
            is_inject = (text == "inject")
            pad_y = 5 if is_inject else 2
            bd_size = 3 if is_inject else 1
            
            b = tk.Button(
                btn_center_tray,
                image=icon,
                text=f" {text} ",
                compound="left",
                font=self.font_papyrus_regular,
                fg=fg_color,
                bg="#001aff", 
                activebackground="#0011cc",
                activeforeground="#ffffff",
                bd=bd_size,
                relief="raised",
                command=self.play_click_sound  # Plays click.mp3 immediately upon selection triggers
            )
            b.image = icon 
            b.pack(side="left", padx=6, pady=pad_y)

if __name__ == "__main__":
    app = tk.Tk()
    ui = CustomAmateurUI(app)
    app.mainloop()