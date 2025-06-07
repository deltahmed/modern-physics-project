

<h1 align="center"> 
🔲 Visualisation de paquet d'ondes 🔳
</h1>
</p>
<p align="center"> 
  <a href="https://github.com/deltahmed/modern-physics-project">
    <img src="https://img.shields.io/github/contributors/deltahmed/modern-physics-project.svg?style=for-the-badge" alt="Contributors" /> </a>
  <a href="https://github.com/deltahmed/modern-physics-project">
    <img alt="Issues" src="https://img.shields.io/github/issues/deltahmed/modern-physics-project?style=for-the-badge">
    </a>
  <a href="https://github.com/deltahmed/modern-physics-project">
    <img alt="Forks" src="https://img.shields.io/github/forks/deltahmed/modern-physics-project.svg?style=for-the-badge"></a>
  <a href="https://github.com/deltahmed/modern-physics-project">
    <img alt="Stars" src="https://img.shields.io/github/stars/deltahmed/modern-physics-project.svg?style=for-the-badge"></a>
  <a href="https://github.com/deltahmed/modern-physics-project?tab=License-1-ov-file">
    <img src="https://img.shields.io/badge/License-BSD2-blue?style=for-the-badge" alt="License" /> </a>
</p>




## Description

**Visualisation de paquet d'ondes** est une application graphique interactive permettant de simuler et visualiser la propagation d'un paquet d'ondes quantique à travers un potentiel (puits ou marche). L'utilisateur peut configurer les paramètres physiques et observer l'évolution de la densité de probabilité en temps réel grâce à une animation.

## Fonctionnalités

- Interface graphique moderne avec système de paramètres reprise d'un [ancien projet](https://github.com/deltahmed/Generateur-de-labyrinthe)
- Configuration des paramètres physiques :
  - Profondeur du puits (V₀)
  - Rapport E/V₀ (énergie/puits)
  - Étalement du paquet (σ)
  - Position initiale (x₀)
- Animation de la densité de probabilité et du potentiel
- Barre d’outils Matplotlib personnalisée (zoom, déplacement, sauvegarde…)
- Sauvegarde automatique des préférences utilisateur
- Gestion des erreurs et valeurs par défaut robustes

## Installation

### Prérequis

- Python 3.10 ou supérieur
- les dépendances python nécessaire 

### Dépendances Python

Installe les dépendances avec :

```sh
pip3 install customtkinter matplotlib pillow numpy scipy
```

### Fichiers nécessaires

- `VisualisationPaquet.pyw`
- `AffichageGraphique.py`
- `preférences.config` (généré automatiquement si absent)
- Dossier `images/` avec les icônes nécessaires

## Utilisation

Lance simplement l’application :

```sh
python3 VisualisationPaquet.pyw
```

### Étapes principales

1. **Accueil** : Choisis de lancer une visualisation ou d’accéder aux paramètres.
2. **Paramètres de simulation** : Renseigne les valeurs physiques ou utilise les valeurs par défaut.
3. **Visualisation** : Observe l’évolution du paquet d’ondes et du potentiel. Utilise la barre d’outils pour zoomer, sauvegarder, etc.
4. **Paramètres** : Change le thème, la couleur ou la taille de la fenêtre. Réinitialise si besoin.

## Structure du projet

- `VisualisationPaquet.pyw` : Point d’entrée principal, gestion des fenêtres et logique de simulation.
- `AffichageGraphique.py` : Composants graphiques réutilisables (boutons, menus, barres d’outils…).
- `images/` : Icônes pour l’interface et la barre d’outils.
- `preférences.config` : Fichier de configuration utilisateur (géré automatiquement).

## Exemples de paramètres

- **Profondeur du puits (V₀)** : -4000 eV (par défaut)
- **Rapport E/V₀** : 5 (par défaut)
- **Étalement (σ)** : 0.05 m (par défaut)
- **Position initiale (x₀)** : 0.6 m (par défaut)


## Build with
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-blue?style=for-the-badge)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Plotting-orange?style=for-the-badge)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-Theme-green?style=for-the-badge)


## Contributors

<a href="https://github.com/deltahmed/modern-physics-project/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=deltahmed/modern-physics-project" />
</a>


## License

[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](https://raw.githubusercontent.com/deltahmed/modern-physics-project/master/LICENSE)
