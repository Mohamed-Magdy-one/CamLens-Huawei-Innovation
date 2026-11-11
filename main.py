import cv2
import customtkinter as ctk
from PIL import Image
import numpy as np
from interlacer import generate_interlaced_image, generate_calibration_pattern

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class VisionCorrectionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CamLens - Huawei ICT Innovation Engine")
        self.geometry("1000x750")

        self.is_fullscreen = False

        # ربط أزرار الكيبورد للتحكم
        self.bind("<F11>", self.enter_fullscreen)
        self.bind("<Escape>", self.exit_fullscreen)

        # التحكم في الـ Pitch (أسهم الكيبورد)
        self.bind("<Right>", lambda e: self.adjust_pitch(0.1))
        self.bind("<Left>", lambda e: self.adjust_pitch(-0.1))
        self.bind("<Up>", lambda e: self.adjust_pitch(0.01))
        self.bind("<Down>", lambda e: self.adjust_pitch(-0.01))

        # التحكم في الـ Eye Shift (حروف A و D)
        self.bind("d", lambda e: self.adjust_shift(1.0))
        self.bind("a", lambda e: self.adjust_shift(-1.0))
        self.bind("D", lambda e: self.adjust_shift(1.0))
        self.bind("A", lambda e: self.adjust_shift(-1.0))

        # الصورة النشطة حالياً (تُولّد تلقائياً)
        self.active_image = self.create_text_sample()
        self.screen_diag_inches = 15.6  # مقاس الشاشة الافتراضي لحساب الـ PPI

        self.setup_ui()
        self.update_image()

    def create_text_sample(self):
        """توليد صورة اختبار مستند نصي تلقائياً"""
        img = np.ones((600, 900, 3), dtype=np.uint8) * 255
        cv2.putText(img, "CamLens - Vision Correction Text Test", (40, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        cv2.line(img, (40, 80), (860, 80), (150, 150, 150), 2)
        lines = [
            "1. Privacy-First Optical System: Replaces camera eye-tracking.",
            "2. Sub-Pixel Interlacing Engine: Real-time NumPy processing.",
            "3. Refractive Compensation: Adjusts view angles dynamically.",
            "4. High Contrast Reading Mode for Myopia Correction Test.",
            "5. Team Apex_Coders - Huawei ICT Innovation Track 2026."
        ]
        y = 140
        for line in lines:
            cv2.putText(img, line, (40, y), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (30, 30, 30), 1)
            y += 50
        return img

    def create_code_sample(self):
        """توليد صورة اختبار محرر أكواد IDE غامق تلقائياً"""
        img = np.ones((600, 900, 3), dtype=np.uint8) * 25
        cv2.rectangle(img, (0, 0), (70, 600), (40, 40, 40), -1)
        code_lines = [
            ("1", "import numpy as np"),
            ("2", "import cv2"),
            ("3", ""),
            ("4", "def generate_interlaced_image(img, pitch, views):"),
            ("5", "    height, width, _ = img.shape"),
            ("6", "    out_img = np.zeros_like(img)"),
            ("7", "    # Calculate lenticular sub-pixel mapping"),
            ("8", "    cols = np.arange(width)"),
            ("9", "    view_map = np.floor((cols % pitch) / strip_w)"),
            ("10", "    return out_img")
        ]
        y = 55
        for num, line in code_lines:
            cv2.putText(img, num, (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (120, 120, 120), 1)
            cv2.putText(img, line, (90, y), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 198), 1)
            y += 40
        return img

    def create_ui_sample(self):
        """توليد صورة اختبار واجهة مستخدم Dashboard تلقائياً"""
        img = np.ones((600, 900, 3), dtype=np.uint8) * 240
        cv2.rectangle(img, (0, 0), (900, 70), (40, 40, 40), -1)
        cv2.putText(img, "DASHBOARD CONTROL PANEL", (30, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.rectangle(img, (40, 100), (420, 320), (220, 220, 255), -1)
        cv2.putText(img, "Analytics Card", (60, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv2.rectangle(img, (460, 100), (840, 320), (220, 255, 220), -1)
        cv2.putText(img, "Performance Metrics", (480, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv2.rectangle(img, (40, 360), (220, 430), (50, 120, 240), -1)
        cv2.putText(img, "Submit", (80, 405), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        return img

    def setup_ui(self):
        # --- الشريط العلوي ---
        self.top_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent")
        self.top_frame.pack(pady=(10, 0), padx=20, fill="x")

        self.calib_switch = ctk.CTkSwitch(self.top_frame, text="⚙️ Calibration Mode", font=("Arial", 13, "bold"),
                                          command=self.update_image)
        self.calib_switch.pack(side="left", padx=10)

        self.btn_fullscreen = ctk.CTkButton(self.top_frame, text="🖥️ Full Screen (F11)", width=120,
                                            command=self.enter_fullscreen)
        self.btn_fullscreen.pack(side="left", padx=10)

        # ربط الأزرار بمولدات الصور التفاعلية
        self.btn_ui = ctk.CTkButton(self.top_frame, text="UI Test", width=90, command=lambda: self.switch_sample("ui"))
        self.btn_ui.pack(side="right", padx=5)
        self.btn_code = ctk.CTkButton(self.top_frame, text="Code Test", width=90,
                                      command=lambda: self.switch_sample("code"))
        self.btn_code.pack(side="right", padx=5)
        self.btn_text = ctk.CTkButton(self.top_frame, text="Text Test", width=90,
                                      command=lambda: self.switch_sample("text"))
        self.btn_text.pack(side="right", padx=5)

        # --- لوحة القراءات الدقيقة ---
        self.metrics_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#1E1E1E")
        self.metrics_frame.pack(pady=10, padx=20, fill="x")

        self.lbl_pitch_val = ctk.CTkLabel(self.metrics_frame, text="Pitch: 10.00 px", font=("Consolas", 13, "bold"),
                                          text_color="#00FFC6")
        self.lbl_pitch_val.pack(side="left", expand=True, pady=5)

        self.lbl_lpi_val = ctk.CTkLabel(self.metrics_frame, text="Est. LPI: --", font=("Consolas", 13, "bold"),
                                        text_color="#00E5FF")
        self.lbl_lpi_val.pack(side="left", expand=True, pady=5)

        self.lbl_ppi_val = ctk.CTkLabel(self.metrics_frame, text="Screen PPI: --", font=("Consolas", 13, "bold"),
                                        text_color="#FFD700")
        self.lbl_ppi_val.pack(side="left", expand=True, pady=5)

        self.lbl_shift_val = ctk.CTkLabel(self.metrics_frame, text="Eye Shift: 3.0 px", font=("Consolas", 13, "bold"),
                                          text_color="#FF4081")
        self.lbl_shift_val.pack(side="left", expand=True, pady=5)

        # --- إطار عرض الصورة ---
        self.image_frame = ctk.CTkFrame(self, corner_radius=15)
        self.image_frame.pack(pady=5, padx=20, fill="both", expand=True)

        self.image_label = ctk.CTkLabel(self.image_frame, text="")
        self.image_label.pack(pady=5, padx=5, expand=True, fill="both")

        # --- إطار أدوات التحكم ---
        self.controls_frame = ctk.CTkFrame(self, corner_radius=15)
        self.controls_frame.pack(pady=(0, 10), padx=20, fill="x")

        instructions = "💡 In Full Screen (F11): Use ⬅️ ➡️ ⬆️ ⬇️ to adjust Pitch | Use 'A' & 'D' to adjust Eye Shift | Press Esc to exit"
        self.lbl_instructions = ctk.CTkLabel(self.controls_frame, text=instructions, font=("Arial", 12, "italic"),
                                             text_color="#FFD700")
        self.lbl_instructions.pack(pady=(5, 5))

        self.lbl_shift_title = ctk.CTkLabel(self.controls_frame, text="👁️ Eye Shift (Digital View Angle)",
                                            font=("Arial", 12, "bold"))
        self.lbl_shift_title.pack(pady=(0, 0))
        self.shift_slider = ctk.CTkSlider(self.controls_frame, from_=-15, to=15, number_of_steps=60,
                                          command=self.update_image)
        self.shift_slider.set(3.0)
        self.shift_slider.pack(pady=(0, 5), padx=30, fill="x")

        self.lbl_pitch_title = ctk.CTkLabel(self.controls_frame, text="📏 Lens Pitch (Hardware Calibration)",
                                            font=("Arial", 12, "bold"))
        self.lbl_pitch_title.pack(pady=(5, 0))
        self.pitch_slider = ctk.CTkSlider(self.controls_frame, from_=2.0, to=30.0, number_of_steps=2800,
                                          command=self.update_image)
        self.pitch_slider.set(10.0)
        self.pitch_slider.pack(pady=(0, 10), padx=30, fill="x")

    def switch_sample(self, sample_type):
        """التبديل بين أنواع العروض التفاعلية الثلاثة"""
        self.calib_switch.deselect()
        if sample_type == "text":
            self.active_image = self.create_text_sample()
        elif sample_type == "code":
            self.active_image = self.create_code_sample()
        elif sample_type == "ui":
            self.active_image = self.create_ui_sample()
        self.update_image()

    def adjust_pitch(self, amount):
        if self.is_fullscreen:
            new_val = float(self.pitch_slider.get()) + amount
            self.pitch_slider.set(max(2.0, min(30.0, new_val)))
            self.update_image()

    def adjust_shift(self, amount):
        if self.is_fullscreen:
            new_val = float(self.shift_slider.get()) + amount
            self.shift_slider.set(max(-15.0, min(15.0, new_val)))
            self.update_image()

    def enter_fullscreen(self, event=None):
        self.is_fullscreen = True
        self.attributes("-fullscreen", True)

        self.top_frame.pack_forget()
        self.metrics_frame.pack_forget()
        self.controls_frame.pack_forget()

        self.image_frame.pack(pady=0, padx=0, fill="both", expand=True)
        self.image_label.pack(pady=0, padx=0, expand=True, fill="both")
        self.update_image()

    def exit_fullscreen(self, event=None):
        if not self.is_fullscreen: return
        self.is_fullscreen = False
        self.attributes("-fullscreen", False)

        self.image_frame.pack_forget()
        self.image_label.pack_forget()

        self.top_frame.pack(pady=(10, 0), padx=20, fill="x")
        self.metrics_frame.pack(pady=10, padx=20, fill="x")

        self.image_frame.pack(pady=5, padx=20, fill="both", expand=True)
        self.image_label.pack(pady=5, padx=5, expand=True, fill="both")

        self.controls_frame.pack(pady=(0, 10), padx=20, fill="x")

        self.update_image()

    def update_image(self, *args):
        current_shift = round(float(self.shift_slider.get()), 2)
        current_pitch = round(float(self.pitch_slider.get()), 2)

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        ppi = np.sqrt(screen_w ** 2 + screen_h ** 2) / self.screen_diag_inches
        lpi = ppi / current_pitch if current_pitch > 0 else 0

        self.lbl_pitch_val.configure(text=f"Pitch: {current_pitch:.2f} px")
        self.lbl_lpi_val.configure(text=f"Est. Lens LPI: {lpi:.1f}")
        self.lbl_ppi_val.configure(text=f"Screen PPI: {int(ppi)}")
        self.lbl_shift_val.configure(text=f"Eye Shift: {current_shift:.1f} px")

        VIEWS = 5
        is_calibration = self.calib_switch.get() or self.is_fullscreen

        if is_calibration:
            result_img = generate_calibration_pattern(screen_w, screen_h, current_pitch, VIEWS, current_shift)
        else:
            result_img = generate_interlaced_image(self.active_image, current_pitch, VIEWS, current_shift)

        if result_img is not None:
            result_rgb = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(result_rgb)

            if self.is_fullscreen:
                tk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(screen_w, screen_h))
            else:
                max_h = 330
                max_w = 850
                pil_img.thumbnail((max_w, max_h))
                tk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=pil_img.size)

            self.image_label.configure(image=tk_img)
            self.image_label.image = tk_img


if __name__ == "__main__":
    app = VisionCorrectionApp()
    app.mainloop()