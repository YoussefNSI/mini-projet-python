"""
Styles et thèmes pour l'interface graphique.
"""

# Palette de couleurs moderne
COLORS = {
    'primary': '#2563eb',       # Bleu principal
    'primary_dark': '#1d4ed8',  # Bleu foncé
    'primary_light': '#3b82f6', # Bleu clair
    'secondary': '#64748b',     # Gris bleu
    'success': '#22c55e',       # Vert
    'warning': '#f59e0b',       # Orange
    'danger': '#ef4444',        # Rouge
    'info': '#06b6d4',          # Cyan
    'background': '#f8fafc',    # Fond clair
    'surface': '#ffffff',       # Surface blanche
    'text': '#1e293b',          # Texte foncé
    'text_secondary': '#64748b', # Texte secondaire
    'border': '#e2e8f0',        # Bordures
    'hover': '#f1f5f9',         # Survol
}

# Style global de l'application
MAIN_STYLE = """
QMainWindow {
    background-color: #f8fafc;
}

QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
    color: #1e293b;
}

/* Menu Bar */
QMenuBar {
    background-color: #ffffff;
    border-bottom: 1px solid #e2e8f0;
    padding: 4px;
}

QMenuBar::item {
    padding: 6px 12px;
    border-radius: 4px;
}

QMenuBar::item:selected {
    background-color: #f1f5f9;
}

QMenu {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 4px;
}

QMenu::item {
    padding: 8px 24px;
    border-radius: 4px;
}

QMenu::item:selected {
    background-color: #2563eb;
    color: white;
}

/* Tool Bar */
QToolBar {
    background-color: #ffffff;
    border-bottom: 1px solid #e2e8f0;
    padding: 8px;
    spacing: 8px;
}

QToolBar::separator {
    width: 1px;
    background-color: #e2e8f0;
    margin: 4px 8px;
}

QToolButton {
    background-color: transparent;
    border: none;
    border-radius: 6px;
    padding: 8px 12px;
    font-weight: 500;
}

QToolButton:hover {
    background-color: #f1f5f9;
}

QToolButton:pressed {
    background-color: #e2e8f0;
}

/* Stacked Widget & Pages */
QStackedWidget {
    background-color: #f8fafc;
}

/* Tables */
QTableWidget, QTableView {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    gridline-color: #f1f5f9;
    selection-background-color: #dbeafe;
    selection-color: #1e293b;
}

QTableWidget::item, QTableView::item {
    padding: 4px 8px;
    border-bottom: 1px solid #f1f5f9;
}

QTableWidget::item:selected, QTableView::item:selected {
    background-color: #dbeafe;
}

QHeaderView::section {
    background-color: #f8fafc;
    padding: 10px 8px;
    border: none;
    border-bottom: 2px solid #e2e8f0;
    font-weight: 600;
    color: #475569;
}

/* Scroll Bars */
QScrollBar:vertical {
    background-color: #f8fafc;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #cbd5e1;
    border-radius: 6px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #94a3b8;
}

QScrollBar:horizontal {
    background-color: #f8fafc;
    height: 12px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal {
    background-color: #cbd5e1;
    border-radius: 6px;
    min-width: 30px;
}

QScrollBar::add-line, QScrollBar::sub-line {
    border: none;
    background: none;
}

/* Buttons */
QPushButton {
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #1d4ed8;
}

QPushButton:pressed {
    background-color: #1e40af;
}

QPushButton:disabled {
    background-color: #94a3b8;
}

QPushButton[secondary="true"] {
    background-color: #f1f5f9;
    color: #475569;
    border: 1px solid #e2e8f0;
}

QPushButton[secondary="true"]:hover {
    background-color: #e2e8f0;
}

QPushButton[danger="true"] {
    background-color: #ef4444;
}

QPushButton[danger="true"]:hover {
    background-color: #dc2626;
}

QPushButton[success="true"] {
    background-color: #22c55e;
}

QPushButton[success="true"]:hover {
    background-color: #16a34a;
}

/* Input Fields */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 10px 12px;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 2px solid #2563eb;
    padding: 9px 11px;
}

QLineEdit:disabled {
    background-color: #f1f5f9;
    color: #94a3b8;
}

/* Combo Box */
QComboBox {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 10px 12px;
    padding-right: 30px;
}

QComboBox:focus {
    border: 2px solid #2563eb;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    width: 12px;
    height: 12px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    selection-background-color: #dbeafe;
    outline: none;
}

/* Spin Box */
QSpinBox, QDoubleSpinBox {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 10px 12px;
}

QSpinBox:focus, QDoubleSpinBox:focus {
    border: 2px solid #2563eb;
}

/* Date Edit */
QDateEdit {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 10px 12px;
}

QDateEdit:focus {
    border: 2px solid #2563eb;
}

QDateEdit::drop-down {
    border: none;
    width: 30px;
}

QCalendarWidget {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
}

/* Check Box */
QCheckBox {
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid #cbd5e1;
}

QCheckBox::indicator:checked {
    background-color: #2563eb;
    border-color: #2563eb;
}

/* Group Box */
QGroupBox {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    margin-top: 12px;
    padding: 16px;
    padding-top: 24px;
    font-weight: 600;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 16px;
    padding: 0 8px;
    background-color: #ffffff;
    color: #475569;
}

/* Tab Widget */
QTabWidget::pane {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 16px;
}

QTabBar::tab {
    background-color: #f1f5f9;
    border: none;
    padding: 10px 20px;
    margin-right: 4px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}

QTabBar::tab:selected {
    background-color: #ffffff;
    border-bottom: 2px solid #2563eb;
}

QTabBar::tab:hover:!selected {
    background-color: #e2e8f0;
}

/* Labels */
QLabel {
    color: #1e293b;
}

QLabel[heading="true"] {
    font-size: 24px;
    font-weight: 700;
    color: #0f172a;
}

QLabel[subheading="true"] {
    font-size: 16px;
    font-weight: 600;
    color: #475569;
}

QLabel[muted="true"] {
    color: #64748b;
    font-size: 12px;
}

/* Status Bar */
QStatusBar {
    background-color: #ffffff;
    border-top: 1px solid #e2e8f0;
    padding: 4px;
}

/* Message Box */
QMessageBox {
    background-color: #ffffff;
}

QMessageBox QPushButton {
    min-width: 80px;
}

/* Dialog */
QDialog {
    background-color: #ffffff;
}

/* Splitter */
QSplitter::handle {
    background-color: #e2e8f0;
}

QSplitter::handle:horizontal {
    width: 2px;
}

QSplitter::handle:vertical {
    height: 2px;
}

/* Progress Bar */
QProgressBar {
    background-color: #e2e8f0;
    border-radius: 4px;
    height: 8px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #2563eb;
    border-radius: 4px;
}

/* List Widget */
QListWidget {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    outline: none;
}

QListWidget::item {
    padding: 12px;
    border-bottom: 1px solid #f1f5f9;
}

QListWidget::item:selected {
    background-color: #dbeafe;
    color: #1e293b;
}

QListWidget::item:hover:!selected {
    background-color: #f1f5f9;
}
"""

