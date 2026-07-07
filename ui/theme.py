"""
ui/theme.py

Central design tokens. Every page/component imports COLORS and FONTS
from here instead of hardcoding values, so a future re-theme (or a
light-mode toggle) only touches this one file.
"""

import customtkinter as ctk

COLORS = {
    "bg_app":         "#15171c",
    "bg_sidebar":     "#111318",
    "bg_surface":     "#1c1f26",
    "bg_surface_alt": "#22262f",
    "border":         "#2b2f38",

    "accent":         "#3B82F6",
    "accent_hover":   "#2563EB",
    "accent_soft":    "#1E3A5F",

    "text_primary":   "#E7EAF0",
    "text_secondary": "#9AA3B2",
    "text_muted":     "#6B7280",

    "success":        "#22C55E",
    "warning":        "#F59E0B",
    "error":          "#EF4444",
}

FONT_FAMILY = "Segoe UI"

FONTS = {
    "h1":     (FONT_FAMILY, 24, "bold"),
    "h2":     (FONT_FAMILY, 18, "bold"),
    "h3":     (FONT_FAMILY, 15, "bold"),
    "body":   (FONT_FAMILY, 13),
    "small":  (FONT_FAMILY, 11),
    "button": (FONT_FAMILY, 13, "bold"),
    "body_bold": ("Segoe UI", 13, "bold"),
}


def apply_theme():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
