import customtkinter as ctk
import threading
from services.summarizer import summarize
from services.translator import translate
from services.speech import speak
from ui.theme import *
 
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
 
# ── Palette ──────────────────────────────────────────────────────────────────
BG           = "#0D0F14"
SURFACE      = "#13161E"
SURFACE2     = "#1A1E2A"
BORDER       = "#252A38"
ACCENT       = "#4F8EF7"
ACCENT_HOVER = "#3A7AE8"
ACCENT2      = "#A78BFA"
TEXT         = "#E8EAF0"
SUBTEXT      = "#7B82A0"
SUCCESS      = "#34D399"
ERROR        = "#F87171"
FONT_HEAD    = ("Georgia", 22, "bold")
FONT_LABEL   = ("Georgia", 11)
FONT_BODY    = ("Consolas", 12)
FONT_BTN     = ("Georgia", 13, "bold")
FONT_CAPTION = ("Georgia", 9)
RADIUS       = 12
# ─────────────────────────────────────────────────────────────────────────────
 
 
def start_app():
    app = ctk.CTk()
    app.title("News·Coo")
    app.geometry("980x900")
    app.configure(fg_color=BG)
    app.resizable(True, True)
 
    # ── STATE ─────────────────────────────────────────────────────────────────
    state = {
        "translated_text": "",
        "selected_language": "",
        "busy": False,
    }
 
    # ── HEADER ────────────────────────────────────────────────────────────────
    header = ctk.CTkFrame(app, fg_color=SURFACE, corner_radius=0, height=64)
    header.pack(fill="x", side="top")
    header.pack_propagate(False)
 
    dot = ctk.CTkLabel(header, text="●", font=("Georgia", 20), text_color=ACCENT)
    dot.pack(side="left", padx=(24, 6), pady=16)
    title_lbl = ctk.CTkLabel(
        header, text="News·Coo", font=FONT_HEAD, text_color=TEXT
    )
    title_lbl.pack(side="left", pady=16)
    sub_lbl = ctk.CTkLabel(
        header,
        text="  Summarise · Translate · Listen",
        font=FONT_CAPTION,
        text_color=SUBTEXT,
    )
    sub_lbl.pack(side="left", pady=22)
 
    # status pill (right side of header)
    status_var = ctk.StringVar(value="Ready")
    status_lbl = ctk.CTkLabel(
        header,
        textvariable=status_var,
        font=("Georgia", 10, "bold"),
        text_color=SUCCESS,
        fg_color=SURFACE2,
        corner_radius=20,
        padx=14,
        pady=4,
    )
    status_lbl.pack(side="right", padx=24)
 
    # ── SCROLL CANVAS ────────────────────────────────────────────────────────
    canvas_frame = ctk.CTkScrollableFrame(
        app, fg_color=BG, scrollbar_button_color=BORDER,
        scrollbar_button_hover_color=ACCENT
    )
    canvas_frame.pack(fill="both", expand=True, padx=0, pady=0)
 
    # ── HELPERS ───────────────────────────────────────────────────────────────
    def section(parent, label_text):
        """Returns a labelled card frame."""
        outer = ctk.CTkFrame(parent, fg_color=SURFACE, corner_radius=RADIUS)
        outer.pack(fill="x", padx=24, pady=(14, 0))
 
        header_row = ctk.CTkFrame(outer, fg_color="transparent")
        header_row.pack(fill="x", padx=16, pady=(12, 4))
 
        accent_bar = ctk.CTkFrame(
            header_row, fg_color=ACCENT, width=3, height=16, corner_radius=2
        )
        accent_bar.pack(side="left", padx=(0, 8))
 
        lbl = ctk.CTkLabel(
            header_row, text=label_text, font=FONT_LABEL, text_color=SUBTEXT
        )
        lbl.pack(side="left")
        return outer
 
    def styled_textbox(parent, height, placeholder=""):
        tb = ctk.CTkTextbox(
            parent,
            height=height,
            font=FONT_BODY,
            fg_color=SURFACE2,
            text_color=TEXT,
            border_color=BORDER,
            border_width=1,
            corner_radius=8,
            scrollbar_button_color=BORDER,
            scrollbar_button_hover_color=ACCENT,
        )
        tb.pack(fill="x", padx=16, pady=(4, 14))
        if placeholder:
            tb.insert("1.0", placeholder)
            tb.bind("<FocusIn>", lambda e, t=tb, p=placeholder: (
                t.delete("1.0", "end") if t.get("1.0", "end").strip() == p else None
            ))
        return tb
 
    def set_status(text, color=SUCCESS):
        status_var.set(text)
        status_lbl.configure(text_color=color)
 
    # ── INPUT SECTION ────────────────────────────────────────────────────────
    card_in = section(canvas_frame, "ARTICLE / TEXT INPUT")
    input_box = styled_textbox(
        card_in, 200,
        placeholder="Paste or type your news article here…"
    )
 
    # ── SUMMARY SECTION ──────────────────────────────────────────────────────
    card_sum = section(canvas_frame, "GENERATED SUMMARY")
    summary_box = styled_textbox(card_sum, 160)
 
    # ── TRANSLATION SECTION ──────────────────────────────────────────────────
    card_tr = section(canvas_frame, "TRANSLATED OUTPUT")
    translated_box = styled_textbox(card_tr, 160)
 
    # ── CONTROLS ROW ─────────────────────────────────────────────────────────
    ctrl_card = ctk.CTkFrame(canvas_frame, fg_color=SURFACE, corner_radius=RADIUS)
    ctrl_card.pack(fill="x", padx=24, pady=14)
 
    ctrl_inner = ctk.CTkFrame(ctrl_card, fg_color="transparent")
    ctrl_inner.pack(fill="x", padx=16, pady=14)
 
    # Language picker label + menu
    lang_lbl = ctk.CTkLabel(
        ctrl_inner, text="Language", font=FONT_LABEL, text_color=SUBTEXT
    )
    lang_lbl.grid(row=0, column=0, sticky="w", padx=(0, 8))
 
    language_menu = ctk.CTkOptionMenu(
        ctrl_inner,
        values=[
            "hi  —  Hindi",
            "fr  —  French",
            "de  —  German",
            "es  —  Spanish",
            "ja  —  Japanese",
        ],
        font=FONT_LABEL,
        fg_color=SURFACE2,
        button_color=ACCENT,
        button_hover_color=ACCENT_HOVER,
        dropdown_fg_color=SURFACE2,
        dropdown_hover_color=BORDER,
        text_color=TEXT,
        corner_radius=8,
        width=200,
    )
    language_menu.grid(row=0, column=1, padx=(0, 20))
 
    def make_btn(parent, label, icon, cmd, col, color=ACCENT, hover=ACCENT_HOVER):
        b = ctk.CTkButton(
            parent,
            text=f"{icon}  {label}",
            command=cmd,
            font=FONT_BTN,
            fg_color=color,
            hover_color=hover,
            corner_radius=8,
            height=40,
            width=160,
        )
        b.grid(row=0, column=col, padx=6)
        return b
 
    # ── LOGIC ─────────────────────────────────────────────────────────────────
    def summarize_text():
        text = input_box.get("1.0", "end").strip()
        if not text or state["busy"]:
            return
        state["busy"] = True
        set_status("Summarising…", ACCENT2)
        btn_summary.configure(state="disabled")
 
        def run():
            try:
                result = summarize(text)
                summary_box.delete("1.0", "end")
                summary_box.insert("1.0", result)
                set_status("Summary ready", SUCCESS)
            except Exception as exc:
                set_status(f"Error: {exc}", ERROR)
            finally:
                state["busy"] = False
                btn_summary.configure(state="normal")
 
        threading.Thread(target=run, daemon=True).start()
 
    def translate_text():
        text = summary_box.get("1.0", "end").strip()
        if not text or state["busy"]:
            return
        raw = language_menu.get()
        lang_code = raw.split()[0]            # "hi", "fr", …
        state["selected_language"] = lang_code
        state["busy"] = True
        set_status("Translating…", ACCENT2)
        btn_translate.configure(state="disabled")
 
        def run():
            try:
                result = translate(text, lang_code)
                state["translated_text"] = result
                translated_box.delete("1.0", "end")
                translated_box.insert("1.0", result)
                set_status("Translation ready", SUCCESS)
            except Exception as exc:
                set_status(f"Error: {exc}", ERROR)
            finally:
                state["busy"] = False
                btn_translate.configure(state="normal")
 
        threading.Thread(target=run, daemon=True).start()
 
    def speak_text():
        text = state["translated_text"]
        if not text or state["busy"]:
            return
        lang = state["selected_language"]
        state["busy"] = True
        set_status("Speaking…", ACCENT)
        btn_speak.configure(state="disabled")
 
        def run():
            try:
                speak(text, lang)
                set_status("Done", SUCCESS)
            except Exception as exc:
                set_status(f"Error: {exc}", ERROR)
            finally:
                state["busy"] = False
                btn_speak.configure(state="normal")
 
        threading.Thread(target=run, daemon=True).start()
 
    # draw buttons
    btn_summary  = make_btn(ctrl_inner, "Summarise",  "⚡", summarize_text, col=2)
    btn_translate = make_btn(ctrl_inner, "Translate",  "🌐", translate_text,  col=3)
    btn_speak    = make_btn(ctrl_inner, "Speak",      "🔊", speak_text,      col=4,
                            color="#2D3A5E", hover="#3A4A72")
 
    # ── FOOTER ────────────────────────────────────────────────────────────────
    footer = ctk.CTkFrame(app, fg_color=SURFACE, corner_radius=0, height=32)
    footer.pack(fill="x", side="bottom")
    footer.pack_propagate(False)
    ctk.CTkLabel(
        footer,
        text="News·Coo  ·  AI-powered news assistant",
        font=FONT_CAPTION,
        text_color=SUBTEXT,
    ).pack(side="left", padx=24)
 
    app.mainloop()
