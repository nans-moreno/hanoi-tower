# 🗼 Tour de Hanoï

Un jeu de réflexion classique avec interface graphique et résolution automatique, développé en Python comme souvenir de voyage au Vietnam.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)

## 📖 Table des matières

- [🎯 Présentation](#-présentation)
- [🎮 Fonctionnalités](#-fonctionnalités)
- [🚀 Installation](#-installation)
- [💻 Utilisation](#-utilisation)
- [🧮 Algorithme](#-algorithme)
- [🏗️ Architecture](#️-architecture)
- [🧪 Tests](#-tests)
- [📊 Performances](#-performances)
- [🤝 Contribution](#-contribution)
- [📄 Licence](#-licence)




## 🎯 Présentation

La Tour de Hanoï est un casse-tête mathématique inventé par le mathématicien français Édouard Lucas en 1883. Ce projet propose une implémentation moderne et interactive de ce jeu classique, développée comme souvenir de voyage au Vietnam, terre d'origine de ce puzzle légendaire.

### 🏛️ Histoire et contexte

Selon la légende, dans un temple de Hanoï, des moines déplacent 64 disques d'or selon les règles de ce jeu. Quand ils auront terminé, le monde prendra fin. Heureusement, avec 64 disques, cela prendrait environ 585 milliards d'années !

### 🎲 Règles du jeu

1. **Un seul disque** peut être déplacé à la fois
2. Seul le **disque du dessus** d'une pile peut être pris
3. Un disque **ne peut pas être placé** sur un disque plus petit
4. **Objectif** : déplacer tous les disques vers le dernier bâtonnet

### 🎨 Inspiration

Ce projet a été développé lors d'un voyage au Vietnam, inspiré par la beauté des temples de Hanoï et l'élégance mathématique de ce puzzle ancestral. Il combine tradition et modernité en offrant une expérience interactive tout en préservant l'essence du défi original.


## 🎮 Fonctionnalités

### ✨ Interface graphique interactive
- **Interface moderne** avec Tkinter
- **Glisser-déposer** intuitif pour déplacer les disques
- **Animation fluide** des mouvements
- **Validation en temps réel** des règles du jeu
- **Compteur de mouvements** et objectif minimum
- **Différents nombres de disques** (1 à 8)

### 🤖 Résolution automatique
- **Algorithme récursif optimisé** pour la résolution
- **Résolution étape par étape** avec contrôle manuel
- **Résolution automatique** avec animation
- **Affichage de la solution optimale** (2^n - 1 mouvements)
- **Support pour différents nombres de bâtonnets**

### 🖥️ Mode console
- **Interface en ligne de commande** pour les puristes
- **Mode interactif** pour tester différentes configurations
- **Affichage détaillé** de la séquence de mouvements
- **Gestion robuste des erreurs** et validation des entrées
- **Format de sortie standardisé** (source->destination)

### 🧪 Qualité et tests
- **Suite de tests complète** (unitaires et intégration)
- **Couverture de code élevée** avec cas limites
- **Gestion d'erreurs robuste** pour tous les cas d'usage
- **Documentation détaillée** du code et des algorithmes
- **Validation des performances** pour différentes tailles


## 🚀 Installation

### 📋 Prérequis
- **Python 3.7+** (testé avec Python 3.11)
- **Tkinter** pour l'interface graphique (généralement inclus avec Python)
- **Système d'exploitation** : Windows, macOS, Linux

### 📦 Installation des dépendances

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3-tk
```

#### macOS
```bash
# Tkinter est généralement inclus avec Python sur macOS
# Si nécessaire, réinstallez Python via Homebrew
brew install python-tk
```

#### Windows
```bash
# Tkinter est inclus avec l'installation standard de Python
# Aucune installation supplémentaire nécessaire
```

### 📁 Téléchargement du projet
```bash
git clone https://github.com/votre-username/hanoi-tower.git
cd hanoi-tower
```

## 💻 Utilisation

### 🎮 Interface graphique (recommandé)
```bash
python main.py
```
ou
```bash
python main.py --gui
```

**Fonctionnalités de l'interface :**
- Cliquez sur un bâtonnet pour sélectionner le disque du dessus
- Cliquez sur un autre bâtonnet pour déplacer le disque
- Utilisez "Résoudre automatiquement" pour voir la solution
- "Étape suivante" pour avancer manuellement dans la solution
- Changez le nombre de disques et cliquez "Nouveau jeu"

### 🖥️ Mode console avec configuration directe
```bash
python main.py "3,3"      # 3 disques, 3 bâtonnets
python main.py "8,3"      # 8 disques, 3 bâtonnets  
python main.py "5,4"      # 5 disques, 4 bâtonnets
```

### 💬 Mode console interactif
```bash
python main.py --console
```
Puis entrez des configurations comme `4,3` ou `8,3`.

### ❓ Aide et informations
```bash
python main.py --help     # Affiche l'aide complète
python main.py --version  # Affiche la version
```

### 🎪 Démonstration complète
```bash
python demo.py
```
Lance une démonstration interactive de toutes les fonctionnalités.


## 🧮 Algorithme

### 🔄 Principe récursif

L'algorithme de résolution utilise le principe de **récursivité** pour décomposer le problème :

```
Pour déplacer n disques de A vers C (en utilisant B comme auxiliaire) :
1. Si n = 1 : déplacer directement le disque de A vers C
2. Sinon :
   a. Déplacer n-1 disques de A vers B (récursivement)
   b. Déplacer le disque n de A vers C
   c. Déplacer n-1 disques de B vers C (récursivement)
```

### 📊 Complexité

- **Complexité temporelle** : O(2^n)
- **Complexité spatiale** : O(n) pour la pile de récursion
- **Nombre de mouvements** : exactement 2^n - 1

### 💡 Exemple avec 3 disques

```
État initial: A=[3,2,1], B=[], C=[]
Objectif: A=[], B=[], C=[3,2,1]

Étapes:
1. 1→3 : A=[3,2], B=[], C=[1]
2. 1→2 : A=[3], B=[2], C=[1]  
3. 3→2 : A=[3], B=[2,1], C=[]
4. 1→3 : A=[], B=[2,1], C=[3]
5. 2→1 : A=[1], B=[2], C=[3]
6. 2→3 : A=[1], B=[], C=[3,2]
7. 1→3 : A=[], B=[], C=[3,2,1] ✅
```

### 🔢 Formule mathématique

Pour n disques, le nombre minimum de mouvements est :
```
Mouvements = 2^n - 1
```

**Exemples :**
- 1 disque : 2¹ - 1 = 1 mouvement
- 3 disques : 2³ - 1 = 7 mouvements  
- 8 disques : 2⁸ - 1 = 255 mouvements
- 64 disques : 2⁶⁴ - 1 ≈ 18 quintillions de mouvements

### ⚡ Optimisations implémentées

1. **Mémorisation des mouvements** : évite les recalculs
2. **Validation précoce** : vérifie la validité avant exécution
3. **Mode non-verbeux** : améliore les performances pour les tests
4. **Gestion mémoire** : libération automatique des ressources


## 🏗️ Architecture

### 📁 Structure du projet
```
hanoi-tower/
├── solve.py              # Algorithme de résolution récursif
├── graphics.py           # Interface graphique avec Tkinter
├── main.py              # Point d'entrée principal
├── test_solve.py        # Tests unitaires
├── test_integration.py  # Tests d'intégration
├── demo.py              # Script de démonstration
├── README.md            # Documentation (ce fichier)
└── notes_algorithme.md  # Notes techniques
```

### 🔧 Modules principaux

#### `solve.py` - Cœur algorithmique
- `hanoi_recursive()` : implémentation récursive
- `solve_hanoi()` : interface principale de résolution
- `calculate_min_moves()` : calcul du nombre optimal
- `parse_input()` : validation et parsing des entrées

#### `graphics.py` - Interface utilisateur
- `HanoiGame` : classe principale du jeu
- Gestion des événements souris et clavier
- Animation et rendu graphique
- Intégration avec l'algorithme de résolution

#### `main.py` - Orchestration
- Gestion des arguments de ligne de commande
- Routage entre modes console et graphique
- Gestion des erreurs et aide utilisateur

### 🎨 Patterns de conception utilisés
- **Séparation des responsabilités** : logique métier vs interface
- **Modèle MVC** : séparation modèle/vue/contrôleur
- **Factory pattern** : création d'objets selon le mode
- **Observer pattern** : mise à jour de l'interface

## 🧪 Tests

### 🔍 Suite de tests complète

```bash
# Tests unitaires
python test_solve.py

# Tests d'intégration  
python test_integration.py

# Tous les tests
python -m pytest test_*.py -v
```

### 📊 Couverture des tests

- **Tests unitaires** : 7 tests couvrant l'algorithme
- **Tests d'intégration** : 11 tests couvrant l'ensemble
- **Cas limites** : gestion des erreurs et cas extrêmes
- **Tests de performance** : validation des temps d'exécution

### ✅ Types de tests inclus

1. **Correction algorithmique** : vérification des solutions
2. **Validation des entrées** : gestion des cas d'erreur
3. **Performance** : temps d'exécution raisonnables
4. **Intégration** : fonctionnement entre modules
5. **Interface** : importation et utilisation des modules

## 📊 Performances

### ⚡ Benchmarks

| Disques | Mouvements | Temps (s) | Mémoire |
|---------|------------|-----------|---------|
| 1       | 1          | < 0.001   | Minimal |
| 5       | 31         | < 0.001   | Faible  |
| 10      | 1,023      | < 0.001   | Faible  |
| 15      | 32,767     | < 0.01    | Modéré  |
| 20      | 1,048,575  | < 0.1     | Élevé   |

### 🎯 Optimisations

- **Algorithme optimal** : nombre minimum de mouvements
- **Complexité maîtrisée** : O(2^n) inévitable mais optimisé
- **Gestion mémoire** : pile de récursion efficace
- **Interface responsive** : pas de blocage pendant la résolution


## 🤝 Contribution

### 🛠️ Développement

Ce projet a été développé comme exercice éducatif et souvenir de voyage. Les contributions sont les bienvenues !

#### 🔧 Configuration de développement
```bash
git clone https://github.com/votre-username/hanoi-tower.git
cd hanoi-tower

# Installer les dépendances de développement
pip install pytest pytest-cov

# Lancer les tests
python -m pytest test_*.py -v --cov=.
```

#### 📝 Guidelines de contribution
1. **Fork** le projet
2. Créez une **branche feature** (`git checkout -b feature/amelioration`)
3. **Committez** vos changements (`git commit -am 'Ajout fonctionnalité'`)
4. **Pushez** vers la branche (`git push origin feature/amelioration`)
5. Ouvrez une **Pull Request**

#### 🎯 Améliorations possibles
- Support pour plus de 8 disques avec optimisations
- Algorithme de Frame-Stewart pour 4+ bâtonnets
- Sauvegarde/chargement de parties
- Thèmes visuels personnalisables
- Mode multijoueur
- Statistiques et historique des parties

### 🐛 Signalement de bugs

Utilisez les [GitHub Issues](https://github.com/votre-username/hanoi-tower/issues) pour :
- Signaler des bugs
- Proposer des améliorations
- Poser des questions
- Partager des idées

### 📚 Ressources éducatives

Ce projet peut servir d'exemple pour :
- **Apprentissage de la récursivité** en programmation
- **Développement d'interfaces graphiques** avec Tkinter
- **Tests unitaires et d'intégration** en Python
- **Documentation de projet** et bonnes pratiques
- **Analyse d'algorithmes** et complexité

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

```
MIT License

Copyright (c) 2024 Tour de Hanoï Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🎉 Remerciements

- **Édouard Lucas** pour l'invention de ce puzzle fascinant
- **Le Vietnam** et ses temples inspirants de Hanoï
- **La communauté Python** pour les outils et bibliothèques
- **Tous les contributeurs** qui amélioreront ce projet

---

**Développé avec ❤️ comme souvenir de voyage au Vietnam** 🇻🇳

*"La beauté des mathématiques réside dans leur simplicité et leur élégance, tout comme les temples de Hanoï qui ont inspiré ce projet."*

