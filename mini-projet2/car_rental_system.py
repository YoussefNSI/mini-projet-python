"""
Module principal du système de location de voitures.
Contient la classe centrale CarRentalSystem.
"""

from datetime import date, datetime, timedelta
from typing import Optional, List, Dict, Tuple
from collections import defaultdict

from models.vehicle import Vehicle, Car, Truck, Motorcycle, VehicleState, VehicleCategory
from models.customer import Customer
from models.rental import Rental, RentalStatus


class CarRentalSystem:
    """
    Classe centrale du système de location de voitures.
    
    Gère l'ensemble des opérations de l'agence:
    - Gestion de la flotte de véhicules
    - Gestion des clients
    - Gestion des locations
    - Génération de rapports
    """
    
    def __init__(self, agency_name: str = "ShopTaLoc31"):
        self._agency_name = agency_name
        self._vehicles: Dict[str, Vehicle] = {}
        self._customers: Dict[str, Customer] = {}
        self._rentals: Dict[str, Rental] = {}
        self._created_at = datetime.now()
    
    # === Gestion des véhicules ===
    
    def add_vehicle(self, vehicle: Vehicle) -> bool:
        """
        Ajoute un véhicule à la flotte
        
        Args:
            vehicle: Le véhicule à ajouter
            
        Returns:
            True si ajouté avec succès
        """
        if vehicle.id in self._vehicles:
            return False
        self._vehicles[vehicle.id] = vehicle
        return True
    
    def remove_vehicle(self, vehicle_id: str) -> bool:
        """
        Retire un véhicule de la flotte.
        
        Args:
            vehicle_id: ID du véhicule à retirer
            
        Returns:
            True si retiré avec succès
        """
        if vehicle_id not in self._vehicles:
            return False
        
        vehicle = self._vehicles[vehicle_id]
        if vehicle.state == VehicleState.RENTED:
            return False  # Ne peut pas retirer un véhicule loué
        
        del self._vehicles[vehicle_id]
        return True
    
    def get_vehicle(self, vehicle_id: str) -> Optional[Vehicle]:
        """Récupère un véhicule par son ID."""
        return self._vehicles.get(vehicle_id)
    
    def get_all_vehicles(self) -> List[Vehicle]:
        """Retourne la liste de tous les véhicules."""
        return list(self._vehicles.values())
    
    def get_available_vehicles(
        self,
        vehicle_type: Optional[str] = None,
        category: Optional[VehicleCategory] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Vehicle]:
        """
        Retourne les véhicules disponibles selon les critères.
        
        Args:
            vehicle_type: Type de véhicule (Voiture, Camion, Moto)
            category: Catégorie de véhicule
            start_date: Date de début souhaitée
            end_date: Date de fin souhaitée
            
        Returns:
            Liste des véhicules disponibles
        """
        available = []
        
        for vehicle in self._vehicles.values():
            # Vérifier l'état du véhicule
            if not vehicle.is_available():
                continue
            
            # Filtrer par type
            if vehicle_type and vehicle.get_vehicle_type() != vehicle_type:
                continue
            
            # Filtrer par catégorie
            if category and vehicle.category != category:
                continue
            
            # Vérifier la disponibilité sur la période
            if start_date and end_date:
                if not self._is_vehicle_available_for_period(vehicle.id, start_date, end_date):
                    continue
            
            available.append(vehicle)
        
        return available
    
    def _is_vehicle_available_for_period(
        self,
        vehicle_id: str,
        start_date: date,
        end_date: date
    ) -> bool:
        """Vérifie si un véhicule est disponible sur une période donnée."""
        for rental in self._rentals.values():
            if rental.vehicle_id != vehicle_id:
                continue
            
            if rental.status in [RentalStatus.CANCELLED, RentalStatus.COMPLETED]:
                continue
            
            # Vérifier le chevauchement des dates
            if not (end_date < rental.start_date or start_date > rental.end_date):
                return False
        
        return True
    
    def search_vehicles(
        self,
        brand: Optional[str] = None,
        model: Optional[str] = None,
        max_daily_rate: Optional[float] = None,
        min_year: Optional[int] = None
    ) -> List[Vehicle]:
        """
        Recherche des véhicules selon plusieurs critères.
        
        Args:
            brand: Marque recherchée
            model: Modèle recherché
            max_daily_rate: Tarif maximum journalier
            min_year: Année minimum
            
        Returns:
            Liste des véhicules correspondants
        """
        results = []
        
        for vehicle in self._vehicles.values():
            if brand and brand.lower() not in vehicle.brand.lower():
                continue
            if model and model.lower() not in vehicle.model.lower():
                continue
            if max_daily_rate and vehicle.daily_rate > max_daily_rate:
                continue
            if min_year and vehicle.year < min_year:
                continue
            
            results.append(vehicle)
        
        return results
    
    # === Gestion des clients ===
    
    def add_customer(self, customer: Customer) -> bool:
        """
        Ajoute un client.
        
        Args:
            customer: Le client à ajouter
            
        Returns:
            True si ajouté avec succès
        """
        if customer.id in self._customers:
            return False
        self._customers[customer.id] = customer
        return True
    
    def remove_customer(self, customer_id: str) -> bool:
        """
        Retire un client.
        
        Args:
            customer_id: ID du client à retirer
            
        Returns:
            True si retiré avec succès
        """
        if customer_id not in self._customers:
            return False
        
        customer = self._customers[customer_id]
        if customer.active_rentals:
            return False  # Ne peut pas retirer un client avec des locations actives
        
        del self._customers[customer_id]
        return True
    
    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Récupère un client par son ID."""
        return self._customers.get(customer_id)
    
    def get_all_customers(self) -> List[Customer]:
        """Retourne la liste de tous les clients."""
        return list(self._customers.values())
    
    def search_customers(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None
    ) -> List[Customer]:
        """
        Recherche des clients.
        
        Args:
            name: Nom ou prénom recherché
            email: Email recherché
            
        Returns:
            Liste des clients correspondants
        """
        results = []
        
        for customer in self._customers.values():
            if name:
                search_name = name.lower()
                if (search_name not in customer.first_name.lower() and 
                    search_name not in customer.last_name.lower()):
                    continue
            if email and email.lower() not in customer.email.lower():
                continue
            
            results.append(customer)
        
        return results
    
    # === Gestion des locations ===
    
    def create_rental(
        self,
        customer_id: str,
        vehicle_id: str,
        start_date: date,
        end_date: date
    ) -> Tuple[Optional[Rental], str]:
        """
        Crée une nouvelle location.
        
        Args:
            customer_id: ID du client
            vehicle_id: ID du véhicule
            start_date: Date de début
            end_date: Date de fin
            
        Returns:
            Tuple (Rental ou None, message d'erreur/succès)
        """
        # Vérifier que le client existe
        customer = self._customers.get(customer_id)
        if not customer:
            return None, "Client non trouvé"
        
        # Vérifier que le véhicule existe
        vehicle = self._vehicles.get(vehicle_id)
        if not vehicle:
            return None, "Véhicule non trouvé"
        
        # Vérifier que le client peut louer ce véhicule
        can_rent, reason = customer.can_rent_vehicle(
            vehicle.get_required_license(),
            vehicle.get_minimum_driver_age()
        )
        if not can_rent:
            return None, reason
        
        # Vérifier la disponibilité du véhicule
        if not self._is_vehicle_available_for_period(vehicle_id, start_date, end_date):
            return None, "Véhicule non disponible pour cette période"
        
        # Créer la location
        try:
            rental = Rental(
                customer_id=customer_id,
                vehicle_id=vehicle_id,
                start_date=start_date,
                end_date=end_date,
                daily_rate=vehicle.daily_rate,
                start_mileage=vehicle.mileage
            )
        except ValueError as e:
            return None, str(e)
        
        # Appliquer la réduction fidélité
        discount = customer.get_loyalty_discount()
        if discount > 0:
            rental.apply_discount(discount)
        
        # Enregistrer la location
        self._rentals[rental.id] = rental
        customer.add_rental(rental.id)
        
        # Si la location commence aujourd'hui, marquer le véhicule comme loué
        if start_date == date.today():
            vehicle.rent()
            rental.start_rental()
        
        return rental, f"Location créée avec succès (ID: {rental.id})"
    
    def start_rental(self, rental_id: str) -> Tuple[bool, str]:
        """
        Démarre une location réservée.
        
        Args:
            rental_id: ID de la location
            
        Returns:
            Tuple (succès, message)
        """
        rental = self._rentals.get(rental_id)
        if not rental:
            return False, "Location non trouvée"
        
        if rental.status != RentalStatus.RESERVED:
            return False, "La location n'est pas en statut réservé"
        
        vehicle = self._vehicles.get(rental.vehicle_id)
        if not vehicle:
            return False, "Véhicule non trouvé"
        
        if not vehicle.rent():
            return False, "Impossible de louer le véhicule"
        
        rental.start_rental()
        return True, "Location démarrée"
    
    def complete_rental(
        self,
        rental_id: str,
        return_date: Optional[date] = None,
        end_mileage: Optional[float] = None
    ) -> Tuple[Optional[float], str]:
        """
        Termine une location.
        
        Args:
            rental_id: ID de la location
            return_date: Date de retour (aujourd'hui par défaut)
            end_mileage: Kilométrage au retour
            
        Returns:
            Tuple (coût total ou None, message)
        """
        rental = self._rentals.get(rental_id)
        if not rental:
            return None, "Location non trouvée"
        
        vehicle = self._vehicles.get(rental.vehicle_id)
        if not vehicle:
            return None, "Véhicule non trouvé"
        
        customer = self._customers.get(rental.customer_id)
        if not customer:
            return None, "Client non trouvé"
        
        return_date = return_date or date.today()
        
        try:
            total_cost = rental.complete_rental(return_date, end_mileage)
        except ValueError as e:
            return None, str(e)
        
        # Retourner le véhicule
        vehicle.return_vehicle(end_mileage)
        
        # Mettre à jour le client
        customer.complete_rental(rental_id)
        
        return total_cost, f"Location terminée. Coût total: {total_cost:.2f}€"
    
    def cancel_rental(self, rental_id: str) -> Tuple[Optional[float], str]:
        """
        Annule une location.
        
        Args:
            rental_id: ID de la location
            
        Returns:
            Tuple (frais d'annulation ou None, message)
        """
        rental = self._rentals.get(rental_id)
        if not rental:
            return None, "Location non trouvée"
        
        vehicle = self._vehicles.get(rental.vehicle_id)
        customer = self._customers.get(rental.customer_id)
        
        try:
            cancellation_fee = rental.cancel_rental()
        except ValueError as e:
            return None, str(e)
        
        # Si le véhicule était loué, le libérer
        if vehicle and vehicle.state == VehicleState.RENTED:
            vehicle.return_vehicle()
        
        # Mettre à jour le client
        if customer:
            customer.complete_rental(rental_id)
        
        if cancellation_fee > 0:
            return cancellation_fee, f"Location annulée. Frais d'annulation: {cancellation_fee:.2f}€"
        return 0, "Location annulée sans frais"
    
    def extend_rental(
        self,
        rental_id: str,
        new_end_date: date
    ) -> Tuple[bool, str]:
        """
        Prolonge une location.
        
        Args:
            rental_id: ID de la location
            new_end_date: Nouvelle date de fin
            
        Returns:
            Tuple (succès, message)
        """
        rental = self._rentals.get(rental_id)
        if not rental:
            return False, "Location non trouvée"
        
        # Vérifier la disponibilité pour la prolongation
        if not self._is_vehicle_available_for_period(
            rental.vehicle_id,
            rental.end_date + timedelta(days=1),
            new_end_date
        ):
            return False, "Véhicule non disponible pour la période de prolongation"
        
        if rental.extend_rental(new_end_date):
            return True, f"Location prolongée jusqu'au {new_end_date}"
        return False, "Impossible de prolonger la location"
    
    def get_rental(self, rental_id: str) -> Optional[Rental]:
        """Récupère une location par son ID."""
        return self._rentals.get(rental_id)
    
    def get_all_rentals(self) -> List[Rental]:
        """Retourne la liste de toutes les locations."""
        return list(self._rentals.values())
    
    def get_active_rentals(self) -> List[Rental]:
        """Retourne les locations en cours."""
        return [r for r in self._rentals.values() 
                if r.status == RentalStatus.ACTIVE]
    
    def get_overdue_rentals(self) -> List[Rental]:
        """Retourne les locations en retard."""
        return [r for r in self._rentals.values() 
                if r.is_overdue()]
    
    def get_customer_rentals(self, customer_id: str) -> List[Rental]:
        """Retourne les locations d'un client."""
        return [r for r in self._rentals.values() 
                if r.customer_id == customer_id]
    
    def get_vehicle_rentals(self, vehicle_id: str) -> List[Rental]:
        """Retourne les locations d'un véhicule."""
        return [r for r in self._rentals.values() 
                if r.vehicle_id == vehicle_id]
    
    # === Rapports ===
    
    def generate_available_vehicles_report(self) -> Dict:
        """
        Génère un rapport des véhicules disponibles.
        
        Returns:
            Dictionnaire contenant le rapport
        """
        available = self.get_available_vehicles()
        
        by_type = defaultdict(list)
        by_category = defaultdict(list)
        
        for vehicle in available:
            by_type[vehicle.get_vehicle_type()].append(vehicle.to_dict())
            by_category[vehicle.category.value].append(vehicle.to_dict())
        
        return {
            'report_type': 'Véhicules disponibles',
            'generated_at': datetime.now().isoformat(),
            'total_available': len(available),
            'total_fleet': len(self._vehicles),
            'availability_rate': len(available) / len(self._vehicles) * 100 if self._vehicles else 0,
            'by_type': dict(by_type),
            'by_category': dict(by_category),
            'vehicles': [v.to_dict() for v in available]
        }
    
    def generate_active_rentals_report(self) -> Dict:
        """
        Génère un rapport des locations en cours.
        
        Returns:
            Dictionnaire contenant le rapport
        """
        active = self.get_active_rentals()
        overdue = self.get_overdue_rentals()
        
        rentals_details = []
        for rental in active:
            customer = self._customers.get(rental.customer_id)
            vehicle = self._vehicles.get(rental.vehicle_id)
            
            detail = rental.to_dict()
            detail['customer_name'] = customer.full_name if customer else "Inconnu"
            detail['vehicle_info'] = str(vehicle) if vehicle else "Inconnu"
            detail['is_overdue'] = rental.is_overdue()
            detail['days_remaining'] = rental.days_remaining()
            rentals_details.append(detail)
        
        return {
            'report_type': 'Locations en cours',
            'generated_at': datetime.now().isoformat(),
            'total_active': len(active),
            'total_overdue': len(overdue),
            'rentals': rentals_details
        }
    
    def generate_revenue_report(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict:
        """
        Génère un rapport du chiffre d'affaires.
        
        Args:
            start_date: Date de début de la période
            end_date: Date de fin de la période
            
        Returns:
            Dictionnaire contenant le rapport
        """
        # Par défaut, le mois en cours
        if not start_date:
            today = date.today()
            start_date = date(today.year, today.month, 1)
        if not end_date:
            end_date = date.today()
        
        completed_rentals = [
            r for r in self._rentals.values()
            if r.status == RentalStatus.COMPLETED
            and r.actual_return_date
            and start_date <= r.actual_return_date <= end_date
        ]
        
        total_revenue = sum(r.total_cost for r in completed_rentals)
        total_penalties = sum(r.penalty for r in completed_rentals)
        total_base = sum(r.calculate_base_cost() for r in completed_rentals)
        
        # Revenus par type de véhicule
        revenue_by_type = defaultdict(float)
        for rental in completed_rentals:
            vehicle = self._vehicles.get(rental.vehicle_id)
            if vehicle:
                revenue_by_type[vehicle.get_vehicle_type()] += rental.total_cost
        
        # Revenus par mois
        revenue_by_month = defaultdict(float)
        for rental in completed_rentals:
            if rental.actual_return_date:
                month_key = rental.actual_return_date.strftime("%Y-%m")
                revenue_by_month[month_key] += rental.total_cost
        
        return {
            'report_type': 'Chiffre d\'affaires',
            'generated_at': datetime.now().isoformat(),
            'period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            },
            'total_revenue': total_revenue,
            'total_base_revenue': total_base,
            'total_penalties': total_penalties,
            'total_rentals_completed': len(completed_rentals),
            'average_rental_value': total_revenue / len(completed_rentals) if completed_rentals else 0,
            'revenue_by_vehicle_type': dict(revenue_by_type),
            'revenue_by_month': dict(revenue_by_month)
        }
    
    def generate_statistics_report(self) -> Dict:
        """
        Génère un rapport de statistiques générales.
        
        Returns:
            Dictionnaire contenant le rapport
        """
        total_vehicles = len(self._vehicles)
        total_customers = len(self._customers)
        total_rentals = len(self._rentals)
        
        # Statistiques des véhicules
        vehicles_by_state = defaultdict(int)
        vehicles_by_type = defaultdict(int)
        vehicles_needing_maintenance = 0
        
        for vehicle in self._vehicles.values():
            vehicles_by_state[vehicle.state.value] += 1
            vehicles_by_type[vehicle.get_vehicle_type()] += 1
            if vehicle.needs_maintenance():
                vehicles_needing_maintenance += 1
        
        # Statistiques des locations
        rentals_by_status = defaultdict(int)
        for rental in self._rentals.values():
            rentals_by_status[rental.status.value] += 1
        
        # Statistiques des clients
        loyal_customers = sum(1 for c in self._customers.values() if c.is_loyal_customer())
        blocked_customers = sum(1 for c in self._customers.values() if c.is_blocked)
        
        # Calcul du taux d'utilisation
        active_rentals = len(self.get_active_rentals())
        utilization_rate = (active_rentals / total_vehicles * 100) if total_vehicles > 0 else 0
        
        # Véhicule le plus loué
        vehicle_rental_counts = defaultdict(int)
        for rental in self._rentals.values():
            vehicle_rental_counts[rental.vehicle_id] += 1
        
        most_rented_vehicle = None
        if vehicle_rental_counts:
            most_rented_id = max(vehicle_rental_counts, key=lambda k: vehicle_rental_counts[k])
            most_rented_vehicle = self._vehicles.get(most_rented_id)
        
        return {
            'report_type': 'Statistiques générales',
            'generated_at': datetime.now().isoformat(),
            'agency_name': self._agency_name,
            'fleet': {
                'total_vehicles': total_vehicles,
                'by_state': dict(vehicles_by_state),
                'by_type': dict(vehicles_by_type),
                'needing_maintenance': vehicles_needing_maintenance,
                'utilization_rate': utilization_rate
            },
            'customers': {
                'total_customers': total_customers,
                'loyal_customers': loyal_customers,
                'blocked_customers': blocked_customers
            },
            'rentals': {
                'total_rentals': total_rentals,
                'by_status': dict(rentals_by_status),
                'active_rentals': active_rentals,
                'overdue_rentals': len(self.get_overdue_rentals())
            },
            'highlights': {
                'most_rented_vehicle': str(most_rented_vehicle) if most_rented_vehicle else None,
                'most_rented_count': max(vehicle_rental_counts.values()) if vehicle_rental_counts else 0
            }
        }
    
    def print_report(self, report: Dict) -> str:
        """
        Formate un rapport pour l'affichage.
        
        Args:
            report: Le rapport à formater
            
        Returns:
            Chaîne formatée du rapport
        """
        lines = []
        lines.append("=" * 60)
        lines.append(f" {report.get('report_type', 'Rapport').upper()}")
        lines.append(f" Généré le: {report.get('generated_at', 'N/A')}")
        lines.append("=" * 60)
        
        def format_dict(d: Dict, indent: int = 0) -> List[str]:
            result = []
            prefix = "  " * indent
            for key, value in d.items():
                if key in ['report_type', 'generated_at']:
                    continue
                if isinstance(value, dict):
                    result.append(f"{prefix}{key.replace('_', ' ').title()}:")
                    result.extend(format_dict(value, indent + 1))
                elif isinstance(value, list):
                    result.append(f"{prefix}{key.replace('_', ' ').title()}: {len(value)} éléments")
                else:
                    result.append(f"{prefix}{key.replace('_', ' ').title()}: {value}")
            return result
        
        lines.extend(format_dict(report))
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    # === Utilitaires ===
    
    def check_and_update_rentals(self) -> None:
        """
        Vérifie et met à jour le statut des locations.
        Doit être appelé régulièrement (ex: au démarrage de l'application).
        """
        today = date.today()
        
        for rental in self._rentals.values():
            # Démarrer les locations qui commencent aujourd'hui
            if rental.status == RentalStatus.RESERVED and rental.start_date <= today:
                vehicle = self._vehicles.get(rental.vehicle_id)
                if vehicle and vehicle.is_available():
                    vehicle.rent()
                    rental.start_rental()
    
    def get_summary(self) -> Dict:
        """Retourne un résumé rapide de l'état du système."""
        return {
            'agency': self._agency_name,
            'total_vehicles': len(self._vehicles),
            'available_vehicles': len(self.get_available_vehicles()),
            'total_customers': len(self._customers),
            'active_rentals': len(self.get_active_rentals()),
            'overdue_rentals': len(self.get_overdue_rentals())
        }
