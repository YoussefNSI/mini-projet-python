#!/usr/bin/env python3
"""
Point d'entrée principal de l'application de location de voitures.

Usage:
    python main.py              # Lance l'interface graphique (par défaut)
    python main.py --gui        # Lance l'interface graphique
    python main.py --console    # Lance la démonstration en console
    python main.py --test       # Lance tous les tests unitaires
    python main.py --help       # Affiche l'aide

Système de Location de Véhicules - IRA3 Python Mini-Projet 2
"""

import sys
import argparse
import subprocess
from pathlib import Path
from datetime import date, timedelta

# Chemin racine du projet
PROJECT_ROOT = Path(__file__).parent


def launch_gui():
    """Lance l'interface graphique PyQt6."""
    print("Lancement de l'interface graphique...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from gui.main_window import MainWindow
        from gui.styles import get_full_stylesheet
        
        # Créer l'application
        app = QApplication(sys.argv)
        app.setApplicationName("ShopTaLoc31 Premium")
        app.setOrganizationName("IRA3")
        app.setStyleSheet(get_full_stylesheet())
        
        # Créer et afficher la fenêtre principale
        # MainWindow crée son propre système avec données de démo
        window = MainWindow()
        window.show()
        
        # Lancer la boucle d'événements
        sys.exit(app.exec())
        
    except ImportError as e:
        print(f"Erreur: PyQt6 n'est pas installe.")
        print(f"   Installez-le avec: pip install PyQt6")
        print(f"   Details: {e}")
        sys.exit(1)


def launch_tests(args: list | None = None):
    """Lance les tests unitaires."""
    print("[TEST] Lancement des tests unitaires...")
    print("=" * 60)
    
    tests_dir = PROJECT_ROOT / "tests"
    
    pytest_args = [
        sys.executable, "-m", "pytest",
        str(tests_dir),
        "-v"
    ]
    
    if args:
        pytest_args.extend(args)
    
    result = subprocess.run(pytest_args)
    
    print("=" * 60)
    if result.returncode == 0:
        print("[OK] TOUS LES TESTS ONT REUSSI !")
    else:
        print("[ERREUR] CERTAINS TESTS ONT ECHOUE")
    
    return result.returncode


def launch_console():
    """Lance la démonstration en console."""
    from car_rental_system import CarRentalSystem
    from models.vehicle import VehicleCategory
    
    print("=" * 60)
    print("    SYSTEME DE LOCATION DE VOITURES")
    print("        Mode Console / Demonstration")
    print("=" * 60)
    
    # Créer le système
    system = CarRentalSystem("ShopTaLoc31 Premium")
    
    # Créer les données de démonstration
    print("\n[...] Creation des donnees de demonstration...")
    create_sample_data(system)
    
    # Afficher le résumé
    summary = system.get_summary()
    print(f"\n[OK] Systeme initialise: {summary['agency']}")
    print(f"   Vehicules: {summary['total_vehicles']}")
    print(f"   Clients: {summary['total_customers']}")
    
    # Démonstrations
    demo_vehicle_search(system)
    demo_age_restrictions(system)
    demo_rental_operations(system)
    demo_reports(system)
    
    print("\n" + "=" * 60)
    print(" FIN DE LA DÉMONSTRATION")
    print("=" * 60)


def create_sample_data(system) -> None:
    """Crée des données de démonstration."""
    from models.vehicle import Car, Truck, Motorcycle, VehicleCategory
    from models.customer import Customer
    
    # === Création des véhicules ===
    
    # Voitures
    cars = [
        Car(
            brand="Renault",
            model="Clio",
            category=VehicleCategory.ECONOMY,
            daily_rate=35.0,
            year=2022,
            license_plate="AB-123-CD",
            num_doors=5,
            num_seats=5,
            fuel_type="essence",
            transmission="manuelle"
        ),
        Car(
            brand="Peugeot",
            model="308",
            category=VehicleCategory.STANDARD,
            daily_rate=50.0,
            year=2023,
            license_plate="EF-456-GH",
            num_doors=5,
            num_seats=5,
            fuel_type="diesel",
            transmission="automatique"
        ),
        Car(
            brand="BMW",
            model="Série 3",
            category=VehicleCategory.PREMIUM,
            daily_rate=90.0,
            year=2023,
            license_plate="IJ-789-KL",
            num_doors=4,
            num_seats=5,
            fuel_type="essence",
            transmission="automatique"
        ),
        Car(
            brand="Mercedes",
            model="Classe S",
            category=VehicleCategory.LUXURY,
            daily_rate=200.0,
            year=2024,
            license_plate="MN-012-OP",
            num_doors=4,
            num_seats=5,
            fuel_type="hybride",
            transmission="automatique"
        ),
        Car(
            brand="Porsche",
            model="911",
            category=VehicleCategory.SPORT,
            daily_rate=300.0,
            year=2024,
            license_plate="QR-345-ST",
            num_doors=2,
            num_seats=2,
            fuel_type="essence",
            transmission="automatique"
        ),
    ]
    
    # Camions
    trucks = [
        Truck(
            brand="Renault",
            model="Master",
            category=VehicleCategory.UTILITY,
            daily_rate=70.0,
            year=2021,
            license_plate="TR-111-CK",
            cargo_capacity=12.0,
            max_weight=3000,
            has_tail_lift=False
        ),
        Truck(
            brand="Mercedes",
            model="Sprinter",
            category=VehicleCategory.UTILITY,
            daily_rate=85.0,
            year=2022,
            license_plate="TR-222-CK",
            cargo_capacity=15.0,
            max_weight=3500,
            has_tail_lift=True
        ),
    ]
    
    # Motos
    motorcycles = [
        Motorcycle(
            brand="Honda",
            model="CB125R",
            category=VehicleCategory.ECONOMY,
            daily_rate=25.0,
            year=2023,
            license_plate="MO-111-TO",
            engine_size=125,
            motorcycle_type="standard"
        ),
        Motorcycle(
            brand="Yamaha",
            model="MT-07",
            category=VehicleCategory.STANDARD,
            daily_rate=60.0,
            year=2023,
            license_plate="MO-222-TO",
            engine_size=689,
            motorcycle_type="roadster"
        ),
    ]
    
    # Ajout des véhicules au système
    for vehicle in cars + trucks + motorcycles:
        system.add_vehicle(vehicle)
    
    # === Création des clients ===
    
    customers = [
        Customer(
            first_name="Jean",
            last_name="Dupont",
            birth_date=date(1985, 3, 15),
            license_number="123456789012",
            license_types={"B"},
            license_date=date(2005, 6, 20),
            email="jean.dupont@email.com",
            phone="0612345678",
            address="12 Rue de Paris, 75001 Paris"
        ),
        Customer(
            first_name="Marie",
            last_name="Martin",
            birth_date=date(1990, 7, 22),
            license_number="987654321098",
            license_types={"B", "A"},
            license_date=date(2010, 8, 15),
            email="marie.martin@email.com",
            phone="0698765432",
            address="45 Avenue de Lyon, 69001 Lyon"
        ),
        Customer(
            first_name="Pierre",
            last_name="Bernard",
            birth_date=date(2000, 11, 8),
            license_number="456789123456",
            license_types={"B", "A1"},
            license_date=date(2020, 5, 10),
            email="pierre.bernard@email.com",
            phone="0611223344",
            address="78 Boulevard de Marseille, 13001 Marseille"
        ),
        Customer(
            first_name="Sophie",
            last_name="Leroy",
            birth_date=date(1988, 12, 3),
            license_number="789123456789",
            license_types={"B", "C1"},
            license_date=date(2008, 4, 25),
            email="sophie.leroy@email.com",
            phone="0655443322",
            address="23 Rue de Bordeaux, 33000 Bordeaux"
        ),
    ]
    
    for customer in customers:
        system.add_customer(customer)
    
    # Ajouter quelques locations à l'historique pour Jean (fidélité)
    jean = customers[0]
    for i in range(6):
        jean.add_rental(f"HIST{i:03d}")
        jean.complete_rental(f"HIST{i:03d}")


def demo_rental_operations(system) -> None:
    """Démontre les opérations de location."""
    
    print("\n" + "=" * 60)
    print(" DÉMONSTRATION DES OPÉRATIONS DE LOCATION")
    print("=" * 60)
    
    # Récupérer un client et un véhicule
    customers = system.get_all_customers()
    vehicles = system.get_available_vehicles()
    
    if not customers or not vehicles:
        print("Erreur: Pas de clients ou de véhicules disponibles")
        return
    
    customer = customers[0]
    vehicle = vehicles[0]
    
    print(f"\n[CLIENT] {customer.full_name} ({customer.age} ans)")
    print(f"   Fidelite: {customer.get_total_rentals()} locations - Reduction: {customer.get_loyalty_discount()*100:.0f}%")
    print(f"[VEHICULE] {vehicle}")
    
    # Créer une location
    start_date = date.today()
    end_date = start_date + timedelta(days=5)
    
    print(f"\n[PERIODE] {start_date} -> {end_date} (6 jours)")
    
    rental, message = system.create_rental(
        customer.id,
        vehicle.id,
        start_date,
        end_date
    )
    
    if rental:
        print(f"[OK] {message}")
        print(f"   Cout estime: {rental.total_cost:.2f}EUR")
        print(f"   Tarif journalier: {rental.daily_rate:.2f}EUR")
        
        # Afficher les details de la location
        print(f"\n[DETAILS] Details de la location:")
        print(f"   ID: {rental.id}")
        print(f"   Statut: {rental.status.value}")
        print(f"   Duree prevue: {rental.planned_duration} jours")
    else:
        print(f"[ERREUR] {message}")


def demo_vehicle_search(system) -> None:
    """Démontre la recherche de véhicules."""
    from models.vehicle import VehicleCategory
    
    print("\n" + "=" * 60)
    print(" DÉMONSTRATION DE RECHERCHE DE VÉHICULES")
    print("=" * 60)
    
    # Recherche par marque
    print("\n[RECHERCHE] Recherche par marque 'Renault':")
    results = system.search_vehicles(brand="Renault")
    for v in results:
        print(f"   - {v}")
    
    # Recherche par tarif max
    print("\n[RECHERCHE] Vehicules a moins de 50EUR/jour:")
    results = system.search_vehicles(max_daily_rate=50.0)
    for v in results:
        print(f"   - {v} ({v.daily_rate:.2f}EUR/jour)")
    
    # Vehicules disponibles par categorie
    print("\n[RECHERCHE] Vehicules economiques disponibles:")
    results = system.get_available_vehicles(category=VehicleCategory.ECONOMY)
    for v in results:
        print(f"   - {v}")


def demo_reports(system) -> None:
    """Démontre la génération de rapports."""
    
    print("\n" + "=" * 60)
    print(" DÉMONSTRATION DES RAPPORTS")
    print("=" * 60)
    
    # Rapport des vehicules disponibles
    print("\n[RAPPORT] Vehicules Disponibles")
    report = system.generate_available_vehicles_report()
    print(f"   Total disponibles: {report['total_available']}/{report['total_fleet']}")
    print(f"   Taux de disponibilite: {report['availability_rate']:.1f}%")
    
    # Rapport statistiques
    print("\n[RAPPORT] Statistiques Generales")
    stats = system.generate_statistics_report()
    print(f"   Véhicules: {stats['fleet']['total_vehicles']}")
    print(f"   Clients: {stats['customers']['total_customers']}")
    print(f"   Clients fidèles: {stats['customers']['loyal_customers']}")


def demo_age_restrictions(system) -> None:
    """Démontre les restrictions d'âge."""
    
    print("\n" + "=" * 60)
    print(" DÉMONSTRATION DES RESTRICTIONS D'ÂGE")
    print("=" * 60)
    
    # Trouver un jeune client
    customers = system.get_all_customers()
    young_customer = None
    for c in customers:
        if c.age < 25:
            young_customer = c
            break
    
    if not young_customer:
        print("Pas de jeune client pour la démonstration")
        return
    
    print(f"\n[CLIENT] {young_customer.full_name} ({young_customer.age} ans)")
    print(f"   Permis: {', '.join(young_customer.license_types)}")
    
    # Essayer de louer différents véhicules
    vehicles = system.get_all_vehicles()
    
    start_date = date.today() + timedelta(days=1)
    end_date = start_date + timedelta(days=3)
    
    for vehicle in vehicles[:5]:  # Limiter à 5 véhicules pour la démo
        rental, message = system.create_rental(
            young_customer.id,
            vehicle.id,
            start_date,
            end_date
        )
        
        if rental:
            print(f"   [OK] {vehicle.get_vehicle_type()} {vehicle.brand} {vehicle.model}: OK")
            # Annuler pour la demonstration
            system.cancel_rental(rental.id)
        else:
            reason = message.split(":")[-1].strip() if ":" in message else message
            print(f"   [X] {vehicle.get_vehicle_type()} {vehicle.brand} {vehicle.model}: {reason}")


def print_help():
    """Affiche l'aide detaillee."""
    print("""
+==============================================================+
|       SYSTEME DE LOCATION DE VEHICULES - AIDE                |
+==============================================================+
|                                                              |
|  USAGE:                                                      |
|    python main.py [OPTIONS]                                  |
|                                                              |
|  OPTIONS:                                                    |
|    --gui, -g      Lance l'interface graphique (defaut)       |
|    --console, -c  Lance la demo en mode console              |
|    --test, -t     Lance tous les tests unitaires             |
|    --help, -h     Affiche cette aide                         |
|                                                              |
|  EXEMPLES:                                                   |
|    python main.py              # Interface graphique         |
|    python main.py --console    # Mode console                |
|    python main.py --test       # Tests unitaires             |
|                                                              |
|  FICHIERS:                                                   |
|    main.py          - Point d'entree principal               |
|    run_gui.py       - Lance uniquement l'interface           |
|    run_tests.py     - Lance les tests avec options           |
|                                                              |
+==============================================================+
""")


def main():
    """Fonction principale - Point d'entrée de l'application."""
    
    parser = argparse.ArgumentParser(
        description="Système de Location de Véhicules - ShopTaLoc31 Premium",
        add_help=False
    )
    
    parser.add_argument(
        "--gui", "-g",
        action="store_true",
        help="Lance l'interface graphique (par défaut)"
    )
    parser.add_argument(
        "--console", "-c",
        action="store_true",
        help="Lance la démonstration en console"
    )
    parser.add_argument(
        "--test", "-t",
        action="store_true",
        help="Lance les tests unitaires"
    )
    parser.add_argument(
        "--help", "-h",
        action="store_true",
        help="Affiche l'aide"
    )
    
    args, remaining = parser.parse_known_args()
    
    # Afficher l'aide
    if args.help:
        print_help()
        return 0
    
    # Lancer les tests
    if args.test:
        return launch_tests(remaining)
    
    # Lancer le mode console
    if args.console:
        launch_console()
        return 0
    
    # Par défaut: lancer l'interface graphique
    launch_gui()
    return 0


if __name__ == "__main__":
    sys.exit(main())
