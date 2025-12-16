"""Module de gestion des véhicules.
Contient la hiérarchie de classes Vehicle, Car, Truck, Motorcycle.
"""

from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime, date
from typing import Optional, List
import uuid

# Constantes locales pour éviter les imports circulaires
# Ces valeurs sont synchronisées avec models/constants.py
_MAINTENANCE_KM_THRESHOLD = 10000
_MIN_AGE_ECONOMY = 21
_MIN_AGE_PREMIUM = 23
_MIN_AGE_LUXURY = 25
_MIN_AGE_SPORT = 25
_MIN_AGE_MOTORCYCLE_SMALL = 18
_MIN_AGE_MOTORCYCLE_LARGE = 21
_MOTORCYCLE_SMALL_ENGINE_LIMIT = 125
_MIN_AGE_TRUCK_LIGHT = 21
_MIN_AGE_TRUCK_MEDIUM = 21
_MIN_AGE_TRUCK_HEAVY = 25
_TRUCK_LIGHT_WEIGHT_LIMIT = 3500
_TRUCK_MEDIUM_WEIGHT_LIMIT = 7500
_MOTORCYCLE_INSURANCE_SUPPLEMENT = 1.15
_WEEKLY_RENTAL_MIN_DAYS = 7
_WEEKLY_RENTAL_DISCOUNT = 0.10
_MONTHLY_RENTAL_MIN_DAYS = 30
_MONTHLY_RENTAL_DISCOUNT = 0.20

# Types de permis
_LICENSE_CAR = "B"
_LICENSE_MOTORCYCLE_SMALL = "A1"
_LICENSE_MOTORCYCLE_LARGE = "A"
_LICENSE_TRUCK_LIGHT = "B"
_LICENSE_TRUCK_MEDIUM = "C1"
_LICENSE_TRUCK_HEAVY = "C"


class VehicleState(Enum):
    """États possibles d'un véhicule."""
    AVAILABLE = "disponible"
    RENTED = "loué"
    MAINTENANCE = "en maintenance"
    OUT_OF_SERVICE = "hors service"


class VehicleCategory(Enum):
    """Catégories de véhicules."""
    ECONOMY = "économique"
    STANDARD = "standard"
    PREMIUM = "premium"
    LUXURY = "luxe"
    UTILITY = "utilitaire"
    SPORT = "sport"


