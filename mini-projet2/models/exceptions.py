"""
Exceptions personnalisées pour le système de location de voitures.
Permet une gestion d'erreurs plus fine et explicite.
"""


class CarRentalError(Exception):
    """Exception de base pour le système de location."""
    
    def __init__(self, message: str, code: str | None = None):
        self.message = message
        self.code = code
        super().__init__(self.message)


# === Exceptions liées aux véhicules ===

class VehicleError(CarRentalError):
    """Exception de base pour les erreurs de véhicules."""
    pass


class VehicleNotFoundError(VehicleError):
    """Véhicule non trouvé dans le système."""
    
    def __init__(self, vehicle_id: str):
        super().__init__(
            f"Véhicule '{vehicle_id}' non trouvé",
            code="VEHICLE_NOT_FOUND"
        )
        self.vehicle_id = vehicle_id


class VehicleNotAvailableError(VehicleError):
    """Véhicule non disponible pour la location."""
    
    def __init__(self, vehicle_id: str, reason: str = ""):
        message = f"Véhicule '{vehicle_id}' non disponible"
        if reason:
            message += f": {reason}"
        super().__init__(message, code="VEHICLE_NOT_AVAILABLE")
        self.vehicle_id = vehicle_id


class VehicleAlreadyExistsError(VehicleError):
    """Véhicule déjà présent dans le système."""
    
    def __init__(self, vehicle_id: str):
        super().__init__(
            f"Véhicule '{vehicle_id}' existe déjà",
            code="VEHICLE_EXISTS"
        )
        self.vehicle_id = vehicle_id


class InvalidMileageError(VehicleError):
    """Kilométrage invalide."""
    
    def __init__(self, current: float, new: float):
        super().__init__(
            f"Le kilométrage ne peut pas diminuer ({current} -> {new})",
            code="INVALID_MILEAGE"
        )


class InvalidDailyRateError(VehicleError):
    """Tarif journalier invalide."""
    
    def __init__(self, rate: float):
        super().__init__(
            f"Le tarif journalier ne peut pas être négatif ({rate})",
            code="INVALID_RATE"
        )


# === Exceptions liées aux clients ===

class CustomerError(CarRentalError):
    """Exception de base pour les erreurs de clients."""
    pass


class CustomerNotFoundError(CustomerError):
    """Client non trouvé dans le système."""
    
    def __init__(self, customer_id: str):
        super().__init__(
            f"Client '{customer_id}' non trouvé",
            code="CUSTOMER_NOT_FOUND"
        )
        self.customer_id = customer_id


class CustomerAlreadyExistsError(CustomerError):
    """Client déjà présent dans le système."""
    
    def __init__(self, customer_id: str):
        super().__init__(
            f"Client '{customer_id}' existe déjà",
            code="CUSTOMER_EXISTS"
        )
        self.customer_id = customer_id


class CustomerBlockedError(CustomerError):
    """Client bloqué."""
    
    def __init__(self, customer_id: str, reason: str = ""):
        message = f"Client '{customer_id}' est bloqué"
        if reason:
            message += f": {reason}"
        super().__init__(message, code="CUSTOMER_BLOCKED")
        self.customer_id = customer_id


class CustomerHasActiveRentalsError(CustomerError):
    """Client a des locations actives."""
    
    def __init__(self, customer_id: str):
        super().__init__(
            f"Client '{customer_id}' a des locations actives",
            code="CUSTOMER_HAS_RENTALS"
        )
        self.customer_id = customer_id


# === Exceptions liées à l'éligibilité ===

class EligibilityError(CarRentalError):
    """Exception de base pour les erreurs d'éligibilité."""
    pass


class AgeTooYoungError(EligibilityError):
    """Client trop jeune pour louer ce véhicule."""
    
    def __init__(self, current_age: int, min_age: int):
        super().__init__(
            f"Âge insuffisant ({current_age} ans, minimum requis: {min_age} ans)",
            code="AGE_TOO_YOUNG"
        )
        self.current_age = current_age
        self.min_age = min_age


class LicenseNotHeldError(EligibilityError):
    """Client ne possède pas le permis requis."""
    
    def __init__(self, required_license: str):
        super().__init__(
            f"Permis {required_license} requis, non détenu par le client",
            code="LICENSE_NOT_HELD"
        )
        self.required_license = required_license


class LicenseTooRecentError(EligibilityError):
    """Permis obtenu trop récemment."""
    
    def __init__(self, years_held: int, min_years: int):
        super().__init__(
            f"Permis détenu depuis {years_held} an(s), minimum requis: {min_years} an(s)",
            code="LICENSE_TOO_RECENT"
        )
        self.years_held = years_held
        self.min_years = min_years


# === Exceptions liées aux locations ===

class RentalError(CarRentalError):
    """Exception de base pour les erreurs de location."""
    pass


class RentalNotFoundError(RentalError):
    """Location non trouvée."""
    
    def __init__(self, rental_id: str):
        super().__init__(
            f"Location '{rental_id}' non trouvée",
            code="RENTAL_NOT_FOUND"
        )
        self.rental_id = rental_id


class InvalidRentalDatesError(RentalError):
    """Dates de location invalides."""
    
    def __init__(self, message: str):
        super().__init__(message, code="INVALID_DATES")


class RentalAlreadyActiveError(RentalError):
    """Location déjà active."""
    
    def __init__(self, rental_id: str):
        super().__init__(
            f"Location '{rental_id}' est déjà active",
            code="RENTAL_ALREADY_ACTIVE"
        )
        self.rental_id = rental_id


class RentalNotActiveError(RentalError):
    """Location non active."""
    
    def __init__(self, rental_id: str, current_status: str):
        super().__init__(
            f"Location '{rental_id}' n'est pas active (statut: {current_status})",
            code="RENTAL_NOT_ACTIVE"
        )
        self.rental_id = rental_id
        self.current_status = current_status


class RentalCannotBeCancelledError(RentalError):
    """Location ne peut pas être annulée."""
    
    def __init__(self, rental_id: str, reason: str):
        super().__init__(
            f"Location '{rental_id}' ne peut pas être annulée: {reason}",
            code="RENTAL_CANNOT_CANCEL"
        )
        self.rental_id = rental_id


class InvalidRentalDurationError(RentalError):
    """Durée de location invalide."""
    
    def __init__(self, days: int):
        super().__init__(
            f"Durée de location invalide: {days} jour(s)",
            code="INVALID_DURATION"
        )
        self.days = days


# === Exceptions liées à la persistance ===

class PersistenceError(CarRentalError):
    """Exception de base pour les erreurs de persistance."""
    pass


class DataLoadError(PersistenceError):
    """Erreur lors du chargement des données."""
    
    def __init__(self, filepath: str, reason: str):
        super().__init__(
            f"Impossible de charger '{filepath}': {reason}",
            code="DATA_LOAD_ERROR"
        )
        self.filepath = filepath


class DataSaveError(PersistenceError):
    """Erreur lors de la sauvegarde des données."""
    
    def __init__(self, filepath: str, reason: str):
        super().__init__(
            f"Impossible de sauvegarder '{filepath}': {reason}",
            code="DATA_SAVE_ERROR"
        )
        self.filepath = filepath
