# 🗼 Tour de Hanoï

Un jeu de réflexion classique avec interface graphique et résolution automatique intelligente.

## 🎯 Description

La Tour de Hanoï est un puzzle mathématique classique où l'objectif est de déplacer une pile de disques d'un bâtonnet à un autre, en respectant les règles suivantes :
- Seul le disque du dessus peut être déplacé
- Un disque ne peut pas être placé sur un disque plus petit
- Tous les disques doivent finir sur le dernier bâtonnet

## ✨ Fonctionnalités

### 🎮 Interface graphique interactive
- Jeu par glisser-déposer intuitif
- Visualisation en temps réel des mouvements
- Compteur de mouvements et objectif optimal

### 🤖 Résolution automatique intelligente
- **Algorithme récursif optimal** : Solution en 2^n-1 mouvements
- **Solveur BFS avancé** : Fonctionne depuis n'importe quel état du jeu
- **Résolution étape par étape** : Contrôle manuel du rythme

### 💡 Aide intelligente
- **Coups possibles** affichés dans le terminal
- **Coup recommandé** calculé avec algorithme optimal
- **Informations détaillées** sur l'état du jeu en temps réel

### 🖥️ Mode console
- Interface en ligne de commande pour résolution rapide
- Format d'entrée simple : `"n_disques,n_bâtonnets"`
- Affichage de la séquence complète de mouvements

## 🚀 Installation et utilisation

### Prérequis
- Python 3.7+
- tkinter (généralement inclus avec Python)

### Lancement

#### Interface graphique (recommandé)
```bash
python main.py
```

#### Mode console
```bash
python main.py "3,3"    # 3 disques, 3 bâtonnets
python main.py "8,3"    # 8 disques, 3 bâtonnets
```

#### Résolution directe
```bash
python solve.py "5,3"   # Affiche la solution pour 5 disques
```

## 🎮 Comment jouer

### Interface graphique
1. **Sélectionner** : Cliquez sur un bâtonnet contenant des disques
2. **Déplacer** : Cliquez sur le bâtonnet de destination
3. **Observer** : Le terminal affiche les coups possibles et le coup recommandé
4. **Aide** : Utilisez "Résoudre automatiquement" ou "Étape suivante"

### Exemple d'affichage terminal
```
🎯 ÉTAT ACTUEL DU JEU:
   Mouvements effectués: 2
   Minimum théorique: 7

📊 ÉTAT DES BÂTONNETS:
   Bâtonnet 1: [3] (dessus: 3)
   Bâtonnet 2: [2 1] (dessus: 1)
   Bâtonnet 3: [vide]

⭐ COUP RECOMMANDÉ:
   🎯 1->3 (déplacer disque 3) ← MEILLEUR CHOIX

🎮 TOUS LES COUPS POSSIBLES (3):
   1. 1->2 (déplacer disque 3)
   2. 1->3 (déplacer disque 3) ⭐ RECOMMANDÉ
   3. 2->3 (déplacer disque 1)
```

## 🧮 Algorithme

### Principe récursif
L'algorithme utilise la stratégie "diviser pour régner" :
1. Déplacer n-1 disques vers le bâtonnet auxiliaire
2. Déplacer le plus grand disque vers la destination
3. Déplacer n-1 disques vers la destination finale

### Complexité
- **Temporelle** : O(2^n) - nombre de mouvements
- **Spatiale** : O(n) - profondeur de récursion
- **Mouvements optimaux** : 2^n - 1

### Solveur BFS
Pour la résolution depuis un état quelconque, un algorithme BFS (Breadth-First Search) garantit la solution optimale.

## 📁 Structure du projet

```
hanoi-tower-clean/
├── solve.py          # Algorithme récursif principal
├── graphics.py       # Interface graphique avec solveur BFS
├── main.py          # Point d'entrée principal
├── README.md        # Cette documentation
└── LICENSE          # Licence MIT
```

## 🔧 Détails techniques

### Fichiers principaux

- **`solve.py`** : Contient l'algorithme récursif pur de la Tour de Hanoï
- **`graphics.py`** : Interface graphique complète avec solveur BFS avancé
- **`main.py`** : Point d'entrée qui gère les modes console et graphique

### Fonctionnalités avancées

- **Solveur BFS** : Calcule la solution optimale depuis n'importe quel état
- **Coup recommandé** : Indique toujours le meilleur mouvement possible
- **Résolution adaptative** : Fonctionne même après avoir commencé à jouer manuellement
- **Interface responsive** : S'adapte à différentes tailles d'écran

## 🎯 Exemples d'utilisation

### Débutant (3 disques)
```bash
python main.py "3,3"
# Solution en 7 mouvements
```

### Intermédiaire (5 disques)
```bash
python main.py "5,3"
# Solution en 31 mouvements
```

### Avancé (8 disques)
```bash
python main.py "8,3"
# Solution en 255 mouvements
```

## 🏆 Objectifs pédagogiques

Ce projet illustre parfaitement :
- **Récursivité** : Algorithme récursif élégant et efficace
- **Algorithmes de recherche** : BFS pour solution optimale
- **Interfaces utilisateur** : GUI intuitive avec tkinter
- **Programmation modulaire** : Séparation claire des responsabilités
- **Documentation** : Code bien documenté et testé

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

**Développé comme souvenir de voyage au Vietnam** 🇻🇳  
*Honore l'héritage mathématique de la Tour de Hanoï*

