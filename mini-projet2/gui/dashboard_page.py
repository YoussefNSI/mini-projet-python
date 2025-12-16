"""
Page du tableau de bord (Dashboard).
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from car_rental_system import CarRentalSystem
from gui.icons import get_icon, ICON_COLORS


class StatCard(QFrame):
    """Carte de statistique pour le dashboard."""
    
    def __init__(self, title: str, value: str, subtitle: str = "", color: str = "#2563eb"):
        super().__init__()
        self.setProperty("card", True)
        self.setMinimumSize(200, 120)
        self.setMaximumHeight(140)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        # Titre
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: #64748b; font-size: 13px; font-weight: 500;")
        
        # Valeur
        value_label = QLabel(value)
        value_label.setStyleSheet(f"color: {color}; font-size: 32px; font-weight: 700;")
        self.value_label = value_label
        
        # Sous-titre
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("color: #94a3b8; font-size: 12px;")
        self.subtitle_label = subtitle_label
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(subtitle_label)
        layout.addStretch()
    
    def update_value(self, value: str, subtitle: str = ""):
        """Met à jour la valeur affichée."""
        self.value_label.setText(value)
        if subtitle:
            self.subtitle_label.setText(subtitle)


class RecentActivityItem(QFrame):
    """Item d'activité récente."""
    
    def __init__(self, icon: str, title: str, description: str, time: str):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: #f8fafc;
                border-radius: 8px;
                padding: 12px;
            }
            QFrame:hover {
                background-color: #f1f5f9;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Icône
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")
        icon_label.setFixedWidth(40)
        
        # Contenu
        content_layout = QVBoxLayout()
        content_layout.setSpacing(2)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: 600; color: #1e293b;")
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet("color: #64748b; font-size: 12px;")
        
        content_layout.addWidget(title_label)
        content_layout.addWidget(desc_label)
        
        # Heure
        time_label = QLabel(time)
        time_label.setStyleSheet("color: #94a3b8; font-size: 11px;")
        time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        
        layout.addWidget(icon_label)
        layout.addLayout(content_layout, 1)
        layout.addWidget(time_label)


class DashboardPage(QWidget):
    """Page du tableau de bord."""
    
    def __init__(self, system: CarRentalSystem):
        super().__init__()
        self.system = system
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface du dashboard."""
        # Scroll area pour le contenu
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")
        
        # Widget contenu
        content = QWidget()
        content.setStyleSheet("background-color: transparent;")
        main_layout = QVBoxLayout(content)
        main_layout.setSpacing(24)
        main_layout.setContentsMargins(24, 24, 24, 24)
        
        # En-tête
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)
        
        title = QLabel("Tableau de bord")
        title.setProperty("heading", True)
        title.setStyleSheet("font-size: 28px; font-weight: 700; color: #0f172a;")
        
        subtitle = QLabel("Vue d'ensemble de votre agence de location")
        subtitle.setStyleSheet("color: #64748b; font-size: 14px;")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)
        
        # Cartes de statistiques
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)
        
        self.card_vehicles = StatCard(
            "Véhicules disponibles",
            "0",
            "sur 0 au total",
            "#22c55e"
        )
        
        self.card_customers = StatCard(
            "Clients enregistrés",
            "0",
            "clients actifs",
            "#2563eb"
        )
        
        self.card_rentals = StatCard(
            "Locations en cours",
            "0",
            "0 en retard",
            "#f59e0b"
        )
        
        self.card_revenue = StatCard(
            "Chiffre d'affaires",
            "0 €",
            "ce mois",
            "#8b5cf6"
        )
        
        stats_layout.addWidget(self.card_vehicles)
        stats_layout.addWidget(self.card_customers)
        stats_layout.addWidget(self.card_rentals)
        stats_layout.addWidget(self.card_revenue)
        
        main_layout.addLayout(stats_layout)
        
        # Section inférieure : deux colonnes
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(24)
        
        # Colonne gauche : Véhicules disponibles par type
        left_card = QFrame()
        left_card.setProperty("card", True)
        left_card.setStyleSheet("""
            QFrame[card="true"] {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        left_layout = QVBoxLayout(left_card)
        
        left_title_layout = QHBoxLayout()
        left_title_icon = QLabel()
        left_title_icon.setPixmap(get_icon("car", "#1e293b", 20).pixmap(20, 20))
        left_title_layout.addWidget(left_title_icon)
        left_title = QLabel("Repartition de la flotte")
        left_title.setStyleSheet("font-size: 16px; font-weight: 600; color: #1e293b; margin-bottom: 16px;")
        left_title_layout.addWidget(left_title)
        left_title_layout.addStretch()
        left_layout.addLayout(left_title_layout)
        
        self.fleet_info = QLabel("Chargement...")
        self.fleet_info.setStyleSheet("color: #64748b; line-height: 1.8;")
        self.fleet_info.setWordWrap(True)
        left_layout.addWidget(self.fleet_info)
        left_layout.addStretch()
        
        # Colonne droite : Activité récente
        right_card = QFrame()
        right_card.setProperty("card", True)
        right_card.setStyleSheet("""
            QFrame[card="true"] {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        right_layout = QVBoxLayout(right_card)
        
        right_title_layout = QHBoxLayout()
        right_title_icon = QLabel()
        right_title_icon.setPixmap(get_icon("chart", "#1e293b", 20).pixmap(20, 20))
        right_title_layout.addWidget(right_title_icon)
        right_title = QLabel("Informations rapides")
        right_title.setStyleSheet("font-size: 16px; font-weight: 600; color: #1e293b; margin-bottom: 16px;")
        right_title_layout.addWidget(right_title)
        right_title_layout.addStretch()
        right_layout.addLayout(right_title_layout)
        
        self.quick_info = QLabel("Chargement...")
        self.quick_info.setStyleSheet("color: #64748b; line-height: 1.8;")
        self.quick_info.setWordWrap(True)
        right_layout.addWidget(self.quick_info)
        right_layout.addStretch()
        
        bottom_layout.addWidget(left_card, 1)
        bottom_layout.addWidget(right_card, 1)
        
        main_layout.addLayout(bottom_layout)
        main_layout.addStretch()
        
        # Ajouter au scroll
        scroll.setWidget(content)
        
        # Layout principal
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.addWidget(scroll)
        
        # Charger les données
        self.refresh_data()
    
    def refresh_data(self):
        """Rafraîchit les données du dashboard."""
        summary = self.system.get_summary()
        
        # Mettre à jour les cartes
        available = len(self.system.get_available_vehicles())
        total_vehicles = summary['total_vehicles']
        self.card_vehicles.update_value(
            str(available),
            f"sur {total_vehicles} au total"
        )
        
        self.card_customers.update_value(
            str(summary['total_customers']),
            "clients enregistrés"
        )
        
        active = summary['active_rentals']
        overdue = summary['overdue_rentals']
        self.card_rentals.update_value(
            str(active),
            f"{overdue} en retard" if overdue > 0 else "aucune en retard"
        )
        
        # Calculer le CA
        report = self.system.generate_revenue_report()
        revenue = report.get('total_revenue', 0)
        self.card_revenue.update_value(
            f"{revenue:.0f} €",
            "ce mois"
        )
        
        # Répartition de la flotte
        stats = self.system.generate_statistics_report()
        fleet = stats.get('fleet', {})
        by_type = fleet.get('by_type', {})
        by_state = fleet.get('by_state', {})
        
        fleet_text = "<b>Par type :</b><br>"
        for vtype, count in by_type.items():
            fleet_text += f"• {vtype}: {count}<br>"
        fleet_text += "<br><b>Par état :</b><br>"
        for state, count in by_state.items():
            fleet_text += f"• {state.capitalize()}: {count}<br>"
        
        utilization = fleet.get('utilization_rate', 0)
        fleet_text += f"<br><b>Taux d'utilisation :</b> {utilization:.1f}%"
        
        self.fleet_info.setText(fleet_text)
        
        # Informations rapides
        customers_stats = stats.get('customers', {})
        rentals_stats = stats.get('rentals', {})
        
        quick_text = f"""
        <b>Clients fidèles :</b> {customers_stats.get('loyal_customers', 0)}<br>
        <b>Clients bloqués :</b> {customers_stats.get('blocked_customers', 0)}<br><br>
        <b>Total des locations :</b> {rentals_stats.get('total_rentals', 0)}<br>
        <b>Locations actives :</b> {rentals_stats.get('active_rentals', 0)}<br>
        <b>Locations en retard :</b> {rentals_stats.get('overdue_rentals', 0)}<br><br>
        <b>Véhicules nécessitant entretien :</b> {fleet.get('needing_maintenance', 0)}
        """
        
        self.quick_info.setText(quick_text.strip())
