"""
Module de constantes pour le système de location de voitures.
Centralise toutes les valeurs configurables du système.
"""

# === Constantes de Location ===

class RentalConstants:
    """Constantes liées aux locations."""
    
    # Réductions pour locations longues durées
    WEEKLY_RENTAL_MIN_DAYS = 7
    WEEKLY_RENTAL_DISCOUNT = 0.10  # 10%
    
    MONTHLY_RENTAL_MIN_DAYS = 30
    MONTHLY_RENTAL_DISCOUNT = 0.20  # 20%
    
    # Pénalités
    LATE_RETURN_PENALTY_PER_DAY = 50.0  # € par jour de retard
    CANCELLATION_FEE_PERCENT = 0.20  # 20% du coût total
    
    # Annulation gratuite
    FREE_CANCELLATION_DAYS_BEFORE = 2  # Jours avant le début


class VehicleConstants:
    """Constantes liées aux véhicules."""
    
    # Maintenance
    MAINTENANCE_KM_THRESHOLD = 10000  # km entre maintenances
    
    # Âges minimum par catégorie
    MIN_AGE_ECONOMY = 21
    MIN_AGE_STANDARD = 21
    MIN_AGE_PREMIUM = 23
    MIN_AGE_LUXURY = 25
    MIN_AGE_SPORT = 25
    MIN_AGE_UTILITY = 21
    
    # Âges minimum pour motos
    MIN_AGE_MOTORCYCLE_SMALL = 18  # Cylindrée <= 125cc
    MIN_AGE_MOTORCYCLE_LARGE = 21  # Cylindrée > 125cc
    MOTORCYCLE_SMALL_ENGINE_LIMIT = 125  # cc
    
    # Âges minimum pour camions
    MIN_AGE_TRUCK_LIGHT = 21  # <= 3.5T
    MIN_AGE_TRUCK_MEDIUM = 21  # 3.5T - 7.5T
    MIN_AGE_TRUCK_HEAVY = 25  # > 7.5T
    TRUCK_LIGHT_WEIGHT_LIMIT = 3500  # kg
    TRUCK_MEDIUM_WEIGHT_LIMIT = 7500  # kg
    
    # Supplément assurance moto
    MOTORCYCLE_INSURANCE_SUPPLEMENT = 1.15  # +15%


class CustomerConstants:
    """Constantes liées aux clients."""
    
    # Ancienneté minimum du permis
    MIN_LICENSE_YEARS = 1
    
    # Seuils de fidélité
    LOYALTY_TIER_1_RENTALS = 5
    LOYALTY_TIER_1_DISCOUNT = 0.05  # 5%
    
    LOYALTY_TIER_2_RENTALS = 10
    LOYALTY_TIER_2_DISCOUNT = 0.10  # 10%
    
    LOYALTY_TIER_3_RENTALS = 20
    LOYALTY_TIER_3_DISCOUNT = 0.15  # 15%


class LicenseTypes:
    """Types de permis de conduire."""
    
    CAR = "B"
    MOTORCYCLE_SMALL = "A1"
    MOTORCYCLE_LARGE = "A"
    TRUCK_LIGHT = "B"
    TRUCK_MEDIUM = "C1"
    TRUCK_HEAVY = "C"
