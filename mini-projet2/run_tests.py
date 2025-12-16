#!/usr/bin/env python3
"""
Script principal pour lancer tous les tests unitaires.
Système de location de véhicules - Tests

Usage:
    python run_tests.py              # Lance tous les tests
    python run_tests.py -v           # Mode verbeux
    python run_tests.py -q           # Mode silencieux
    python run_tests.py --cov        # Avec couverture de code
    python run_tests.py --html       # Génère un rapport HTML
    python run_tests.py <test_file>  # Lance un fichier de test spécifique
"""

import sys
import subprocess
import argparse
from pathlib import Path


def get_project_root() -> Path:
    """Retourne le chemin racine du projet."""
    return Path(__file__).parent


def run_tests(args: list[str] | None = None) -> int:
    """
    Lance les tests avec pytest.
    
    Args:
        args: Arguments supplémentaires pour pytest
        
    Returns:
        Code de retour (0 = succès)
    """
    project_root = get_project_root()
    tests_dir = project_root / "tests"
    
    # Arguments de base
    pytest_args = [
        sys.executable, "-m", "pytest",
        str(tests_dir),
    ]
    
    # Ajouter les arguments supplémentaires
    if args:
        pytest_args.extend(args)
    
    # Lancer pytest
    print("=" * 60)
    print("[TEST] LANCEMENT DES TESTS UNITAIRES")
    print("=" * 60)
    print(f"[DIR] Dossier des tests: {tests_dir}")
    print(f"[PYTHON] Python: {sys.version.split()[0]}")
    print("-" * 60)
    
    result = subprocess.run(pytest_args)
    
    print("-" * 60)
    if result.returncode == 0:
        print("[OK] TOUS LES TESTS ONT REUSSI !")
    else:
        print("[ERREUR] CERTAINS TESTS ONT ECHOUE")
    print("=" * 60)
    
    return result.returncode


def run_with_coverage() -> int:
    """Lance les tests avec mesure de couverture de code."""
    project_root = get_project_root()
    
    pytest_args = [
        sys.executable, "-m", "pytest",
        str(project_root / "tests"),
        "--cov=models",
        "--cov=car_rental_system",
        "--cov-report=term-missing",
        "--cov-report=html:coverage_report",
        "-v"
    ]
    
    print("=" * 60)
    print("[COV] TESTS AVEC COUVERTURE DE CODE")
    print("=" * 60)
    
    result = subprocess.run(pytest_args)
    
    if result.returncode == 0:
        print("\n[RAPPORT] Rapport de couverture genere dans: coverage_report/index.html")
    
    return result.returncode


def run_specific_tests(test_name: str) -> int:
    """Lance un test ou fichier de test spécifique."""
    project_root = get_project_root()
    tests_dir = project_root / "tests"
    
    # Vérifier si c'est un fichier complet ou un nom de test
    if test_name.endswith(".py"):
        test_path = tests_dir / test_name
    else:
        test_path = str(tests_dir) + f" -k {test_name}"
    
    pytest_args = [
        sys.executable, "-m", "pytest",
        str(test_path) if isinstance(test_path, Path) else test_path,
        "-v"
    ]
    
    return subprocess.run(pytest_args).returncode


def list_tests() -> None:
    """Affiche la liste des fichiers de tests disponibles."""
    project_root = get_project_root()
    tests_dir = project_root / "tests"
    
    print("=" * 60)
    print("[LISTE] FICHIERS DE TESTS DISPONIBLES")
    print("=" * 60)
    
    for test_file in sorted(tests_dir.glob("test_*.py")):
        print(f"  [FILE] {test_file.name}")
    
    print("-" * 60)
    print("Usage: python run_tests.py <nom_fichier>")
    print("=" * 60)


def main():
    """Point d'entrée principal."""
    parser = argparse.ArgumentParser(
        description="Lance les tests unitaires du système de location de véhicules",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python run_tests.py                    Lance tous les tests
  python run_tests.py -v                 Mode verbeux
  python run_tests.py --cov              Avec couverture de code
  python run_tests.py --list             Liste les fichiers de tests
  python run_tests.py test_vehicle.py    Lance uniquement les tests de véhicules
  python run_tests.py -k "rental"        Lance les tests contenant "rental"
        """
    )
    
    parser.add_argument(
        "test_file",
        nargs="?",
        help="Fichier de test spécifique à lancer"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Mode verbeux"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Mode silencieux"
    )
    parser.add_argument(
        "--cov", "--coverage",
        action="store_true",
        help="Mesurer la couverture de code"
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="Générer un rapport HTML"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Lister les fichiers de tests"
    )
    parser.add_argument(
        "-k",
        metavar="EXPRESSION",
        help="Filtrer les tests par expression"
    )
    parser.add_argument(
        "-x", "--exitfirst",
        action="store_true",
        help="Arrêter au premier échec"
    )
    
    args = parser.parse_args()
    
    # Liste des tests
    if args.list:
        list_tests()
        return 0
    
    # Couverture
    if args.cov:
        return run_with_coverage()
    
    # Fichier spécifique
    if args.test_file:
        return run_specific_tests(args.test_file)
    
    # Construction des arguments pytest
    pytest_args = []
    
    if args.verbose:
        pytest_args.append("-v")
    elif args.quiet:
        pytest_args.append("-q")
    else:
        pytest_args.append("-v")  # Verbeux par défaut
    
    if args.html:
        pytest_args.extend(["--html=test_report.html", "--self-contained-html"])
    
    if args.k:
        pytest_args.extend(["-k", args.k])
    
    if args.exitfirst:
        pytest_args.append("-x")
    
    return run_tests(pytest_args)


if __name__ == "__main__":
    sys.exit(main())
