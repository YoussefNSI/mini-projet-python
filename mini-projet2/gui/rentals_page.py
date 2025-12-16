"""
Page de gestion des locations et réservations.
"""

from datetime import date
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QDialog, QFormLayout, QComboBox,
    QDoubleSpinBox, QCheckBox, QMessageBox, QDateEdit,
    QGroupBox, QTextEdit, QScrollArea,
    QDialogButtonBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate

from car_rental_system import CarRentalSystem
from models.rental import Rental, RentalStatus
from gui.icons import get_icon, create_action_button


class NewRentalDialog(QDialog):
    """Dialogue pour créer une nouvelle location."""
    
    def __init__(self, parent, system: CarRentalSystem):
        super().__init__(parent)
        self.system = system
        self.setWindowTitle("Nouvelle location")
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        self.setMaximumHeight(700)
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface du dialogue."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
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
        title = QLabel("Créer une nouvelle location")
        title.setStyleSheet("font-size: 20px; font-weight: 700; color: #1e293b;")
        layout.addWidget(title)
        
        # Sélection du client
        client_group = QGroupBox("Client")
        client_layout = QFormLayout(client_group)
        
        self.customer_combo = QComboBox()
        self.customer_combo.addItem("-- Sélectionner un client --", None)
        for customer in self.system.get_all_customers():
            if not customer.is_blocked:
                self.customer_combo.addItem(
                    f"{customer.full_name} ({customer.age} ans) - Permis: {', '.join(customer.license_types)}",
                    customer.id
                )
        self.customer_combo.currentIndexChanged.connect(self.update_available_vehicles)
        client_layout.addRow("Client:", self.customer_combo)
        
        layout.addWidget(client_group)
        
        # Sélection du véhicule
        vehicle_group = QGroupBox("Véhicule")
        vehicle_layout = QFormLayout(vehicle_group)
        
        self.vehicle_combo = QComboBox()
        self.vehicle_combo.addItem("-- Sélectionner d'abord un client --", None)
        self.vehicle_combo.currentIndexChanged.connect(self.update_cost_preview)
        vehicle_layout.addRow("Véhicule:", self.vehicle_combo)
        
        layout.addWidget(vehicle_group)
        
        # Dates
        dates_group = QGroupBox("Période de location")
        dates_layout = QFormLayout(dates_group)
        
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate())  # Permettre aujourd'hui
        self.start_date_edit.setMinimumDate(QDate.currentDate())
        self.start_date_edit.dateChanged.connect(self.on_start_date_changed)
        dates_layout.addRow("Date de début:", self.start_date_edit)
        
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.currentDate().addDays(3))
        self.end_date_edit.setMinimumDate(QDate.currentDate())  # Permettre même jour
        self.end_date_edit.dateChanged.connect(self.update_cost_preview)
        dates_layout.addRow("Date de fin:", self.end_date_edit)
        
        layout.addWidget(dates_group)
        
        # Notes
        notes_group = QGroupBox("Notes (optionnel)")
        notes_layout = QVBoxLayout(notes_group)
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(80)
        self.notes_edit.setPlaceholderText("Ajouter des notes sur cette location...")
        notes_layout.addWidget(self.notes_edit)
        layout.addWidget(notes_group)
        
        # Aperçu du coût
        cost_group = QGroupBox("Aperçu du coût")
        cost_layout = QVBoxLayout(cost_group)
        
        self.cost_preview = QLabel("Sélectionnez un véhicule pour voir l'aperçu")
        self.cost_preview.setStyleSheet("font-size: 14px; padding: 10px; background-color: #f8fafc; border-radius: 8px;")
        cost_layout.addWidget(self.cost_preview)
        
        layout.addWidget(cost_group)
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
        
        self.create_btn = QPushButton("  Créer la location")
        self.create_btn.setIcon(get_icon("check", "#ffffff", 18))
        self.create_btn.setFixedHeight(40)
        self.create_btn.setMinimumWidth(160)
        self.create_btn.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #16a34a;
            }
            QPushButton:disabled {
                background-color: #94a3b8;
            }
        """)
        self.create_btn.clicked.connect(self.create_rental)
        self.create_btn.setEnabled(False)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(self.create_btn)
        
        main_layout.addWidget(buttons_widget)
    
    def on_start_date_changed(self):
        """Appelé quand la date de début change."""
        start = self.start_date_edit.date()
        self.end_date_edit.setMinimumDate(start)  # Permettre même jour
        if self.end_date_edit.date() < start:
            self.end_date_edit.setDate(start)
        self.update_available_vehicles()
    
    def update_available_vehicles(self):
        """Met à jour la liste des véhicules disponibles."""
        self.vehicle_combo.clear()
        
        customer_id = self.customer_combo.currentData()
        if not customer_id:
            self.vehicle_combo.addItem("-- Sélectionner d'abord un client --", None)
            return
        
        customer = self.system.get_customer(customer_id)
        if not customer:
            return
        
        start_qdate = self.start_date_edit.date()
        end_qdate = self.end_date_edit.date()
        start = date(start_qdate.year(), start_qdate.month(), start_qdate.day())
        end = date(end_qdate.year(), end_qdate.month(), end_qdate.day())
        
        available = self.system.get_available_vehicles(start_date=start, end_date=end)
        
        self.vehicle_combo.addItem("-- Sélectionner un véhicule --", None)
        
        for vehicle in available:
            # Vérifier si le client peut louer ce véhicule
            can_rent, reason = customer.can_rent_vehicle(
                vehicle.get_required_license(),
                vehicle.get_minimum_driver_age()
            )
            
            if can_rent:
                self.vehicle_combo.addItem(
                    f"{vehicle.get_vehicle_type()} - {vehicle.brand} {vehicle.model} ({vehicle.daily_rate:.2f}€/jour)",
                    vehicle.id
                )
        
        if self.vehicle_combo.count() == 1:
            self.vehicle_combo.clear()
            self.vehicle_combo.addItem("-- Aucun véhicule disponible pour ce client --", None)
    
    def update_cost_preview(self):
        """Met à jour l'aperçu du coût."""
        vehicle_id = self.vehicle_combo.currentData()
        customer_id = self.customer_combo.currentData()
        
        if not vehicle_id or not customer_id:
            self.cost_preview.setText("Sélectionnez un véhicule pour voir l'aperçu")
            self.create_btn.setEnabled(False)
            return
        
        vehicle = self.system.get_vehicle(vehicle_id)
        customer = self.system.get_customer(customer_id)
        
        if not vehicle or not customer:
            self.cost_preview.setText("Erreur: véhicule ou client non trouvé")
            self.create_btn.setEnabled(False)
            return
        
        start_qdate = self.start_date_edit.date()
        end_qdate = self.end_date_edit.date()
        
        days = start_qdate.daysTo(end_qdate) + 1
        base_cost = vehicle.calculate_rental_cost(days)
        
        discount = customer.get_loyalty_discount()
        discount_amount = base_cost * discount
        final_cost = base_cost - discount_amount
        
        preview_text = f"""
        <b>Durée:</b> {days} jours<br>
        <b>Tarif journalier:</b> {vehicle.daily_rate:.2f}€<br>
        <b>Coût de base:</b> {base_cost:.2f}€<br>
        """
        
        if discount > 0:
            preview_text += f"""
            <b>Réduction fidélité ({discount*100:.0f}%):</b> -{discount_amount:.2f}€<br>
            """
        
        preview_text += f"""<br><b style="font-size: 16px;">Total: {final_cost:.2f}€</b>"""
        
        self.cost_preview.setText(preview_text)
        self.create_btn.setEnabled(True)
    
    def create_rental(self):
        """Crée la location."""
        customer_id = self.customer_combo.currentData()
        vehicle_id = self.vehicle_combo.currentData()
        
        start_qdate = self.start_date_edit.date()
        end_qdate = self.end_date_edit.date()
        start = date(start_qdate.year(), start_qdate.month(), start_qdate.day())
        end = date(end_qdate.year(), end_qdate.month(), end_qdate.day())
        
        rental, message = self.system.create_rental(customer_id, vehicle_id, start, end)
        
        if rental:
            rental.notes = self.notes_edit.toPlainText()
            self.rental = rental
            self.accept()
        else:
            QMessageBox.warning(self, "Erreur", message)


