import customtkinter as ctk

def make_panel(parent):

    frame = ctk.CTkFrame(
        parent,
        corner_radius=6,
        border_width=1
    )

    return frame