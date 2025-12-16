# GUI Package - Interface graphique PyQt pour le système de location
from .styles import get_full_stylesheet, COLORS
from .dashboard_page import DashboardPage
from .vehicles_page import VehiclesPage
from .customers_page import CustomersPage
from .rentals_page import RentalsPage
from .reports_page import ReportsPage
from .main_window import MainWindow

__all__ = [
    "MainWindow",
    "DashboardPage",
    "VehiclesPage",
    "CustomersPage",
    "RentalsPage",
    "ReportsPage",
    "get_full_stylesheet",
    "COLORS"
]