class EditRentalDialog(QDialog):
    """Dialogue pour modifier une location."""
    
    def __init__(self, parent, system: CarRentalSystem, rental: Rental):
        super().__init__(parent)
        self.system = system
        self.rental = rental
        self.setWindowTitle("Modifier la location")
        self.setMinimumWidth(500)
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface du dialogue."""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Titre
        title = QLabel(f"Modifier la location {self.rental.id}")
        title.setStyleSheet("font-size: 20px; font-weight: 700; color: #1e293b;")
        layout.addWidget(title)
        
        # Informations non modifiables
        info_frame = QFrame()
        info_frame.setStyleSheet("background-color: #f1f5f9; border-radius: 8px; padding: 12px;")
        info_layout = QVBoxLayout(info_frame)
        
        customer = self.system.get_customer(self.rental.customer_id)
        vehicle = self.system.get_vehicle(self.rental.vehicle_id)
        
        info_layout.addWidget(QLabel(f"<b>Client:</b> {customer.full_name if customer else 'Inconnu'}"))
        info_layout.addWidget(QLabel(f"<b>Véhicule:</b> {vehicle.brand} {vehicle.model} ({vehicle.license_plate})" if vehicle else 'Inconnu'))
        info_layout.addWidget(QLabel(f"<b>Statut:</b> {self.rental.status.value}"))
        
        layout.addWidget(info_frame)
        
        # Dates modifiables (prolongation)
        dates_group = QGroupBox("Dates de location")
        dates_layout = QFormLayout(dates_group)
        
        self.start_label = QLabel(str(self.rental.start_date))
        dates_layout.addRow("Date de début:", self.start_label)
        
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        start_qdate = QDate(self.rental.start_date.year, self.rental.start_date.month, self.rental.start_date.day)
        end_qdate = QDate(self.rental.end_date.year, self.rental.end_date.month, self.rental.end_date.day)
        self.end_date_edit.setDate(end_qdate)
        self.end_date_edit.setMinimumDate(start_qdate.addDays(1))
        self.end_date_edit.dateChanged.connect(self.update_cost)
        dates_layout.addRow("Date de fin:", self.end_date_edit)
        
        layout.addWidget(dates_group)
        
        # Notes
        notes_group = QGroupBox("Notes")
        notes_layout = QVBoxLayout(notes_group)
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlainText(self.rental.notes)
        self.notes_edit.setMaximumHeight(100)
        notes_layout.addWidget(self.notes_edit)
        layout.addWidget(notes_group)
        
        # Aperçu du coût
        self.cost_label = QLabel()
        self.cost_label.setStyleSheet("font-size: 14px; padding: 12px; background-color: #dbeafe; border-radius: 8px;")
        layout.addWidget(self.cost_label)
        self.update_cost()
        
        # Boutons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.save_changes)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def update_cost(self):
        """Met à jour l'affichage du coût."""
        end_qdate = self.end_date_edit.date()
        new_end = date(end_qdate.year(), end_qdate.month(), end_qdate.day())
        
        days = (new_end - self.rental.start_date).days + 1
        vehicle = self.system.get_vehicle(self.rental.vehicle_id)
        
        if vehicle:
            cost = vehicle.calculate_rental_cost(days)
            self.cost_label.setText(f"<b>Durée:</b> {days} jours | <b>Coût estimé:</b> {cost:.2f}€")
    
    def save_changes(self):
        """Sauvegarde les modifications."""
        end_qdate = self.end_date_edit.date()
        new_end = date(end_qdate.year(), end_qdate.month(), end_qdate.day())
        
        if new_end != self.rental.end_date:
            if new_end > self.rental.end_date:
                success = self.rental.extend_rental(new_end)
                if not success:
                    QMessageBox.warning(self, "Erreur", "Impossible de prolonger cette location.")
                    return
            else:
                self.rental.end_date = new_end
        
        self.rental.notes = self.notes_edit.toPlainText()
        self.accept()


