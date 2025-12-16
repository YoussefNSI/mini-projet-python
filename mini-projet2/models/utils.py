"""
Module utilitaire avec des fonctions helpers réutilisables.
"""

from datetime import date
from typing import Tuple


def calculate_years_difference(from_date: date, to_date: date | None = None) -> int:
    """
    Calcule le nombre d'années complètes entre deux dates.
    
    Utile pour calculer l'âge d'une personne ou l'ancienneté d'un permis.
    
    Args:
        from_date: Date de départ (ex: date de naissance)
        to_date: Date de fin (par défaut: aujourd'hui)
        
    Returns:
        Nombre d'années complètes
        
    Example:
        >>> calculate_years_difference(date(1990, 5, 15))
        35  # Si on est en 2025
    """
    if to_date is None:
        to_date = date.today()
    
    years = to_date.year - from_date.year
    
    # Ajustement si l'anniversaire n'est pas encore passé cette année
    if (to_date.month, to_date.day) < (from_date.month, from_date.day):
        years -= 1
    
    return years


def validate_date_range(start_date: date, end_date: date) -> Tuple[bool, str]:
    """
    Valide une plage de dates pour une location.
    
    Args:
        start_date: Date de début
        end_date: Date de fin
        
    Returns:
        Tuple (est_valide, message_erreur)
    """
    if end_date < start_date:
        return False, "La date de fin ne peut pas être antérieure à la date de début"
    
    if start_date < date.today():
        return False, "La date de début ne peut pas être dans le passé"
    
    return True, "OK"


def format_currency(amount: float, currency: str = "€") -> str:
    """
    Formate un montant en devise.
    
    Args:
        amount: Montant à formater
        currency: Symbole de la devise
        
    Returns:
        Montant formaté (ex: "45.50 €")
    """
    return f"{amount:.2f} {currency}"


def calculate_rental_discount(days: int, base_cost: float) -> Tuple[float, float]:
    """
    Calcule la réduction applicable selon la durée de location.
    
    Args:
        days: Nombre de jours de location
        base_cost: Coût de base sans réduction
        
    Returns:
        Tuple (coût_final, pourcentage_réduction)
    """
    from models.constants import RentalConstants
    
    if days >= RentalConstants.MONTHLY_RENTAL_MIN_DAYS:
        discount = RentalConstants.MONTHLY_RENTAL_DISCOUNT
    elif days >= RentalConstants.WEEKLY_RENTAL_MIN_DAYS:
        discount = RentalConstants.WEEKLY_RENTAL_DISCOUNT
    else:
        discount = 0.0
    
    final_cost = base_cost * (1 - discount)
    return final_cost, discount
