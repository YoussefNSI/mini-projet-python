# mini-projet-python
Mini Projet ESAIP - IRA3 
PROJET FAIT PAR GAYA YOUCEF DERADJI , RADOUANE YOUSSEF , LIVOREIL MAROUANE 

Système de Réservation de Trains
Un projet d'application de bureau simple pour gérer les réservations de trains, construit avec Python et l'interface graphique Tkinter.

Ce projet simule les opérations de base d'un système de réservation, permettant de réserver, d'annuler et de consulter l'état des trains et des passagers en temps réel.


Fonctionnalités
L'application est organisée en plusieurs onglets pour une navigation facile :

Trains : Affiche un tableau de tous les trajets disponibles, leur capacité totale, le nombre de places restantes et leur statut ("Disponible" ou "COMPLET").

Réserver : Un formulaire pour effectuer une nouvelle réservation en choisissant un trajet et en entrant le nom du passager.

Annuler : Un formulaire pour annuler une réservation existante à l'aide du trajet et du nom du passager.

Passagers : Permet de sélectionner un trajet pour afficher la liste complète de tous les passagers actuellement inscrits.

Trains Complets : Une vue filtrée affichant uniquement les trains qui n'ont plus de places disponibles.

Tickets : Un journal de tous les tickets valides actuellement générés, montrant le passager, le trajet et le numéro de place attribué.

Technologies utilisées
Python 3

Tkinter (et ttk pour les widgets modernes) : La bibliothèque standard de Python pour les interfaces graphiques (GUI).