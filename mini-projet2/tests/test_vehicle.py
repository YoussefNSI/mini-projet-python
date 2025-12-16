"""
Tests unitaires pour les classes de véhicules.
"""

import pytest
from datetime import date

import sys
sys.path.insert(0, '..')

from models.vehicle import (
    Vehicle, Car, Truck, Motorcycle,
    VehicleState, VehicleCategory
)


class TestVehicleState:
    """Tests pour l'énumération VehicleState."""
    
    def test_vehicle_states_exist(self):
        assert VehicleState.AVAILABLE.value == "disponible"
        assert VehicleState.RENTED.value == "loué"
        assert VehicleState.MAINTENANCE.value == "en maintenance"
        assert VehicleState.OUT_OF_SERVICE.value == "hors service"


class TestVehicleCategory:
    """Tests pour l'énumération VehicleCategory."""
    
    def test_vehicle_categories_exist(self):
        assert VehicleCategory.ECONOMY.value == "économique"
        assert VehicleCategory.STANDARD.value == "standard"
        assert VehicleCategory.PREMIUM.value == "premium"
        assert VehicleCategory.LUXURY.value == "luxe"


class TestCar:
    """Tests pour la classe Car."""
    
    @pytest.fixture
    def sample_car(self):
        """Crée une voiture de test."""
        return Car(
            brand="Renault",
            model="Clio",
            category=VehicleCategory.ECONOMY,
            daily_rate=45.0,
            year=2022,
            license_plate="AB-123-CD",
            num_doors=5,
            num_seats=5,
            fuel_type="essence",
            transmission="manuelle"
        )
    
    @pytest.fixture
    def luxury_car(self):
        """Crée une voiture de luxe de test."""
        return Car(
            brand="Mercedes",
            model="Classe S",
            category=VehicleCategory.LUXURY,
            daily_rate=250.0,
            year=2023,
            license_plate="LX-999-LX"
        )
    
    def test_car_creation(self, sample_car):
        """Test de création d'une voiture."""
        assert sample_car.brand == "Renault"
        assert sample_car.model == "Clio"
        assert sample_car.category == VehicleCategory.ECONOMY
        assert sample_car.daily_rate == 45.0
        assert sample_car.year == 2022
        assert sample_car.license_plate == "AB-123-CD"
        assert sample_car.num_doors == 5
        assert sample_car.num_seats == 5
    
    def test_car_initial_state(self, sample_car):
        """Test de l'état initial d'une voiture."""
        assert sample_car.state == VehicleState.AVAILABLE
        assert sample_car.is_available() == True
        assert sample_car.mileage == 0.0
    
    def test_car_type(self, sample_car):
        """Test du type de véhicule."""
        assert sample_car.get_vehicle_type() == "Voiture"
    
    def test_car_required_license(self, sample_car):
        """Test du permis requis."""
        assert sample_car.get_required_license() == "B"
    
    def test_car_minimum_age_economy(self, sample_car):
        """Test de l'âge minimum pour voiture économique."""
        assert sample_car.get_minimum_driver_age() == 21
    
    def test_car_minimum_age_luxury(self, luxury_car):
        """Test de l'âge minimum pour voiture de luxe."""
        assert luxury_car.get_minimum_driver_age() == 25
    
    def test_car_rent(self, sample_car):
        """Test de la location d'une voiture."""
        assert sample_car.rent() == True
        assert sample_car.state == VehicleState.RENTED
        assert sample_car.is_available() == False
    
    def test_car_rent_twice_fails(self, sample_car):
        """Test qu'on ne peut pas louer deux fois."""
        sample_car.rent()
        assert sample_car.rent() == False
    
    def test_car_return(self, sample_car):
        """Test du retour d'une voiture."""
        sample_car.rent()
        assert sample_car.return_vehicle(100.0) == True
        assert sample_car.state == VehicleState.AVAILABLE
        assert sample_car.mileage == 100.0
    
    def test_car_return_not_rented_fails(self, sample_car):
        """Test qu'on ne peut pas retourner une voiture non louée."""
        assert sample_car.return_vehicle() == False
    
    def test_car_maintenance(self, sample_car):
        """Test de l'envoi en maintenance."""
        assert sample_car.send_to_maintenance("Révision annuelle") == True
        assert sample_car.state == VehicleState.MAINTENANCE
        assert len(sample_car.maintenance_history) == 1
    
    def test_car_complete_maintenance(self, sample_car):
        """Test de la fin de maintenance."""
        sample_car.send_to_maintenance("Révision")
        assert sample_car.complete_maintenance("Révision terminée", 150.0) == True
        assert sample_car.state == VehicleState.AVAILABLE
        assert len(sample_car.maintenance_history) == 2
    
    def test_car_cannot_maintenance_when_rented(self, sample_car):
        """Test qu'on ne peut pas envoyer en maintenance si loué."""
        sample_car.rent()
        assert sample_car.send_to_maintenance("Test") == False
    
    def test_car_rental_cost_basic(self, sample_car):
        """Test du calcul de coût basique."""
        cost = sample_car.calculate_rental_cost(3)
        assert cost == 45.0 * 3  # 135€
    
    def test_car_rental_cost_weekly_discount(self, sample_car):
        """Test du calcul avec réduction hebdomadaire."""
        cost = sample_car.calculate_rental_cost(7)
        expected = 45.0 * 7 * 0.90  # 10% de réduction
        assert cost == expected
    
    def test_car_rental_cost_monthly_discount(self, sample_car):
        """Test du calcul avec réduction mensuelle."""
        cost = sample_car.calculate_rental_cost(30)
        expected = 45.0 * 30 * 0.80  # 20% de réduction
        assert cost == expected
    
    def test_car_rental_cost_invalid_days(self, sample_car):
        """Test que les jours négatifs lèvent une exception."""
        with pytest.raises(ValueError):
            sample_car.calculate_rental_cost(0)
        with pytest.raises(ValueError):
            sample_car.calculate_rental_cost(-1)
    
    def test_car_mileage_cannot_decrease(self, sample_car):
        """Test que le kilométrage ne peut pas diminuer."""
        sample_car.mileage = 100
        with pytest.raises(ValueError):
            sample_car.mileage = 50
    
    def test_car_daily_rate_cannot_be_negative(self, sample_car):
        """Test que le tarif ne peut pas être négatif."""
        with pytest.raises(ValueError):
            sample_car.daily_rate = -10
    
    def test_car_to_dict(self, sample_car):
        """Test de la conversion en dictionnaire."""
        data = sample_car.to_dict()
        assert data['brand'] == "Renault"
        assert data['model'] == "Clio"
        assert data['type'] == "Voiture"
        assert data['num_doors'] == 5
        assert 'id' in data
    
    def test_car_str(self, sample_car):
        """Test de la représentation en chaîne."""
        assert "Voiture" in str(sample_car)
        assert "Renault" in str(sample_car)
        assert "Clio" in str(sample_car)
    
    def test_car_needs_maintenance(self, sample_car):
        """Test de la vérification de maintenance."""
        assert sample_car.needs_maintenance() == False
        sample_car._mileage = 10000
        assert sample_car.needs_maintenance() == True


