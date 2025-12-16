"""
Page de gestion des clients.
"""

from datetime import date
from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QDialog, QFormLayout, QLineEdit,
    QCheckBox, QMessageBox, QDateEdit,
    QGroupBox, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate

from car_rental_system import CarRentalSystem
from models.customer import Customer
from gui.icons import get_icon, create_action_button


class CustomerDialog(QDialog):
    """Dialogue pour ajouter/modifier un client."""
    
    def __init__(self, parent: Optional[QWidget] = None, customer: Optional[Customer] = None):
        super().__init__(parent)
        self.customer = customer
        self.setWindowTitle("Modifier le client" if customer else "Ajouter un client")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        self.setMaximumHeight(700)
        self.setup_ui()
        
        if customer:
            self.load_customer_data()
    
    def setup_ui(self):
        """Configure l'interface du dialogue."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Zone défilante pour le contenu
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 16)
        
        # Titre
        title = QLabel("Modifier le client" if self.customer else "Nouveau client")
        title.setStyleSheet("font-size: 20px; font-weight: 700; color: #1e293b;")
        layout.addWidget(title)
        
        # Informations personnelles
        personal_group = QGroupBox("Informations personnelles")
        personal_layout = QFormLayout(personal_group)
        personal_layout.setSpacing(12)
        
        self.first_name_edit = QLineEdit()
        self.first_name_edit.setPlaceholderText("Prénom")
        personal_layout.addRow("Prénom:", self.first_name_edit)
        
        self.last_name_edit = QLineEdit()
        self.last_name_edit.setPlaceholderText("Nom de famille")
        personal_layout.addRow("Nom:", self.last_name_edit)
        
        self.birth_date_edit = QDateEdit()
        self.birth_date_edit.setCalendarPopup(True)
        self.birth_date_edit.setDate(QDate(1990, 1, 1))
        self.birth_date_edit.setMaximumDate(QDate.currentDate())
        personal_layout.addRow("Date de naissance:", self.birth_date_edit)
        
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("email@exemple.com")
        personal_layout.addRow("Email:", self.email_edit)
        
        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("06 12 34 56 78")
        personal_layout.addRow("Téléphone:", self.phone_edit)
        
        self.address_edit = QLineEdit()
        self.address_edit.setPlaceholderText("Adresse complète")
        personal_layout.addRow("Adresse:", self.address_edit)
        
        layout.addWidget(personal_group)
        
        # Informations permis
        license_group = QGroupBox("Permis de conduire")
        license_layout = QFormLayout(license_group)
        license_layout.setSpacing(12)
        
        self.license_number_edit = QLineEdit()
        self.license_number_edit.setPlaceholderText("Numéro de permis")
        license_layout.addRow("N° de permis:", self.license_number_edit)
        
        self.license_date_edit = QDateEdit()
        self.license_date_edit.setCalendarPopup(True)
        self.license_date_edit.setDate(QDate(2015, 1, 1))
        self.license_date_edit.setMaximumDate(QDate.currentDate())
        license_layout.addRow("Date d'obtention:", self.license_date_edit)
        
        # Types de permis
        license_types_layout = QHBoxLayout()
        self.license_b = QCheckBox("B (Voiture)")
        self.license_b.setChecked(True)
        self.license_a = QCheckBox("A (Moto)")
        self.license_a1 = QCheckBox("A1 (125cc)")
        self.license_c = QCheckBox("C (Camion)")
        
        license_types_layout.addWidget(self.license_b)
        license_types_layout.addWidget(self.license_a)
        license_types_layout.addWidget(self.license_a1)
        license_types_layout.addWidget(self.license_c)
        license_types_layout.addStretch()
        
        license_layout.addRow("Types de permis:", license_types_layout)
        
        layout.addWidget(license_group)
        layout.addStretch()
        
        scroll.setWidget(content)
        main_layout.addWidget(scroll, 1)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #e2e8f0;")
        separator.setFixedHeight(1)
        main_layout.addWidget(separator)
        
        # Boutons (en dehors du scroll)
        buttons_widget = QWidget()
        buttons_widget.setStyleSheet("background-color: #f8fafc;")
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(24, 16, 24, 16)
        buttons_layout.setSpacing(12)
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setFixedHeight(40)
        cancel_btn.setMinimumWidth(100)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #475569;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                font-weight: 600;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        save_btn = QPushButton("  Enregistrer")
        save_btn.setIcon(get_icon("check", "#ffffff", 18))
        save_btn.setFixedHeight(40)
        save_btn.setMinimumWidth(140)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)
        save_btn.clicked.connect(self.validate_and_accept)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(save_btn)
        
        main_layout.addWidget(buttons_widget)
    
    def load_customer_data(self):
        """Charge les données du client existant."""
        c = self.customer
        if not c:
            return
        
        self.first_name_edit.setText(c.first_name)
        self.last_name_edit.setText(c.last_name)
        self.birth_date_edit.setDate(QDate(c.birth_date.year, c.birth_date.month, c.birth_date.day))
        self.email_edit.setText(c.email)
        self.phone_edit.setText(c.phone)
        self.address_edit.setText(c.address)
        
        self.license_number_edit.setText(c.license_number)
        self.license_date_edit.setDate(QDate(c.license_date.year, c.license_date.month, c.license_date.day))
        
        self.license_b.setChecked("B" in c.license_types)
        self.license_a.setChecked("A" in c.license_types)
        self.license_a1.setChecked("A1" in c.license_types)
        self.license_c.setChecked("C" in c.license_types)
    
    def validate_and_accept(self):
        """Valide les données et accepte le dialogue."""
        if not self.first_name_edit.text() or not self.last_name_edit.text():
            QMessageBox.warning(self, "Erreur", "Le prénom et le nom sont obligatoires.")
            return
        
        if not self.license_number_edit.text():
            QMessageBox.warning(self, "Erreur", "Le numéro de permis est obligatoire.")
            return
        
        if not any([self.license_b.isChecked(), self.license_a.isChecked(), 
                    self.license_a1.isChecked(), self.license_c.isChecked()]):
            QMessageBox.warning(self, "Erreur", "Sélectionnez au moins un type de permis.")
            return
        
        self.accept()
    
    def get_customer(self) -> Customer:
        """Crée et retourne le client selon les données du formulaire."""
        license_types = set()
        if self.license_b.isChecked():
            license_types.add("B")
        if self.license_a.isChecked():
            license_types.add("A")
        if self.license_a1.isChecked():
            license_types.add("A1")
        if self.license_c.isChecked():
            license_types.add("C")
        
        birth_qdate = self.birth_date_edit.date()
        license_qdate = self.license_date_edit.date()
        
        customer_id = self.customer.id if self.customer else None
        
        return Customer(
            first_name=self.first_name_edit.text(),
            last_name=self.last_name_edit.text(),
            birth_date=date(birth_qdate.year(), birth_qdate.month(), birth_qdate.day()),
            license_number=self.license_number_edit.text(),
            license_types=license_types,
            license_date=date(license_qdate.year(), license_qdate.month(), license_qdate.day()),
            email=self.email_edit.text(),
            phone=self.phone_edit.text(),
            address=self.address_edit.text(),
            customer_id=customer_id
        )


class CustomersPage(QWidget):
    """Page de gestion des clients."""
    
    data_changed = pyqtSignal()
    
    def __init__(self, system: CarRentalSystem):
        super().__init__()
        self.system = system
        self.setup_ui()
        self.refresh_data()
    
    def setup_ui(self):
        """Configure l'interface de la page."""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # En-tête
        header_layout = QHBoxLayout()
        
        title_layout = QVBoxLayout()
        title = QLabel("Gestion des clients")
        title.setStyleSheet("font-size: 24px; font-weight: 700; color: #0f172a;")
        subtitle = QLabel("Gérez votre base de clients")
        subtitle.setStyleSheet("color: #64748b;")
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        add_btn = QPushButton("  Ajouter un client")
        add_btn.setIcon(get_icon("add", "#ffffff", 18))
        add_btn.setFixedHeight(44)
        add_btn.setMinimumWidth(200)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                font-size: 14px;
                font-weight: 600;
                border-radius: 8px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
        """)
        add_btn.clicked.connect(self.add_customer)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addWidget(add_btn)
        
        layout.addLayout(header_layout)
        
        # Recherche
        search_layout = QHBoxLayout()
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Rechercher par nom, email ou telephone...")
        self.search_edit.textChanged.connect(self.apply_filter)
        self.search_edit.setMaximumWidth(400)
        
        search_layout.addWidget(self.search_edit)
        search_layout.addStretch()
        
        layout.addLayout(search_layout)
        
        # Tableau des clients
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nom complet", "Âge", "Email", "Téléphone", 
            "Permis", "Locations", "Statut", "Actions"
        ])
        
        # Configuration du tableau
        header = self.table.horizontalHeader()
        if header:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # ID
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Nom
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)  # Âge
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Email
            header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)  # Téléphone
            header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)  # Permis
            header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)  # Locations
            header.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)  # Statut
            header.setSectionResizeMode(8, QHeaderView.ResizeMode.Fixed)  # Actions
        
        # Largeurs fixes des colonnes
        self.table.setColumnWidth(0, 90)   # ID
        self.table.setColumnWidth(2, 70)   # Âge
        self.table.setColumnWidth(4, 120)  # Téléphone
        self.table.setColumnWidth(5, 80)   # Permis
        self.table.setColumnWidth(6, 80)   # Locations
        self.table.setColumnWidth(7, 100)  # Statut
        self.table.setColumnWidth(8, 120)  # Actions
        
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        v_header = self.table.verticalHeader()
        if v_header:
            v_header.setDefaultSectionSize(45)
            v_header.setMinimumSectionSize(45)
            v_header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        
        layout.addWidget(self.table)
    
    def refresh_data(self):
        """Rafraîchit les données du tableau."""
        self.all_customers = self.system.get_all_customers()
        self.apply_filter()
    
    def apply_filter(self):
        """Applique le filtre de recherche."""
        customers = self.all_customers
        
        search = self.search_edit.text().lower()
        if search:
            customers = [c for c in customers 
                        if search in c.first_name.lower()
                        or search in c.last_name.lower()
                        or search in c.email.lower()
                        or search in c.phone]
        
        self.display_customers(customers)
    
    def display_customers(self, customers: list):
        """Affiche les clients dans le tableau."""
        self.table.setRowCount(len(customers))
        
        for row, customer in enumerate(customers):
            self.table.setItem(row, 0, QTableWidgetItem(customer.id))
            self.table.setItem(row, 1, QTableWidgetItem(customer.full_name))
            self.table.setItem(row, 2, QTableWidgetItem(f"{customer.age} ans"))
            self.table.setItem(row, 3, QTableWidgetItem(customer.email))
            self.table.setItem(row, 4, QTableWidgetItem(customer.phone))
            self.table.setItem(row, 5, QTableWidgetItem(", ".join(sorted(customer.license_types))))
            self.table.setItem(row, 6, QTableWidgetItem(str(customer.get_total_rentals())))
            
            # Statut avec badge
            status_widget = QWidget()
            status_layout = QHBoxLayout(status_widget)
            status_layout.setContentsMargins(2, 2, 2, 2)
            status_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            status_label = QLabel()
            if customer.is_blocked:
                status_label.setText("Bloqué")
                status_label.setStyleSheet("""
                    QLabel {
                        background-color: #fef2f2;
                        color: #dc2626;
                        padding: 2px 8px;
                        border-radius: 10px;
                        font-weight: 600;
                        font-size: 11px;
                        border: 1px solid #fecaca;
                    }
                """)
            elif customer.is_loyal_customer():
                status_label.setText("Fidèle")
                status_label.setStyleSheet("""
                    QLabel {
                        background-color: #f0fdf4;
                        color: #16a34a;
                        padding: 2px 8px;
                        border-radius: 10px;
                        font-weight: 600;
                        font-size: 11px;
                        border: 1px solid #bbf7d0;
                    }
                """)
            else:
                status_label.setText("Actif")
                status_label.setStyleSheet("""
                    QLabel {
                        background-color: #eff6ff;
                        color: #2563eb;
                        padding: 2px 8px;
                        border-radius: 10px;
                        font-weight: 600;
                        font-size: 11px;
                        border: 1px solid #bfdbfe;
                    }
                """)
            status_layout.addWidget(status_label)
            self.table.setCellWidget(row, 7, status_widget)
            
            # Boutons d'action
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4, 0, 4, 0)
            actions_layout.setSpacing(6)
            actions_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            edit_btn = create_action_button(
                "edit", "Modifier",
                icon_color="#3b82f6",
                bg_color="#eff6ff",
                hover_color="#dbeafe",
                border_color="#bfdbfe",
                size=28
            )
            edit_btn.clicked.connect(lambda checked, c=customer: self.edit_customer(c))
            
            delete_btn = create_action_button(
                "delete", "Supprimer",
                icon_color="#ef4444",
                bg_color="#fef2f2",
                hover_color="#fee2e2",
                border_color="#fecaca",
                size=28
            )
            delete_btn.clicked.connect(lambda checked, c=customer: self.delete_customer(c))
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            
            self.table.setCellWidget(row, 8, actions_widget)
    
    def add_customer(self):
        """Ouvre le dialogue pour ajouter un client."""
        dialog = CustomerDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            customer = dialog.get_customer()
            if self.system.add_customer(customer):
                self.refresh_data()
                self.data_changed.emit()
                QMessageBox.information(self, "Succès", "Client ajouté avec succès!")
            else:
                QMessageBox.warning(self, "Erreur", "Impossible d'ajouter le client.")
    
    def edit_customer(self, customer: Customer):
        """Ouvre le dialogue pour modifier un client."""
        dialog = CustomerDialog(self, customer)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Conserver l'historique via les getters publics
            old_history = customer.rental_history
            old_active = customer.active_rentals
            old_blocked = customer.is_blocked
            old_blocked_reason = customer.blocked_reason
            
            self.system.remove_customer(customer.id)
            new_customer = dialog.get_customer()
            # Restaurer l'état via la méthode publique
            new_customer.restore_state(
                rental_history=old_history,
                active_rentals=old_active,
                is_blocked=old_blocked,
                blocked_reason=old_blocked_reason
            )
            
            self.system.add_customer(new_customer)
            self.refresh_data()
            self.data_changed.emit()
            QMessageBox.information(self, "Succès", "Client modifié avec succès!")
    
    def delete_customer(self, customer: Customer):
        """Supprime un client."""
        reply = QMessageBox.question(
            self, "Confirmation",
            f"Voulez-vous vraiment supprimer le client {customer.full_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.system.remove_customer(customer.id):
                self.refresh_data()
                self.data_changed.emit()
                QMessageBox.information(self, "Succès", "Client supprimé!")
            else:
                QMessageBox.warning(
                    self, "Erreur",
                    "Impossible de supprimer ce client.\nIl a peut-être des locations actives."
                )
