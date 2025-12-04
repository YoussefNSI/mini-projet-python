# Explication de chaque fonction du code

## Données Globales

```python
trains = {
    'LYO-PAR': {'places_total': 5, 'places_restantes': 5, 'passagers': set()},
    'VEN-ROM': {'places_total': 3, 'places_restantes': 3, 'passagers': set()},
    'BDX-MTP': {'places_total': 4, 'places_restantes': 4, 'passagers': set()},
}
tickets = []
```

**Rôle :** Stocke les données de l'application

- `trains` : Dictionnaire des 3 trajets (Lyon-Paris, Venise-Rome, Bordeaux-Montpellier)
- `tickets` : Liste des billets générés

---

## Classe AppReservationTrains

### **`__init__(self, root)`**

```python
def __init__(self, root):
```

| Aspect        | Description                                                        |
| ------------- | ------------------------------------------------------------------ |
| **Rôle**      | Initialise l'application                                           |
| **Paramètre** | `root` - La fenêtre Tkinter principale                             |
| **Actions**   | Configure le titre, la taille (900x700), les couleurs, les polices |
| **Appelle**   | `setup_ui()` pour construire l'interface                           |

---

### **`setup_ui(self)`**

```python
def setup_ui(self):
```

| Aspect      | Description                              |
| ----------- | ---------------------------------------- |
| **Rôle**    | Construit toute l'interface utilisateur  |
| **Actions** | Crée l'en-tête + le système de 6 onglets |
| **Appelle** | Les 6 fonctions `setup_tab_*()`          |

---

## Onglet 1 : Trains

### **`setup_tab_trains(self)`**

```python
def setup_tab_trains(self):
```

| Aspect                  | Description                                         |
| ----------------------- | --------------------------------------------------- |
| **Rôle**                | Crée l'onglet "Trains"                              |
| **Widgets créés**       | Titre + Tableau (Treeview) + Bouton "Rafraichir"    |
| **Colonnes du tableau** | Code Trajet, Places Restantes, Places Total, Statut |
| **Appelle**             | `refresh_trains_tab()` pour charger les données     |

---

### **`refresh_trains_tab(self)`**

```python
def refresh_trains_tab(self):
```

| Aspect      | Description                                                    |
| ----------- | -------------------------------------------------------------- |
| **Rôle**    | Met à jour le tableau des trains                               |
| **Actions** | 1. Vide le tableau 2. Parcourt `trains` 3. Insère chaque ligne |
| **Logique** | Si `places_restantes > 0` → "Disponible", sinon → "COMPLET"    |

---

## Onglet 2 : Réserver

### **`setup_tab_reserver(self)`**

```python
def setup_tab_reserver(self):
```

| Aspect            | Description                                                   |
| ----------------- | ------------------------------------------------------------- |
| **Rôle**          | Crée l'onglet "Réserver"                                      |
| **Widgets créés** | Combobox (trajet) + Entry (nom) + Bouton vert + Zone de texte |
| **Variables**     | `self.var_trajet_reserver`, `self.entry_nom_reserver`         |

---

### **`reserver_place(self)`**

```python
def reserver_place(self):
```

| Aspect            | Description                                                                                               |
| ----------------- | --------------------------------------------------------------------------------------------------------- |
| **Rôle**          | Effectue une réservation                                                                                  |
| **Validations**   | 5 vérifications (trajet choisi, nom rempli, trajet existe, passager pas déjà inscrit, places disponibles) |
| **Actions si OK** | Ajoute passager, décrémente places, crée ticket, affiche confirmation                                     |
| **Appelle**       | `refresh_all_tabs()` pour synchroniser                                                                    |

**Flux :**

```
Récupère trajet + nom
    ↓
5 validations (erreur si échec)
    ↓
trains[trajet]['passagers'].add(nom)
trains[trajet]['places_restantes'] -= 1
    ↓
Crée ticket (nom, trajet, numéro_place)
    ↓
Affiche confirmation + rafraîchit tout
```

---

## Onglet 3 : Annuler

### **`setup_tab_annuler(self)`**

```python
def setup_tab_annuler(self):
```

| Aspect            | Description                                                    |
| ----------------- | -------------------------------------------------------------- |
| **Rôle**          | Crée l'onglet "Annuler"                                        |
| **Widgets créés** | Combobox (trajet) + Entry (nom) + Bouton rouge + Zone de texte |
| **Variables**     | `self.var_trajet_annuler`, `self.entry_nom_annuler`            |

---

### **`annuler_reservation(self)`**

```python
def annuler_reservation(self):
```

| Aspect            | Description                                                                  |
| ----------------- | ---------------------------------------------------------------------------- |
| **Rôle**          | Annule une réservation existante                                             |
| **Validations**   | 4 vérifications (trajet choisi, nom rempli, trajet existe, passager inscrit) |
| **Actions si OK** | Retire passager, incrémente places, supprime ticket                          |
| **Appelle**       | `refresh_all_tabs()` pour synchroniser                                       |

**Flux :**

```
Récupère trajet + nom
    ↓
4 validations (erreur si échec)
    ↓
trains[trajet]['passagers'].remove(nom)
trains[trajet]['places_restantes'] += 1
    ↓
Supprime le ticket correspondant
    ↓
Affiche confirmation + rafraîchit tout
```

