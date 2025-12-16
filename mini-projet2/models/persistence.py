"""
Module de persistance pour le système de location de voitures.
Gère la sauvegarde et le chargement des données en JSON.
"""

import json
import logging
from datetime import date, datetime
from pathlib import Path
from typing import Dict, Any, Optional

from models import vehicle as vehicle_module
from models.customer import Customer
from models.rental import Rental, RentalStatus
from models.exceptions import DataLoadError, DataSaveError

# Références locales pour les classes de véhicules
Car = vehicle_module.Car
Truck = vehicle_module.Truck
Motorcycle = vehicle_module.Motorcycle
VehicleCategory = vehicle_module.VehicleCategory
VehicleState = vehicle_module.VehicleState

# Configuration du logging
logger = logging.getLogger(__name__)


class DateTimeEncoder(json.JSONEncoder):
    """Encodeur JSON personnalisé pour les dates et datetime."""
    
    def default(self, o):
        if isinstance(o, datetime):
            return {'_type': 'datetime', 'value': o.isoformat()}
        elif isinstance(o, date):
            return {'_type': 'date', 'value': o.isoformat()}
        return super().default(o)


def datetime_decoder(dct: Dict) -> Any:
    """Décodeur pour les dates et datetime."""
    if '_type' in dct:
        if dct['_type'] == 'datetime':
            return datetime.fromisoformat(dct['value'])
        elif dct['_type'] == 'date':
            return date.fromisoformat(dct['value'])
    return dct


