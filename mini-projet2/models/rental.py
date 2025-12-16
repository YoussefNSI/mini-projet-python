"""
Module de gestion des locations.
"""

from datetime import date, datetime, timedelta
from typing import Optional
from enum import Enum
import uuid

# Constantes locales pour éviter les imports circulaires
# Ces valeurs sont synchronisées avec models/constants.py
_LATE_RETURN_PENALTY_PER_DAY = 50.0
_CANCELLATION_FEE_PERCENT = 0.20
_WEEKLY_RENTAL_MIN_DAYS = 7
_WEEKLY_RENTAL_DISCOUNT = 0.10
_MONTHLY_RENTAL_MIN_DAYS = 30
_MONTHLY_RENTAL_DISCOUNT = 0.20
_FREE_CANCELLATION_DAYS_BEFORE = 2


class RentalStatus(Enum):
    """Statuts possibles d'une location."""
    RESERVED = "réservée"
    ACTIVE = "en cours"
    COMPLETED = "terminée"
    CANCELLED = "annulée"


class Rental:
    """
    Classe représentant une location de véhicule.
    
    Attributes:
        id (str): Identifiant unique de la location
        customer_id (str): ID du client
        vehicle_id (str): ID du véhicule
        start_date (date): Date de début de location
        end_date (date): Date de fin prévue
        actual_return_date (Optional[date]): Date de retour effective
        status (RentalStatus): Statut de la location
        daily_rate (float): Tarif journalier appliqué
        total_cost (float): Coût total de la location
        penalty (float): Pénalités appliquées
        start_mileage (float): Kilométrage au départ
        end_mileage (Optional[float]): Kilométrage au retour
    """
    
    # Constantes pour les pénalités
    LATE_RETURN_PENALTY_PER_DAY = _LATE_RETURN_PENALTY_PER_DAY
    CANCELLATION_FEE_PERCENT = _CANCELLATION_FEE_PERCENT
    
    def __init__(
        self,
        customer_id: str,
        vehicle_id: str,
        start_date: date,
        end_date: date,
        daily_rate: float,
        start_mileage: float = 0.0,
        rental_id: Optional[str] = None
    ):
        # Validation des dates
        if end_date < start_date:
            raise ValueError(
                "La date de fin ne peut pas être antérieure à la date de début"
            )
        
        # Permettre les dates d'aujourd'hui et futures (pas dans le passé)
        if start_date < date.today():
            raise ValueError(
                "La date de début ne peut pas être dans le passé"
            )
        
        self._id = rental_id or str(uuid.uuid4())[:8].upper()
        self._customer_id = customer_id
        self._vehicle_id = vehicle_id
        self._start_date = start_date
        self._end_date = end_date
        self._actual_return_date: Optional[date] = None
        self._status = RentalStatus.RESERVED
        self._daily_rate = daily_rate
        self._start_mileage = start_mileage
        self._end_mileage: Optional[float] = None
        self._penalty = 0.0
        self._created_at = datetime.now()
        self._notes: str = ""
        self._discount_applied = 0.0
    
    # Propriétés
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def customer_id(self) -> str:
        return self._customer_id
    
    @property
    def vehicle_id(self) -> str:
        return self._vehicle_id
    
    @property
    def start_date(self) -> date:
        return self._start_date
    
    @property
    def end_date(self) -> date:
        return self._end_date
    
    @end_date.setter
    def end_date(self, value: date):
        if value < self._start_date:
            raise ValueError("La date de fin ne peut pas être antérieure à la date de début")
        self._end_date = value
    
    @property
    def actual_return_date(self) -> Optional[date]:
        return self._actual_return_date
    
    @property
    def status(self) -> RentalStatus:
        return self._status
    
    @property
    def daily_rate(self) -> float:
        return self._daily_rate
    
    @property
    def start_mileage(self) -> float:
        return self._start_mileage
    
    @property
    def end_mileage(self) -> Optional[float]:
        return self._end_mileage
    
    @property
    def penalty(self) -> float:
        return self._penalty
    
    @property
    def notes(self) -> str:
        return self._notes
    
    @notes.setter
    def notes(self, value: str):
        self._notes = value
    
    @property
    def discount_applied(self) -> float:
        return self._discount_applied
    
    # Méthodes de calcul
    @property
    def planned_duration(self) -> int:
        """Durée prévue de la location en jours."""
        return (self._end_date - self._start_date).days + 1
    
    @property
    def actual_duration(self) -> Optional[int]:
        """Durée effective de la location en jours."""
        if self._actual_return_date:
            return (self._actual_return_date - self._start_date).days + 1
        return None
    
    @property
    def days_late(self) -> int:
        """Nombre de jours de retard."""
        if self._actual_return_date and self._actual_return_date > self._end_date:
            return (self._actual_return_date - self._end_date).days
        return 0
    
    @property
    def distance_traveled(self) -> Optional[float]:
        """Distance parcourue en km."""
        if self._end_mileage is not None:
            return self._end_mileage - self._start_mileage
        return None
    
    def calculate_base_cost(self) -> float:
        """Calcule le coût de base de la location."""
        duration = self.actual_duration or self.planned_duration
        base_cost = self._daily_rate * duration
        
        # Réductions pour locations longues
        if duration >= _MONTHLY_RENTAL_MIN_DAYS:
            base_cost *= (1 - _MONTHLY_RENTAL_DISCOUNT)
        elif duration >= _WEEKLY_RENTAL_MIN_DAYS:
            base_cost *= (1 - _WEEKLY_RENTAL_DISCOUNT)
        
        return base_cost
    
    def calculate_total_cost(self) -> float:
        """Calcule le coût total incluant les pénalités."""
        base_cost = self.calculate_base_cost()
        
        # Application de la réduction fidélité
        cost_after_discount = base_cost * (1 - self._discount_applied)
        
        # Ajout des pénalités
        return cost_after_discount + self._penalty
    
    @property
    def total_cost(self) -> float:
        return self.calculate_total_cost()
    
    def apply_discount(self, discount_percent: float) -> None:
        """Applique une réduction au coût de la location."""
        if 0 <= discount_percent <= 1:
            self._discount_applied = discount_percent
    
    # Méthodes de gestion du cycle de vie
    def start_rental(self) -> bool:
        """Démarre la location (passage de réservé à actif)."""
        if self._status == RentalStatus.RESERVED:
            if self._start_date <= date.today():
                self._status = RentalStatus.ACTIVE
                return True
        return False
    
    def complete_rental(
        self,
        return_date: date,
        end_mileage: Optional[float] = None
    ) -> float:
        """
        Termine la location et calcule le coût final.
        
        Args:
            return_date: Date de retour du véhicule
            end_mileage: Kilométrage au retour
            
        Returns:
            Le coût total de la location
            
        Raises:
            ValueError: Si la location n'est pas active
        """
        if self._status not in [RentalStatus.ACTIVE, RentalStatus.RESERVED]:
            raise ValueError(f"Location '{self._id}' n'est pas active (statut: {self._status.value})")
        
        self._actual_return_date = return_date
        self._end_mileage = end_mileage
        
        # Calcul des pénalités de retard
        if return_date > self._end_date:
            days_late = (return_date - self._end_date).days
            self._penalty = days_late * self.LATE_RETURN_PENALTY_PER_DAY
        
        self._status = RentalStatus.COMPLETED
        return self.calculate_total_cost()
    
    def cancel_rental(self) -> float:
        """
        Annule la location et calcule les frais d'annulation.
        
        Returns:
            Les frais d'annulation
            
        Raises:
            ValueError: Si la location ne peut pas être annulée
        """
        if self._status == RentalStatus.COMPLETED:
            raise ValueError(f"Location '{self._id}' ne peut pas être annulée: location déjà terminée")
        
        cancellation_fee = 0.0
        
        # Frais d'annulation selon le délai
        days_until_start = (self._start_date - date.today()).days
        
        if days_until_start <= 1:
            # Annulation de dernière minute: 100% du coût
            cancellation_fee = self.calculate_base_cost()
        elif days_until_start <= 3:
            # Annulation tardive: 50% du coût
            cancellation_fee = self.calculate_base_cost() * 0.50
        elif days_until_start <= _FREE_CANCELLATION_DAYS_BEFORE + 5:
            # Annulation: frais standards
            cancellation_fee = self.calculate_base_cost() * _CANCELLATION_FEE_PERCENT
        # Plus de 7 jours avant: gratuit
        
        self._penalty = cancellation_fee
        self._status = RentalStatus.CANCELLED
        return cancellation_fee
    
    def extend_rental(self, new_end_date: date) -> bool:
        """
        Prolonge la location.
        
        Args:
            new_end_date: Nouvelle date de fin
            
        Returns:
            True si la prolongation est effectuée
        """
        if self._status not in [RentalStatus.ACTIVE, RentalStatus.RESERVED]:
            return False
        
        if new_end_date <= self._end_date:
            return False
        
        self._end_date = new_end_date
        return True
    
    def is_overdue(self) -> bool:
        """Vérifie si la location est en retard."""
        if self._status == RentalStatus.ACTIVE:
            return date.today() > self._end_date
        return False
    
    def days_remaining(self) -> int:
        """Retourne le nombre de jours restants (négatif si en retard)."""
        if self._status == RentalStatus.ACTIVE:
            return (self._end_date - date.today()).days
        return 0
    
    def __str__(self) -> str:
        return f"Location {self._id}: {self._start_date} -> {self._end_date} ({self._status.value})"
    
    def __repr__(self) -> str:
        return f"Rental(id={self._id}, customer={self._customer_id}, vehicle={self._vehicle_id})"
    
    def to_dict(self) -> dict:
        """Convertit la location en dictionnaire."""
        return {
            'id': self._id,
            'customer_id': self._customer_id,
            'vehicle_id': self._vehicle_id,
            'start_date': self._start_date.isoformat(),
            'end_date': self._end_date.isoformat(),
            'actual_return_date': self._actual_return_date.isoformat() if self._actual_return_date else None,
            'status': self._status.value,
            'daily_rate': self._daily_rate,
            'planned_duration': self.planned_duration,
            'actual_duration': self.actual_duration,
            'base_cost': self.calculate_base_cost(),
            'discount_applied': self._discount_applied,
            'penalty': self._penalty,
            'total_cost': self.calculate_total_cost(),
            'start_mileage': self._start_mileage,
            'end_mileage': self._end_mileage,
            'distance_traveled': self.distance_traveled,
            'days_late': self.days_late,
            'notes': self._notes,
            'created_at': self._created_at.isoformat()
        }