---

## Onglet 4 : Passagers

### **`setup_tab_passagers(self)`**

```python
def setup_tab_passagers(self):
```

| Aspect            | Description                                                        |
| ----------------- | ------------------------------------------------------------------ |
| **Rôle**          | Crée l'onglet "Passagers"                                          |
| **Widgets créés** | Combobox (trajet) + Tableau (N°, Nom)                              |
| **Événement**     | bind("<<ComboboxSelected>>") - appelle afficher_passagers_trajet() |

---

### **`afficher_passagers_trajet(self)`**

```python
def afficher_passagers_trajet(self):
```

| Aspect      | Description                                                                     |
| ----------- | ------------------------------------------------------------------------------- |
| **Rôle**    | Affiche les passagers du trajet sélectionné                                     |
| **Actions** | 1. Vide le tableau 2. Récupère passagers triés 3. Insère chaque ligne numérotée |
| **Tri**     | `sorted()` pour ordre alphabétique                                              |

---

## Onglet 5 : Trains Complets

### **`setup_tab_complets(self)`**

```python
def setup_tab_complets(self):
```

| Aspect            | Description                                  |
| ----------------- | -------------------------------------------- |
| **Rôle**          | Crée l'onglet "Trains Complets"              |
| **Widgets créés** | Tableau (Code, Places) + Bouton "Rafraîchir" |
| **Appelle**       | `refresh_complets_tab()`                     |

---

### **`refresh_complets_tab(self)`**

```python
def refresh_complets_tab(self):
```

| Aspect      | Description                                   |
| ----------- | --------------------------------------------- |
| **Rôle**    | Met à jour la liste des trains complets       |
| **Logique** | Filtre les trajets où `places_restantes == 0` |
| **Si vide** | Affiche "Aucun train complet"                 |

**Code clé :**

```python
trains_complets = [code for code, info in trains.items()
                   if info['places_restantes'] == 0]
```

---

## Onglet 6 : Tickets

### **`setup_tab_tickets(self)`**

```python
def setup_tab_tickets(self):
```

| Aspect            | Description                                                 |
| ----------------- | ----------------------------------------------------------- |
| **Rôle**          | Crée l'onglet "Tickets"                                     |
| **Widgets créés** | Tableau (N°, Passager, Trajet, Place) + Bouton "Rafraîchir" |
| **Appelle**       | `refresh_tickets_tab()`                                     |

---

### **`refresh_tickets_tab(self)`**

```python
def refresh_tickets_tab(self):
```

| Aspect      | Description                                          |
| ----------- | ---------------------------------------------------- |
| **Rôle**    | Met à jour la liste des tickets                      |
| **Actions** | Parcourt la liste `tickets` et affiche chaque billet |
| **Si vide** | Affiche "Aucun ticket généré"                        |

---

## 🔄 Fonction de synchronisation

### **`refresh_all_tabs(self)`**

```python
def refresh_all_tabs(self):
```

| Aspect          | Description                                                                                              |
| --------------- | -------------------------------------------------------------------------------------------------------- |
| **Rôle**        | Synchronise TOUS les onglets après une action                                                            |
| **Appelle**     | `refresh_trains_tab()`, `refresh_complets_tab()`, `refresh_tickets_tab()`, `afficher_passagers_trajet()` |
| **Appelée par** | `reserver_place()` et `annuler_reservation()`                                                            |

---

## 🚀 Point d'entrée

```python
if __name__ == "__main__":
    root = tk.Tk()
    app = AppReservationTrains(root)
    root.mainloop()
```

| Ligne                              | Description                                                   |
| ---------------------------------- | ------------------------------------------------------------- |
| `root = tk.Tk()`                   | Crée la fenêtre principale                                    |
| `app = AppReservationTrains(root)` | Initialise l'application                                      |
| `root.mainloop()`                  | Lance la boucle d'événements (attend les actions utilisateur) |

---

## 📋 Tableau récapitulatif

| Fonction                    | Onglet    | Rôle                        |
| --------------------------- | --------- | --------------------------- |
| `__init__`                  | -         | Initialise l'app            |
| `setup_ui`                  | -         | Construit l'UI              |
| `setup_tab_trains`          | Trains    | Crée l'onglet               |
| `refresh_trains_tab`        | Trains    | Met à jour le tableau       |
| `setup_tab_reserver`        | Réserver  | Crée le formulaire          |
| `reserver_place`            | Réserver  | **Effectue la réservation** |
| `setup_tab_annuler`         | Annuler   | Crée le formulaire          |
| `annuler_reservation`       | Annuler   | **Effectue l'annulation**   |
| `setup_tab_passagers`       | Passagers | Crée l'onglet               |
| `afficher_passagers_trajet` | Passagers | Affiche les passagers       |
| `setup_tab_complets`        | Complets  | Crée l'onglet               |
| `refresh_complets_tab`      | Complets  | Met à jour                  |
| `setup_tab_tickets`         | Tickets   | Crée l'onglet               |
| `refresh_tickets_tab`       | Tickets   | Met à jour                  |
| `refresh_all_tabs`          | Tous      | **Synchronise tout**        |

---

**Document généré le 3 décembre 2025**
