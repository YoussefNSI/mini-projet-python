"""
Tests unitaires pour la classe Rental.
"""

import pytest
from datetime import date, timedelta

import sys
sys.path.insert(0, '..')

from models.rental import Rental, RentalStatus


class TestRental:
    """Tests pour la classe Rental."""
    
    @pytest.fixture
    def future_date(self):
        """Date de début dans le futur."""
        return date.today() + timedelta(days=1)
    
    @pytest.fixture
    def sample_rental(self, future_date):
        """Crée une location de test."""
        return Rental(
            customer_id="CUST001",
            vehicle_id="VEH001",
            start_date=future_date,
            end_date=future_date + timedelta(days=5),
            daily_rate=50.0,
            start_mileage=10000.0
        )
    
    @pytest.fixture
    def active_rental(self, future_date):
        """Crée une location active."""
        rental = Rental(
            customer_id="CUST001",
            vehicle_id="VEH001",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=5),
            daily_rate=50.0
        )
        rental._status = RentalStatus.ACTIVE
        return rental
    
    def test_rental_creation(self, sample_rental, future_date):
        """Test de création d'une location."""
        assert sample_rental.customer_id == "CUST001"
        assert sample_rental.vehicle_id == "VEH001"
        assert sample_rental.start_date == future_date
        assert sample_rental.daily_rate == 50.0
        assert sample_rental.status == RentalStatus.RESERVED
    
    def test_rental_invalid_dates(self, future_date):
        """Test de dates invalides."""
        with pytest.raises(ValueError):
            Rental(
                customer_id="CUST001",
                vehicle_id="VEH001",
                start_date=future_date + timedelta(days=5),
                end_date=future_date,  # Fin avant début
                daily_rate=50.0
            )
    
    def test_rental_past_start_date(self):
        """Test de date de début dans le passé."""
        with pytest.raises(ValueError):
            Rental(
                customer_id="CUST001",
                vehicle_id="VEH001",
                start_date=date.today() - timedelta(days=1),
                end_date=date.today() + timedelta(days=5),
                daily_rate=50.0
            )
    
    def test_rental_planned_duration(self, sample_rental):
        """Test du calcul de la durée prévue."""
        assert sample_rental.planned_duration == 6  # 5 jours + 1
    
    def test_rental_base_cost(self, sample_rental):
        """Test du calcul du coût de base."""
        expected = 50.0 * 6  # 6 jours
        assert sample_rental.calculate_base_cost() == expected
    
    def test_rental_cost_weekly_discount(self, future_date):
        """Test de la réduction hebdomadaire."""
        rental = Rental(
            customer_id="CUST001",
            vehicle_id="VEH001",
            start_date=future_date,
            end_date=future_date + timedelta(days=9),  # 10 jours
            daily_rate=50.0
        )
        expected = 50.0 * 10 * 0.90  # 10% de réduction
        assert rental.calculate_base_cost() == expected
    
    def test_rental_cost_monthly_discount(self, future_date):
        """Test de la réduction mensuelle."""
        rental = Rental(
            customer_id="CUST001",
            vehicle_id="VEH001",
            start_date=future_date,
            end_date=future_date + timedelta(days=29),  # 30 jours
            daily_rate=50.0
        )
        expected = 50.0 * 30 * 0.80  # 20% de réduction
        assert rental.calculate_base_cost() == expected
    
    def test_rental_apply_discount(self, sample_rental):
        """Test de l'application d'une réduction."""
        sample_rental.apply_discount(0.10)  # 10%
        assert sample_rental.discount_applied == 0.10
        
        base_cost = sample_rental.calculate_base_cost()
        expected = base_cost * 0.90
        assert sample_rental.calculate_total_cost() == expected
    
    def test_rental_start(self):
        """Test du démarrage d'une location."""
        rental = Rental(
            customer_id="CUST001",
            vehicle_id="VEH001",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=5),
            daily_rate=50.0
        )
        assert rental.start_rental() == True
        assert rental.status == RentalStatus.ACTIVE
    
    def test_rental_start_future_fails(self, sample_rental):
        """Test qu'on ne peut pas démarrer une location future."""
        assert sample_rental.start_rental() == False
    
    def test_rental_complete(self, active_rental):
        """Test de la fin d'une location."""
        return_date = date.today() + timedelta(days=3)
        total = active_rental.complete_rental(return_date, 10500.0)
        
        assert active_rental.status == RentalStatus.COMPLETED
        assert active_rental.actual_return_date == return_date
        assert active_rental.end_mileage == 10500.0
        assert total > 0
    
    def test_rental_complete_late(self, active_rental):
        """Test de la fin avec retard."""
        # Retour 2 jours après la fin prévue
        late_date = active_rental.end_date + timedelta(days=2)
        active_rental.complete_rental(late_date)
        
        assert active_rental.days_late == 2
        assert active_rental.penalty == 2 * Rental.LATE_RETURN_PENALTY_PER_DAY
    
    def test_rental_cancel_free(self, future_date):
        """Test d'annulation gratuite (plus de 7 jours)."""
        rental = Rental(
            customer_id="CUST001",
            vehicle_id="VEH001",
            start_date=future_date + timedelta(days=10),
            end_date=future_date + timedelta(days=15),
            daily_rate=50.0
        )
        fee = rental.cancel_rental()
        assert fee == 0
        assert rental.status == RentalStatus.CANCELLED
    
    def test_rental_cancel_with_fee(self, future_date):
        """Test d'annulation avec frais."""
        rental = Rental(
            customer_id="CUST001",
            vehicle_id="VEH001",
            start_date=future_date + timedelta(days=5),
            end_date=future_date + timedelta(days=10),
            daily_rate=50.0
        )
        fee = rental.cancel_rental()
        assert fee > 0
        assert rental.status == RentalStatus.CANCELLED
    
    def test_rental_cancel_completed_fails(self, active_rental):
        """Test qu'on ne peut pas annuler une location terminée."""
        active_rental.complete_rental(date.today())
        
        with pytest.raises(ValueError):
            active_rental.cancel_rental()
    
    def test_rental_extend(self, sample_rental, future_date):
        """Test de prolongation."""
        new_end = future_date + timedelta(days=10)
        assert sample_rental.extend_rental(new_end) == True
        assert sample_rental.end_date == new_end
    
    def test_rental_extend_earlier_fails(self, sample_rental, future_date):
        """Test qu'on ne peut pas raccourcir une location."""
        earlier_end = future_date + timedelta(days=2)
        assert sample_rental.extend_rental(earlier_end) == False
    
    def test_rental_is_overdue(self, active_rental):
        """Test de vérification de retard."""
        # Location non en retard
        assert active_rental.is_overdue() == False
        
        # Simuler un retard
        active_rental._end_date = date.today() - timedelta(days=1)
        assert active_rental.is_overdue() == True
    
    def test_rental_days_remaining(self, active_rental):
        """Test des jours restants."""
        expected = (active_rental.end_date - date.today()).days
        assert active_rental.days_remaining() == expected
    
    def test_rental_distance_traveled(self, sample_rental):
        """Test du calcul de distance."""
        assert sample_rental.distance_traveled is None
        
        sample_rental._end_mileage = 10500.0
        assert sample_rental.distance_traveled == 500.0
    
    def test_rental_notes(self, sample_rental):
        """Test des notes."""
        sample_rental.notes = "Client VIP"
        assert sample_rental.notes == "Client VIP"
    
    def test_rental_to_dict(self, sample_rental):
        """Test de la conversion en dictionnaire."""
        data = sample_rental.to_dict()
        
        assert data['customer_id'] == "CUST001"
        assert data['vehicle_id'] == "VEH001"
        assert data['status'] == "réservée"
        assert data['daily_rate'] == 50.0
        assert 'id' in data
        assert 'total_cost' in data
    
    def test_rental_str(self, sample_rental):
        """Test de la représentation en chaîne."""
        string = str(sample_rental)
        assert "Location" in string
        assert "réservée" in string


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
