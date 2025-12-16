"""
Tests unitaires pour la classe CarRentalSystem.
"""

import pytest
from datetime import date, timedelta

import sys
sys.path.insert(0, '..')

from car_rental_system import CarRentalSystem
from models.vehicle import Car, Truck, Motorcycle, VehicleCategory, VehicleState
from models.customer import Customer
from models.rental import RentalStatus


class TestCarRentalSystem:
    """Tests pour la classe CarRentalSystem."""
    
    @pytest.fixture
    def system(self):
        """Crée un système de location de test."""
        return CarRentalSystem("TestAgency")
    
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
            vehicle_id="CAR001"
        )
    
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
            vehicle_id="TRK001"
        )
    
    @pytest.fixture
    def sample_customer(self):
        """Crée un client de test."""
        return Customer(
            first_name="Jean",
            last_name="Dupont",
            birth_date=date(1990, 5, 15),
            license_number="123456789012",
            license_types={"B"},
            license_date=date(2010, 6, 20),
            email="jean.dupont@email.com",
            phone="0612345678",
            customer_id="CUST001"
        )
    
    @pytest.fixture
    def young_customer(self):
        """Crée un jeune client de test."""
        today = date.today()
        return Customer(
            first_name="Marie",
            last_name="Martin",
            birth_date=date(today.year - 19, today.month, today.day),
            license_number="987654321098",
            license_types={"B"},
            license_date=date(today.year - 2, today.month, today.day),
            email="marie.martin@email.com",
            phone="0698765432",
            customer_id="CUST002"
        )
    
    @pytest.fixture
    def populated_system(self, system, sample_car, sample_truck, sample_customer):
        """Crée un système avec des données."""
        system.add_vehicle(sample_car)
        system.add_vehicle(sample_truck)
        system.add_customer(sample_customer)
        return system
    
    # === Tests de gestion des véhicules ===
    
    def test_add_vehicle(self, system, sample_car):
        """Test d'ajout de véhicule."""
        assert system.add_vehicle(sample_car) == True
        assert len(system.get_all_vehicles()) == 1
    
    def test_add_vehicle_duplicate(self, system, sample_car):
        """Test d'ajout de véhicule en double."""
        system.add_vehicle(sample_car)
        assert system.add_vehicle(sample_car) == False
    
    def test_remove_vehicle(self, system, sample_car):
        """Test de suppression de véhicule."""
        system.add_vehicle(sample_car)
        assert system.remove_vehicle("CAR001") == True
        assert len(system.get_all_vehicles()) == 0
    
    def test_remove_vehicle_not_found(self, system):
        """Test de suppression de véhicule inexistant."""
        assert system.remove_vehicle("NOTFOUND") == False
    
    def test_get_vehicle(self, populated_system):
        """Test de récupération de véhicule."""
        vehicle = populated_system.get_vehicle("CAR001")
        assert vehicle is not None
        assert vehicle.brand == "Renault"
    
    def test_get_available_vehicles(self, populated_system):
        """Test de récupération des véhicules disponibles."""
        available = populated_system.get_available_vehicles()
        assert len(available) == 2
    
    def test_get_available_vehicles_by_type(self, populated_system):
        """Test de filtrage par type."""
        cars = populated_system.get_available_vehicles(vehicle_type="Voiture")
        assert len(cars) == 1
        assert cars[0].get_vehicle_type() == "Voiture"
    
    def test_get_available_vehicles_by_category(self, populated_system):
        """Test de filtrage par catégorie."""
        economy = populated_system.get_available_vehicles(category=VehicleCategory.ECONOMY)
        assert len(economy) == 1
    
    def test_search_vehicles_by_brand(self, populated_system):
        """Test de recherche par marque."""
        results = populated_system.search_vehicles(brand="Renault")
        assert len(results) == 2
    
    def test_search_vehicles_by_max_rate(self, populated_system):
        """Test de recherche par tarif max."""
        results = populated_system.search_vehicles(max_daily_rate=50.0)
        assert len(results) == 1
    
    # === Tests de gestion des clients ===
    
    def test_add_customer(self, system, sample_customer):
        """Test d'ajout de client."""
        assert system.add_customer(sample_customer) == True
        assert len(system.get_all_customers()) == 1
    
    def test_add_customer_duplicate(self, system, sample_customer):
        """Test d'ajout de client en double."""
        system.add_customer(sample_customer)
        assert system.add_customer(sample_customer) == False
    
    def test_remove_customer(self, system, sample_customer):
        """Test de suppression de client."""
        system.add_customer(sample_customer)
        assert system.remove_customer("CUST001") == True
    
    def test_get_customer(self, populated_system):
        """Test de récupération de client."""
        customer = populated_system.get_customer("CUST001")
        assert customer is not None
        assert customer.first_name == "Jean"
    
    def test_search_customers(self, populated_system):
        """Test de recherche de clients."""
        results = populated_system.search_customers(name="Jean")
        assert len(results) == 1
    
    # === Tests de gestion des locations ===
    
    def test_create_rental_success(self, populated_system):
        """Test de création de location réussie."""
        start = date.today() + timedelta(days=1)
        end = start + timedelta(days=3)
        
        rental, message = populated_system.create_rental(
            "CUST001", "CAR001", start, end
        )
        
        assert rental is not None
        assert "succès" in message.lower()
        assert len(populated_system.get_all_rentals()) == 1
    
    def test_create_rental_customer_not_found(self, populated_system):
        """Test de location avec client inexistant."""
        start = date.today() + timedelta(days=1)
        end = start + timedelta(days=3)
        
        rental, message = populated_system.create_rental(
            "NOTFOUND", "CAR001", start, end
        )
        
        assert rental is None
        assert "client" in message.lower()
    
    def test_create_rental_vehicle_not_found(self, populated_system):
        """Test de location avec véhicule inexistant."""
        start = date.today() + timedelta(days=1)
        end = start + timedelta(days=3)
        
        rental, message = populated_system.create_rental(
            "CUST001", "NOTFOUND", start, end
        )
        
        assert rental is None
        assert "véhicule" in message.lower()
    
    def test_create_rental_age_restriction(self, populated_system, young_customer):
        """Test de restriction d'âge."""
        populated_system.add_customer(young_customer)
        
        # Ajouter une voiture de luxe (âge min 25)
        luxury_car = Car(
            brand="BMW",
            model="M5",
            category=VehicleCategory.LUXURY,
            daily_rate=200.0,
            year=2023,
            license_plate="LX-999-LX",
            vehicle_id="LUX001"
        )
        populated_system.add_vehicle(luxury_car)
        
        start = date.today() + timedelta(days=1)
        end = start + timedelta(days=3)
        
        rental, message = populated_system.create_rental(
            "CUST002", "LUX001", start, end
        )
        
        assert rental is None
        assert "âge" in message.lower()
    
    def test_create_rental_vehicle_not_available(self, populated_system):
        """Test de location avec véhicule non disponible."""
        start = date.today() + timedelta(days=1)
        end = start + timedelta(days=3)
        
        # Première location
        populated_system.create_rental("CUST001", "CAR001", start, end)
        
        # Deuxième location sur la même période
        rental, message = populated_system.create_rental(
            "CUST001", "CAR001", start, end
        )
        
        assert rental is None
        assert "disponible" in message.lower()
    
    def test_complete_rental(self, populated_system):
        """Test de fin de location."""
        # Créer une location qui commence aujourd'hui
        start = date.today()
        end = start + timedelta(days=3)
        
        rental, _ = populated_system.create_rental(
            "CUST001", "CAR001", start, end
        )
        
        # Terminer la location
        cost, message = populated_system.complete_rental(
            rental.id, date.today(), 10500.0
        )
        
        assert cost is not None
        assert cost > 0
        
        # Vérifier que le véhicule est à nouveau disponible
        vehicle = populated_system.get_vehicle("CAR001")
        assert vehicle.state == VehicleState.AVAILABLE
    
    def test_cancel_rental(self, populated_system):
        """Test d'annulation de location."""
        start = date.today() + timedelta(days=10)
        end = start + timedelta(days=3)
        
        rental, _ = populated_system.create_rental(
            "CUST001", "CAR001", start, end
        )
        
        fee, message = populated_system.cancel_rental(rental.id)
        
        assert fee == 0  # Annulation gratuite à plus de 7 jours
        assert "annulée" in message.lower()
    
    def test_extend_rental(self, populated_system):
        """Test de prolongation de location."""
        start = date.today() + timedelta(days=1)
        end = start + timedelta(days=3)
        
        rental, _ = populated_system.create_rental(
            "CUST001", "CAR001", start, end
        )
        
        new_end = end + timedelta(days=2)
        success, message = populated_system.extend_rental(rental.id, new_end)
        
        assert success == True
    
    def test_get_active_rentals(self, populated_system):
        """Test de récupération des locations actives."""
        start = date.today()
        end = start + timedelta(days=3)
        
        populated_system.create_rental("CUST001", "CAR001", start, end)
        
        active = populated_system.get_active_rentals()
        assert len(active) == 1
    
    def test_get_customer_rentals(self, populated_system):
        """Test de récupération des locations d'un client."""
        start = date.today() + timedelta(days=1)
        end = start + timedelta(days=3)
        
        populated_system.create_rental("CUST001", "CAR001", start, end)
        
        rentals = populated_system.get_customer_rentals("CUST001")
        assert len(rentals) == 1
    
    # === Tests des rapports ===
    
    def test_generate_available_vehicles_report(self, populated_system):
        """Test du rapport des véhicules disponibles."""
        report = populated_system.generate_available_vehicles_report()
        
        assert report['report_type'] == 'Véhicules disponibles'
        assert report['total_available'] == 2
        assert report['total_fleet'] == 2
    
    def test_generate_active_rentals_report(self, populated_system):
        """Test du rapport des locations actives."""
        start = date.today()
        end = start + timedelta(days=3)
        populated_system.create_rental("CUST001", "CAR001", start, end)
        
        report = populated_system.generate_active_rentals_report()
        
        assert report['report_type'] == 'Locations en cours'
        assert report['total_active'] == 1
    
    def test_generate_revenue_report(self, populated_system):
        """Test du rapport de chiffre d'affaires."""
        report = populated_system.generate_revenue_report()
        
        assert report['report_type'] == "Chiffre d'affaires"
        assert 'total_revenue' in report
    
    def test_generate_statistics_report(self, populated_system):
        """Test du rapport de statistiques."""
        report = populated_system.generate_statistics_report()
        
        assert report['report_type'] == 'Statistiques générales'
        assert report['fleet']['total_vehicles'] == 2
        assert report['customers']['total_customers'] == 1
    
    def test_get_summary(self, populated_system):
        """Test du résumé."""
        summary = populated_system.get_summary()
        
        assert summary['agency'] == "TestAgency"
        assert summary['total_vehicles'] == 2
        assert summary['total_customers'] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