# Style pour les cartes du dashboard
CARD_STYLE = """
QFrame[card="true"] {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px;
}

QFrame[card="true"]:hover {
    border-color: #cbd5e1;
}
"""

# Style pour la sidebar de navigation
SIDEBAR_STYLE = """
QFrame[sidebar="true"] {
    background-color: #1e293b;
    border-right: none;
}

QFrame[sidebar="true"] QPushButton {
    background-color: transparent;
    color: #94a3b8;
    text-align: left;
    padding: 14px 20px;
    border-radius: 0;
    font-weight: 500;
    border-left: 3px solid transparent;
}

QFrame[sidebar="true"] QPushButton:hover {
    background-color: #334155;
    color: #f1f5f9;
}

QFrame[sidebar="true"] QPushButton:checked {
    background-color: #334155;
    color: #ffffff;
    border-left: 3px solid #2563eb;
}

QFrame[sidebar="true"] QLabel {
    color: #f8fafc;
}

QFrame[sidebar="true"] QLabel[logo="true"] {
    font-size: 18px;
    font-weight: 700;
    padding: 20px;
}
"""

# Combiner tous les styles
def get_full_stylesheet():
    """Retourne la feuille de style complète."""
    return MAIN_STYLE + CARD_STYLE + SIDEBAR_STYLE
