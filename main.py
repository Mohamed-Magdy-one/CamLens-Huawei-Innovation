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

        # مسار الصورة الافتراضية
        self.image_path = "test.png"
        self.screen_diag_inches = 15.6  # مقاس الشاشة الافتراضي لحساب الـ PPI

        self.setup_ui()
        self.update_image()

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

        self.btn_ui = ctk.CTkButton(self.top_frame, text="UI Test", width=90,
                                    command=lambda: self.change_image("test.png"))
        self.btn_ui.pack(side="right", padx=5)
        self.btn_code = ctk.CTkButton(self.top_frame, text="Code Test", width=90,
                                      command=lambda: self.change_image("test.png"))
        self.btn_code.pack(side="right", padx=5)
        self.btn_text = ctk.CTkButton(self.top_frame, text="Text Test", width=90,
                                      command=lambda: self.change_image("test.png"))
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

        # تعليمات الشاشة الكاملة (Hint Text)
        instructions = "💡 In Full Screen (F11): Use ⬅️ ➡️ ⬆️ ⬇️ to adjust Pitch | Use 'A' & 'D' to adjust Eye Shift | Press Esc to exit"
        self.lbl_instructions = ctk.CTkLabel(self.controls_frame, text=instructions, font=("Arial", 12, "italic"),
                                             text_color="#FFD700")
        self.lbl_instructions.pack(pady=(5, 5))

        # عنوان وسلايدر الـ Eye Shift
        self.lbl_shift_title = ctk.CTkLabel(self.controls_frame, text="👁️ Eye Shift (Digital View Angle)",
                                            font=("Arial", 12, "bold"))
        self.lbl_shift_title.pack(pady=(0, 0))
        self.shift_slider = ctk.CTkSlider(self.controls_frame, from_=-15, to=15, number_of_steps=60,
                                          command=self.update_image)
        self.shift_slider.set(3.0)
        self.shift_slider.pack(pady=(0, 5), padx=30, fill="x")

        # عنوان وسلايدر الـ Pitch
        self.lbl_pitch_title = ctk.CTkLabel(self.controls_frame, text="📏 Lens Pitch (Hardware Calibration)",
                                            font=("Arial", 12, "bold"))
        self.lbl_pitch_title.pack(pady=(5, 0))
        self.pitch_slider = ctk.CTkSlider(self.controls_frame, from_=2.0, to=30.0, number_of_steps=2800,
                                          command=self.update_image)
        self.pitch_slider.set(10.0)
        self.pitch_slider.pack(pady=(0, 10), padx=30, fill="x")

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

        # إخفاء جميع الواجهات وترك الصورة فقط
        self.top_frame.pack_forget()
        self.metrics_frame.pack_forget()
        self.controls_frame.pack_forget()

        # توسيع إطار الصورة لملء الشاشة بدون حواف
        self.image_frame.pack(pady=0, padx=0, fill="both", expand=True)
        self.image_label.pack(pady=0, padx=0, expand=True, fill="both")
        self.update_image()

    def exit_fullscreen(self, event=None):
        if not self.is_fullscreen: return
        self.is_fullscreen = False
        self.attributes("-fullscreen", False)

        # إخفاء الصورة مؤقتاً عشان نرص الواجهة بالترتيب الصح من جديد
        self.image_frame.pack_forget()
        self.image_label.pack_forget()

        # إعادة ترتيب الواجهة بنفس الترتيب الأصلي
        self.top_frame.pack(pady=(10, 0), padx=20, fill="x")
        self.metrics_frame.pack(pady=10, padx=20, fill="x")

        self.image_frame.pack(pady=5, padx=20, fill="both", expand=True)
        self.image_label.pack(pady=5, padx=5, expand=True, fill="both")

        self.controls_frame.pack(pady=(0, 10), padx=20, fill="x")

        self.update_image()

    def change_image(self, new_path):
        self.image_path = new_path
        self.calib_switch.deselect()
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
        # إجبار نمط المعايرة في وضع ملء الشاشة
        is_calibration = self.calib_switch.get() or self.is_fullscreen

        if is_calibration:
            # تمرير current_shift عشان نمط المعايرة يتحرك يمين وشمال
            result_img = generate_calibration_pattern(screen_w, screen_h, current_pitch, VIEWS, current_shift)
        else:
            result_img = generate_interlaced_image(self.image_path, current_pitch, VIEWS, current_shift)

        if result_img is not None:
            result_rgb = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(result_rgb)

            if self.is_fullscreen:
                # عرض الصورة بحجمها الأصلي (Pixel-Perfect) بدون أي تصغير
                tk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(screen_w, screen_h))
            else:
                # قللنا الارتفاع شوية لـ 330 عشان العناوين والنصوص الجديدة تبان وماتنزلش تحت الشاشة
                max_h = 330
                max_w = 850
                pil_img.thumbnail((max_w, max_h))
                tk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=pil_img.size)

            self.image_label.configure(image=tk_img)
            self.image_label.image = tk_img


if __name__ == "__main__":
    app = VisionCorrectionApp()
    app.mainloop()