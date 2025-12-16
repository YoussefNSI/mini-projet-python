"""
Module de gestion des clients.
"""

from datetime import date, datetime
from typing import Optional, List, Set
import uuid

# Constantes locales pour éviter les imports circulaires
# Ces valeurs sont synchronisées avec models/constants.py
_LOYALTY_TIER_1_RENTALS = 5
_LOYALTY_TIER_1_DISCOUNT = 0.05
_LOYALTY_TIER_2_RENTALS = 10
_LOYALTY_TIER_2_DISCOUNT = 0.10
_LOYALTY_TIER_3_RENTALS = 20
_LOYALTY_TIER_3_DISCOUNT = 0.15
_MIN_LICENSE_YEARS = 1


def _calculate_years_difference(from_date: date, to_date: date | None = None) -> int:
    """Calcule le nombre d'années complètes entre deux dates."""
    if to_date is None:
        to_date = date.today()
    years = to_date.year - from_date.year
    if (to_date.month, to_date.day) < (from_date.month, from_date.day):
        years -= 1
    return years


class Customer:
    """
    Classe représentant un client de l'agence de location.
    
    Attributes:
        id (str): Identifiant unique du client
        first_name (str): Prénom du client
        last_name (str): Nom de famille du client
        birth_date (date): Date de naissance
        license_number (str): Numéro de permis de conduire
        license_types (Set[str]): Types de permis détenus (B, A, C, etc.)
        license_date (date): Date d'obtention du permis
        email (str): Adresse email
        phone (str): Numéro de téléphone
        address (str): Adresse postale
        rental_history (List[str]): Historique des IDs de locations
    """
    
    def __init__(
        self,
        first_name: str,
        last_name: str,
        birth_date: date,
        license_number: str,
        license_types: Set[str],
        license_date: date,
        email: str,
        phone: str,
        address: str = "",
        customer_id: Optional[str] = None
    ):
        self._id = customer_id or str(uuid.uuid4())[:8].upper()
        self._first_name = first_name
        self._last_name = last_name
        self._birth_date = birth_date
        self._license_number = license_number
        self._license_types = license_types
        self._license_date = license_date
        self._email = email
        self._phone = phone
        self._address = address
        self._rental_history: List[str] = []
        self._active_rentals: List[str] = []
        self._created_at = datetime.now()
        self._is_blocked = False
        self._blocked_reason: Optional[str] = None
    
    # Propriétés
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def first_name(self) -> str:
        return self._first_name
    
    @first_name.setter
    def first_name(self, value: str):
        self._first_name = value
    
    @property
    def last_name(self) -> str:
        return self._last_name
    
    @last_name.setter
    def last_name(self, value: str):
        self._last_name = value
    
    @property
    def full_name(self) -> str:
        return f"{self._first_name} {self._last_name}"
    
    @property
    def birth_date(self) -> date:
        return self._birth_date
    
    @property
    def age(self) -> int:
        """Calcule l'âge actuel du client."""
        return _calculate_years_difference(self._birth_date)
    
    @property
    def license_number(self) -> str:
        return self._license_number
    
    @property
    def license_types(self) -> Set[str]:
        return self._license_types.copy()
    
    @property
    def license_date(self) -> date:
        return self._license_date
    
    @property
    def years_of_license(self) -> int:
        """Calcule le nombre d'années depuis l'obtention du permis."""
        return _calculate_years_difference(self._license_date)
    
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str):
        self._email = value
    
    @property
    def phone(self) -> str:
        return self._phone
    
    @phone.setter
    def phone(self, value: str):
        self._phone = value
    
    @property
    def address(self) -> str:
        return self._address
    
    @address.setter
    def address(self, value: str):
        self._address = value
    
    @property
    def rental_history(self) -> List[str]:
        return self._rental_history.copy()
    
    @property
    def active_rentals(self) -> List[str]:
        return self._active_rentals.copy()
    
    @property
    def is_blocked(self) -> bool:
        return self._is_blocked
    
    @property
    def blocked_reason(self) -> Optional[str]:
        return self._blocked_reason
    
    # Méthodes
    def add_license_type(self, license_type: str) -> None:
        """Ajoute un type de permis au client."""
        self._license_types.add(license_type.upper())
    
    def has_license(self, license_type: str) -> bool:
        """Vérifie si le client possède un type de permis spécifique."""
        return license_type.upper() in self._license_types
    
    def can_rent_vehicle(self, required_license: str, minimum_age: int) -> tuple[bool, str]:
        """
        Vérifie si le client peut louer un véhicule.
        
        Args:
            required_license: Type de permis requis
            minimum_age: Âge minimum requis
            
        Returns:
            Tuple (peut_louer: bool, raison: str)
            
        Note:
            Cette méthode retourne un tuple pour compatibilité ascendante.
            Les exceptions correspondantes sont disponibles pour une gestion
            d'erreurs plus fine.
        """
        if self._is_blocked:
            return False, f"Client bloqué: {self._blocked_reason}"
        
        if self.age < minimum_age:
            return False, f"Âge insuffisant ({self.age} ans, minimum requis: {minimum_age} ans)"
        
        if not self.has_license(required_license):
            return False, f"Permis {required_license} requis, non détenu par le client"
        
        if self.years_of_license < _MIN_LICENSE_YEARS:
            return False, f"Le permis doit être détenu depuis au moins {_MIN_LICENSE_YEARS} an"
        
        return True, "OK"
    
    def check_rental_eligibility(self, required_license: str, minimum_age: int) -> None:
        """
        Vérifie l'éligibilité du client et lève une exception si non éligible.
        
        Args:
            required_license: Type de permis requis
            minimum_age: Âge minimum requis
            
        Raises:
            CustomerBlockedError: Si le client est bloqué
            AgeTooYoungError: Si le client est trop jeune
            LicenseNotHeldError: Si le client n'a pas le permis requis
            LicenseTooRecentError: Si le permis est trop récent
        """
        from models.exceptions import (
            CustomerBlockedError, AgeTooYoungError, 
            LicenseNotHeldError, LicenseTooRecentError
        )
        
        if self._is_blocked:
            raise CustomerBlockedError(self._id, self._blocked_reason or "")
        
        if self.age < minimum_age:
            raise AgeTooYoungError(self.age, minimum_age)
        
        if not self.has_license(required_license):
            raise LicenseNotHeldError(required_license)
        
        if self.years_of_license < _MIN_LICENSE_YEARS:
            raise LicenseTooRecentError(self.years_of_license, _MIN_LICENSE_YEARS)
    
    def add_rental(self, rental_id: str) -> None:
        """Ajoute une location à l'historique et aux locations actives."""
        self._rental_history.append(rental_id)
        self._active_rentals.append(rental_id)
    
    def complete_rental(self, rental_id: str) -> bool:
        """Marque une location comme terminée."""
        if rental_id in self._active_rentals:
            self._active_rentals.remove(rental_id)
            return True
        return False
    
    def get_total_rentals(self) -> int:
        """Retourne le nombre total de locations effectuées."""
        return len(self._rental_history)
    
    def block(self, reason: str) -> None:
        """Bloque le client avec une raison."""
        self._is_blocked = True
        self._blocked_reason = reason
    
    def unblock(self) -> None:
        """Débloque le client."""
        self._is_blocked = False
        self._blocked_reason = None
    
    def restore_state(
        self,
        rental_history: List[str],
        active_rentals: List[str],
        is_blocked: bool,
        blocked_reason: Optional[str]
    ) -> None:
        """
        Restaure l'état interne du client (historique, blocage).
        
        Utilisé lors de la modification d'un client pour conserver son historique.
        
        Args:
            rental_history: Liste des IDs de locations passées
            active_rentals: Liste des IDs de locations actives
            is_blocked: Si le client est bloqué
            blocked_reason: Raison du blocage si applicable
        """
        self._rental_history = list(rental_history)
        self._active_rentals = list(active_rentals)
        self._is_blocked = is_blocked
        self._blocked_reason = blocked_reason
    
    def is_loyal_customer(self, min_rentals: int = _LOYALTY_TIER_1_RENTALS) -> bool:
        """Vérifie si le client est un client fidèle."""
        return len(self._rental_history) >= min_rentals
    
    def get_loyalty_discount(self) -> float:
        """
        Retourne le pourcentage de réduction fidélité.
        
        Returns:
            Pourcentage de réduction (0.0 à 0.15)
        """
        total_rentals = len(self._rental_history)
        if total_rentals >= _LOYALTY_TIER_3_RENTALS:
            return _LOYALTY_TIER_3_DISCOUNT
        elif total_rentals >= _LOYALTY_TIER_2_RENTALS:
            return _LOYALTY_TIER_2_DISCOUNT
        elif total_rentals >= _LOYALTY_TIER_1_RENTALS:
            return _LOYALTY_TIER_1_DISCOUNT
        return 0.0
    
    def __str__(self) -> str:
        return f"Client {self._id}: {self.full_name} ({self.age} ans)"
    
    def __repr__(self) -> str:
        return f"Customer(id={self._id}, name={self.full_name})"
    
    def to_dict(self) -> dict:
        """Convertit le client en dictionnaire."""
        return {
            'id': self._id,
            'first_name': self._first_name,
            'last_name': self._last_name,
            'full_name': self.full_name,
            'birth_date': self._birth_date.isoformat(),
            'age': self.age,
            'license_number': self._license_number,
            'license_types': list(self._license_types),
            'license_date': self._license_date.isoformat(),
            'years_of_license': self.years_of_license,
            'email': self._email,
            'phone': self._phone,
            'address': self._address,
            'total_rentals': len(self._rental_history),
            'active_rentals': len(self._active_rentals),
            'is_blocked': self._is_blocked,
            'is_loyal': self.is_loyal_customer(),
            'loyalty_discount': self.get_loyalty_discount()
        }