class RentalDetailsDialog(QDialog):
    """Dialogue pour afficher les détails d'une location."""
    
    def __init__(self, parent, system: CarRentalSystem, rental: Rental):
        super().__init__(parent)
        self.system = system
        self.rental = rental
        self.setWindowTitle(f"Détails de la location {rental.id}")
        self.setMinimumSize(550, 500)
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface du dialogue."""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # En-tête avec statut
        header = QHBoxLayout()
        title = QLabel(f"Location #{self.rental.id}")
        title.setStyleSheet("font-size: 22px; font-weight: 700; color: #0f172a;")
        
        status_badge = QLabel(self.rental.status.value.upper())
        status_colors = {
            RentalStatus.RESERVED: "#3b82f6",
            RentalStatus.ACTIVE: "#22c55e",
            RentalStatus.COMPLETED: "#64748b",
            RentalStatus.CANCELLED: "#ef4444"
        }
        color = status_colors.get(self.rental.status, "#64748b")
        status_badge.setStyleSheet(f"""
            background-color: {color};
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 12px;
        """)
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(status_badge)
        layout.addLayout(header)
        
        # Scroll pour le contenu
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(16)
        
        # Section Client
        customer = self.system.get_customer(self.rental.customer_id)
        client_group = QGroupBox("Client")
        client_layout = QFormLayout(client_group)
        if customer:
            client_layout.addRow("Nom:", QLabel(customer.full_name))
            client_layout.addRow("Email:", QLabel(customer.email or "-"))
            client_layout.addRow("Telephone:", QLabel(customer.phone or "-"))
            client_layout.addRow("Fidelite:", QLabel("[FIDELE] Client fidele" if customer.is_loyal_customer() else "Standard"))
        content_layout.addWidget(client_group)
        
        # Section Vehicule
        vehicle = self.system.get_vehicle(self.rental.vehicle_id)
        vehicle_group = QGroupBox("Vehicule")
        vehicle_layout = QFormLayout(vehicle_group)
        if vehicle:
            vehicle_layout.addRow("Type:", QLabel(vehicle.get_vehicle_type()))
            vehicle_layout.addRow("Marque/Modèle:", QLabel(f"{vehicle.brand} {vehicle.model}"))
            vehicle_layout.addRow("Immatriculation:", QLabel(vehicle.license_plate))
            vehicle_layout.addRow("Catégorie:", QLabel(vehicle.category.value))
            vehicle_layout.addRow("Tarif journalier:", QLabel(f"{vehicle.daily_rate:.2f}€"))
        content_layout.addWidget(vehicle_group)
        
        # Section Dates
        dates_group = QGroupBox("Periode")
        dates_layout = QFormLayout(dates_group)
        dates_layout.addRow("Date de debut:", QLabel(str(self.rental.start_date)))
        dates_layout.addRow("Date de fin prevue:", QLabel(str(self.rental.end_date)))
        dates_layout.addRow("Duree prevue:", QLabel(f"{self.rental.planned_duration} jours"))
        
        if self.rental.actual_return_date:
            dates_layout.addRow("Date de retour:", QLabel(str(self.rental.actual_return_date)))
            dates_layout.addRow("Duree effective:", QLabel(f"{self.rental.actual_duration} jours"))
            if self.rental.days_late > 0:
                late_label = QLabel(f"{self.rental.days_late} jours de retard")
                late_label.setStyleSheet("color: #ef4444; font-weight: 600;")
                dates_layout.addRow("Retard:", late_label)
        elif self.rental.status == RentalStatus.ACTIVE:
            remaining = self.rental.days_remaining()
            if remaining >= 0:
                dates_layout.addRow("Jours restants:", QLabel(f"{remaining} jours"))
            else:
                late_label = QLabel(f"{-remaining} jours de retard")
                late_label.setStyleSheet("color: #ef4444; font-weight: 600;")
                dates_layout.addRow("Retard:", late_label)
        content_layout.addWidget(dates_group)
        
        # Section Kilométrage
        km_group = QGroupBox("Kilometrage")
        km_layout = QFormLayout(km_group)
        km_layout.addRow("Kilométrage départ:", QLabel(f"{self.rental.start_mileage:.0f} km"))
        if self.rental.end_mileage:
            km_layout.addRow("Kilométrage retour:", QLabel(f"{self.rental.end_mileage:.0f} km"))
            km_layout.addRow("Distance parcourue:", QLabel(f"{self.rental.distance_traveled:.0f} km"))
        content_layout.addWidget(km_group)
        
        # Section Cout
        cost_group = QGroupBox("Facturation")
        cost_layout = QFormLayout(cost_group)
        cost_layout.addRow("Cout de base:", QLabel(f"{self.rental.calculate_base_cost():.2f}EUR"))
        if self.rental.discount_applied > 0:
            cost_layout.addRow("Reduction:", QLabel(f"-{self.rental.discount_applied * 100:.0f}%"))
        if self.rental.penalty > 0:
            penalty_label = QLabel(f"+{self.rental.penalty:.2f}EUR")
            penalty_label.setStyleSheet("color: #ef4444;")
            cost_layout.addRow("Penalites:", penalty_label)
        
        total_label = QLabel(f"{self.rental.total_cost:.2f}EUR")
        total_label.setStyleSheet("font-size: 18px; font-weight: 700; color: #2563eb;")
        cost_layout.addRow("Total:", total_label)
        content_layout.addWidget(cost_group)
        
        # Notes
        if self.rental.notes:
            notes_group = QGroupBox("Notes")
            notes_layout = QVBoxLayout(notes_group)
            notes_label = QLabel(self.rental.notes)
            notes_label.setWordWrap(True)
            notes_layout.addWidget(notes_label)
            content_layout.addWidget(notes_group)
        
        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        # Bouton fermer
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)


class CompleteRentalDialog(QDialog):
    """Dialogue pour terminer une location."""
    
    def __init__(self, parent, system: CarRentalSystem, rental: Rental):
        super().__init__(parent)
        self.system = system
        self.rental = rental
        self.setWindowTitle("Terminer la location")
        self.setMinimumWidth(500)
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface du dialogue."""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Titre
        title = QLabel("Terminer la location")
        title.setStyleSheet("font-size: 20px; font-weight: 700; color: #1e293b;")
        layout.addWidget(title)
        
        # Informations
        vehicle = self.system.get_vehicle(self.rental.vehicle_id)
        customer = self.system.get_customer(self.rental.customer_id)
        
        vehicle_info = f"{vehicle.brand} {vehicle.model}" if vehicle else "Inconnu"
        customer_info = customer.full_name if customer else "Inconnu"
        
        info_text = f"""
        <b>Client:</b> {customer_info}<br>
        <b>Véhicule:</b> {vehicle_info}<br>
        <b>Début:</b> {self.rental.start_date}<br>
        <b>Fin prévue:</b> {self.rental.end_date}
        """
        
        info_label = QLabel(info_text)
        info_label.setStyleSheet("background-color: #f8fafc; padding: 12px; border-radius: 8px;")
        layout.addWidget(info_label)
        
        # Date de retour
        form = QFormLayout()
        
        self.return_date_edit = QDateEdit()
        self.return_date_edit.setCalendarPopup(True)
        self.return_date_edit.setDate(QDate.currentDate())
        self.return_date_edit.dateChanged.connect(self.update_cost)
        form.addRow("Date de retour:", self.return_date_edit)
        
        self.mileage_spin = QDoubleSpinBox()
        self.mileage_spin.setRange(0, 999999)
        self.mileage_spin.setValue(self.rental.start_mileage)
        self.mileage_spin.setSuffix(" km")
        form.addRow("Kilométrage retour:", self.mileage_spin)
        
        layout.addLayout(form)
        
        # Coût
        self.cost_label = QLabel()
        self.cost_label.setStyleSheet("font-size: 16px; font-weight: 600; padding: 12px; background-color: #dbeafe; border-radius: 8px;")
        layout.addWidget(self.cost_label)
        
        self.update_cost()
        
        # Boutons
        buttons_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.setProperty("secondary", True)
        cancel_btn.clicked.connect(self.reject)
        
        complete_btn = QPushButton("  Terminer la location")
        complete_btn.setIcon(get_icon("check", "#ffffff", 18))
        complete_btn.setProperty("success", True)
        complete_btn.clicked.connect(self.complete_rental)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(complete_btn)
        
        layout.addLayout(buttons_layout)
    
    def update_cost(self):
        """Met à jour l'affichage du coût."""
        return_qdate = self.return_date_edit.date()
        return_date = date(return_qdate.year(), return_qdate.month(), return_qdate.day())
        
        # Calcul approximatif
        base_cost = self.rental.calculate_base_cost()
        penalty = 0
        
        if return_date > self.rental.end_date:
            days_late = (return_date - self.rental.end_date).days
            penalty = days_late * Rental.LATE_RETURN_PENALTY_PER_DAY
            self.cost_label.setStyleSheet("font-size: 16px; font-weight: 600; padding: 12px; background-color: #fee2e2; border-radius: 8px;")
            self.cost_label.setText(f"Retard de {days_late} jours\nCout total: {base_cost + penalty:.2f}EUR (dont {penalty:.2f}EUR de penalites)")
        else:
            self.cost_label.setStyleSheet("font-size: 16px; font-weight: 600; padding: 12px; background-color: #dcfce7; border-radius: 8px;")
            self.cost_label.setText(f"Retour dans les temps\nCout total: {base_cost:.2f}EUR")
    
    def complete_rental(self):
        """Termine la location."""
        return_qdate = self.return_date_edit.date()
        return_date = date(return_qdate.year(), return_qdate.month(), return_qdate.day())
        mileage = self.mileage_spin.value()
        
        cost, message = self.system.complete_rental(self.rental.id, return_date, mileage)
        
        if cost is not None:
            self.accept()
        else:
            QMessageBox.warning(self, "Erreur", message)


