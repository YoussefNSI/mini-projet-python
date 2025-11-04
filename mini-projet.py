# ===== PROGRAMME DE GESTION DE RESERVATIONS DE TRAINS =====
# Structure de départ avec les trajets

trains = {
    'TUN-PAR': {'places_total': 5, 'places_restantes': 5, 'passagers': set()},
    'TUN-ROM': {'places_total': 3, 'places_restantes': 3, 'passagers': set()},
    'TUN-MAD': {'places_total': 4, 'places_restantes': 4, 'passagers': set()},
}

# Liste pour stocker les tickets générés
tickets = []


# ===== FONCTION 1 : AFFICHER LES TRAINS =====
def afficher_trains():
    """Affiche tous les trajets avec le nombre de places restantes et total"""
    print("\n" + "="*50)
    print("LISTE DES TRAJETS DISPONIBLES")
    print("="*50)
    
    if not trains:
        print("Aucun trajet disponible.")
        return
    
    for code_trajet, info in trains.items():
        places_restantes = info['places_restantes']
        places_total = info['places_total']
        statut = "[Disponible]" if places_restantes > 0 else "[COMPLET]"
        print(f"{code_trajet} --> {places_restantes} places restantes / {places_total}  {statut}")
    
    print("="*50)


# ===== FONCTION 2 : RÉSERVER UNE PLACE =====
def reserver_place():
    """Réserve une place pour un passager sur un trajet choisi"""
    print("\n" + "="*50)
    print("RESERVATION D'UNE PLACE")
    print("="*50)
    
    # Afficher les trajets disponibles
    afficher_trains()
    
    # Demander le code du trajet
    code_trajet = input("\nEntrez le code du trajet (ex. TUN-PAR) : ").upper().strip()
    
    # Vérifier si le trajet existe
    if code_trajet not in trains:
        print(f"Erreur : Le trajet '{code_trajet}' n'existe pas.")
        return
    
    # Demander le nom du passager
    nom_passager = input("Entrez le nom du passager : ").strip()
    
    if not nom_passager:
        print("Erreur : Le nom du passager ne peut pas être vide.")
        return
    
    # Vérifier si le passager est déjà inscrit
    if nom_passager in trains[code_trajet]['passagers']:
        print(f"Erreur : {nom_passager} est déjà inscrit(e) sur le trajet {code_trajet}.")
        return
    
    # Vérifier s'il reste des places
    if trains[code_trajet]['places_restantes'] <= 0:
        print(f"Erreur : Le trajet {code_trajet} est complet.")
        return
    
    # Effectuer la réservation
    trains[code_trajet]['passagers'].add(nom_passager)
    trains[code_trajet]['places_restantes'] -= 1
    
    # Générer le ticket
    numero_place = trains[code_trajet]['places_total'] - trains[code_trajet]['places_restantes']
    ticket = (nom_passager, code_trajet, numero_place)
    tickets.append(ticket)
    
    print(f"\nReservation confirmee !")
    print(f"   Passager : {nom_passager}")
    print(f"   Trajet : {code_trajet}")
    print(f"   Numero de place : {numero_place}")
    print(f"   Places restantes : {trains[code_trajet]['places_restantes']}/{trains[code_trajet]['places_total']}")


# ===== FONCTION 3 : ANNULER UNE RÉSERVATION =====
def annuler_reservation():
    """Annule une réservation existante"""
    print("\n" + "="*50)
    print("ANNULATION DE RESERVATION")
    print("="*50)
    
    # Demander le code du trajet
    code_trajet = input("Entrez le code du trajet (ex. TUN-PAR) : ").upper().strip()
    
    # Vérifier si le trajet existe
    if code_trajet not in trains:
        print(f"Erreur : Le trajet '{code_trajet}' n'existe pas.")
        return
    
    # Demander le nom du passager
    nom_passager = input("Entrez le nom du passager a annuler : ").strip()
    
    if not nom_passager:
        print("Erreur : Le nom du passager ne peut pas être vide.")
        return
    
    # Vérifier si le passager est inscrit
    if nom_passager not in trains[code_trajet]['passagers']:
        print(f"Erreur : {nom_passager} n'est pas inscrit(e) sur le trajet {code_trajet}.")
        return
    
    # Effectuer l'annulation
    trains[code_trajet]['passagers'].remove(nom_passager)
    trains[code_trajet]['places_restantes'] += 1
    
    # Supprimer le ticket correspondant
    global tickets
    tickets = [t for t in tickets if not (t[0] == nom_passager and t[1] == code_trajet)]
    
    print(f"\nAnnulation confirmee !")
    print(f"   Passager : {nom_passager}")
    print(f"   Trajet : {code_trajet}")
    print(f"   Places restantes : {trains[code_trajet]['places_restantes']}/{trains[code_trajet]['places_total']}")


