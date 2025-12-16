# Système de Location de Voitures

## Description

Application de gestion de location de voitures développée en Python, basée sur les principes de la **Programmation Orientée Objet (POO)**.

Cette application permet à une agence de location de :

- Gérer son parc automobile (voitures, camions, motos)
- Gérer ses clients
- Effectuer et suivre les locations
- Calculer le coût des locations avec réductions
- Générer des rapports détaillés
- **Sauvegarder et charger les données** (nouveau !)

## Structure du Projet

```
mini-projet2/
├── models/
│   ├── __init__.py
│   ├── vehicle.py          # Classes Vehicle, Car, Truck, Motorcycle
│   ├── customer.py         # Classe Customer
│   ├── rental.py           # Classe Rental
│   ├── constants.py        # Constantes centralisées (nouveau)
│   ├── exceptions.py       # Exceptions personnalisées (nouveau)
│   ├── persistence.py      # Sauvegarde/chargement JSON (nouveau)
│   └── utils.py            # Fonctions utilitaires (nouveau)
├── tests/
│   ├── __init__.py
│   ├── test_vehicle.py     # Tests des véhicules
│   ├── test_customer.py    # Tests des clients
│   ├── test_rental.py      # Tests des locations
│   └── test_car_rental_system.py  # Tests du système
├── data/                   # Données persistées (nouveau)
├── car_rental_system.py    # Classe principale CarRentalSystem
├── main.py                 # Point d'entrée avec démonstration
├── requirements.txt        # Dépendances
├── README.md               # Documentation
└── UML_DIAGRAM.md          # Diagramme de classes UML
```

## Architecture des Classes

### Hiérarchie des Véhicules

```
Vehicle (ABC)
├── Car          # Voitures
├── Truck        # Camions/Utilitaires
└── Motorcycle   # Motos
```

### Classes Principales

| Classe            | Description                                           |
| ----------------- | ----------------------------------------------------- |
| `Vehicle`         | Classe abstraite de base pour tous les véhicules      |
| `Car`             | Voitures avec portes, places, carburant, transmission |
| `Truck`           | Camions avec capacité de chargement et poids max      |
| `Motorcycle`      | Motos avec cylindrée et type                          |
| `Customer`        | Clients avec permis, historique, fidélité             |
| `Rental`          | Locations avec dates, coûts, pénalités                |
| `CarRentalSystem` | Système central de gestion                            |

## Fonctionnalites

### 1. Gestion de la Flotte Automobile

- **Attributs des véhicules** :

  - ID unique, marque, modèle
  - Catégorie (économique, standard, premium, luxe, utilitaire, sport)
  - Tarif journalier, état, année, immatriculation
  - Kilométrage, historique d'entretien

- **États des véhicules** :

  - `AVAILABLE` - Disponible
  - `RENTED` - Loué
  - `MAINTENANCE` - En maintenance
  - `OUT_OF_SERVICE` - Hors service

- **Gestion de la maintenance** :
  - Suivi de l'historique d'entretien
  - Alerte de maintenance (tous les 10 000 km)

### 2. Gestion des Clients

- **Informations client** :

  - ID, nom, prénom, date de naissance
  - Numéro de permis, types de permis détenus
  - Email, téléphone, adresse
  - Historique des locations

- **Règles d'éligibilité** :

  - Âge minimum selon le type de véhicule
  - Permis requis (B, A, A1, C, C1)
  - Permis détenu depuis au moins 1 an

- **Programme de fidélité** :
  - 5+ locations : 5% de réduction
  - 10+ locations : 10% de réduction
  - 20+ locations : 15% de réduction

### 3. Système de Réservation

- **Création de location** :

  - Vérification de disponibilité
  - Validation des dates
  - Vérification de l'éligibilité client

- **Tarification** :

  - Tarif de base × nombre de jours
  - Réduction 10% pour 7+ jours
  - Réduction 20% pour 30+ jours
  - Réduction fidélité cumulable

- **Pénalités** :
  - Retard : 50€/jour
  - Annulation < 7 jours : 20% du total
  - Annulation < 3 jours : 50% du total
  - Annulation < 1 jour : 100% du total

### 4. Rapports

- **Véhicules disponibles** : Liste par type et catégorie
- **Locations en cours** : Avec statut et retards
- **Chiffre d'affaires** : Par période, type de véhicule
- **Statistiques générales** : Taux d'utilisation, fidélité

## Installation

### Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
pip install -r requirements.txt
```

## Utilisation

### Exécution de la démonstration

```bash
python main.py
```

### Exemple de code

```python
from datetime import date, timedelta
from car_rental_system import CarRentalSystem
from models.vehicle import Car, VehicleCategory
from models.customer import Customer

# Créer le système
system = CarRentalSystem("MonAgence")

# Ajouter un véhicule
car = Car(
    brand="Renault",
    model="Clio",
    category=VehicleCategory.ECONOMY,
    daily_rate=45.0,
    year=2022,
    license_plate="AB-123-CD"
)
system.add_vehicle(car)

# Ajouter un client
customer = Customer(
    first_name="Jean",
    last_name="Dupont",
    birth_date=date(1990, 5, 15),
    license_number="123456789012",
    license_types={"B"},
    license_date=date(2010, 6, 20),
    email="jean@email.com",
    phone="0612345678"
)
system.add_customer(customer)

# Créer une location
start = date.today() + timedelta(days=1)
end = start + timedelta(days=5)
rental, message = system.create_rental(
    customer.id, car.id, start, end
)
print(message)

# Générer un rapport
report = system.generate_statistics_report()
print(system.print_report(report))
```

## Tests

### Exécution des tests

```bash
# Tous les tests
pytest tests/ -v

# Tests par module
pytest tests/test_vehicle.py -v
pytest tests/test_customer.py -v
pytest tests/test_rental.py -v
pytest tests/test_car_rental_system.py -v

# Avec couverture
pytest tests/ --cov=. --cov-report=html
```

### Structure des tests

- `test_vehicle.py` : Tests des classes Vehicle, Car, Truck, Motorcycle
- `test_customer.py` : Tests de la classe Customer
- `test_rental.py` : Tests de la classe Rental
- `test_car_rental_system.py` : Tests d'intégration du système

## Contraintes d'Age par Vehicule

| Type de Véhicule | Catégorie           | Âge Minimum | Permis |
| ---------------- | ------------------- | ----------- | ------ |
| Voiture          | Économique/Standard | 21 ans      | B      |
| Voiture          | Premium             | 23 ans      | B      |
| Voiture          | Luxe/Sport          | 25 ans      | B      |
| Camion           | ≤ 3.5t              | 18 ans      | B      |
| Camion           | 3.5t - 7.5t         | 21 ans      | C1     |
| Camion           | > 7.5t              | 21 ans      | C      |
| Moto             | ≤ 125cc             | 18 ans      | A1     |
| Moto             | > 125cc             | 20 ans      | A      |

## Technologies Utilisees

- **Python 3.10+** : Langage de programmation
- **pytest** : Framework de tests
- **ABC** : Classes abstraites
- **Enum** : Énumérations pour les états et catégories
- **dataclasses** : Pour les structures de données
- **typing** : Annotations de types

## Licence

Ce projet est développé dans le cadre du cours IRA3 - Mini Projet 2.

## Auteurs

- Étudiant IRA3

---

_Dernière mise à jour : Décembre 2024_