class Vehicle(ABC):
    """
    Classe abstraite représentant un véhicule.
    
    Attributes:
        id (str): Identifiant unique du véhicule
        brand (str): Marque du véhicule
        model (str): Modèle du véhicule
        category (VehicleCategory): Catégorie du véhicule
        daily_rate (float): Tarif journalier de location
        state (VehicleState): État actuel du véhicule
        year (int): Année de fabrication
        license_plate (str): Numéro d'immatriculation
        mileage (float): Kilométrage actuel
        maintenance_history (List[dict]): Historique d'entretien
    """
    
    def __init__(
        self,
        brand: str,
        model: str,
        category: VehicleCategory,
        daily_rate: float,
        year: int,
        license_plate: str,
        mileage: float = 0.0,
        vehicle_id: Optional[str] = None
    ):
        self._id = vehicle_id or str(uuid.uuid4())[:8].upper()
        self._brand = brand
        self._model = model
        self._category = category
        self._daily_rate = daily_rate
        self._state = VehicleState.AVAILABLE
        self._year = year
        self._license_plate = license_plate
        self._mileage = mileage
        self._maintenance_history: List[dict] = []
        self._last_maintenance_date: Optional[date] = None
    
    # Propriétés avec getters
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def brand(self) -> str:
        return self._brand
    
    @property
    def model(self) -> str:
        return self._model
    
    @property
    def category(self) -> VehicleCategory:
        return self._category
    
    @property
    def daily_rate(self) -> float:
        return self._daily_rate
    
    @daily_rate.setter
    def daily_rate(self, value: float):
        if value < 0:
            raise ValueError(f"Le tarif journalier ne peut pas être négatif ({value})")
        self._daily_rate = value
    
    @property
    def state(self) -> VehicleState:
        return self._state
    
    @state.setter
    def state(self, value: VehicleState):
        self._state = value
    
    @property
    def year(self) -> int:
        return self._year
    
    @property
    def license_plate(self) -> str:
        return self._license_plate
    
    @property
    def mileage(self) -> float:
        return self._mileage
    
    @mileage.setter
    def mileage(self, value: float):
        if value < self._mileage:
            raise ValueError(f"Le kilométrage ne peut pas diminuer ({self._mileage} -> {value})")
        self._mileage = value
    
    @property
    def maintenance_history(self) -> List[dict]:
        return self._maintenance_history.copy()
    
    @property
    def last_maintenance_date(self) -> Optional[date]:
        return self._last_maintenance_date
    
    # Méthodes
    def is_available(self) -> bool:
        """Vérifie si le véhicule est disponible à la location."""
        return self._state == VehicleState.AVAILABLE
    
    def rent(self) -> bool:
        """Marque le véhicule comme loué."""
        if self.is_available():
            self._state = VehicleState.RENTED
            return True
        return False
    
    def return_vehicle(self, new_mileage: Optional[float] = None) -> bool:
        """Retourne le véhicule et le marque comme disponible."""
        if self._state == VehicleState.RENTED:
            if new_mileage is not None:
                self.mileage = new_mileage
            self._state = VehicleState.AVAILABLE
            return True
        return False
    
    def send_to_maintenance(self, description: str) -> bool:
        """Envoie le véhicule en maintenance."""
        if self._state != VehicleState.RENTED:
            self._state = VehicleState.MAINTENANCE
            self._maintenance_history.append({
                'date': datetime.now(),
                'description': description,
                'type': 'début maintenance',
                'mileage': self._mileage
            })
            return True
        return False
    
    def complete_maintenance(self, description: str, cost: float = 0.0) -> bool:
        """Termine la maintenance du véhicule."""
        if self._state == VehicleState.MAINTENANCE:
            self._state = VehicleState.AVAILABLE
            self._last_maintenance_date = date.today()
            self._maintenance_history.append({
                'date': datetime.now(),
                'description': description,
                'type': 'fin maintenance',
                'cost': cost,
                'mileage': self._mileage
            })
            return True
        return False
    
    def needs_maintenance(self, km_threshold: float = _MAINTENANCE_KM_THRESHOLD) -> bool:
        """Vérifie si le véhicule nécessite une maintenance."""
        if not self._maintenance_history:
            return self._mileage >= km_threshold
        
        last_maintenance_mileage = 0
        for record in reversed(self._maintenance_history):
            if record['type'] == 'fin maintenance':
                last_maintenance_mileage = record.get('mileage', 0)
                break
        
        return (self._mileage - last_maintenance_mileage) >= km_threshold
    
    @abstractmethod
    def get_vehicle_type(self) -> str:
        """Retourne le type de véhicule."""
        pass
    
    @abstractmethod
    def get_minimum_driver_age(self) -> int:
        """Retourne l'âge minimum requis pour conduire ce véhicule."""
        pass
    
    @abstractmethod
    def get_required_license(self) -> str:
        """Retourne le type de permis requis."""
        pass
    
    def calculate_rental_cost(self, days: int) -> float:
        """Calcule le coût de location pour un nombre de jours donné."""
        if days <= 0:
            raise ValueError(f"Le nombre de jours doit être positif ({days})")
        
        base_cost = self._daily_rate * days
        
        # Réductions pour locations longues
        if days >= _MONTHLY_RENTAL_MIN_DAYS:
            return base_cost * (1 - _MONTHLY_RENTAL_DISCOUNT)
        elif days >= _WEEKLY_RENTAL_MIN_DAYS:
            return base_cost * (1 - _WEEKLY_RENTAL_DISCOUNT)
        
        return base_cost
    
    def __str__(self) -> str:
        return f"{self.get_vehicle_type()} {self._brand} {self._model} ({self._year}) - {self._license_plate}"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self._id}, brand={self._brand}, model={self._model})"
    
    def to_dict(self) -> dict:
        """Convertit le véhicule en dictionnaire."""
        return {
            'id': self._id,
            'type': self.get_vehicle_type(),
            'brand': self._brand,
            'model': self._model,
            'category': self._category.value,
            'daily_rate': self._daily_rate,
            'state': self._state.value,
            'year': self._year,
            'license_plate': self._license_plate,
            'mileage': self._mileage,
            'minimum_age': self.get_minimum_driver_age(),
            'required_license': self.get_required_license()
        }


class Car(Vehicle):
    """
    Classe représentant une voiture.
    
    Attributes:
        num_doors (int): Nombre de portes
        num_seats (int): Nombre de places
        fuel_type (str): Type de carburant
        transmission (str): Type de transmission
    """
    
    def __init__(
        self,
        brand: str,
        model: str,
        category: VehicleCategory,
        daily_rate: float,
        year: int,
        license_plate: str,
        num_doors: int = 5,
        num_seats: int = 5,
        fuel_type: str = "essence",
        transmission: str = "manuelle",
        mileage: float = 0.0,
        vehicle_id: Optional[str] = None
    ):
        super().__init__(
            brand, model, category, daily_rate, 
            year, license_plate, mileage, vehicle_id
        )
        self._num_doors = num_doors
        self._num_seats = num_seats
        self._fuel_type = fuel_type
        self._transmission = transmission
    
    @property
    def num_doors(self) -> int:
        return self._num_doors
    
    @property
    def num_seats(self) -> int:
        return self._num_seats
    
    @property
    def fuel_type(self) -> str:
        return self._fuel_type
    
    @property
    def transmission(self) -> str:
        return self._transmission
    
    def get_vehicle_type(self) -> str:
        return "Voiture"
    
    def get_minimum_driver_age(self) -> int:
        """Retourne l'âge minimum selon la catégorie du véhicule."""
        if self._category == VehicleCategory.LUXURY:
            return _MIN_AGE_LUXURY
        elif self._category == VehicleCategory.SPORT:
            return _MIN_AGE_SPORT
        elif self._category == VehicleCategory.PREMIUM:
            return _MIN_AGE_PREMIUM
        return _MIN_AGE_ECONOMY
    
    def get_required_license(self) -> str:
        return _LICENSE_CAR
    
    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            'num_doors': self._num_doors,
            'num_seats': self._num_seats,
            'fuel_type': self._fuel_type,
            'transmission': self._transmission
        })
        return data


