"""
Page de gestion des véhicules.
"""

from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QDialog, QFormLayout, QLineEdit, QComboBox,
    QSpinBox, QDoubleSpinBox, QCheckBox, QMessageBox,
    QScrollArea, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSignal

from car_rental_system import CarRentalSystem
from models.vehicle import Vehicle, Car, Truck, Motorcycle, VehicleCategory, VehicleState
from gui.icons import get_icon, create_action_button


class VehicleDialog(QDialog):
    """Dialogue pour ajouter/modifier un véhicule."""
    
    def __init__(self, parent: Optional[QWidget] = None, vehicle: Optional[Vehicle] = None):
        super().__init__(parent)
        self.vehicle = vehicle
        self.setWindowTitle("Modifier le véhicule" if vehicle else "Ajouter un véhicule")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        self.setMaximumHeight(700)
        self.setup_ui()
        
        if vehicle:
            self.load_vehicle_data()
    
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
        title = QLabel("Modifier le véhicule" if self.vehicle else "Nouveau véhicule")
        title.setStyleSheet("font-size: 20px; font-weight: 700; color: #1e293b;")
        layout.addWidget(title)
        
        # Type de véhicule
        type_group = QGroupBox("Type de véhicule")
        type_group_layout = QHBoxLayout(type_group)
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Voiture", "Camion", "Moto"])
        self.type_combo.currentTextChanged.connect(self.on_type_changed)
        
        if self.vehicle:
            self.type_combo.setEnabled(False)
        
        type_group_layout.addWidget(self.type_combo)
        layout.addWidget(type_group)
        
        # Formulaire principal
        info_group = QGroupBox("Informations générales")
        form = QFormLayout(info_group)
        form.setSpacing(12)
        
        self.brand_edit = QLineEdit()
        self.brand_edit.setPlaceholderText("Ex: Renault, BMW, Honda...")
        form.addRow("Marque:", self.brand_edit)
        
        self.model_edit = QLineEdit()
        self.model_edit.setPlaceholderText("Ex: Clio, Série 3, CB500...")
        form.addRow("Modèle:", self.model_edit)
        
        self.year_spin = QSpinBox()
        self.year_spin.setRange(2000, 2030)
        self.year_spin.setValue(2024)
        form.addRow("Année:", self.year_spin)
        
        self.plate_edit = QLineEdit()
        self.plate_edit.setPlaceholderText("Ex: AB-123-CD")
        form.addRow("Immatriculation:", self.plate_edit)
        
        self.category_combo = QComboBox()
        for cat in VehicleCategory:
            self.category_combo.addItem(cat.value, cat)
        form.addRow("Catégorie:", self.category_combo)
        
        self.rate_spin = QDoubleSpinBox()
        self.rate_spin.setRange(0, 9999)
        self.rate_spin.setValue(50)
        self.rate_spin.setSuffix(" €/jour")
        form.addRow("Tarif journalier:", self.rate_spin)
        
        self.mileage_spin = QDoubleSpinBox()
        self.mileage_spin.setRange(0, 999999)
        self.mileage_spin.setSuffix(" km")
        form.addRow("Kilométrage:", self.mileage_spin)
        
        layout.addWidget(info_group)
        
        # Champs spécifiques au type
        self.specific_group = QGroupBox("Caractéristiques spécifiques")
        self.specific_layout = QFormLayout(self.specific_group)
        self.specific_layout.setSpacing(12)
        layout.addWidget(self.specific_group)
        
        self.setup_specific_fields("Voiture")
        
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
        save_btn.clicked.connect(self.accept)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(save_btn)
        
        main_layout.addWidget(buttons_widget)
    
    def setup_specific_fields(self, vehicle_type: str):
        """Configure les champs spécifiques au type de véhicule."""
        # Nettoyer les anciens champs
        while self.specific_layout.count():
            item = self.specific_layout.takeAt(0)
            widget = item.widget() if item else None
            if widget:
                widget.deleteLater()
        
        if vehicle_type == "Voiture":
            self.doors_spin = QSpinBox()
            self.doors_spin.setRange(2, 5)
            self.doors_spin.setValue(5)
            self.specific_layout.addRow("Nombre de portes:", self.doors_spin)
            
            self.seats_spin = QSpinBox()
            self.seats_spin.setRange(2, 9)
            self.seats_spin.setValue(5)
            self.specific_layout.addRow("Nombre de places:", self.seats_spin)
            
            self.fuel_combo = QComboBox()
            self.fuel_combo.addItems(["essence", "diesel", "électrique", "hybride"])
            self.specific_layout.addRow("Carburant:", self.fuel_combo)
            
            self.transmission_combo = QComboBox()
            self.transmission_combo.addItems(["manuelle", "automatique"])
            self.specific_layout.addRow("Transmission:", self.transmission_combo)
            
        elif vehicle_type == "Camion":
            self.cargo_spin = QDoubleSpinBox()
            self.cargo_spin.setRange(1, 100)
            self.cargo_spin.setValue(12)
            self.cargo_spin.setSuffix(" m³")
            self.specific_layout.addRow("Capacité cargo:", self.cargo_spin)
            
            self.weight_spin = QSpinBox()
            self.weight_spin.setRange(500, 50000)
            self.weight_spin.setValue(3000)
            self.weight_spin.setSuffix(" kg")
            self.specific_layout.addRow("Poids max:", self.weight_spin)
            
            self.tail_lift_check = QCheckBox("Hayon élévateur")
            self.specific_layout.addRow("", self.tail_lift_check)
            
        elif vehicle_type == "Moto":
            self.engine_spin = QSpinBox()
            self.engine_spin.setRange(50, 2000)
            self.engine_spin.setValue(125)
            self.engine_spin.setSuffix(" cm³")
            self.specific_layout.addRow("Cylindrée:", self.engine_spin)
            
            self.moto_type_combo = QComboBox()
            self.moto_type_combo.addItems(["standard", "sport", "touring", "roadster", "trail"])
            self.specific_layout.addRow("Type de moto:", self.moto_type_combo)
    
    def on_type_changed(self, vehicle_type: str):
        """Appelé quand le type de véhicule change."""
        self.setup_specific_fields(vehicle_type)
    
    def load_vehicle_data(self):
        """Charge les données du véhicule existant."""
        v = self.vehicle
        if not v:
            return
        
        if isinstance(v, Car):
            self.type_combo.setCurrentText("Voiture")
        elif isinstance(v, Truck):
            self.type_combo.setCurrentText("Camion")
        elif isinstance(v, Motorcycle):
            self.type_combo.setCurrentText("Moto")
        
        self.brand_edit.setText(v.brand)
        self.model_edit.setText(v.model)
        self.year_spin.setValue(v.year)
        self.plate_edit.setText(v.license_plate)
        
        # Trouver l'index de la catégorie
        for i in range(self.category_combo.count()):
            if self.category_combo.itemData(i) == v.category:
                self.category_combo.setCurrentIndex(i)
                break
        
        self.rate_spin.setValue(v.daily_rate)
        self.mileage_spin.setValue(v.mileage)
        
        # Champs spécifiques
        if isinstance(v, Car):
            self.doors_spin.setValue(v.num_doors)
            self.seats_spin.setValue(v.num_seats)
            self.fuel_combo.setCurrentText(v.fuel_type)
            self.transmission_combo.setCurrentText(v.transmission)
        elif isinstance(v, Truck):
            self.cargo_spin.setValue(v.cargo_capacity)
            self.weight_spin.setValue(int(v.max_weight))
            self.tail_lift_check.setChecked(v.has_tail_lift)
        elif isinstance(v, Motorcycle):
            self.engine_spin.setValue(v.engine_size)
            self.moto_type_combo.setCurrentText(v.motorcycle_type)
    
    def get_vehicle(self) -> Optional[Vehicle]:
        """Crée et retourne le véhicule selon les données du formulaire."""
        vehicle_type = self.type_combo.currentText()
        category = self.category_combo.currentData()
        
        base_args = {
            'brand': self.brand_edit.text(),
            'model': self.model_edit.text(),
            'category': category,
            'daily_rate': self.rate_spin.value(),
            'year': self.year_spin.value(),
            'license_plate': self.plate_edit.text(),
            'mileage': self.mileage_spin.value(),
        }
        
        if self.vehicle:
            base_args['vehicle_id'] = self.vehicle.id
        
        if vehicle_type == "Voiture":
            return Car(
                **base_args,
                num_doors=self.doors_spin.value(),
                num_seats=self.seats_spin.value(),
                fuel_type=self.fuel_combo.currentText(),
                transmission=self.transmission_combo.currentText()
            )
        elif vehicle_type == "Camion":
            return Truck(
                **base_args,
                cargo_capacity=self.cargo_spin.value(),
                max_weight=self.weight_spin.value(),
                has_tail_lift=self.tail_lift_check.isChecked()
            )
        elif vehicle_type == "Moto":
            return Motorcycle(
                **base_args,
                engine_size=self.engine_spin.value(),
                motorcycle_type=self.moto_type_combo.currentText()
            )
        return None


