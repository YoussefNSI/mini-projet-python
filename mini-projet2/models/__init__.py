# Models package
from .vehicle import Vehicle, Car, Truck, Motorcycle, VehicleState, VehicleCategory
from .customer import Customer
from .rental import Rental, RentalStatus

__all__ = [
    # Classes principales
    'Vehicle', 'Car', 'Truck', 'Motorcycle', 
    'VehicleState', 'VehicleCategory',
    'Customer', 
    'Rental', 'RentalStatus',
]