class Truck(Vehicle):
    """
    Classe représentant un camion/utilitaire.
    
    Attributes:
        cargo_capacity (float): Capacité de chargement en m³
        max_weight (float): Poids maximum autorisé en kg
        has_tail_lift (bool): Présence d'un hayon élévateur
    """
    
    def __init__(
        self,
        brand: str,
        model: str,
        category: VehicleCategory,
        daily_rate: float,
        year: int,
        license_plate: str,
        cargo_capacity: float,
        max_weight: float,
        has_tail_lift: bool = False,
        mileage: float = 0.0,
        vehicle_id: Optional[str] = None
    ):
        super().__init__(
            brand, model, category, daily_rate,
            year, license_plate, mileage, vehicle_id
        )
        self._cargo_capacity = cargo_capacity
        self._max_weight = max_weight
        self._has_tail_lift = has_tail_lift
    
    @property
    def cargo_capacity(self) -> float:
        return self._cargo_capacity
    
    @property
    def max_weight(self) -> float:
        return self._max_weight
    
    @property
    def has_tail_lift(self) -> bool:
        return self._has_tail_lift
    
    def get_vehicle_type(self) -> str:
        return "Camion"
    
    def get_minimum_driver_age(self) -> int:
        """Retourne l'âge minimum selon le poids du camion."""
        if self._max_weight > _TRUCK_MEDIUM_WEIGHT_LIMIT:
            return _MIN_AGE_TRUCK_HEAVY
        elif self._max_weight > _TRUCK_LIGHT_WEIGHT_LIMIT:
            return _MIN_AGE_TRUCK_MEDIUM
        return _MIN_AGE_TRUCK_LIGHT
    
    def get_required_license(self) -> str:
        """Retourne le permis requis selon le poids du camion."""
        if self._max_weight > _TRUCK_MEDIUM_WEIGHT_LIMIT:
            return _LICENSE_TRUCK_HEAVY
        elif self._max_weight > _TRUCK_LIGHT_WEIGHT_LIMIT:
            return _LICENSE_TRUCK_MEDIUM
        return _LICENSE_TRUCK_LIGHT
    
    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            'cargo_capacity': self._cargo_capacity,
            'max_weight': self._max_weight,
            'has_tail_lift': self._has_tail_lift
        })
        return data


class Motorcycle(Vehicle):
    """
    Classe représentant une moto.
    
    Attributes:
        engine_size (int): Cylindrée en cm³
        motorcycle_type (str): Type de moto (sport, touring, etc.)
    """
    
    def __init__(
        self,
        brand: str,
        model: str,
        category: VehicleCategory,
        daily_rate: float,
        year: int,
        license_plate: str,
        engine_size: int,
        motorcycle_type: str = "standard",
        mileage: float = 0.0,
        vehicle_id: Optional[str] = None
    ):
        super().__init__(
            brand, model, category, daily_rate,
            year, license_plate, mileage, vehicle_id
        )
        self._engine_size = engine_size
        self._motorcycle_type = motorcycle_type
    
    @property
    def engine_size(self) -> int:
        return self._engine_size
    
    @property
    def motorcycle_type(self) -> str:
        return self._motorcycle_type
    
    def get_vehicle_type(self) -> str:
        return "Moto"
    
    def get_minimum_driver_age(self) -> int:
        """Retourne l'âge minimum selon la cylindrée."""
        if self._engine_size > _MOTORCYCLE_SMALL_ENGINE_LIMIT:
            return _MIN_AGE_MOTORCYCLE_LARGE
        return _MIN_AGE_MOTORCYCLE_SMALL
    
    def get_required_license(self) -> str:
        """Retourne le permis requis selon la cylindrée."""
        if self._engine_size > _MOTORCYCLE_SMALL_ENGINE_LIMIT:
            return _LICENSE_MOTORCYCLE_LARGE
        return _LICENSE_MOTORCYCLE_SMALL
    
    def calculate_rental_cost(self, days: int) -> float:
        """Les motos ont un supplément assurance (+15%)."""
        base_cost = super().calculate_rental_cost(days)
        return base_cost * _MOTORCYCLE_INSURANCE_SUPPLEMENT
    
    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            'engine_size': self._engine_size,
            'motorcycle_type': self._motorcycle_type
        })
        return data