class RentalsPage(QWidget):
    """Page de gestion des locations."""
    
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
        title = QLabel("Gestion des locations")
        title.setStyleSheet("font-size: 24px; font-weight: 700; color: #0f172a;")
        subtitle = QLabel("Créez, gérez et suivez toutes les locations de véhicules")
        subtitle.setStyleSheet("color: #64748b;")
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        # Bouton principal pour creer une location
        add_btn = QPushButton("  Nouvelle location")
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
        add_btn.clicked.connect(self.new_rental)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addWidget(add_btn)
        
        layout.addLayout(header_layout)
        
        # Statistiques rapides
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(12)
        
        self.stat_active = self.create_stat_card("play", "En cours", "0", "#22c55e")
        self.stat_reserved = self.create_stat_card("calendar", "Reservees", "0", "#3b82f6")
        self.stat_overdue = self.create_stat_card("warning", "En retard", "0", "#ef4444")
        self.stat_completed = self.create_stat_card("check", "Terminees", "0", "#64748b")
        
        stats_layout.addWidget(self.stat_active)
        stats_layout.addWidget(self.stat_reserved)
        stats_layout.addWidget(self.stat_overdue)
        stats_layout.addWidget(self.stat_completed)
        
        layout.addLayout(stats_layout)
        
        # Filtres
        filter_frame = QFrame()
        filter_frame.setStyleSheet("background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px;")
        filter_layout = QHBoxLayout(filter_frame)
        
        filter_layout.addWidget(QLabel("Filtrer:"))
        
        self.status_filter = QComboBox()
        self.status_filter.addItem("Tous les statuts", None)
        self.status_filter.addItem("En cours", RentalStatus.ACTIVE)
        self.status_filter.addItem("Reservees", RentalStatus.RESERVED)
        self.status_filter.addItem("Terminees", RentalStatus.COMPLETED)
        self.status_filter.addItem("Annulees", RentalStatus.CANCELLED)
        self.status_filter.currentIndexChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.status_filter)
        
        filter_layout.addWidget(QLabel("Client:"))
        self.customer_filter = QComboBox()
        self.customer_filter.addItem("Tous les clients", None)
        self.customer_filter.currentIndexChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.customer_filter)
        
        filter_layout.addWidget(QLabel("Véhicule:"))
        self.vehicle_filter = QComboBox()
        self.vehicle_filter.addItem("Tous les véhicules", None)
        self.vehicle_filter.currentIndexChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.vehicle_filter)
        
        self.overdue_only = QCheckBox("En retard uniquement")
        self.overdue_only.stateChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.overdue_only)
        
        filter_layout.addStretch()
        
        refresh_btn = QPushButton()
        refresh_btn.setIcon(get_icon("refresh", "#64748b", 18))
        refresh_btn.setFixedSize(36, 36)
        refresh_btn.setStyleSheet("QPushButton { background-color: #f1f5f9; border-radius: 6px; } QPushButton:hover { background-color: #e2e8f0; }")
        refresh_btn.setToolTip("Actualiser")
        refresh_btn.clicked.connect(self.refresh_data)
        filter_layout.addWidget(refresh_btn)
        
        layout.addWidget(filter_frame)
        
        # Tableau des locations
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "ID", "Client", "Véhicule", "Début", "Fin", 
            "Statut", "Coût", "Jours restants", "Notes", "Actions"
        ])
        
        header = self.table.horizontalHeader()
        if header:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # ID
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Client
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Véhicule
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)  # Début
            header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)  # Fin
            header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)  # Statut
            header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)  # Coût
            header.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)  # Jours
            header.setSectionResizeMode(8, QHeaderView.ResizeMode.Fixed)  # Notes
            header.setSectionResizeMode(9, QHeaderView.ResizeMode.Fixed)  # Actions
        
        # Largeurs fixes des colonnes
        self.table.setColumnWidth(0, 90)   # ID
        self.table.setColumnWidth(3, 100)  # Début
        self.table.setColumnWidth(4, 100)  # Fin
        self.table.setColumnWidth(5, 100)  # Statut
        self.table.setColumnWidth(6, 80)   # Coût
        self.table.setColumnWidth(7, 90)   # Jours
        self.table.setColumnWidth(8, 50)   # Notes
        self.table.setColumnWidth(9, 180)  # Actions
        
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        v_header = self.table.verticalHeader()
        if v_header:
            v_header.setDefaultSectionSize(45)
            v_header.setMinimumSectionSize(45)
            v_header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.table.doubleClicked.connect(self.show_rental_details)
        
        layout.addWidget(self.table)
    
    def create_stat_card(self, icon_name: str, label: str, value: str, color: str) -> QFrame:
        """Crée une carte de statistique."""
        card = QFrame()
        card.setObjectName("statCard")
        card.setStyleSheet(f"""
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
        
        layout = QHBoxLayout(card)
        layout.setContentsMargins(12, 12, 12, 12)
        
        icon_label = QLabel()
        icon_label.setPixmap(get_icon(icon_name, color, 28).pixmap(28, 28))
        layout.addWidget(icon_label)
        
        text_layout = QVBoxLayout()
        value_label = QLabel(value)
        value_label.setStyleSheet(f"font-size: 20px; font-weight: 700; color: {color}; background: transparent; border: none;")
        value_label.setObjectName("value")
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet("color: #64748b; font-size: 12px; background: transparent; border: none;")
        
        text_layout.addWidget(value_label)
        text_layout.addWidget(label_widget)
        layout.addLayout(text_layout)
        layout.addStretch()
        
        return card
    
    def update_stat_card(self, card: QFrame, value: str):
        """Met à jour la valeur d'une carte de statistique."""
        value_label = card.findChild(QLabel, "value")
        if value_label:
            value_label.setText(value)
    
    def refresh_data(self):
        """Rafraîchit toutes les données."""
        self.update_filters()
        self.update_stats()
        self.apply_filters()
    
    def update_filters(self):
        """Met à jour les listes des filtres."""
        # Sauvegarder les sélections
        current_customer = self.customer_filter.currentData()
        current_vehicle = self.vehicle_filter.currentData()
        
        # Clients
        self.customer_filter.clear()
        self.customer_filter.addItem("Tous les clients", None)
        for customer in self.system.get_all_customers():
            self.customer_filter.addItem(customer.full_name, customer.id)
        
        # Restaurer la sélection
        if current_customer:
            idx = self.customer_filter.findData(current_customer)
            if idx >= 0:
                self.customer_filter.setCurrentIndex(idx)
        
        # Véhicules
        self.vehicle_filter.clear()
        self.vehicle_filter.addItem("Tous les véhicules", None)
        for vehicle in self.system.get_all_vehicles():
            self.vehicle_filter.addItem(f"{vehicle.brand} {vehicle.model}", vehicle.id)
        
        # Restaurer la sélection
        if current_vehicle:
            idx = self.vehicle_filter.findData(current_vehicle)
            if idx >= 0:
                self.vehicle_filter.setCurrentIndex(idx)
    
    def update_stats(self):
        """Met à jour les statistiques."""
        rentals = self.system.get_all_rentals()
        
        active = len([r for r in rentals if r.status == RentalStatus.ACTIVE])
        reserved = len([r for r in rentals if r.status == RentalStatus.RESERVED])
        overdue = len([r for r in rentals if r.is_overdue()])
        completed = len([r for r in rentals if r.status == RentalStatus.COMPLETED])
        
        self.update_stat_card(self.stat_active, str(active))
        self.update_stat_card(self.stat_reserved, str(reserved))
        self.update_stat_card(self.stat_overdue, str(overdue))
        self.update_stat_card(self.stat_completed, str(completed))
    
    def apply_filters(self):
        """Applique les filtres et affiche les résultats."""
        rentals = self.system.get_all_rentals()
        
        # Filtre par statut
        status_filter = self.status_filter.currentData()
        if status_filter:
            rentals = [r for r in rentals if r.status == status_filter]
        
        # Filtre par client
        customer_filter = self.customer_filter.currentData()
        if customer_filter:
            rentals = [r for r in rentals if r.customer_id == customer_filter]
        
        # Filtre par véhicule
        vehicle_filter = self.vehicle_filter.currentData()
        if vehicle_filter:
            rentals = [r for r in rentals if r.vehicle_id == vehicle_filter]
        
        # Filtre en retard
        if self.overdue_only.isChecked():
            rentals = [r for r in rentals if r.is_overdue()]
        
        # Tri: actives et réservées d'abord, puis par date
        rentals.sort(key=lambda r: (
            0 if r.status == RentalStatus.ACTIVE else (1 if r.status == RentalStatus.RESERVED else 2),
            r.start_date
        ))
        
        self.display_rentals(rentals)
    
    def display_rentals(self, rentals: list):
        """Affiche les locations dans le tableau."""
        self.table.setRowCount(len(rentals))
        
        for row, rental in enumerate(rentals):
            customer = self.system.get_customer(rental.customer_id)
            vehicle = self.system.get_vehicle(rental.vehicle_id)
            
            # ID
            id_item = QTableWidgetItem(rental.id)
            id_item.setData(Qt.ItemDataRole.UserRole, rental)
            self.table.setItem(row, 0, id_item)
            
            # Client
            self.table.setItem(row, 1, QTableWidgetItem(customer.full_name if customer else "Inconnu"))
            
            # Véhicule
            self.table.setItem(row, 2, QTableWidgetItem(f"{vehicle.brand} {vehicle.model}" if vehicle else "Inconnu"))
            
            # Dates
            self.table.setItem(row, 3, QTableWidgetItem(str(rental.start_date)))
            self.table.setItem(row, 4, QTableWidgetItem(str(rental.end_date)))
            
            # Statut avec badge
            status_widget = QWidget()
            status_layout = QHBoxLayout(status_widget)
            status_layout.setContentsMargins(2, 2, 2, 2)
            status_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            status_label = QLabel(rental.status.value)
            if rental.status == RentalStatus.ACTIVE:
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
            elif rental.status == RentalStatus.RESERVED:
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
            elif rental.status == RentalStatus.COMPLETED:
                status_label.setStyleSheet("""
                    QLabel {
                        background-color: #f1f5f9;
                        color: #64748b;
                        padding: 2px 8px;
                        border-radius: 10px;
                        font-weight: 600;
                        font-size: 11px;
                        border: 1px solid #e2e8f0;
                    }
                """)
            else:
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
            status_layout.addWidget(status_label)
            self.table.setCellWidget(row, 5, status_widget)
            
            # Coût
            self.table.setItem(row, 6, QTableWidgetItem(f"{rental.total_cost:.2f}€"))
            
            # Jours restants / Retard
            if rental.status == RentalStatus.ACTIVE:
                if rental.is_overdue():
                    late_item = QTableWidgetItem(f"-{abs(rental.days_remaining())} j")
                    late_item.setForeground(Qt.GlobalColor.red)
                else:
                    late_item = QTableWidgetItem(f"{rental.days_remaining()} j")
                    late_item.setForeground(Qt.GlobalColor.darkGreen)
            elif rental.status == RentalStatus.RESERVED:
                days_until = (rental.start_date - date.today()).days
                late_item = QTableWidgetItem(f"dans {days_until} j")
                late_item.setForeground(Qt.GlobalColor.darkBlue)
            else:
                late_item = QTableWidgetItem("-")
            self.table.setItem(row, 7, late_item)
            
            # Notes
            notes_item = QTableWidgetItem("" if rental.notes else "")
            if rental.notes:
                notes_item.setIcon(get_icon("documents", "#64748b", 16))
            notes_item.setToolTip(rental.notes if rental.notes else "Pas de notes")
            self.table.setItem(row, 8, notes_item)
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4, 0, 4, 0)
            actions_layout.setSpacing(4)
            actions_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Bouton details
            detail_btn = create_action_button(
                "eye", "Voir les détails",
                icon_color="#64748b",
                bg_color="#f1f5f9",
                hover_color="#e2e8f0",
                border_color="#e2e8f0",
                size=26
            )
            detail_btn.clicked.connect(lambda checked, r=rental: self.show_rental_details_for(r))
            actions_layout.addWidget(detail_btn)
            
            if rental.status == RentalStatus.RESERVED:
                # Demarrer
                start_btn = create_action_button(
                    "play", "Démarrer la location",
                    icon_color="#ffffff",
                    bg_color="#22c55e",
                    hover_color="#16a34a",
                    border_color="#16a34a",
                    size=26
                )
                start_btn.clicked.connect(lambda checked, r=rental: self.start_rental(r))
                actions_layout.addWidget(start_btn)
                
                # Modifier
                edit_btn = create_action_button(
                    "edit", "Modifier",
                    icon_color="#3b82f6",
                    bg_color="#eff6ff",
                    hover_color="#dbeafe",
                    border_color="#bfdbfe",
                    size=26
                )
                edit_btn.clicked.connect(lambda checked, r=rental: self.edit_rental(r))
                actions_layout.addWidget(edit_btn)
            
            if rental.status == RentalStatus.ACTIVE:
                # Terminer
                complete_btn = create_action_button(
                    "check", "Terminer la location",
                    icon_color="#ffffff",
                    bg_color="#22c55e",
                    hover_color="#16a34a",
                    border_color="#16a34a",
                    size=26
                )
                complete_btn.clicked.connect(lambda checked, r=rental: self.complete_rental(r))
                actions_layout.addWidget(complete_btn)
                
                # Prolonger
                extend_btn = create_action_button(
                    "calendar", "Prolonger",
                    icon_color="#8b5cf6",
                    bg_color="#f5f3ff",
                    hover_color="#ede9fe",
                    border_color="#ddd6fe",
                    size=26
                )
                extend_btn.clicked.connect(lambda checked, r=rental: self.edit_rental(r))
                actions_layout.addWidget(extend_btn)
            
            if rental.status in [RentalStatus.ACTIVE, RentalStatus.RESERVED]:
                # Annuler
                cancel_btn = create_action_button(
                    "cancel", "Annuler",
                    icon_color="#ffffff",
                    bg_color="#ef4444",
                    hover_color="#dc2626",
                    border_color="#dc2626",
                    size=26
                )
                cancel_btn.clicked.connect(lambda checked, r=rental: self.cancel_rental(r))
                actions_layout.addWidget(cancel_btn)
            
            self.table.setCellWidget(row, 9, actions_widget)
    
    def show_rental_details(self, index):
        """Affiche les détails d'une location (double-clic)."""
        item = self.table.item(index.row(), 0)
        if item:
            rental = item.data(Qt.ItemDataRole.UserRole)
            if rental:
                self.show_rental_details_for(rental)
    
    def show_rental_details_for(self, rental: Rental):
        """Affiche le dialogue des détails."""
        dialog = RentalDetailsDialog(self, self.system, rental)
        dialog.exec()
    
    def new_rental(self):
        """Ouvre le dialogue pour créer une location."""
        if not self.system.get_all_customers():
            QMessageBox.warning(self, "Attention", "Ajoutez d'abord des clients!")
            return
        
        if not self.system.get_available_vehicles():
            QMessageBox.warning(self, "Attention", "Aucun véhicule disponible!")
            return
        
        dialog = NewRentalDialog(self, self.system)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_data()
            self.data_changed.emit()
            QMessageBox.information(
                self, "Succès", 
                f"Location créée avec succès!\nID: {dialog.rental.id}\nCoût estimé: {dialog.rental.total_cost:.2f}€"
            )
    
    def edit_rental(self, rental: Rental):
        """Ouvre le dialogue pour modifier une location."""
        dialog = EditRentalDialog(self, self.system, rental)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_data()
            self.data_changed.emit()
            QMessageBox.information(self, "Succès", "Location modifiée avec succès!")
    
    def start_rental(self, rental: Rental):
        """Démarre une location."""
        success, message = self.system.start_rental(rental.id)
        if success:
            self.refresh_data()
            self.data_changed.emit()
            QMessageBox.information(self, "Succès", "Location démarrée!")
        else:
            QMessageBox.warning(self, "Erreur", message)
    
    def complete_rental(self, rental: Rental):
        """Termine une location."""
        dialog = CompleteRentalDialog(self, self.system, rental)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_data()
            self.data_changed.emit()
            QMessageBox.information(self, "Succès", "Location terminée avec succès!")
    
    def cancel_rental(self, rental: Rental):
        """Annule une location."""
        reply = QMessageBox.question(
            self, "Confirmation",
            "Voulez-vous vraiment annuler cette location?\nDes frais d'annulation peuvent s'appliquer selon le délai.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            fee, message = self.system.cancel_rental(rental.id)
            self.refresh_data()
            self.data_changed.emit()
            QMessageBox.information(self, "Location annulée", message)
