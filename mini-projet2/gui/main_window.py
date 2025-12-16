"""
Fenêtre principale de l'application.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QPushButton, QLabel, QFrame,
    QMessageBox, QApplication, QSplitter
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont, QAction, QPixmap

from car_rental_system import CarRentalSystem
from models.vehicle import Car, Truck, Motorcycle, VehicleCategory
from models.customer import Customer
from datetime import date

from gui.styles import get_full_stylesheet, COLORS
from gui.dashboard_page import DashboardPage
from gui.vehicles_page import VehiclesPage
from gui.customers_page import CustomersPage
from gui.rentals_page import RentalsPage
from gui.reports_page import ReportsPage
from gui.icons import get_icon, ICON_COLORS


class SidebarButton(QPushButton):
    """Bouton personnalisé pour la sidebar avec icône."""
    
    def __init__(self, text: str, icon_name: str = ""):
        super().__init__(text)
        self.setCheckable(True)
        self.setFixedHeight(48)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._icon_name = icon_name
        
        if icon_name:
            self.setIcon(get_icon(icon_name, "#94a3b8", 20))
            self.setIconSize(QSize(20, 20))
    
    def set_active(self, active: bool):
        """Met à jour l'icône selon l'état actif."""
        self.setChecked(active)
        if self._icon_name:
            color = "#ffffff" if active else "#94a3b8"
            self.setIcon(get_icon(self._icon_name, color, 20))


class MainWindow(QMainWindow):
    """Fenêtre principale de l'application."""
    
    def __init__(self):
        super().__init__()
        
        # Initialiser le système
        self.system = CarRentalSystem("AutoLoc Premium")
        
        # Charger les données de démonstration
        self.load_demo_data()
        
        # Configurer l'interface
        self.setup_ui()
        
        # Appliquer le style
        self.setStyleSheet(get_full_stylesheet())
    
    def setup_ui(self):
        """Configure l'interface principale."""
        self.setWindowTitle("AutoLoc - Systeme de Location de Voitures")
        self.setMinimumSize(1200, 800)
        
        # Icône de la fenêtre
        self.setWindowIcon(get_icon("car", "#2563eb", 32))
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal avec sidebar et contenu
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # === Sidebar ===
        sidebar = QFrame()
        sidebar.setProperty("sidebar", True)
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet("""
            QFrame[sidebar="true"] {
                background-color: #1e293b;
            }
        """)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Logo
        logo_frame = QFrame()
        logo_frame.setStyleSheet("background-color: #0f172a; padding: 20px;")
        logo_layout = QHBoxLayout(logo_frame)
        
        # Icône du logo
        logo_icon = QLabel()
        logo_icon.setPixmap(get_icon("car", "#3b82f6", 32).pixmap(32, 32))
        logo_icon.setFixedSize(40, 40)
        
        logo_text_layout = QVBoxLayout()
        logo_label = QLabel("AutoLoc")
        logo_label.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: 700;")
        
        subtitle_label = QLabel("Gestion de Location")
        subtitle_label.setStyleSheet("color: #94a3b8; font-size: 11px;")
        
        logo_text_layout.addWidget(logo_label)
        logo_text_layout.addWidget(subtitle_label)
        logo_text_layout.setSpacing(2)
        
        logo_layout.addWidget(logo_icon)
        logo_layout.addLayout(logo_text_layout)
        logo_layout.addStretch()
        
        sidebar_layout.addWidget(logo_frame)
        
        # Boutons de navigation avec icônes
        nav_layout = QVBoxLayout()
        nav_layout.setContentsMargins(8, 16, 8, 16)
        nav_layout.setSpacing(4)
        
        self.btn_dashboard = SidebarButton("Tableau de bord", "dashboard")
        self.btn_vehicles = SidebarButton("Vehicules", "car")
        self.btn_customers = SidebarButton("Clients", "customers")
        self.btn_rentals = SidebarButton("Locations", "rental")
        self.btn_reports = SidebarButton("Rapports", "reports")
        
        self.nav_buttons = [
            self.btn_dashboard,
            self.btn_vehicles,
            self.btn_customers,
            self.btn_rentals,
            self.btn_reports
        ]
        
        # Style des boutons sidebar
        for btn in self.nav_buttons:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #94a3b8;
                    text-align: left;
                    padding: 12px 16px;
                    border: none;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #334155;
                    color: #f1f5f9;
                }
                QPushButton:checked {
                    background-color: #2563eb;
                    color: #ffffff;
                }
            """)
            nav_layout.addWidget(btn)
        
        self.btn_dashboard.set_active(True)
        
        sidebar_layout.addLayout(nav_layout)
        sidebar_layout.addStretch()
        
        # Info version
        version_label = QLabel("Version 1.0.0")
        version_label.setStyleSheet("color: #475569; font-size: 11px; padding: 16px;")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(version_label)
        
        main_layout.addWidget(sidebar)
        
        # === Contenu principal ===
        content_frame = QFrame()
        content_frame.setStyleSheet("background-color: #f8fafc;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Stack pour les pages
        self.stack = QStackedWidget()
        
        # Créer les pages
        self.dashboard_page = DashboardPage(self.system)
        self.vehicles_page = VehiclesPage(self.system)
        self.customers_page = CustomersPage(self.system)
        self.rentals_page = RentalsPage(self.system)
        self.reports_page = ReportsPage(self.system)
        
        # Connecter les signaux de mise à jour
        self.vehicles_page.data_changed.connect(self.refresh_all)
        self.customers_page.data_changed.connect(self.refresh_all)
        self.rentals_page.data_changed.connect(self.refresh_all)
        
        # Ajouter les pages au stack
        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.vehicles_page)
        self.stack.addWidget(self.customers_page)
        self.stack.addWidget(self.rentals_page)
        self.stack.addWidget(self.reports_page)
        
        content_layout.addWidget(self.stack)
        
        main_layout.addWidget(content_frame)
        
        # Connecter les boutons de navigation
        self.btn_dashboard.clicked.connect(lambda: self.switch_page(0))
        self.btn_vehicles.clicked.connect(lambda: self.switch_page(1))
        self.btn_customers.clicked.connect(lambda: self.switch_page(2))
        self.btn_rentals.clicked.connect(lambda: self.switch_page(3))
        self.btn_reports.clicked.connect(lambda: self.switch_page(4))
        
        # Barre de statut
        status_bar = self.statusBar()
        if status_bar:
            status_bar.showMessage("Prêt")
            status_bar.setStyleSheet("background-color: #ffffff; border-top: 1px solid #e2e8f0;")
    
    def switch_page(self, index: int):
        """Change la page affichée."""
        self.stack.setCurrentIndex(index)
        
        # Mettre à jour les boutons avec les icônes
        for i, btn in enumerate(self.nav_buttons):
            btn.set_active(i == index)
        
        # Rafraîchir la page si nécessaire
        if index == 0:
            self.dashboard_page.refresh_data()
        elif index == 1:
            self.vehicles_page.refresh_data()
        elif index == 2:
            self.customers_page.refresh_data()
        elif index == 3:
            self.rentals_page.refresh_data()
        elif index == 4:
            self.reports_page.refresh_data()
    
    def refresh_all(self):
        """Rafraîchit toutes les pages."""
        self.dashboard_page.refresh_data()
        # Les autres pages se rafraîchissent à l'ouverture
    
    def load_demo_data(self):
        """Charge des données de démonstration."""
        # Voitures
        cars = [
            Car(
                brand="Renault", model="Clio", category=VehicleCategory.ECONOMY,
                daily_rate=35.0, year=2022, license_plate="AB-123-CD",
                num_doors=5, num_seats=5, fuel_type="essence", transmission="manuelle"
            ),
            Car(
                brand="Peugeot", model="308", category=VehicleCategory.STANDARD,
                daily_rate=50.0, year=2023, license_plate="EF-456-GH",
                num_doors=5, num_seats=5, fuel_type="diesel", transmission="automatique"
            ),
            Car(
                brand="BMW", model="Série 3", category=VehicleCategory.PREMIUM,
                daily_rate=90.0, year=2023, license_plate="IJ-789-KL",
                num_doors=4, num_seats=5, fuel_type="essence", transmission="automatique"
            ),
            Car(
                brand="Mercedes", model="Classe S", category=VehicleCategory.LUXURY,
                daily_rate=200.0, year=2024, license_plate="MN-012-OP",
                num_doors=4, num_seats=5, fuel_type="hybride", transmission="automatique"
            ),
        ]
        
        # Camions
        trucks = [
            Truck(
                brand="Renault", model="Master", category=VehicleCategory.UTILITY,
                daily_rate=70.0, year=2021, license_plate="TR-111-CK",
                cargo_capacity=12.0, max_weight=3000, has_tail_lift=False
            ),
            Truck(
                brand="Mercedes", model="Sprinter", category=VehicleCategory.UTILITY,
                daily_rate=85.0, year=2022, license_plate="TR-222-CK",
                cargo_capacity=15.0, max_weight=3500, has_tail_lift=True
            ),
        ]
        
        # Motos
        motorcycles = [
            Motorcycle(
                brand="Honda", model="CB125R", category=VehicleCategory.ECONOMY,
                daily_rate=25.0, year=2023, license_plate="MO-111-TO",
                engine_size=125, motorcycle_type="standard"
            ),
            Motorcycle(
                brand="Yamaha", model="MT-07", category=VehicleCategory.STANDARD,
                daily_rate=60.0, year=2023, license_plate="MO-222-TO",
                engine_size=689, motorcycle_type="roadster"
            ),
        ]
        
        for vehicle in cars + trucks + motorcycles:
            self.system.add_vehicle(vehicle)
        
        # Clients
        customers = [
            Customer(
                first_name="Jean", last_name="Dupont",
                birth_date=date(1985, 3, 15),
                license_number="123456789012",
                license_types={"B"},
                license_date=date(2005, 6, 20),
                email="jean.dupont@email.com",
                phone="06 12 34 56 78",
                address="12 Rue de Paris, 75001 Paris"
            ),
            Customer(
                first_name="Marie", last_name="Martin",
                birth_date=date(1990, 7, 22),
                license_number="987654321098",
                license_types={"B", "A"},
                license_date=date(2010, 8, 15),
                email="marie.martin@email.com",
                phone="06 98 76 54 32",
                address="45 Avenue de Lyon, 69001 Lyon"
            ),
            Customer(
                first_name="Pierre", last_name="Bernard",
                birth_date=date(1988, 11, 8),
                license_number="456789123456",
                license_types={"B", "A1", "C"},
                license_date=date(2008, 5, 10),
                email="pierre.bernard@email.com",
                phone="06 11 22 33 44",
                address="78 Boulevard de Marseille, 13001 Marseille"
            ),
        ]
        
        for customer in customers:
            self.system.add_customer(customer)