class DataPersistence:
    """
    Classe gérant la persistance des données du système de location.
    
    Permet de sauvegarder et charger l'état complet du système en JSON.
    
    Attributes:
        data_dir: Répertoire de stockage des données
        vehicles_file: Fichier des véhicules
        customers_file: Fichier des clients
        rentals_file: Fichier des locations
    """
    
    DEFAULT_DATA_DIR = "data"
    VEHICLES_FILE = "vehicles.json"
    CUSTOMERS_FILE = "customers.json"
    RENTALS_FILE = "rentals.json"
    
    def __init__(self, data_dir: str | Path = DEFAULT_DATA_DIR):
        """
        Initialise le gestionnaire de persistance.
        
        Args:
            data_dir: Répertoire de stockage des données
        """
        self.data_dir = Path(data_dir)
        self._ensure_data_dir()
    
    def _ensure_data_dir(self) -> None:
        """Crée le répertoire de données s'il n'existe pas."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    @property
    def vehicles_path(self) -> Path:
        return self.data_dir / self.VEHICLES_FILE
    
    @property
    def customers_path(self) -> Path:
        return self.data_dir / self.CUSTOMERS_FILE
    
    @property
    def rentals_path(self) -> Path:
        return self.data_dir / self.RENTALS_FILE
    
    # === Sauvegarde ===
    
    def save_vehicles(self, vehicles: Dict[str, Any]) -> bool:
        """
        Sauvegarde les véhicules dans un fichier JSON.
        
        Args:
            vehicles: Dictionnaire des véhicules {id: vehicle}
            
        Returns:
            True si la sauvegarde a réussi
        """
        try:
            data = []
            for vehicle in vehicles.values():
                vehicle_data = vehicle.to_dict()
                # Ajouter les informations spécifiques selon le type
                if isinstance(vehicle, Car):
                    vehicle_data['_class'] = 'Car'
                    vehicle_data['num_doors'] = vehicle.num_doors
                    vehicle_data['num_seats'] = vehicle.num_seats
                    vehicle_data['fuel_type'] = vehicle.fuel_type
                    vehicle_data['transmission'] = vehicle.transmission
                elif isinstance(vehicle, Truck):
                    vehicle_data['_class'] = 'Truck'
                    vehicle_data['cargo_capacity'] = vehicle.cargo_capacity
                    vehicle_data['max_weight'] = vehicle.max_weight
                    vehicle_data['has_tail_lift'] = vehicle.has_tail_lift
                elif isinstance(vehicle, Motorcycle):
                    vehicle_data['_class'] = 'Motorcycle'
                    vehicle_data['engine_size'] = vehicle.engine_size
                    vehicle_data['motorcycle_type'] = vehicle.motorcycle_type
                
                data.append(vehicle_data)
            
            with open(self.vehicles_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, cls=DateTimeEncoder, indent=2, ensure_ascii=False)
            
            logger.info(f"Sauvegarde de {len(data)} véhicules réussie")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des véhicules: {e}")
            raise DataSaveError(str(self.vehicles_path), str(e))
    
    def save_customers(self, customers: Dict[str, Customer]) -> bool:
        """
        Sauvegarde les clients dans un fichier JSON.
        
        Args:
            customers: Dictionnaire des clients {id: customer}
            
        Returns:
            True si la sauvegarde a réussi
        """
        try:
            data = []
            for customer in customers.values():
                customer_data = {
                    'id': customer.id,
                    'first_name': customer.first_name,
                    'last_name': customer.last_name,
                    'birth_date': customer.birth_date.isoformat(),
                    'license_number': customer.license_number,
                    'license_types': list(customer.license_types),
                    'license_date': customer.license_date.isoformat(),
                    'email': customer.email,
                    'phone': customer.phone,
                    'address': customer.address,
                    'rental_history': customer.rental_history,
                    'active_rentals': customer.active_rentals,
                    'is_blocked': customer.is_blocked,
                    'blocked_reason': customer.blocked_reason
                }
                data.append(customer_data)
            
            with open(self.customers_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Sauvegarde de {len(data)} clients réussie")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des clients: {e}")
            raise DataSaveError(str(self.customers_path), str(e))
    
    def save_rentals(self, rentals: Dict[str, Rental]) -> bool:
        """
        Sauvegarde les locations dans un fichier JSON.
        
        Args:
            rentals: Dictionnaire des locations {id: rental}
            
        Returns:
            True si la sauvegarde a réussi
        """
        try:
            data = []
            for rental in rentals.values():
                rental_data = rental.to_dict()
                rental_data['_status'] = rental.status.name  # Sauver le nom de l'enum
                data.append(rental_data)
            
            with open(self.rentals_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Sauvegarde de {len(data)} locations réussie")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des locations: {e}")
            raise DataSaveError(str(self.rentals_path), str(e))
    
    def save_all(
        self,
        vehicles: Dict[str, Any],
        customers: Dict[str, Customer],
        rentals: Dict[str, Rental]
    ) -> bool:
        """
        Sauvegarde toutes les données du système.
        
        Args:
            vehicles: Dictionnaire des véhicules
            customers: Dictionnaire des clients
            rentals: Dictionnaire des locations
            
        Returns:
            True si toutes les sauvegardes ont réussi
        """
        success = True
        success = self.save_vehicles(vehicles) and success
        success = self.save_customers(customers) and success
        success = self.save_rentals(rentals) and success
        return success
    
    # === Chargement ===
    
    def load_vehicles(self) -> Dict[str, Any]:
        """
        Charge les véhicules depuis le fichier JSON.
        
        Returns:
            Dictionnaire des véhicules {id: vehicle}
        """
        if not self.vehicles_path.exists():
            logger.info("Aucun fichier de véhicules trouvé")
            return {}
        
        try:
            with open(self.vehicles_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            vehicles = {}
            for item in data:
                vehicle = self._create_vehicle_from_dict(item)
                if vehicle:
                    vehicles[vehicle.id] = vehicle
            
            logger.info(f"Chargement de {len(vehicles)} véhicules réussi")
            return vehicles
            
        except json.JSONDecodeError as e:
            logger.error(f"Erreur de décodage JSON: {e}")
            raise DataLoadError(str(self.vehicles_path), f"JSON invalide: {e}")
        except Exception as e:
            logger.error(f"Erreur lors du chargement des véhicules: {e}")
            raise DataLoadError(str(self.vehicles_path), str(e))
    
    def _create_vehicle_from_dict(self, data: Dict) -> Optional[Any]:
        """Crée un véhicule à partir d'un dictionnaire."""
        vehicle_class = data.get('_class', data.get('type', ''))
        
        # Mapper le type français vers la classe
        type_mapping = {
            'Voiture': 'Car',
            'Camion': 'Truck', 
            'Moto': 'Motorcycle'
        }
        vehicle_class = type_mapping.get(vehicle_class, vehicle_class)
        
        # Récupérer la catégorie
        category_value = data.get('category', 'standard')
        category = VehicleCategory.STANDARD
        for cat in VehicleCategory.__members__.values():
            if cat.value == category_value:
                category = cat
                break
        
        common_args = {
            'brand': data['brand'],
            'model': data['model'],
            'category': category,
            'daily_rate': data['daily_rate'],
            'year': data['year'],
            'license_plate': data['license_plate'],
            'mileage': data.get('mileage', 0),
            'vehicle_id': data['id']
        }
        
        try:
            if vehicle_class == 'Car':
                vehicle = Car(
                    **common_args,
                    num_doors=data.get('num_doors', 5),
                    num_seats=data.get('num_seats', 5),
                    fuel_type=data.get('fuel_type', 'essence'),
                    transmission=data.get('transmission', 'manuelle')
                )
            elif vehicle_class == 'Truck':
                vehicle = Truck(
                    **common_args,
                    cargo_capacity=data.get('cargo_capacity', 10),
                    max_weight=data.get('max_weight', 3500),
                    has_tail_lift=data.get('has_tail_lift', False)
                )
            elif vehicle_class == 'Motorcycle':
                vehicle = Motorcycle(
                    **common_args,
                    engine_size=data.get('engine_size', 125),
                    motorcycle_type=data.get('motorcycle_type', 'standard')
                )
            else:
                logger.warning(f"Type de véhicule inconnu: {vehicle_class}")
                return None
            
            # Restaurer l'état
            state_value = data.get('state', 'disponible')
            for state in VehicleState.__members__.values():
                if state.value == state_value:
                    vehicle.state = state
                    break
            
            return vehicle
            
        except Exception as e:
            logger.error(f"Erreur lors de la création du véhicule: {e}")
            return None
    
    def load_customers(self) -> Dict[str, Customer]:
        """
        Charge les clients depuis le fichier JSON.
        
        Returns:
            Dictionnaire des clients {id: customer}
        """
        if not self.customers_path.exists():
            logger.info("Aucun fichier de clients trouvé")
            return {}
        
        try:
            with open(self.customers_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            customers = {}
            for item in data:
                customer = Customer(
                    first_name=item['first_name'],
                    last_name=item['last_name'],
                    birth_date=date.fromisoformat(item['birth_date']),
                    license_number=item['license_number'],
                    license_types=set(item['license_types']),
                    license_date=date.fromisoformat(item['license_date']),
                    email=item['email'],
                    phone=item['phone'],
                    address=item.get('address', ''),
                    customer_id=item['id']
                )
                
                # Restaurer l'état
                customer.restore_state(
                    rental_history=item.get('rental_history', []),
                    active_rentals=item.get('active_rentals', []),
                    is_blocked=item.get('is_blocked', False),
                    blocked_reason=item.get('blocked_reason')
                )
                
                customers[customer.id] = customer
            
            logger.info(f"Chargement de {len(customers)} clients réussi")
            return customers
            
        except json.JSONDecodeError as e:
            logger.error(f"Erreur de décodage JSON: {e}")
            raise DataLoadError(str(self.customers_path), f"JSON invalide: {e}")
        except Exception as e:
            logger.error(f"Erreur lors du chargement des clients: {e}")
            raise DataLoadError(str(self.customers_path), str(e))
    
    def load_rentals(self) -> Dict[str, Rental]:
        """
        Charge les locations depuis le fichier JSON.
        
        Note: Les locations passées ne peuvent pas être recréées avec des dates
        dans le passé. Seules les locations futures sont restaurées.
        
        Returns:
            Dictionnaire des locations {id: rental}
        """
        if not self.rentals_path.exists():
            logger.info("Aucun fichier de locations trouvé")
            return {}
        
        try:
            with open(self.rentals_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            rentals = {}
            skipped = 0
            
            for item in data:
                start_date = date.fromisoformat(item['start_date'])
                end_date = date.fromisoformat(item['end_date'])
                
                # Ignorer les locations passées (ne peuvent pas être recréées)
                if start_date < date.today() and item.get('_status') not in ['ACTIVE', 'RESERVED']:
                    skipped += 1
                    continue
                
                # Pour les locations passées actives, ajuster la date de début
                if start_date < date.today():
                    start_date = date.today()
                
                try:
                    rental = Rental(
                        customer_id=item['customer_id'],
                        vehicle_id=item['vehicle_id'],
                        start_date=start_date,
                        end_date=end_date,
                        daily_rate=item['daily_rate'],
                        start_mileage=item.get('start_mileage', 0),
                        rental_id=item['id']
                    )
                    
                    # Restaurer la réduction appliquée
                    if item.get('discount_applied', 0) > 0:
                        rental.apply_discount(item['discount_applied'])
                    
                    rentals[rental.id] = rental
                    
                except Exception as e:
                    logger.warning(f"Impossible de restaurer la location {item['id']}: {e}")
                    skipped += 1
            
            logger.info(f"Chargement de {len(rentals)} locations réussi ({skipped} ignorées)")
            return rentals
            
        except json.JSONDecodeError as e:
            logger.error(f"Erreur de décodage JSON: {e}")
            raise DataLoadError(str(self.rentals_path), f"JSON invalide: {e}")
        except Exception as e:
            logger.error(f"Erreur lors du chargement des locations: {e}")
            raise DataLoadError(str(self.rentals_path), str(e))
    
    def load_all(self) -> tuple[Dict, Dict, Dict]:
        """
        Charge toutes les données du système.
        
        Returns:
            Tuple (vehicles, customers, rentals)
        """
        vehicles = self.load_vehicles()
        customers = self.load_customers()
        rentals = self.load_rentals()
        return vehicles, customers, rentals
    
    def clear_all_data(self) -> bool:
        """
        Supprime tous les fichiers de données.
        
        Returns:
            True si la suppression a réussi
        """
        try:
            for path in [self.vehicles_path, self.customers_path, self.rentals_path]:
                if path.exists():
                    path.unlink()
            logger.info("Toutes les données ont été supprimées")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la suppression des données: {e}")
            return False
    
    def data_exists(self) -> bool:
        """Vérifie si des données existent."""
        return any(p.exists() for p in [
            self.vehicles_path,
            self.customers_path, 
            self.rentals_path
        ])