class TestTruck:
    """Tests pour la classe Truck."""
    
    @pytest.fixture
    def sample_truck(self):
        """Crée un camion de test."""
        return Truck(
            brand="Renault",
            model="Master",
            category=VehicleCategory.UTILITY,
            daily_rate=80.0,
            year=2021,
            license_plate="TR-456-UK",
            cargo_capacity=12.0,
            max_weight=3000,
            has_tail_lift=True
        )
    
    @pytest.fixture
    def heavy_truck(self):
        """Crée un camion lourd de test."""
        return Truck(
            brand="Mercedes",
            model="Actros",
            category=VehicleCategory.UTILITY,
            daily_rate=150.0,
            year=2020,
            license_plate="HV-789-HV",
            cargo_capacity=50.0,
            max_weight=10000
        )
    
    def test_truck_creation(self, sample_truck):
        """Test de création d'un camion."""
        assert sample_truck.brand == "Renault"
        assert sample_truck.cargo_capacity == 12.0
        assert sample_truck.max_weight == 3000
        assert sample_truck.has_tail_lift == True
    
    def test_truck_type(self, sample_truck):
        """Test du type de véhicule."""
        assert sample_truck.get_vehicle_type() == "Camion"
    
    def test_truck_license_light(self, sample_truck):
        """Test du permis pour camion léger."""
        assert sample_truck.get_required_license() == "B"
    
    def test_truck_license_medium(self):
        """Test du permis pour camion moyen."""
        truck = Truck(
            brand="Iveco",
            model="Daily",
            category=VehicleCategory.UTILITY,
            daily_rate=100.0,
            year=2022,
            license_plate="MD-123-MD",
            cargo_capacity=20.0,
            max_weight=5000
        )
        assert truck.get_required_license() == "C1"
    
    def test_truck_license_heavy(self, heavy_truck):
        """Test du permis pour camion lourd."""
        assert heavy_truck.get_required_license() == "C"
    
    def test_truck_minimum_age_light(self, sample_truck):
        """Test de l'âge minimum pour camion léger."""
        assert sample_truck.get_minimum_driver_age() == 21  # Camion léger: 21 ans
    
    def test_truck_minimum_age_heavy(self, heavy_truck):
        """Test de l'âge minimum pour camion lourd."""
        assert heavy_truck.get_minimum_driver_age() == 25  # Camion lourd (>7.5T): 25 ans