# ===== FONCTION 4 : AFFICHER LES PASSAGERS D'UN TRAIN =====
def afficher_passagers():
    """Affiche la liste triée des passagers d'un trajet donné"""
    print("\n" + "="*50)
    print("LISTE DES PASSAGERS")
    print("="*50)
    
    # Demander le code du trajet
    code_trajet = input("Entrez le code du trajet (ex. TUN-PAR) : ").upper().strip()
    
    # Vérifier si le trajet existe
    if code_trajet not in trains:
        print(f"Erreur : Le trajet '{code_trajet}' n'existe pas.")
        return
    
    # Récupérer et trier les passagers
    passagers = sorted(trains[code_trajet]['passagers'])
    
    print(f"\nTrajet : {code_trajet}")
    print(f"Nombre de passagers : {len(passagers)}/{trains[code_trajet]['places_total']}")
    
    if passagers:
        print("\nPassagers inscrits :")
        for i, nom in enumerate(passagers, 1):
            print(f"   {i}. {nom}")
    else:
        print("\nAucun passager inscrit sur ce trajet.")
    
    print("="*50)


# ===== FONCTION 5 : AFFICHER LES TRAINS COMPLETS =====
def afficher_trains_complets():
    """Affiche la liste des trains dont le nombre de places restantes est zéro"""
    print("\n" + "="*50)
    print("TRAINS COMPLETS")
    print("="*50)
    
    trains_complets = [code for code, info in trains.items() if info['places_restantes'] == 0]
    
    if trains_complets:
        print(f"Nombre de trains complets : {len(trains_complets)}\n")
        for code_trajet in trains_complets:
            print(f"   - {code_trajet} ({trains[code_trajet]['places_total']} places)")
    else:
        print("Aucun train complet actuellement.")
    
    print("="*50)


# ===== FONCTION BONUS 6 : AFFICHER LES TICKETS =====
def afficher_tickets():
    """Affiche tous les tickets générés"""
    print("\n" + "="*50)
    print("TICKETS GENERES")
    print("="*50)
    
    if tickets:
        print(f"Nombre total de tickets : {len(tickets)}\n")
        for i, (nom, trajet, place) in enumerate(tickets, 1):
            print(f"   {i}. Ticket({nom}, {trajet}, {place})")
    else:
        print("Aucun ticket généré.")
    
    print("="*50)


# ===== MENU PRINCIPAL =====
def menu_principal():
    """Boucle principale avec menu interactif"""
    while True:
        print("\n" + "="*50)
        print("=== MENU RESERVATION TRAIN ===")
        print("="*50)
        print("1 - Afficher les trains")
        print("2 - Reserver une place")
        print("3 - Annuler une reservation")
        print("4 - Afficher les passagers d'un train")
        print("5 - Voir les trains complets")
        print("6 - Voir les tickets (Bonus)")
        print("0 - Quitter")
        print("="*50)
        
        choix = input("\nChoisissez une option (0-6) : ").strip()
        
        if choix == "1":
            afficher_trains()
        elif choix == "2":
            reserver_place()
        elif choix == "3":
            annuler_reservation()
        elif choix == "4":
            afficher_passagers()
        elif choix == "5":
            afficher_trains_complets()
        elif choix == "6":
            afficher_tickets()
        elif choix == "0":
            print("\nAu revoir ! Merci d'avoir utilise le systeme de reservation.")
            break
        else:
            print("\nOption invalide. Veuillez choisir entre 0 et 6.")


# ===== POINT D'ENTREE =====
if __name__ == "__main__":
    print("\n" + "="*50)
    print("BIENVENUE DANS LE SYSTEME DE RESERVATION DE TRAINS")
    print("="*50 + "\n")
    menu_principal()
