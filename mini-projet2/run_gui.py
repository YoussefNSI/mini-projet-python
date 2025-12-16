#!/usr/bin/env python3
"""
Point d'entrée de l'interface graphique AutoLoc.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

from gui.main_window import MainWindow


def main():
    """Lance l'application graphique."""
    app = QApplication(sys.argv)
    
    # Configurer la police par défaut
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Nom de l'application
    app.setApplicationName("AutoLoc")
    app.setOrganizationName("AutoLoc Inc.")
    
    # Créer et afficher la fenêtre principale
    window = MainWindow()
    window.show()
    
    # Exécuter l'application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
