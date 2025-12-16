"""
Tests unitaires pour la classe Customer.
"""

import pytest
from datetime import date, timedelta

import sys
sys.path.insert(0, '..')

from models.customer import Customer


class TestCustomer:
    """Tests pour la classe Customer."""
    
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
            address="123 Rue de Paris, 75001 Paris"
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
            license_types={"B", "A1"},
            license_date=date(today.year - 1, today.month, today.day),
            email="marie.martin@email.com",
            phone="0698765432"
        )
    
    @pytest.fixture
    def new_driver(self):
        """Crée un conducteur avec permis récent."""
        today = date.today()
        return Customer(
            first_name="Pierre",
            last_name="Bernard",
            birth_date=date(1995, 3, 10),
            license_number="111222333444",
            license_types={"B"},
            license_date=date(today.year, today.month, today.day) - timedelta(days=180),
            email="pierre.bernard@email.com",
            phone="0611223344"
        )
    
    def test_customer_creation(self, sample_customer):
        """Test de création d'un client."""
        assert sample_customer.first_name == "Jean"
        assert sample_customer.last_name == "Dupont"
        assert sample_customer.email == "jean.dupont@email.com"
        assert sample_customer.phone == "0612345678"
    
    def test_customer_full_name(self, sample_customer):
        """Test du nom complet."""
        assert sample_customer.full_name == "Jean Dupont"
    
    def test_customer_age(self, sample_customer):
        """Test du calcul de l'âge."""
        expected_age = date.today().year - 1990
        if (date.today().month, date.today().day) < (5, 15):
            expected_age -= 1
        assert sample_customer.age == expected_age
    
    def test_customer_years_of_license(self, sample_customer):
        """Test du calcul des années de permis."""
        expected_years = date.today().year - 2010
        if (date.today().month, date.today().day) < (6, 20):
            expected_years -= 1
        assert sample_customer.years_of_license == expected_years
    
    def test_customer_has_license(self, sample_customer):
        """Test de vérification de permis."""
        assert sample_customer.has_license("B") == True
        assert sample_customer.has_license("A") == False
    
    def test_customer_add_license(self, sample_customer):
        """Test d'ajout de permis."""
        sample_customer.add_license_type("A")
        assert sample_customer.has_license("A") == True
    
    def test_customer_can_rent_vehicle_success(self, sample_customer):
        """Test de vérification de location réussie."""
        can_rent, reason = sample_customer.can_rent_vehicle("B", 21)
        assert can_rent == True
        assert reason == "OK"
    
    def test_customer_cannot_rent_wrong_license(self, sample_customer):
        """Test de refus pour mauvais permis."""
        can_rent, reason = sample_customer.can_rent_vehicle("A", 21)
        assert can_rent == False
        assert "Permis A requis" in reason
    
    def test_customer_cannot_rent_too_young(self, young_customer):
        """Test de refus pour âge insuffisant."""
        can_rent, reason = young_customer.can_rent_vehicle("B", 21)
        assert can_rent == False
        assert "Âge insuffisant" in reason
    
    def test_customer_cannot_rent_new_driver(self, new_driver):
        """Test de refus pour permis trop récent."""
        can_rent, reason = new_driver.can_rent_vehicle("B", 21)
        assert can_rent == False
        assert "au moins 1 an" in reason
    
    def test_customer_blocked(self, sample_customer):
        """Test du blocage d'un client."""
        sample_customer.block("Impayés")
        assert sample_customer.is_blocked == True
        assert sample_customer.blocked_reason == "Impayés"
        
        can_rent, reason = sample_customer.can_rent_vehicle("B", 21)
        assert can_rent == False
        assert "bloqué" in reason.lower()
    
    def test_customer_unblock(self, sample_customer):
        """Test du déblocage d'un client."""
        sample_customer.block("Test")
        sample_customer.unblock()
        assert sample_customer.is_blocked == False
        assert sample_customer.blocked_reason is None
    
    def test_customer_rental_history(self, sample_customer):
        """Test de l'historique de locations."""
        assert sample_customer.get_total_rentals() == 0
        
        sample_customer.add_rental("RENT001")
        sample_customer.add_rental("RENT002")
        
        assert sample_customer.get_total_rentals() == 2
        assert "RENT001" in sample_customer.rental_history
        assert len(sample_customer.active_rentals) == 2
    
    def test_customer_complete_rental(self, sample_customer):
        """Test de la fin d'une location."""
        sample_customer.add_rental("RENT001")
        assert sample_customer.complete_rental("RENT001") == True
        assert len(sample_customer.active_rentals) == 0
        assert sample_customer.get_total_rentals() == 1  # Reste dans l'historique
    
    def test_customer_loyalty_not_loyal(self, sample_customer):
        """Test fidélité - pas encore fidèle."""
        assert sample_customer.is_loyal_customer() == False
        assert sample_customer.get_loyalty_discount() == 0.0
    
    def test_customer_loyalty_5_rentals(self, sample_customer):
        """Test fidélité - 5 locations."""
        for i in range(5):
            sample_customer.add_rental(f"RENT{i:03d}")
        
        assert sample_customer.is_loyal_customer() == True
        assert sample_customer.get_loyalty_discount() == 0.05
    
    def test_customer_loyalty_10_rentals(self, sample_customer):
        """Test fidélité - 10 locations."""
        for i in range(10):
            sample_customer.add_rental(f"RENT{i:03d}")
        
        assert sample_customer.get_loyalty_discount() == 0.10
    
    def test_customer_loyalty_20_rentals(self, sample_customer):
        """Test fidélité - 20 locations."""
        for i in range(20):
            sample_customer.add_rental(f"RENT{i:03d}")
        
        assert sample_customer.get_loyalty_discount() == 0.15
    
    def test_customer_to_dict(self, sample_customer):
        """Test de la conversion en dictionnaire."""
        data = sample_customer.to_dict()
        
        assert data['first_name'] == "Jean"
        assert data['last_name'] == "Dupont"
        assert data['full_name'] == "Jean Dupont"
        assert data['email'] == "jean.dupont@email.com"
        assert 'B' in data['license_types']
        assert 'id' in data
    
    def test_customer_str(self, sample_customer):
        """Test de la représentation en chaîne."""
        string = str(sample_customer)
        assert "Jean Dupont" in string
        assert "ans" in string
    
    def test_customer_properties_setters(self, sample_customer):
        """Test des setters de propriétés."""
        sample_customer.first_name = "Jacques"
        sample_customer.last_name = "Martin"
        sample_customer.email = "jacques@test.com"
        sample_customer.phone = "0699999999"
        sample_customer.address = "456 Rue Test"
        
        assert sample_customer.first_name == "Jacques"
        assert sample_customer.last_name == "Martin"
        assert sample_customer.full_name == "Jacques Martin"
        assert sample_customer.email == "jacques@test.com"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
