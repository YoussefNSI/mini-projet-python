"""
Page des rapports et statistiques.
"""

from datetime import date
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QDateEdit, QGroupBox,
    QScrollArea, QComboBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QColor

from car_rental_system import CarRentalSystem
from gui.icons import get_icon, ICON_COLORS


class StatCard(QFrame):
    """Widget de statistique avec carte."""
    
    def __init__(self, title: str, value: str, icon_name: str = "", color: str = "#2563eb"):
        super().__init__()
        self.color = color
        self.setObjectName("statCard")
        self.setStyleSheet(f"""
            QFrame#statCard {{
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-left: 4px solid {color};
                border-radius: 8px;
            }}
            QFrame#statCard QLabel {{
                background: transparent;
                border: none;
            }}
        """)
        self.setMinimumHeight(90)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        
        if icon_name:
            icon_label = QLabel()
            icon_label.setPixmap(get_icon(icon_name, color, 32).pixmap(32, 32))
            layout.addWidget(icon_label)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(f"font-size: 28px; font-weight: 700; color: {color}; background: transparent; border: none;")
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #64748b; font-size: 13px; background: transparent; border: none;")
        
        text_layout.addWidget(self.value_label)
        text_layout.addWidget(title_label)
        
        layout.addLayout(text_layout)
        layout.addStretch()
    
    def set_value(self, value: str):
        """Met à jour la valeur."""
        self.value_label.setText(value)


