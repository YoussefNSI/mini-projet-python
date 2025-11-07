import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import tkinter.font as tkFont

# ===== DONNEES GLOBALES =====
trains = {
    'TUN-PAR': {'places_total': 5, 'places_restantes': 5, 'passagers': set()},
    'TUN-ROM': {'places_total': 3, 'places_restantes': 3, 'passagers': set()},
    'TUN-MAD': {'places_total': 4, 'places_restantes': 4, 'passagers': set()},
}

tickets = []


# ===== APPLICATION PRINCIPALE =====
class AppReservationTrains:
    def __init__(self, root):
        self.root = root
        self.root.title("Système de Réservation de Trains")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Couleurs
        self.bg_color = "#f0f0f0"
        self.header_color = "#2c3e50"
        self.button_color = "#3498db"
        self.success_color = "#27ae60"
        self.error_color = "#e74c3c"
        
        self.root.config(bg=self.bg_color)
        
        # Police
        self.title_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
        self.header_font = tkFont.Font(family="Helvetica", size=12, weight="bold")
        self.normal_font = tkFont.Font(family="Helvetica", size=10)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # En-tête
        header = tk.Frame(self.root, bg=self.header_color)
        header.pack(fill=tk.X, pady=(0, 10))
        
        title = tk.Label(
            header,
            text="SYSTÈME DE RÉSERVATION DE TRAINS",
            font=self.title_font,
            bg=self.header_color,
            fg="white",
            pady=10
        )
        title.pack()
        
        # Cadre principal avec onglets
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Onglet 1: Afficher les trains
        self.setup_tab_trains()
        
        # Onglet 2: Réserver
        self.setup_tab_reserver()
        
        # Onglet 3: Annuler
        self.setup_tab_annuler()
        
        # Onglet 4: Passagers
        self.setup_tab_passagers()
        
        # Onglet 5: Trains complets
        self.setup_tab_complets()
        
        # Onglet 6: Tickets
        self.setup_tab_tickets()
    
    def setup_tab_trains(self):
        """Onglet pour afficher les trains"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Trains")
        
        frame = tk.Frame(tab, bg=self.bg_color)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title = tk.Label(
            frame,
            text="Liste des Trajets Disponibles",
            font=self.header_font,
            bg=self.bg_color
        )
        title.pack(pady=(0, 20))
        
        # Cadre pour les trains
        trains_frame = tk.Frame(frame, bg="white")
        trains_frame.pack(fill=tk.BOTH, expand=True)
        
        self.trains_tree = ttk.Treeview(
            trains_frame,
            columns=("Code", "Restantes", "Total", "Statut"),
            height=15,
            show="headings"
        )
        
        self.trains_tree.column("Code", width=150, anchor=tk.CENTER)
        self.trains_tree.column("Restantes", width=150, anchor=tk.CENTER)
        self.trains_tree.column("Total", width=150, anchor=tk.CENTER)
        self.trains_tree.column("Statut", width=150, anchor=tk.CENTER)
        
        self.trains_tree.heading("Code", text="Code Trajet")
        self.trains_tree.heading("Restantes", text="Places Restantes")
        self.trains_tree.heading("Total", text="Places Total")
        self.trains_tree.heading("Statut", text="Statut")
        
        self.trains_tree.pack(fill=tk.BOTH, expand=True)
        
        # Bouton de rafraîchissement
        btn_frame = tk.Frame(frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
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
        
        self.refresh_trains_tab()
    
    def refresh_trains_tab(self):
        """Rafraîchit l'onglet des trains"""
        # Vider la table
        for item in self.trains_tree.get_children():
            self.trains_tree.delete(item)
        
        # Remplir avec les données actuelles
        for code_trajet, info in trains.items():
            places_restantes = info['places_restantes']
            places_total = info['places_total']
            statut = "Disponible" if places_restantes > 0 else "COMPLET"
            
            self.trains_tree.insert(
                "",
                tk.END,
                values=(code_trajet, places_restantes, places_total, statut)
            )
    
    def setup_tab_reserver(self):
        """Onglet pour réserver une place"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Réserver")
        
        frame = tk.Frame(tab, bg=self.bg_color)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title = tk.Label(
            frame,
            text="Réserver une Place",
            font=self.header_font,
            bg=self.bg_color
        )
        title.pack(pady=(0, 20))
        
        # Choix du trajet
        trajet_frame = tk.Frame(frame, bg=self.bg_color)
        trajet_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            trajet_frame,
            text="Trajet :",
            font=self.normal_font,
            bg=self.bg_color,
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT, padx=5)
        
        self.var_trajet_reserver = tk.StringVar()
        trajets_combo = ttk.Combobox(
            trajet_frame,
            textvariable=self.var_trajet_reserver,
            values=list(trains.keys()),
            state="readonly",
            width=20,
            font=self.normal_font
        )
        trajets_combo.pack(side=tk.LEFT, padx=5)
        
        # Nom du passager
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
        
        self.entry_nom_reserver = tk.Entry(nom_frame, font=self.normal_font, width=25)
        self.entry_nom_reserver.pack(side=tk.LEFT, padx=5)
        
        # Bouton réserver
        btn_frame = tk.Frame(frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=20)
        
        btn = tk.Button(
            btn_frame,
            text="Confirmer la Réservation",
            command=self.reserver_place,
            bg=self.success_color,
            fg="white",
            padx=20,
            pady=10,
            font=self.header_font
        )
        btn.pack()
        
        # Zone de résultat
        self.text_reserver = tk.Text(frame, height=10, font=self.normal_font, wrap=tk.WORD)
        self.text_reserver.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def refresh_all_tabs(self):
        """Rafraîchit tous les onglets"""
        self.refresh_trains_tab()
        self.refresh_complets_tab()
        self.refresh_tickets_tab()
        # Rafraîchir les passagers si un trajet est sélectionné
        if self.var_trajet_passagers.get():
            self.afficher_passagers_trajet()
    
    def reserver_place(self):
        """Effectue une réservation"""
        code_trajet = self.var_trajet_reserver.get().upper().strip()
        nom_passager = self.entry_nom_reserver.get().strip()
        
        self.text_reserver.delete(1.0, tk.END)
        
        # Validations
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
            messagebox.showerror("Erreur", f"{nom_passager} est déjà inscrit(e) sur le trajet {code_trajet}.")
            return
        
        if trains[code_trajet]['places_restantes'] <= 0:
            messagebox.showerror("Erreur", f"Le trajet {code_trajet} est complet.")
            return
        
        # Effectuer la réservation
        trains[code_trajet]['passagers'].add(nom_passager)
        trains[code_trajet]['places_restantes'] -= 1
        
        numero_place = trains[code_trajet]['places_total'] - trains[code_trajet]['places_restantes']
        ticket = (nom_passager, code_trajet, numero_place)
        tickets.append(ticket)
        
        # Afficher le résultat
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
        
        # Réinitialiser les champs
        self.var_trajet_reserver.set("")
        self.entry_nom_reserver.delete(0, tk.END)
        
        # Rafraîchir tous les onglets
        self.refresh_all_tabs()
    
    def setup_tab_annuler(self):
        """Onglet pour annuler une réservation"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Annuler")
        
        frame = tk.Frame(tab, bg=self.bg_color)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title = tk.Label(
            frame,
            text="Annuler une Réservation",
            font=self.header_font,
            bg=self.bg_color
        )
        title.pack(pady=(0, 20))
        
        # Choix du trajet
        trajet_frame = tk.Frame(frame, bg=self.bg_color)
        trajet_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            trajet_frame,
            text="Trajet :",
            font=self.normal_font,
            bg=self.bg_color,
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT, padx=5)
        
        self.var_trajet_annuler = tk.StringVar()
        trajets_combo = ttk.Combobox(
            trajet_frame,
            textvariable=self.var_trajet_annuler,
            values=list(trains.keys()),
            state="readonly",
            width=20,
            font=self.normal_font
        )
        trajets_combo.pack(side=tk.LEFT, padx=5)
        
        # Nom du passager
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
        
        self.entry_nom_annuler = tk.Entry(nom_frame, font=self.normal_font, width=25)
        self.entry_nom_annuler.pack(side=tk.LEFT, padx=5)
        
        # Bouton annuler
        btn_frame = tk.Frame(frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=20)
        
        btn = tk.Button(
            btn_frame,
            text="Annuler la Réservation",
            command=self.annuler_reservation,
            bg=self.error_color,
            fg="white",
            padx=20,
            pady=10,
            font=self.header_font
        )
        btn.pack()
        
        # Zone de résultat
        self.text_annuler = tk.Text(frame, height=10, font=self.normal_font, wrap=tk.WORD)
        self.text_annuler.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def annuler_reservation(self):
        """Annule une réservation"""
        code_trajet = self.var_trajet_annuler.get().upper().strip()
        nom_passager = self.entry_nom_annuler.get().strip()
        
        self.text_annuler.delete(1.0, tk.END)
        
        # Validations
        if not code_trajet:
            messagebox.showerror("Erreur", "Veuillez sélectionner un trajet.")
            return
        
        if not nom_passager:
            messagebox.showerror("Erreur", "Veuillez entrer le nom du passager.")
            return
        
        if code_trajet not in trains:
            messagebox.showerror("Erreur", f"Le trajet '{code_trajet}' n'existe pas.")
            return
        
        if nom_passager not in trains[code_trajet]['passagers']:
            messagebox.showerror("Erreur", f"{nom_passager} n'est pas inscrit(e) sur le trajet {code_trajet}.")
            return
        
        # Effectuer l'annulation
        trains[code_trajet]['passagers'].remove(nom_passager)
        trains[code_trajet]['places_restantes'] += 1
        
        global tickets
        tickets = [t for t in tickets if not (t[0] == nom_passager and t[1] == code_trajet)]
        
        # Afficher le résultat
        resultat = f"""
ANNULATION CONFIRMÉE !

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Passager : {nom_passager}
Trajet : {code_trajet}
Places restantes : {trains[code_trajet]['places_restantes']}/{trains[code_trajet]['places_total']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        self.text_annuler.insert(tk.END, resultat)
        messagebox.showinfo("Succès", "Annulation confirmée !")
        
        # Réinitialiser les champs
        self.var_trajet_annuler.set("")
        self.entry_nom_annuler.delete(0, tk.END)
        
        # Rafraîchir tous les onglets
        self.refresh_all_tabs()
    
    def setup_tab_passagers(self):
        """Onglet pour afficher les passagers"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Passagers")
        
        frame = tk.Frame(tab, bg=self.bg_color)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title = tk.Label(
            frame,
            text="Liste des Passagers par Trajet",
            font=self.header_font,
            bg=self.bg_color
        )
        title.pack(pady=(0, 20))
        
        # Choix du trajet
        trajet_frame = tk.Frame(frame, bg=self.bg_color)
        trajet_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            trajet_frame,
            text="Sélectionner un trajet :",
            font=self.normal_font,
            bg=self.bg_color
        ).pack(side=tk.LEFT, padx=5)
        
        self.var_trajet_passagers = tk.StringVar()
        trajets_combo = ttk.Combobox(
            trajet_frame,
            textvariable=self.var_trajet_passagers,
            values=list(trains.keys()),
            state="readonly",
            width=20,
            font=self.normal_font
        )
        trajets_combo.pack(side=tk.LEFT, padx=5)
        trajets_combo.bind("<<ComboboxSelected>>", lambda e: self.afficher_passagers_trajet())
        
        # Cadre pour les passagers
        passagers_frame = tk.Frame(frame, bg="white")
        passagers_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
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
        """Affiche les passagers du trajet sélectionné"""
        code_trajet = self.var_trajet_passagers.get().upper().strip()
        
        # Vider la table
        for item in self.passagers_tree.get_children():
            self.passagers_tree.delete(item)
        
        if code_trajet not in trains:
            return
        
        passagers = sorted(trains[code_trajet]['passagers'])
        
        for i, nom in enumerate(passagers, 1):
            self.passagers_tree.insert(
                "",
                tk.END,
                values=(i, nom)
            )
    
    def setup_tab_complets(self):
        """Onglet pour afficher les trains complets"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Trains Complets")
        
        frame = tk.Frame(tab, bg=self.bg_color)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title = tk.Label(
            frame,
            text="Trains Complets",
            font=self.header_font,
            bg=self.bg_color
        )
        title.pack(pady=(0, 20))
        
        # Cadre pour les trains complets
        complets_frame = tk.Frame(frame, bg="white")
        complets_frame.pack(fill=tk.BOTH, expand=True)
        
        self.complets_tree = ttk.Treeview(
            complets_frame,
            columns=("Code", "Places"),
            height=15,
            show="headings"
        )
        
        self.complets_tree.column("Code", width=200, anchor=tk.CENTER)
        self.complets_tree.column("Places", width=200, anchor=tk.CENTER)
        
        self.complets_tree.heading("Code", text="Code Trajet")
        self.complets_tree.heading("Places", text="Nombre de Places")
        
        self.complets_tree.pack(fill=tk.BOTH, expand=True)
        
        # Bouton de rafraîchissement
        btn_frame = tk.Frame(frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        btn_refresh = tk.Button(
            btn_frame,
            text="Rafraîchir",
            command=self.refresh_complets_tab,
            bg=self.button_color,
            fg="white",
            padx=15,
            pady=5,
            font=self.normal_font
        )
        btn_refresh.pack()
        
        self.refresh_complets_tab()
    
    def refresh_complets_tab(self):
        """Rafraîchit l'onglet des trains complets"""
        # Vider la table
        for item in self.complets_tree.get_children():
            self.complets_tree.delete(item)
        
        trains_complets = [code for code, info in trains.items() if info['places_restantes'] == 0]
        
        if trains_complets:
            for code_trajet in trains_complets:
                self.complets_tree.insert(
                    "",
                    tk.END,
                    values=(code_trajet, trains[code_trajet]['places_total'])
                )
        else:
            self.complets_tree.insert("", tk.END, values=("Aucun train complet", ""))
    
    def setup_tab_tickets(self):
        """Onglet pour afficher les tickets"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Tickets")
        
        frame = tk.Frame(tab, bg=self.bg_color)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title = tk.Label(
            frame,
            text="Tickets Générés",
            font=self.header_font,
            bg=self.bg_color
        )
        title.pack(pady=(0, 20))
        
        # Cadre pour les tickets
        tickets_frame = tk.Frame(frame, bg="white")
        tickets_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tickets_tree = ttk.Treeview(
            tickets_frame,
            columns=("#", "Passager", "Trajet", "Place"),
            height=15,
            show="headings"
        )
        
        self.tickets_tree.column("#", width=50, anchor=tk.CENTER)
        self.tickets_tree.column("Passager", width=200, anchor=tk.W)
        self.tickets_tree.column("Trajet", width=200, anchor=tk.CENTER)
        self.tickets_tree.column("Place", width=100, anchor=tk.CENTER)
        
        self.tickets_tree.heading("#", text="N°")
        self.tickets_tree.heading("Passager", text="Passager")
        self.tickets_tree.heading("Trajet", text="Trajet")
        self.tickets_tree.heading("Place", text="Place")
        
        self.tickets_tree.pack(fill=tk.BOTH, expand=True)
        
        # Bouton de rafraîchissement
        btn_frame = tk.Frame(frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        btn_refresh = tk.Button(
            btn_frame,
            text="Rafraîchir",
            command=self.refresh_tickets_tab,
            bg=self.button_color,
            fg="white",
            padx=15,
            pady=5,
            font=self.normal_font
        )
        btn_refresh.pack()
        
        self.refresh_tickets_tab()
    
    def refresh_tickets_tab(self):
        """Rafraîchit l'onglet des tickets"""
        # Vider la table
        for item in self.tickets_tree.get_children():
            self.tickets_tree.delete(item)
        
        if tickets:
            for i, (nom, trajet, place) in enumerate(tickets, 1):
                self.tickets_tree.insert(
                    "",
                    tk.END,
                    values=(i, nom, trajet, place)
                )
        else:
            self.tickets_tree.insert("", tk.END, values=("", "Aucun ticket généré", "", ""))


# ===== POINT D'ENTREE =====
if __name__ == "__main__":
    root = tk.Tk()
    app = AppReservationTrains(root)
    root.mainloop()