class VehiclesPage(QWidget):
    """Page de gestion des véhicules."""
    
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
        title = QLabel("Gestion des véhicules")
        title.setStyleSheet("font-size: 24px; font-weight: 700; color: #0f172a;")
        subtitle = QLabel("Gérez votre flotte de véhicules")
        subtitle.setStyleSheet("color: #64748b;")
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        add_btn = QPushButton("  Ajouter un vehicule")
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
        add_btn.clicked.connect(self.add_vehicle)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addWidget(add_btn)
        
        layout.addLayout(header_layout)
        
        # Filtres
        filter_layout = QHBoxLayout()
        
        filter_label = QLabel("Filtrer:")
        filter_label.setStyleSheet("font-weight: 500;")
        
        self.type_filter = QComboBox()
        self.type_filter.addItems(["Tous les types", "Voiture", "Camion", "Moto"])
        self.type_filter.currentTextChanged.connect(self.apply_filters)
        
        self.state_filter = QComboBox()
        self.state_filter.addItem("Tous les états")
        for state in VehicleState:
            self.state_filter.addItem(state.value, state)
        self.state_filter.currentTextChanged.connect(self.apply_filters)
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Rechercher...")
        self.search_edit.textChanged.connect(self.apply_filters)
        self.search_edit.setMaximumWidth(250)
        
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.type_filter)
        filter_layout.addWidget(self.state_filter)
        filter_layout.addStretch()
        filter_layout.addWidget(self.search_edit)
        
        layout.addLayout(filter_layout)
        
        # Tableau des véhicules
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "Type", "Marque", "Modèle", "Catégorie", 
            "Tarif/jour", "État", "Année", "Actions"
        ])
        
        # Configuration du tableau
        header = self.table.horizontalHeader()
        if header:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # ID
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)  # Type
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Marque
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Modèle
            header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)  # Catégorie
            header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)  # Tarif
            header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)  # État
            header.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)  # Année
            header.setSectionResizeMode(8, QHeaderView.ResizeMode.Fixed)  # Actions
        
        # Largeurs fixes des colonnes
        self.table.setColumnWidth(0, 90)   # ID
        self.table.setColumnWidth(1, 80)   # Type
        self.table.setColumnWidth(4, 100)  # Catégorie
        self.table.setColumnWidth(5, 90)   # Tarif
        self.table.setColumnWidth(6, 110)  # État
        self.table.setColumnWidth(7, 60)   # Année
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
        self.all_vehicles = self.system.get_all_vehicles()
        self.apply_filters()
    
    def apply_filters(self):
        """Applique les filtres et affiche les véhicules."""
        vehicles = self.all_vehicles
        
        # Filtre par type
        type_filter = self.type_filter.currentText()
        if type_filter != "Tous les types":
            vehicles = [v for v in vehicles if v.get_vehicle_type() == type_filter]
        
        # Filtre par état
        state_data = self.state_filter.currentData()
        if state_data:
            vehicles = [v for v in vehicles if v.state == state_data]
        
        # Filtre par recherche
        search = self.search_edit.text().lower()
        if search:
            vehicles = [v for v in vehicles 
                       if search in v.brand.lower() 
                       or search in v.model.lower()
                       or search in v.license_plate.lower()]
        
        self.display_vehicles(vehicles)
    
    def display_vehicles(self, vehicles: list):
        """Affiche les véhicules dans le tableau."""
        self.table.setRowCount(len(vehicles))
        
        for row, vehicle in enumerate(vehicles):
            self.table.setItem(row, 0, QTableWidgetItem(vehicle.id))
            self.table.setItem(row, 1, QTableWidgetItem(vehicle.get_vehicle_type()))
            self.table.setItem(row, 2, QTableWidgetItem(vehicle.brand))
            self.table.setItem(row, 3, QTableWidgetItem(vehicle.model))
            self.table.setItem(row, 4, QTableWidgetItem(vehicle.category.value))
            self.table.setItem(row, 5, QTableWidgetItem(f"{vehicle.daily_rate:.2f} €"))
            
            # État avec badge
            state_widget = QWidget()
            state_layout = QHBoxLayout(state_widget)
            state_layout.setContentsMargins(2, 2, 2, 2)
            state_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            state_label = QLabel(vehicle.state.value)
            if vehicle.state == VehicleState.AVAILABLE:
                state_label.setStyleSheet("""
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
            elif vehicle.state == VehicleState.RENTED:
                state_label.setStyleSheet("""
                    QLabel {
                        background-color: #fefce8;
                        color: #ca8a04;
                        padding: 2px 8px;
                        border-radius: 10px;
                        font-weight: 600;
                        font-size: 11px;
                        border: 1px solid #fef08a;
                    }
                """)
            elif vehicle.state == VehicleState.MAINTENANCE:
                state_label.setStyleSheet("""
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
            else:
                state_label.setStyleSheet("""
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
            state_layout.addWidget(state_label)
            self.table.setCellWidget(row, 6, state_widget)
            
            self.table.setItem(row, 7, QTableWidgetItem(str(vehicle.year)))
            
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
            edit_btn.clicked.connect(lambda checked, v=vehicle: self.edit_vehicle(v))
            
            delete_btn = create_action_button(
                "delete", "Supprimer",
                icon_color="#ef4444",
                bg_color="#fef2f2",
                hover_color="#fee2e2",
                border_color="#fecaca",
                size=28
            )
            delete_btn.clicked.connect(lambda checked, v=vehicle: self.delete_vehicle(v))
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            
            self.table.setCellWidget(row, 8, actions_widget)
    
    def add_vehicle(self):
        """Ouvre le dialogue pour ajouter un véhicule."""
        dialog = VehicleDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            vehicle = dialog.get_vehicle()
            if vehicle and self.system.add_vehicle(vehicle):
                self.refresh_data()
                self.data_changed.emit()
                QMessageBox.information(self, "Succès", "Véhicule ajouté avec succès!")
            else:
                QMessageBox.warning(self, "Erreur", "Impossible d'ajouter le véhicule.")
    
    def edit_vehicle(self, vehicle: Vehicle):
        """Ouvre le dialogue pour modifier un véhicule."""
        dialog = VehicleDialog(self, vehicle)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Supprimer l'ancien et ajouter le nouveau
            old_state = vehicle.state  # Conserver l'état via le getter public
            self.system.remove_vehicle(vehicle.id)
            new_vehicle = dialog.get_vehicle()
            if new_vehicle:
                new_vehicle.state = old_state  # Utiliser le setter public
                self.system.add_vehicle(new_vehicle)
            self.refresh_data()
            self.data_changed.emit()
            QMessageBox.information(self, "Succès", "Véhicule modifié avec succès!")
    
    def delete_vehicle(self, vehicle: Vehicle):
        """Supprime un véhicule."""
        reply = QMessageBox.question(
            self, "Confirmation",
            f"Voulez-vous vraiment supprimer le véhicule {vehicle.brand} {vehicle.model}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.system.remove_vehicle(vehicle.id):
                self.refresh_data()
                self.data_changed.emit()
                QMessageBox.information(self, "Succès", "Véhicule supprimé!")
            else:
                QMessageBox.warning(
                    self, "Erreur", 
                    "Impossible de supprimer ce véhicule.\nIl est peut-être en cours de location."
                )