class ReportSection(QFrame):
    """Section de rapport avec titre et contenu."""
    
    def __init__(self, title: str, icon_name: str = ""):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
            }
        """)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 16, 20, 16)
        self.main_layout.setSpacing(12)
        
        # Titre avec icône
        title_layout = QHBoxLayout()
        if icon_name:
            icon_label = QLabel()
            icon_label.setPixmap(get_icon(icon_name, "#1e293b", 20).pixmap(20, 20))
            title_layout.addWidget(icon_label)
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #1e293b;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        self.main_layout.addLayout(title_layout)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #e2e8f0;")
        separator.setFixedHeight(1)
        self.main_layout.addWidget(separator)
        
        # Content layout
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(8)
        self.main_layout.addLayout(self.content_layout)
    
    def add_stat_row(self, label: str, value: str, highlight: bool = False):
        """Ajoute une ligne de statistique."""
        row = QHBoxLayout()
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet("color: #64748b;")
        
        value_widget = QLabel(value)
        if highlight:
            value_widget.setStyleSheet("font-weight: 600; color: #2563eb; font-size: 15px;")
        else:
            value_widget.setStyleSheet("font-weight: 500; color: #1e293b;")
        
        row.addWidget(label_widget)
        row.addStretch()
        row.addWidget(value_widget)
        
        self.content_layout.addLayout(row)
    
    def add_widget(self, widget: QWidget):
        """Ajoute un widget au contenu."""
        self.content_layout.addWidget(widget)


class ReportsPage(QWidget):
    """Page des rapports et statistiques."""
    
    def __init__(self, system: CarRentalSystem):
        super().__init__()
        self.system = system
        self.setup_ui()
        self.refresh_data()
    
    def setup_ui(self):
        """Configure l'interface de la page."""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # ScrollArea comme conteneur principal
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: #f8fafc;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #f1f5f9;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #cbd5e1;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #94a3b8;
            }
        """)
        
        # Contenu scrollable
        content = QWidget()
        content.setStyleSheet("background-color: #f8fafc;")
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(24)
        content_layout.setContentsMargins(24, 24, 24, 24)
        
        # En-tête
        header_layout = QHBoxLayout()
        
        title_layout = QVBoxLayout()
        title = QLabel("Rapports et statistiques")
        title.setStyleSheet("font-size: 24px; font-weight: 700; color: #0f172a;")
        subtitle = QLabel("Analysez les performances de votre agence de location")
        subtitle.setStyleSheet("color: #64748b; font-size: 14px;")
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        refresh_btn = QPushButton("  Actualiser")
        refresh_btn.setIcon(get_icon("refresh", "#64748b", 18))
        refresh_btn.setFixedHeight(40)
        refresh_btn.setProperty("secondary", True)
        refresh_btn.clicked.connect(self.refresh_data)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addWidget(refresh_btn)
        
        content_layout.addLayout(header_layout)
        
        # Statistiques rapides (4 cartes)
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)
        
        self.stat_revenue = StatCard("Chiffre d'affaires total", "0 EUR", "money", "#22c55e")
        self.stat_rentals = StatCard("Locations completees", "0", "documents", "#2563eb")
        self.stat_avg = StatCard("Panier moyen", "0 EUR", "chart", "#8b5cf6")
        self.stat_utilization = StatCard("Taux d'utilisation", "0%", "car", "#f59e0b")
        
        stats_layout.addWidget(self.stat_revenue)
        stats_layout.addWidget(self.stat_rentals)
        stats_layout.addWidget(self.stat_avg)
        stats_layout.addWidget(self.stat_utilization)
        
        content_layout.addLayout(stats_layout)
        
        # Filtres de période
        filter_frame = QFrame()
        filter_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
            }
        """)
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(16, 12, 16, 12)
        
        filter_layout.addWidget(QLabel("Periode:"))
        
        self.period_combo = QComboBox()
        self.period_combo.addItems(["Ce mois", "Les 3 derniers mois", "Cette année", "Tout", "Personnalisé"])
        self.period_combo.setMinimumWidth(150)
        self.period_combo.currentTextChanged.connect(self.on_period_changed)
        filter_layout.addWidget(self.period_combo)
        
        filter_layout.addWidget(QLabel("Du:"))
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.start_date.setEnabled(False)
        filter_layout.addWidget(self.start_date)
        
        filter_layout.addWidget(QLabel("Au:"))
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setEnabled(False)
        filter_layout.addWidget(self.end_date)
        
        filter_layout.addStretch()
        
        apply_btn = QPushButton("Appliquer")
        apply_btn.clicked.connect(self.refresh_data)
        filter_layout.addWidget(apply_btn)
        
        content_layout.addWidget(filter_frame)
        
        # Grille de rapports (2 colonnes)
        reports_grid = QGridLayout()
        reports_grid.setSpacing(16)
        
        # Rapport Chiffre d'affaires
        self.revenue_section = ReportSection("Chiffre d'affaires", "money")
        reports_grid.addWidget(self.revenue_section, 0, 0)
        
        # Rapport par type de vehicule
        self.vehicle_type_section = ReportSection("Revenus par type de vehicule", "car")
        reports_grid.addWidget(self.vehicle_type_section, 0, 1)
        
        # Rapport Flotte
        self.fleet_section = ReportSection("Etat de la flotte", "chart")
        reports_grid.addWidget(self.fleet_section, 1, 0)
        
        # Rapport Clients
        self.customers_section = ReportSection("Statistiques clients", "users")
        reports_grid.addWidget(self.customers_section, 1, 1)
        
        content_layout.addLayout(reports_grid)
        
        # Tableau des meilleurs clients
        top_customers_section = ReportSection("Meilleurs clients", "users")
        
        self.top_customers_table = QTableWidget()
        self.top_customers_table.setColumnCount(5)
        self.top_customers_table.setHorizontalHeaderLabels([
            "Client", "Locations", "Fidelite", "Reduction", "Statut"
        ])
        
        header = self.top_customers_table.horizontalHeader()
        if header:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        self.top_customers_table.setAlternatingRowColors(True)
        v_header = self.top_customers_table.verticalHeader()
        if v_header:
            v_header.setVisible(False)
        self.top_customers_table.setMinimumHeight(200)
        self.top_customers_table.setMaximumHeight(350)
        self.top_customers_table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                font-size: 13px;
                gridline-color: #f1f5f9;
            }
            QTableWidget::item {
                padding: 8px 12px;
            }
            QTableWidget::item:selected {
                background-color: #dbeafe;
                color: #1e40af;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #e2e8f0;
                font-weight: 600;
                color: #475569;
            }
        """)
        
        top_customers_section.add_widget(self.top_customers_table)
        content_layout.addWidget(top_customers_section)
        
        # Tableau maintenance
        maintenance_section = ReportSection("Vehicules necessitant une maintenance", "warning")
        
        self.maintenance_table = QTableWidget()
        self.maintenance_table.setColumnCount(5)
        self.maintenance_table.setHorizontalHeaderLabels([
            "ID", "Vehicule", "Kilometrage", "Derniere maintenance", "Etat"
        ])
        
        header2 = self.maintenance_table.horizontalHeader()
        if header2:
            header2.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            header2.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            header2.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
            header2.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
            header2.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        self.maintenance_table.setAlternatingRowColors(True)
        v_header2 = self.maintenance_table.verticalHeader()
        if v_header2:
            v_header2.setVisible(False)
        self.maintenance_table.setMinimumHeight(150)
        self.maintenance_table.setMaximumHeight(300)
        self.maintenance_table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #fecaca;
                border-radius: 8px;
                font-size: 13px;
                gridline-color: #fee2e2;
            }
            QTableWidget::item {
                padding: 8px 12px;
            }
            QTableWidget::item:selected {
                background-color: #fef3c7;
                color: #92400e;
            }
            QHeaderView::section {
                background-color: #fef2f2;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #fecaca;
                font-weight: 600;
                color: #991b1b;
            }
        """)
        
        maintenance_section.add_widget(self.maintenance_table)
        content_layout.addWidget(maintenance_section)
        
        # Espace en bas
        content_layout.addStretch()
        
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
    
    def on_period_changed(self, period: str):
        """Appelé quand la période change."""
        custom = period == "Personnalisé"
        self.start_date.setEnabled(custom)
        self.end_date.setEnabled(custom)
        
        if not custom:
            today = QDate.currentDate()
            if period == "Ce mois":
                self.start_date.setDate(QDate(today.year(), today.month(), 1))
            elif period == "Les 3 derniers mois":
                self.start_date.setDate(today.addMonths(-3))
            elif period == "Cette année":
                self.start_date.setDate(QDate(today.year(), 1, 1))
            elif period == "Tout":
                self.start_date.setDate(QDate(2020, 1, 1))
            self.end_date.setDate(today)
    
    def refresh_data(self):
        """Rafraîchit toutes les données."""
        self.refresh_stats()
        self.refresh_revenue_section()
        self.refresh_vehicle_type_section()
        self.refresh_fleet_section()
        self.refresh_customers_section()
        self.refresh_top_customers()
        self.refresh_maintenance()
    
    def refresh_stats(self):
        """Rafraîchit les statistiques rapides."""
        stats = self.system.generate_statistics_report()
        revenue = self.system.generate_revenue_report()
        
        self.stat_revenue.set_value(f"{revenue.get('total_revenue', 0):.0f} €")
        self.stat_rentals.set_value(str(revenue.get('total_rentals_completed', 0)))
        self.stat_avg.set_value(f"{revenue.get('average_rental_value', 0):.0f} €")
        
        utilization = stats.get('fleet', {}).get('utilization_rate', 0)
        self.stat_utilization.set_value(f"{utilization:.1f}%")
    
    def refresh_revenue_section(self):
        """Rafraîchit la section chiffre d'affaires."""
        # Effacer le contenu
        while self.revenue_section.content_layout.count():
            item = self.revenue_section.content_layout.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                else:
                    sub_layout = item.layout()
                    if sub_layout:
                        while sub_layout.count():
                            sub_item = sub_layout.takeAt(0)
                            if sub_item:
                                sub_widget = sub_item.widget()
                                if sub_widget:
                                    sub_widget.deleteLater()
        
        start_qdate = self.start_date.date()
        end_qdate = self.end_date.date()
        start = date(start_qdate.year(), start_qdate.month(), start_qdate.day())
        end = date(end_qdate.year(), end_qdate.month(), end_qdate.day())
        
        report = self.system.generate_revenue_report(start, end)
        
        self.revenue_section.add_stat_row("Chiffre d'affaires total", f"{report.get('total_revenue', 0):.2f} €", True)
        self.revenue_section.add_stat_row("Revenus de base", f"{report.get('total_base_revenue', 0):.2f} €")
        self.revenue_section.add_stat_row("Pénalités perçues", f"{report.get('total_penalties', 0):.2f} €")
        self.revenue_section.add_stat_row("Locations terminées", str(report.get('total_rentals_completed', 0)))
        self.revenue_section.add_stat_row("Valeur moyenne", f"{report.get('average_rental_value', 0):.2f} €")
    
    def refresh_vehicle_type_section(self):
        """Rafraîchit la section revenus par type."""
        # Effacer le contenu
        while self.vehicle_type_section.content_layout.count():
            item = self.vehicle_type_section.content_layout.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                else:
                    sub_layout = item.layout()
                    if sub_layout:
                        while sub_layout.count():
                            sub_item = sub_layout.takeAt(0)
                            if sub_item:
                                sub_widget = sub_item.widget()
                                if sub_widget:
                                    sub_widget.deleteLater()
        
        start_qdate = self.start_date.date()
        end_qdate = self.end_date.date()
        start = date(start_qdate.year(), start_qdate.month(), start_qdate.day())
        end = date(end_qdate.year(), end_qdate.month(), end_qdate.day())
        
        report = self.system.generate_revenue_report(start, end)
        
        for vtype, revenue in report.get('revenue_by_vehicle_type', {}).items():
            self.vehicle_type_section.add_stat_row(vtype, f"{revenue:.2f} €")
        
        if not report.get('revenue_by_vehicle_type'):
            empty_label = QLabel("Aucune donnée disponible")
            empty_label.setStyleSheet("color: #94a3b8; font-style: italic;")
            self.vehicle_type_section.add_widget(empty_label)
    
    def refresh_fleet_section(self):
        """Rafraîchit la section flotte."""
        # Effacer le contenu
        while self.fleet_section.content_layout.count():
            item = self.fleet_section.content_layout.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                else:
                    sub_layout = item.layout()
                    if sub_layout:
                        while sub_layout.count():
                            sub_item = sub_layout.takeAt(0)
                            if sub_item:
                                sub_widget = sub_item.widget()
                                if sub_widget:
                                    sub_widget.deleteLater()
        
        report = self.system.generate_available_vehicles_report()
        stats = self.system.generate_statistics_report()
        fleet = stats.get('fleet', {})
        
        self.fleet_section.add_stat_row("Total véhicules", str(fleet.get('total_vehicles', 0)), True)
        self.fleet_section.add_stat_row("Disponibles", str(report.get('total_available', 0)))
        self.fleet_section.add_stat_row("Taux de disponibilité", f"{report.get('availability_rate', 0):.1f}%")
        self.fleet_section.add_stat_row("Taux d'utilisation", f"{fleet.get('utilization_rate', 0):.1f}%")
        self.fleet_section.add_stat_row("À maintenir", str(fleet.get('needing_maintenance', 0)))
        
        # Par type
        for vtype, count in fleet.get('by_type', {}).items():
            self.fleet_section.add_stat_row(f"  {vtype}", str(count))
    
    def refresh_customers_section(self):
        """Rafraîchit la section clients."""
        # Effacer le contenu
        while self.customers_section.content_layout.count():
            item = self.customers_section.content_layout.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                else:
                    sub_layout = item.layout()
                    if sub_layout:
                        while sub_layout.count():
                            sub_item = sub_layout.takeAt(0)
                            if sub_item:
                                sub_widget = sub_item.widget()
                                if sub_widget:
                                    sub_widget.deleteLater()
        
        stats = self.system.generate_statistics_report()
        customers_stats = stats.get('customers', {})
        
        self.customers_section.add_stat_row("Total clients", str(customers_stats.get('total_customers', 0)), True)
        self.customers_section.add_stat_row("Clients fidèles", str(customers_stats.get('loyal_customers', 0)))
        self.customers_section.add_stat_row("Clients bloqués", str(customers_stats.get('blocked_customers', 0)))
        
        # Programme fidélité
        fidelity_label = QLabel("Programme de fidélité:")
        fidelity_label.setStyleSheet("font-weight: 600; margin-top: 8px;")
        self.customers_section.add_widget(fidelity_label)
        
        self.customers_section.add_stat_row("5+ locations", "5% de réduction")
        self.customers_section.add_stat_row("10+ locations", "10% de réduction")
        self.customers_section.add_stat_row("20+ locations", "15% de réduction")
    
    def refresh_top_customers(self):
        """Rafraîchit le tableau des meilleurs clients."""
        customers = sorted(
            self.system.get_all_customers(),
            key=lambda c: c.get_total_rentals(),
            reverse=True
        )[:10]
        
        self.top_customers_table.setRowCount(len(customers))
        
        for row, c in enumerate(customers):
            # Rang et nom du client
            rank_prefix = ["#1", "#2", "#3"][row] if row < 3 else f"#{row + 1}"
            name_item = QTableWidgetItem(f"{rank_prefix} {c.full_name}")
            name_item.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold if row < 3 else QFont.Weight.Normal))
            self.top_customers_table.setItem(row, 0, name_item)
            
            # Nombre de locations
            rentals_item = QTableWidgetItem(str(c.get_total_rentals()))
            rentals_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.top_customers_table.setItem(row, 1, rentals_item)
            
            # Fidelite avec couleur
            if c.is_loyal_customer():
                loyalty_item = QTableWidgetItem("Fidele")
                loyalty_item.setForeground(QColor("#f59e0b"))
            else:
                loyalty_item = QTableWidgetItem("Standard")
                loyalty_item.setForeground(QColor("#64748b"))
            loyalty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.top_customers_table.setItem(row, 2, loyalty_item)
            
            # Réduction
            discount = c.get_loyalty_discount() * 100
            discount_item = QTableWidgetItem(f"{discount:.0f}%" if discount > 0 else "-")
            discount_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if discount > 0:
                discount_item.setForeground(QColor("#059669"))
                discount_item.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            self.top_customers_table.setItem(row, 3, discount_item)
            
            # Statut
            if c.is_blocked:
                status_item = QTableWidgetItem("Bloque")
                status_item.setForeground(QColor("#dc2626"))
            else:
                status_item = QTableWidgetItem("Actif")
                status_item.setForeground(QColor("#059669"))
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.top_customers_table.setItem(row, 4, status_item)
        
        # Si aucun client
        if not customers:
            self.top_customers_table.setRowCount(1)
            empty_item = QTableWidgetItem("Aucun client enregistré")
            empty_item.setForeground(QColor("#94a3b8"))
            self.top_customers_table.setItem(0, 0, empty_item)
            for col in range(1, 5):
                self.top_customers_table.setItem(0, col, QTableWidgetItem(""))
    
    def refresh_maintenance(self):
        """Rafraîchit le tableau de maintenance."""
        vehicles_needing_maintenance = [
            v for v in self.system.get_all_vehicles() if v.needs_maintenance()
        ]
        
        self.maintenance_table.setRowCount(len(vehicles_needing_maintenance))
        
        for row, v in enumerate(vehicles_needing_maintenance):
            # ID
            id_item = QTableWidgetItem(v.id)
            id_item.setFont(QFont("Consolas", 9))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.maintenance_table.setItem(row, 0, id_item)
            
            # Véhicule
            vehicle_item = QTableWidgetItem(f"{v.brand} {v.model} ({v.year})")
            vehicle_item.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            self.maintenance_table.setItem(row, 1, vehicle_item)
            
            # Kilométrage avec alerte visuelle
            mileage = v.mileage
            mileage_item = QTableWidgetItem(f"{mileage:,.0f} km")
            mileage_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if mileage > 50000:
                mileage_item.setForeground(QColor("#dc2626"))
                mileage_item.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            elif mileage > 30000:
                mileage_item.setForeground(QColor("#f59e0b"))
            self.maintenance_table.setItem(row, 2, mileage_item)
            
            # Derniere maintenance
            if v.last_maintenance_date:
                days_since = (date.today() - v.last_maintenance_date).days
                date_str = v.last_maintenance_date.strftime("%d/%m/%Y")
                maintenance_item = QTableWidgetItem(f"{date_str} ({days_since}j)")
                if days_since > 180:
                    maintenance_item.setForeground(QColor("#dc2626"))
                elif days_since > 90:
                    maintenance_item.setForeground(QColor("#f59e0b"))
            else:
                maintenance_item = QTableWidgetItem("Jamais")
                maintenance_item.setForeground(QColor("#dc2626"))
                maintenance_item.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            maintenance_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.maintenance_table.setItem(row, 3, maintenance_item)
            
            # Etat avec icone
            state_text = {
                "En maintenance": "Maintenance",
                "Hors service": "Hors service",
                "Disponible": "A reviser",
                "Reserve": "A reviser",
                "Loue": "A reviser"
            }.get(v.state.value, v.state.value)
            state_item = QTableWidgetItem(state_text)
            state_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            state_item.setForeground(QColor("#b45309"))
            self.maintenance_table.setItem(row, 4, state_item)
        
        # Si aucun vehicule a maintenir
        if not vehicles_needing_maintenance:
            self.maintenance_table.setRowCount(1)
            ok_item = QTableWidgetItem("Aucun vehicule necessitant une maintenance")
            ok_item.setForeground(QColor("#059669"))
            ok_item.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
            self.maintenance_table.setItem(0, 0, ok_item)
            self.maintenance_table.setSpan(0, 0, 1, 5)  # Fusionner les cellules
