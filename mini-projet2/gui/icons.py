"""
Module de gestion des icônes pour l'interface graphique.
Utilise des icônes SVG intégrées pour une apparence professionnelle.
"""

from PyQt6.QtWidgets import QStyle, QApplication, QPushButton
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PyQt6.QtCore import Qt, QSize, QRect
from PyQt6.QtSvg import QSvgRenderer
from io import BytesIO


# Icônes SVG personnalisées (Material Design style)
SVG_ICONS = {
    "dashboard": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/>
        </svg>
    """,
    "car": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.21.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.5 16c-.83 0-1.5-.67-1.5-1.5S5.67 13 6.5 13s1.5.67 1.5 1.5S7.33 16 6.5 16zm11 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zM5 11l1.5-4.5h11L19 11H5z"/>
        </svg>
    """,
    "customers": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/>
        </svg>
    """,
    "rental": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/>
        </svg>
    """,
    "reports": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
        </svg>
    """,
    "add": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
        </svg>
    """,
    "edit": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
        </svg>
    """,
    "delete": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/>
        </svg>
    """,
    "view": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
        </svg>
    """,
    "eye": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
        </svg>
    """,
    "cancel": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M12 2C6.47 2 2 6.47 2 12s4.47 10 10 10 10-4.47 10-10S17.53 2 12 2zm5 13.59L15.59 17 12 13.41 8.41 17 7 15.59 10.59 12 7 8.41 8.41 7 12 10.59 15.59 7 17 8.41 13.41 12 17 15.59z"/>
        </svg>
    """,
    "chart": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
        </svg>
    """,
    "users": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/>
        </svg>
    """,
    "documents": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/>
        </svg>
    """,
    "check": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
        </svg>
    """,
    "close": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
        </svg>
    """,
    "warning": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/>
        </svg>
    """,
    "calendar": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM9 10H7v2h2v-2zm4 0h-2v2h2v-2zm4 0h-2v2h2v-2z"/>
        </svg>
    """,
    "money": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M11.8 10.9c-2.27-.59-3-1.2-3-2.15 0-1.09 1.01-1.85 2.7-1.85 1.78 0 2.44.85 2.5 2.1h2.21c-.07-1.72-1.12-3.3-3.21-3.81V3h-3v2.16c-1.94.42-3.5 1.68-3.5 3.61 0 2.31 1.91 3.46 4.7 4.13 2.5.6 3 1.48 3 2.41 0 .69-.49 1.79-2.7 1.79-2.06 0-2.87-.92-2.98-2.1h-2.2c.12 2.19 1.76 3.42 3.68 3.83V21h3v-2.15c1.95-.37 3.5-1.5 3.5-3.55 0-2.84-2.43-3.81-4.7-4.4z"/>
        </svg>
    """,
    "star": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
        </svg>
    """,
    "person": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
        </svg>
    """,
    "refresh": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/>
        </svg>
    """,
    "play": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M8 5v14l11-7z"/>
        </svg>
    """,
    "stop": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M6 6h12v12H6z"/>
        </svg>
    """,
    "extend": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M19 19H5V8h14m-3-7v2H8V1H6v2H5c-1.11 0-2 .89-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2h-1V1m-1 11h-5v5h5v-5z"/>
        </svg>
    """,
    "notes": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M3 18h12v-2H3v2zM3 6v2h18V6H3zm0 7h18v-2H3v2z"/>
        </svg>
    """,
    "blocked": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zM4 12c0-4.42 3.58-8 8-8 1.85 0 3.55.63 4.9 1.69L5.69 16.9C4.63 15.55 4 13.85 4 12zm8 8c-1.85 0-3.55-.63-4.9-1.69L18.31 7.1C19.37 8.45 20 10.15 20 12c0 4.42-3.58 8-8 8z"/>
        </svg>
    """,
    "maintenance": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z"/>
        </svg>
    """,
    "trophy": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M19 5h-2V3H7v2H5c-1.1 0-2 .9-2 2v1c0 2.55 1.92 4.63 4.39 4.94.63 1.5 1.98 2.63 3.61 2.96V19H7v2h10v-2h-4v-3.1c1.63-.33 2.98-1.46 3.61-2.96C19.08 12.63 21 10.55 21 8V7c0-1.1-.9-2-2-2zM5 8V7h2v3.82C5.84 10.4 5 9.3 5 8zm14 0c0 1.3-.84 2.4-2 2.82V7h2v1z"/>
        </svg>
    """,
    "info": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
        </svg>
    """,
    "speedometer": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm-1-4h2v-6h-2v6zm1-10c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/>
        </svg>
    """,
}


def create_icon_from_svg(svg_content: str, color: str = "#ffffff", size: int = 24) -> QIcon:
    """Crée une QIcon à partir d'un contenu SVG."""
    # Remplacer la couleur
    svg_data = svg_content.format(color=color).encode('utf-8')
    
    # Utiliser une résolution plus élevée pour un meilleur rendu
    scale = 2  # Facteur d'échelle pour la qualité
    render_size = size * scale
    
    # Créer le pixmap avec une résolution plus élevée
    pixmap = QPixmap(render_size, render_size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    # Rendre le SVG
    renderer = QSvgRenderer(svg_data)
    if renderer.isValid():
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        renderer.render(painter)
        painter.end()
    
    # Redimensionner pour la taille finale avec une bonne qualité
    final_pixmap = pixmap.scaled(
        size, size,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation
    )
    
    return QIcon(final_pixmap)


def get_icon(name: str, color: str = "#ffffff", size: int = 24) -> QIcon:
    """Récupère une icône par son nom."""
    if name in SVG_ICONS:
        return create_icon_from_svg(SVG_ICONS[name], color, size)
    return QIcon()


def create_colored_icon(icon_name: str, color: str, size: int = 32) -> QIcon:
    """Crée une icône colorée."""
    return get_icon(icon_name, color, size)


def create_action_button(
    icon_name: str,
    tooltip: str,
    icon_color: str = "#64748b",
    bg_color: str = "#f1f5f9",
    hover_color: str = "#e2e8f0",
    border_color: str = "#e2e8f0",
    size: int = 28
) -> QPushButton:
    """
    Crée un bouton d'action pour les tableaux.
    
    Args:
        icon_name: Nom de l'icône SVG
        tooltip: Texte du tooltip
        icon_color: Couleur de l'icône
        bg_color: Couleur de fond
        hover_color: Couleur de fond au survol
        border_color: Couleur de la bordure
        size: Taille du bouton
    
    Returns:
        QPushButton configuré
    """
    from PyQt6.QtCore import QSize as QtSize
    
    btn = QPushButton()
    btn.setFixedSize(size, size)
    btn.setToolTip(tooltip)
    
    # Icône avec taille adaptée
    icon_size = int(size * 0.55)  # L'icône fait 55% de la taille du bouton
    btn.setIcon(get_icon(icon_name, icon_color, icon_size * 2))
    btn.setIconSize(QtSize(icon_size, icon_size))
    
    btn.setStyleSheet(f"""
        QPushButton {{
            background-color: {bg_color};
            border: 1px solid {border_color};
            border-radius: {size // 4}px;
        }}
        QPushButton:hover {{
            background-color: {hover_color};
        }}
        QPushButton:pressed {{
            background-color: {border_color};
        }}
    """)
    
    return btn


class IconButton:
    """Helper pour créer des boutons avec icônes."""
    
    @staticmethod
    def apply(button, icon_name: str, color: str = "#ffffff", size: int = 20):
        """Applique une icône à un bouton."""
        icon = get_icon(icon_name, color, size)
        button.setIcon(icon)
        button.setIconSize(QSize(size, size))


# Couleurs par défaut pour les icônes
ICON_COLORS = {
    "primary": "#2563eb",
    "success": "#22c55e", 
    "danger": "#ef4444",
    "warning": "#f59e0b",
    "info": "#3b82f6",
    "secondary": "#64748b",
    "white": "#ffffff",
    "dark": "#1e293b",
}