class TestMotorcycle:
    """Tests pour la classe Motorcycle."""
    
    @pytest.fixture
    def small_motorcycle(self):
        """Crée une petite moto de test."""
        return Motorcycle(
            brand="Honda",
            model="CB125R",
            category=VehicleCategory.ECONOMY,
            daily_rate=35.0,
            year=2022,
            license_plate="MO-125-TO",
            engine_size=125,
            motorcycle_type="standard"
        )
    
    @pytest.fixture
    def large_motorcycle(self):
        """Crée une grosse moto de test."""
        return Motorcycle(
            brand="Kawasaki",
            model="Ninja ZX-10R",
            category=VehicleCategory.SPORT,
            daily_rate=120.0,
            year=2023,
            license_plate="SP-999-RT",
            engine_size=1000,
            motorcycle_type="sport"
        )
    
    def test_motorcycle_creation(self, small_motorcycle):
        """Test de création d'une moto."""
        assert small_motorcycle.brand == "Honda"
        assert small_motorcycle.engine_size == 125
        assert small_motorcycle.motorcycle_type == "standard"
    
    def test_motorcycle_type(self, small_motorcycle):
        """Test du type de véhicule."""
        assert small_motorcycle.get_vehicle_type() == "Moto"
    
    def test_motorcycle_license_small(self, small_motorcycle):
        """Test du permis pour petite moto."""
        assert small_motorcycle.get_required_license() == "A1"
    
    def test_motorcycle_license_large(self, large_motorcycle):
        """Test du permis pour grosse moto."""
        assert large_motorcycle.get_required_license() == "A"
    
    def test_motorcycle_minimum_age_small(self, small_motorcycle):
        """Test de l'âge minimum pour petite moto."""
        assert small_motorcycle.get_minimum_driver_age() == 18
    
    def test_motorcycle_minimum_age_large(self, large_motorcycle):
        """Test de l'âge minimum pour grosse moto."""
        assert large_motorcycle.get_minimum_driver_age() == 21  # Moto >125cc: 21 ans
    
    def test_motorcycle_rental_cost_with_insurance(self, small_motorcycle):
        """Test du coût avec supplément assurance (+15%)."""
        cost = small_motorcycle.calculate_rental_cost(3)
        expected = (35.0 * 3) * 1.15  # Base * 1.15 pour supplément assurance
        assert cost == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
