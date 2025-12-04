# 🖥️ Fonctionnement de l'Interface Graphique - Système de Réservation de Trains

## Table des matières

1. [Fondamentaux Tkinter](#fondamentaux-tkinter)
2. [Architecture UI](#architecture-ui)
3. [Les Widgets utilisés](#les-widgets-utilisés)
4. [Système de couleurs et polices](#système-de-couleurs-et-polices)
5. [Les 6 Onglets en détail](#les-6-onglets-en-détail)
6. [Gestion des événements](#gestion-des-événements)
7. [Synchronisation des données](#synchronisation-des-données)

---

## Fondamentaux Tkinter

### Qu'est-ce que Tkinter ?

Tkinter est la **bibliothèque graphique native de Python** pour créer des interfaces utilisateur (GUI).

```python
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
```

**Imports expliqués :**

- `tk` : Module principal Tkinter
- `ttk` : Theme Tkinter (widgets modernes avec thèmes)
- `messagebox` : Boîtes de dialogue (erreur, info, etc.)
- `tkFont` : Gestion des polices personnalisées

### Structure de base

```python
root = tk.Tk()              # Crée la fenêtre principale
app = AppReservationTrains(root)  # Initialise l'app
root.mainloop()             # Lance la boucle d'événements
```

---

## Architecture UI

### Hiérarchie de la fenêtre

```
┌────────────────────────────────────────────────┐
│        FENÊTRE PRINCIPALE (tk.Tk)              │
│                  900x700px                     │
├────────────────────────────────────────────────┤
│                                                │
│  ┌──────────────────────────────────────────┐ │
│  │ EN-TÊTE (Header Frame)                   │ │
│  │ Fond : #2c3e50 (bleu foncé)              │ │
│  │ ┌──────────────────────────────────────┐ │ │
│  │ │ SYSTÈME DE RÉSERVATION DE TRAINS    │ │ │
│  │ │ (Titre blanc, Helvetica 16, gras)  │ │ │
│  │ └──────────────────────────────────────┘ │ │
│  └──────────────────────────────────────────┘ │
│                                                │
│  ┌──────────────────────────────────────────┐ │
│  │ NOTEBOOK (Onglets)                       │ │
│  │ ┌──────┬──────┬─────┬──────┬────┬────┐  │ │
│  │ │Trains│Réser.│Annu.│Pass.│Cpl.│Tkt.│  │ │
│  │ ├──────────────────────────────────┤  │ │
│  │ │  CONTENU DE L'ONGLET ACTIF      │  │ │
│  │ │                                 │  │ │
│  │ │  (Change selon l'onglet)        │  │ │
│  │ │                                 │  │ │
│  │ └──────────────────────────────────┘  │ │
│  └──────────────────────────────────────────┘ │
│                                                │
└────────────────────────────────────────────────┘
```

### Code de création de la fenêtre

```python
def __init__(self, root):
    self.root = root

    # Paramètres de la fenêtre
    self.root.title("Système de Réservation de Trains")  # Titre
    self.root.geometry("900x700")                        # Taille
    self.root.resizable(True, True)                      # Redimensionnable

    # Couleur de fond
    self.root.config(bg=self.bg_color)  # #f0f0f0 (gris clair)

    # Appeler setup_ui() pour construire l'interface
    self.setup_ui()
```

---

## Les Widgets utilisés

### 1. **Frame** - Conteneur

Organise les autres widgets en zones.

```python
frame = tk.Frame(tab, bg=self.bg_color)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
```

**Attributs clés :**

- `bg` : Couleur de fond
- `pack()` : Position le widget (remplir l'espace, avec marge)
- `fill=tk.BOTH` : Remplit horizontalement et verticalement
- `expand=True` : Agrandir si la fenêtre s'agrandit
- `padx`, `pady` : Marges extérieures

### 2. **Label** - Texte statique

Affiche du texte (titres, labels).

```python
title = tk.Label(
    frame,
    text="Réserver une Place",
    font=self.header_font,      # Police personnalisée
    bg=self.bg_color,           # Fond
    fg="white"                  # Texte blanc
)
title.pack(pady=(0, 20))        # Marge en bas
```

### 3. **Entry** - Champ de saisie

Permet à l'utilisateur de taper du texte.

```python
self.entry_nom_reserver = tk.Entry(
    nom_frame,
    font=self.normal_font,
    width=25                    # Largeur en caractères
)
self.entry_nom_reserver.pack(side=tk.LEFT, padx=5)
```

**Méthodes importantes :**

```python
# Récupérer la valeur
nom = self.entry_nom_reserver.get()

# Effacer le champ
self.entry_nom_reserver.delete(0, tk.END)  # Du début à la fin

# Insérer du texte
self.entry_nom_reserver.insert(0, "Ahmed")
```

### 4. **Combobox (ttk)** - Liste déroulante

```python
self.var_trajet_reserver = tk.StringVar()  # Variable pour stocker la sélection

trajets_combo = ttk.Combobox(
    trajet_frame,
    textvariable=self.var_trajet_reserver,  # Lié à la variable
    values=list(trains.keys()),              # ['TUN-PAR', 'TUN-ROM', 'TUN-MAD']
    state="readonly",                        # Lecture seule (pas d'édition)
    width=20
)
trajets_combo.pack(side=tk.LEFT, padx=5)
```

**Récupérer la sélection :**

```python
code_trajet = self.var_trajet_reserver.get()  # 'TUN-PAR'
```

### 5. **Button** - Bouton

Bouton cliquable qui appelle une fonction.

```python
btn = tk.Button(
    btn_frame,
    text="Confirmer la Réservation",
    command=self.reserver_place,        # Fonction appelée au clic
    bg=self.success_color,              # Couleur fond (vert)
    fg="white",                         # Couleur texte
    padx=20, pady=10,                   # Marges intérieures
    font=self.header_font
)
btn.pack()
```

### 6. **Text** - Zone de texte multiligne

Affiche du texte formaté sur plusieurs lignes.

```python
self.text_reserver = tk.Text(
    frame,
    height=10,                          # Hauteur en lignes
    font=self.normal_font,
    wrap=tk.WORD                        # Retour à la ligne automatique
)
self.text_reserver.pack(fill=tk.BOTH, expand=True, pady=10)
```

**Utilisation :**

```python
# Effacer tout le contenu
self.text_reserver.delete(1.0, tk.END)  # De la ligne 1, colonne 0 à la fin

# Insérer du texte
self.text_reserver.insert(tk.END, "Résultat ici")
```

### 7. **Treeview (ttk)** - Tableau

Affiche des données dans un tableau avec colonnes.

```python
self.trains_tree = ttk.Treeview(
    trains_frame,
    columns=("Code", "Restantes", "Total", "Statut"),  # Noms des colonnes
    height=15,                          # Hauteur affichage
    show="headings"                     # Afficher les en-têtes
)

# Configurer les colonnes
self.trains_tree.column("Code", width=150, anchor=tk.CENTER)
                                        # Centrer le texte

# Définir les en-têtes
self.trains_tree.heading("Code", text="Code Trajet")

# Insérer une ligne
self.trains_tree.insert("", tk.END, values=("TUN-PAR", 5, 5, "Disponible"))

# Vider le tableau
for item in self.trains_tree.get_children():
    self.trains_tree.delete(item)
```

### 8. **Notebook (ttk)** - Système d'onglets

```python
self.notebook = ttk.Notebook(self.root)
self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Ajouter un onglet
tab = ttk.Frame(self.notebook)
self.notebook.add(tab, text="Trains")  # "Trains" = nom de l'onglet
```

---

## Système de couleurs et polices

### 🎨 Palette de couleurs

```python
self.bg_color = "#f0f0f0"        # Gris très clair (fond principal)
self.header_color = "#2c3e50"    # Bleu foncé (en-tête)
self.button_color = "#3498db"    # Bleu ciel (boutons standards)
self.success_color = "#27ae60"   # Vert (bouton réserver/succès)
self.error_color = "#e74c3c"     # Rouge (bouton annuler/erreur)
```

**Utilisation :**

```python
# Fond gris
frame = tk.Frame(tab, bg=self.bg_color)

# Bouton vert
btn = tk.Button(..., bg=self.success_color, fg="white")

# Bouton rouge
btn = tk.Button(..., bg=self.error_color, fg="white")
```

### 🔤 Polices personnalisées

```python
self.title_font = tkFont.Font(
    family="Helvetica",      # Police
    size=16,                 # Taille (points)
    weight="bold"            # Gras
)

self.header_font = tkFont.Font(
    family="Helvetica",
    size=12,
    weight="bold"
)

self.normal_font = tkFont.Font(
    family="Helvetica",
    size=10
    # weight="normal" (par défaut)
)
```

**Utilisation :**

```python
title = tk.Label(..., font=self.title_font)      # Très gros
header = tk.Label(..., font=self.header_font)    # Moyen gras
text = tk.Label(..., font=self.normal_font)      # Normal
```

---

## Les 6 Onglets en détail

### ONGLET 1️⃣ : "Trains" - Consulter les trajets

**Workflow :**

```
setup_tab_trains()
    ↓
Crée le frame et le titre
    ↓
Crée le Treeview (tableau)
    ↓
Ajoute bouton "Rafraîchir"
    ↓
Appelle refresh_trains_tab()
    ↓
Affiche les trajets dans le tableau
```

**Code complet :**

```python
def setup_tab_trains(self):
    # 1. Créer l'onglet
    tab = ttk.Frame(self.notebook)
    self.notebook.add(tab, text="Trains")

    # 2. Frame principal (conteneur)
    frame = tk.Frame(tab, bg=self.bg_color)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # 3. Titre
    title = tk.Label(
        frame,
        text="Liste des Trajets Disponibles",
        font=self.header_font,
        bg=self.bg_color
    )
    title.pack(pady=(0, 20))

    # 4. Frame blanc pour le tableau
    trains_frame = tk.Frame(frame, bg="white")
    trains_frame.pack(fill=tk.BOTH, expand=True)

    # 5. Créer le Treeview (tableau)
    self.trains_tree = ttk.Treeview(
        trains_frame,
        columns=("Code", "Restantes", "Total", "Statut"),
        height=15,
        show="headings"
    )

    # 6. Configurer les colonnes
    self.trains_tree.column("Code", width=150, anchor=tk.CENTER)
    self.trains_tree.column("Restantes", width=150, anchor=tk.CENTER)
    self.trains_tree.column("Total", width=150, anchor=tk.CENTER)
    self.trains_tree.column("Statut", width=150, anchor=tk.CENTER)

    # 7. Définir les en-têtes
    self.trains_tree.heading("Code", text="Code Trajet")
    self.trains_tree.heading("Restantes", text="Places Restantes")
    self.trains_tree.heading("Total", text="Places Total")
    self.trains_tree.heading("Statut", text="Statut")

    # 8. Afficher le tableau
    self.trains_tree.pack(fill=tk.BOTH, expand=True)

    # 9. Frame pour les boutons
    btn_frame = tk.Frame(frame, bg=self.bg_color)
    btn_frame.pack(fill=tk.X, pady=(10, 0))

    # 10. Bouton Rafraîchir
    btn_refresh = tk.Button(
        btn_frame,
        text="Rafraîchir",
        command=self.refresh_trains_tab,
        bg=self.button_color,
        fg="white",
        padx=15,
        pady=5,
        font=self.normal_font
    )
    btn_refresh.pack()

    # 11. Charger les données
    self.refresh_trains_tab()

def refresh_trains_tab(self):
    """Remplit le tableau avec les données actuelles"""

    # 1. Vider le tableau
    for item in self.trains_tree.get_children():
        self.trains_tree.delete(item)

    # 2. Pour chaque trajet...
    for code_trajet, info in trains.items():
        places_restantes = info['places_restantes']
        places_total = info['places_total']

        # 3. Déterminer le statut
        statut = "Disponible" if places_restantes > 0 else "COMPLET"

        # 4. Insérer une ligne dans le tableau
        self.trains_tree.insert(
            "",
            tk.END,
            values=(code_trajet, places_restantes, places_total, statut)
        )
```

**Affichage exemple :**

```
Code Trajet  │ Places Restantes │ Places Total │ Statut
─────────────┼──────────────────┼──────────────┼──────────
TUN-PAR      │        3         │      5       │ Disponible
TUN-ROM      │        0         │      3       │ COMPLET
TUN-MAD      │        4         │      4       │ Disponible
```

---

### ONGLET 2️⃣ : "Réserver" - Créer une réservation

**Structure :**

```
setup_tab_reserver()
    ├─ Titre
    ├─ Frame 1 : Sélection du trajet (Combobox)
    ├─ Frame 2 : Saisie du nom (Entry)
    ├─ Frame 3 : Bouton "Confirmer" (Button)
    └─ Zone de résultat (Text)
```

**Code clé du formulaire :**

```python
def setup_tab_reserver(self):
    # ... (création du tab et frame)

    # ===== SECTION 1 : Choix du trajet =====
    trajet_frame = tk.Frame(frame, bg=self.bg_color)
    trajet_frame.pack(fill=tk.X, pady=10)

    # Label "Trajet :"
    tk.Label(
        trajet_frame,
        text="Trajet :",
        font=self.normal_font,
        bg=self.bg_color,
        width=15,
        anchor="w"
    ).pack(side=tk.LEFT, padx=5)

    # Variable pour stocker la sélection
    self.var_trajet_reserver = tk.StringVar()

    # Combobox déroulant
    trajets_combo = ttk.Combobox(
        trajet_frame,
        textvariable=self.var_trajet_reserver,
        values=list(trains.keys()),  # ['TUN-PAR', 'TUN-ROM', 'TUN-MAD']
        state="readonly",            # Pas modifiable
        width=20,
        font=self.normal_font
    )
    trajets_combo.pack(side=tk.LEFT, padx=5)

    # ===== SECTION 2 : Nom du passager =====
    nom_frame = tk.Frame(frame, bg=self.bg_color)
    nom_frame.pack(fill=tk.X, pady=10)

    tk.Label(
        nom_frame,
        text="Nom du passager :",
        font=self.normal_font,
        bg=self.bg_color,
        width=15,
        anchor="w"
    ).pack(side=tk.LEFT, padx=5)

    # Champ de saisie
    self.entry_nom_reserver = tk.Entry(
        nom_frame,
        font=self.normal_font,
        width=25
    )
    self.entry_nom_reserver.pack(side=tk.LEFT, padx=5)

    # ===== SECTION 3 : Bouton de confirmation =====
    btn_frame = tk.Frame(frame, bg=self.bg_color)
    btn_frame.pack(fill=tk.X, pady=20)

    btn = tk.Button(
        btn_frame,
        text="Confirmer la Réservation",
        command=self.reserver_place,
        bg=self.success_color,    # VERT
        fg="white",
        padx=20,
        pady=10,
        font=self.header_font
    )
    btn.pack()

    # ===== SECTION 4 : Zone de résultat =====
    self.text_reserver = tk.Text(
        frame,
        height=10,
        font=self.normal_font,
        wrap=tk.WORD
    )
    self.text_reserver.pack(fill=tk.BOTH, expand=True, pady=10)
```

**Affichage visuel :**

```
┌─────────────────────────────────────┐
│   Réserver une Place                │
├─────────────────────────────────────┤
│ Trajet :        [TUN-PAR ▼]         │ ← Combobox
├─────────────────────────────────────┤
│ Nom du passager : [Ahmed          ] │ ← Entry
├─────────────────────────────────────┤
│     [Confirmer la Réservation]      │ ← Button vert
├─────────────────────────────────────┤
│ RÉSERVATION CONFIRMÉE !             │
│                                     │ ← Text (résultat)
│ Passager : Ahmed Lahmar             │
│ Trajet : TUN-PAR                    │
│ Numéro de place : 4                 │
└─────────────────────────────────────┘
```

**Fonction de réservation :**

```python
def reserver_place(self):
    # 1. RÉCUPÉRER LES DONNÉES SAISIES
    code_trajet = self.var_trajet_reserver.get().upper().strip()
    nom_passager = self.entry_nom_reserver.get().strip()

    # 2. NETTOYER LA ZONE DE RÉSULTAT
    self.text_reserver.delete(1.0, tk.END)

    # 3. VALIDATIONS (5 vérifications)
    if not code_trajet:
        messagebox.showerror("Erreur", "Veuillez sélectionner un trajet.")
        return

    if not nom_passager:
        messagebox.showerror("Erreur", "Veuillez entrer le nom du passager.")
        return

    if code_trajet not in trains:
        messagebox.showerror("Erreur", f"Le trajet '{code_trajet}' n'existe pas.")
        return

    if nom_passager in trains[code_trajet]['passagers']:
        messagebox.showerror("Erreur",
            f"{nom_passager} est déjà inscrit(e) sur le trajet {code_trajet}.")
        return

    if trains[code_trajet]['places_restantes'] <= 0:
        messagebox.showerror("Erreur", f"Le trajet {code_trajet} est complet.")
        return

    # 4. EFFECTUER LA RÉSERVATION (modifier les données)
    trains[code_trajet]['passagers'].add(nom_passager)
    trains[code_trajet]['places_restantes'] -= 1

    # 5. CRÉER LE TICKET
    numero_place = trains[code_trajet]['places_total'] - \
                   trains[code_trajet]['places_restantes']
    ticket = (nom_passager, code_trajet, numero_place)
    tickets.append(ticket)

    # 6. AFFICHER LE RÉSULTAT
    resultat = f"""
 RÉSERVATION CONFIRMÉE !

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Passager : {nom_passager}
Trajet : {code_trajet}
Numéro de place : {numero_place}
Places restantes : {trains[code_trajet]['places_restantes']}/{trains[code_trajet]['places_total']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """

    self.text_reserver.insert(tk.END, resultat)
    messagebox.showinfo("Succès", "Réservation confirmée !")

    # 7. RÉINITIALISER LE FORMULAIRE
    self.var_trajet_reserver.set("")
    self.entry_nom_reserver.delete(0, tk.END)

    # 8. RAFRAÎCHIR TOUS LES ONGLETS
    self.refresh_all_tabs()
```

---

### ONGLET 3️⃣ : "Annuler" - Structure identique à "Réserver"

**Différences principales :**

- Bouton ROUGE (`bg=self.error_color`)
- Validation : vérifier que le passager EST inscrit
- Effectue une suppression au lieu d'une ajout

```python
def annuler_reservation(self):
    # Structure similaire...

    # Au lieu d'AJOUTER le passager :
    trains[code_trajet]['passagers'].remove(nom_passager)
    trains[code_trajet]['places_restantes'] += 1

    # Supprimer le ticket correspondant
    global tickets
    tickets = [t for t in tickets
               if not (t[0] == nom_passager and t[1] == code_trajet)]

    # Rafraîchir
    self.refresh_all_tabs()
```

---

### ONGLET 4️⃣ : "Passagers" - Lister les passagers

**Points clés :**

- Combobox pour sélectionner un trajet
- Tableau Treeview pour afficher les passagers
- Événement `bind()` pour synchroniser

```python
def setup_tab_passagers(self):
    # ... (création du tab et frame)

    # Combobox
    self.var_trajet_passagers = tk.StringVar()
    trajets_combo = ttk.Combobox(
        trajet_frame,
        textvariable=self.var_trajet_passagers,
        values=list(trains.keys()),
        state="readonly"
    )
    trajets_combo.pack(side=tk.LEFT, padx=5)

    # ⭐ ÉVÉNEMENT : Quand la sélection change
    trajets_combo.bind("<<ComboboxSelected>>",
                      lambda e: self.afficher_passagers_trajet())

    # Tableau des passagers
    self.passagers_tree = ttk.Treeview(
        passagers_frame,
        columns=("#", "Nom"),
        height=15,
        show="headings"
    )

    self.passagers_tree.column("#", width=50, anchor=tk.CENTER)
    self.passagers_tree.column("Nom", width=350, anchor=tk.W)

    self.passagers_tree.heading("#", text="N°")
    self.passagers_tree.heading("Nom", text="Nom du Passager")

    self.passagers_tree.pack(fill=tk.BOTH, expand=True)

def afficher_passagers_trajet(self):
    """Appelée quand l'utilisateur sélectionne un trajet"""

    # Récupérer le trajet sélectionné
    code_trajet = self.var_trajet_passagers.get().upper().strip()

    # Vider le tableau
    for item in self.passagers_tree.get_children():
        self.passagers_tree.delete(item)

    # Vérifier que le trajet existe
    if code_trajet not in trains:
        return

    # Récupérer les passagers et les trier alphabétiquement
    passagers = sorted(trains[code_trajet]['passagers'])

    # Ajouter chaque passager avec numéro
    for i, nom in enumerate(passagers, 1):  # enumerate(list, 1) : numéro à partir de 1
        self.passagers_tree.insert("", tk.END, values=(i, nom))
```

**Affichage exemple :**

```
Sélectionner un trajet : [TUN-PAR ▼]

N° │ Nom du Passager
───┼──────────────────
 1 │ Ahmed Lahmar
 2 │ Fatima Ben Ali
 3 │ Mohamed Krim
```

---

### ONGLET 5️⃣ : "Trains Complets"

Affiche UNIQUEMENT les trajets avec 0 places restantes.

```python
def refresh_complets_tab(self):
    # Vider le tableau
    for item in self.complets_tree.get_children():
        self.complets_tree.delete(item)

    # Créer une liste des trajets complets
    # (places_restantes == 0)
    trains_complets = [code for code, info in trains.items()
                       if info['places_restantes'] == 0]

    if trains_complets:
        # Afficher chaque trajet complet
        for code_trajet in trains_complets:
            self.complets_tree.insert("", tk.END,
                values=(code_trajet, trains[code_trajet]['places_total']))
    else:
        # Message si aucun train complet
        self.complets_tree.insert("", tk.END,
                                 values=("Aucun train complet", ""))
```

---

### ONGLET 6️⃣ : "Tickets" - Voir tous les billets

Affiche la liste complète des tickets générés.

```python
def refresh_tickets_tab(self):
    # Vider le tableau
    for item in self.tickets_tree.get_children():
        self.tickets_tree.delete(item)

    if tickets:  # Si la liste n'est pas vide
        # tickets = [(nom, trajet, place), ...]
        for i, (nom, trajet, place) in enumerate(tickets, 1):
            self.tickets_tree.insert("", tk.END,
                values=(i, nom, trajet, place))
    else:
        # Message si aucun ticket
        self.tickets_tree.insert("", tk.END,
            values=("", "Aucun ticket généré", "", ""))
```

**Affichage exemple :**

```
# │ Passager        │ Trajet   │ Place
──┼─────────────────┼──────────┼──────
1 │ Ahmed Lahmar    │ TUN-PAR  │ 4
2 │ Fatima Ben Ali  │ TUN-ROM  │ 2
3 │ Mohamed Krim    │ TUN-PAR  │ 5
```

---

## Gestion des événements

### Types d'événements

#### 1. **Clic sur un bouton**

```python
btn = tk.Button(
    btn_frame,
    text="Confirmer la Réservation",
    command=self.reserver_place  # Fonction appelée au clic
)
```

**Flux :**

```
Utilisateur clique sur le bouton
            ↓
Tkinter appelle self.reserver_place()
            ↓
La fonction s'exécute
            ↓
Les données sont modifiées
            ↓
L'interface est mise à jour
```

#### 2. **Sélection dans une Combobox**

```python
trajets_combo = ttk.Combobox(...)
trajets_combo.bind("<<ComboboxSelected>>", lambda e: self.afficher_passagers_trajet())
```

**Flux :**

```
Utilisateur sélectionne un trajet dans la Combobox
            ↓
L'événement "<<ComboboxSelected>>" est déclenché
            ↓
Tkinter appelle la fonction lambda
            ↓
self.afficher_passagers_trajet() est exécutée
            ↓
Le tableau des passagers se met à jour
```

#### 3. **Boîtes de dialogue**

```python
from tkinter import messagebox

# Afficher une erreur
messagebox.showerror("Titre", "Message d'erreur")

# Afficher une info
messagebox.showinfo("Titre", "Message informatif")
```

---

## Synchronisation des données

### Le problème

Quand l'utilisateur fait une réservation :

1. Les données changent (trains, tickets)
2. Tous les onglets doivent se mettre à jour
3. Sinon, les données affichées seraient obsolètes

### La solution : `refresh_all_tabs()`

```python
def refresh_all_tabs(self):
    """Synchronise TOUS les onglets"""

    # 1. Rafraîchir la liste des trains
    self.refresh_trains_tab()

    # 2. Rafraîchir les trains complets
    self.refresh_complets_tab()

    # 3. Rafraîchir les tickets
    self.refresh_tickets_tab()

    # 4. Rafraîchir les passagers si un trajet est sélectionné
    if self.var_trajet_passagers.get():
        self.afficher_passagers_trajet()
```

**Appelée après :**

- ✅ Une nouvelle réservation
- ✅ Une annulation
- ✅ Toute modification des données

### Exemple de flux complet

```
UTILISATEUR FAIT UNE RÉSERVATION
            ↓
reserver_place() est appelée
            ↓
Validations (5 vérifications)
            ↓
Modification des données :
  - trains['TUN-PAR']['passagers'].add('Ahmed')
  - trains['TUN-PAR']['places_restantes'] -= 1
  - tickets.append(('Ahmed', 'TUN-PAR', 4))
            ↓
self.refresh_all_tabs() est appelée
            ↓
┌────────────────────────────────────┐
│ Tous les onglets se mettent à jour │
├────────────────────────────────────┤
│ • refresh_trains_tab()             │
│   → Les places restantes changent  │
│                                    │
│ • refresh_complets_tab()           │
│   → Les trains complets sont mises │
│     à jour si nécessaire           │
│                                    │
│ • refresh_tickets_tab()            │
│   → Le nouveau ticket apparaît     │
│                                    │
│ • afficher_passagers_trajet()      │
│   → La liste des passagers change  │
└────────────────────────────────────┘
```

---

## Diagramme de l'architecture complète

```
┌─────────────────────────────────────────────────┐
│          FENÊTRE PRINCIPALE                     │
│  900x700 pixels, Gris clair #f0f0f0            │
└─────────────────────────────────────────────────┘
            │
        ┌───▼─────────────┐
        │   EN-TÊTE       │
        │ Fond #2c3e50    │
        │ Titre blanc     │
        └────────────────┘
            │
        ┌───▼──────────────────────────────┐
        │      NOTEBOOK (Onglets)          │
        └───┬──────────────────────────────┘
            │
    ┌───────┼───────┬───────┬───────┬───────┬───────┐
    │       │       │       │       │       │       │
    ▼       ▼       ▼       ▼       ▼       ▼       ▼
  Trains Réserver Annuler Passagers Complets Tickets
   [Tab1]  [Tab2]  [Tab3]  [Tab4]   [Tab5]   [Tab6]
    │       │       │       │       │       │
    │   ┌───┴──────────┐    │       │       │
    │   │  Combobox    │    │       │       │
    │   │  + Entry     │    │       │       │
    │   │  + Button    │    │       │       │
    │   │  + Text      │    │       │       │
    │   └──────────────┘    │       │       │
    │                       │       │       │
    └───────────────────────┴───────┴───────┘
            ▲                   ▲
            └─── Données ───────┘
                (trains, tickets)
```

---

## Résumé des concepts clés

| Concept        | Rôle                   | Exemple                             |
| -------------- | ---------------------- | ----------------------------------- |
| **Widget**     | Élément UI             | Button, Entry, Label, Treeview      |
| **Pack**       | Positionnement         | `pack(fill=tk.BOTH, expand=True)`   |
| **Variable**   | Stocke une valeur      | `tk.StringVar()` pour Combobox      |
| **Command**    | Fonction au clic       | `command=self.reserver_place`       |
| **Bind**       | Événement personnalisé | `bind("<<ComboboxSelected>>", ...)` |
| **Refresh**    | Mise à jour            | `refresh_trains_tab()`              |
| **Messagebox** | Dialog                 | `messagebox.showerror()`            |
| **Treeview**   | Tableau                | Affiche données en colonnes         |
| **Notebook**   | Onglets                | Contient 6 onglets                  |

---

**Document généré le 7 novembre 2025**  
**Interface Graphique - Guide Détaillé**
