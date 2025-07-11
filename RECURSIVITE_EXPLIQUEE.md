# 🔄 LA RÉCURSIVITÉ DANS NOTRE PROGRAMME TOUR DE HANOÏ

## ✅ **RÉPONSE DIRECTE : OUI, LE PROGRAMME UTILISE LA RÉCURSIVITÉ**

Notre programme Tour de Hanoï utilise **exclusivement la récursivité** pour résoudre le puzzle. C'est même le cœur de l'algorithme !

---

## 🧠 **QU'EST-CE QUE LA RÉCURSIVITÉ ?**

La récursivité est une technique de programmation où **une fonction s'appelle elle-même** pour résoudre un problème en le décomposant en sous-problèmes plus petits.

### 📋 **Composants essentiels :**
1. **CAS DE BASE** : Condition d'arrêt (quand arrêter la récursion)
2. **CAS RÉCURSIF** : La fonction s'appelle elle-même avec des paramètres modifiés
3. **PROGRESSION** : Chaque appel récursif se rapproche du cas de base

---

## 🔍 **RÉCURSIVITÉ DANS NOTRE CODE**

### 📄 **Fonction récursive principale :**

```python
def hanoi_recursive(n: int, source: int, destination: int, auxiliary: int, moves: List[str], verbose: bool = True) -> None:
    # 🛑 CAS DE BASE : Si un seul disque, déplacer directement
    if n == 1:
        move = f"{source}->{destination}"
        moves.append(move)
        if verbose:
            print(move)
        return
    
    # 🔄 CAS RÉCURSIF : Décomposer en 3 étapes
    
    # Étape 1: Déplacer n-1 disques vers auxiliaire (RÉCURSION)
    hanoi_recursive(n-1, source, auxiliary, destination, moves, verbose)
    
    # Étape 2: Déplacer le gros disque vers destination
    move = f"{source}->{destination}"
    moves.append(move)
    if verbose:
        print(move)
    
    # Étape 3: Déplacer n-1 disques vers destination finale (RÉCURSION)
    hanoi_recursive(n-1, auxiliary, destination, source, moves, verbose)
```

### 🎯 **Analyse de la récursivité :**

1. **CAS DE BASE** : `if n == 1` → Arrête la récursion
2. **APPELS RÉCURSIFS** : La fonction `hanoi_recursive` s'appelle **2 fois** elle-même
3. **PROGRESSION** : À chaque appel, `n` diminue de 1, se rapprochant du cas de base

---

## 🔢 **EXEMPLE CONCRET : 3 DISQUES**

Voici comment la récursivité se déroule pour 3 disques :

```
hanoi_recursive(3, 1, 3, 2)  ← APPEL INITIAL
├── hanoi_recursive(2, 1, 2, 3)  ← RÉCURSION 1
│   ├── hanoi_recursive(1, 1, 3, 2)  ← CAS DE BASE: 1->3
│   ├── Déplacer disque 2: 1->2
│   └── hanoi_recursive(1, 3, 2, 1)  ← CAS DE BASE: 3->2
├── Déplacer disque 3: 1->3
└── hanoi_recursive(2, 2, 3, 1)  ← RÉCURSION 2
    ├── hanoi_recursive(1, 2, 1, 3)  ← CAS DE BASE: 2->1
    ├── Déplacer disque 2: 2->3
    └── hanoi_recursive(1, 1, 3, 2)  ← CAS DE BASE: 1->3
```

**Résultat :** `1->3, 1->2, 3->2, 1->3, 2->1, 2->3, 1->3` (7 mouvements)

---

## 🧪 **DÉMONSTRATION PRATIQUE**

### 🚀 **Test avec 2 disques :**
```bash
$ python main.py "2,3"
1->2    # Premier appel récursif (n=1)
1->3    # Déplacement du gros disque
2->3    # Deuxième appel récursif (n=1)
```

### 🚀 **Test avec 3 disques :**
```bash
$ python main.py "3,3"
1->3    # Récursion niveau 1
1->2    # Récursion niveau 1
3->2    # Récursion niveau 1
1->3    # Déplacement du gros disque
2->1    # Récursion niveau 2
2->3    # Récursion niveau 2
1->3    # Récursion niveau 2
```

---

## 📊 **PROPRIÉTÉS DE NOTRE RÉCURSIVITÉ**

### ✅ **Avantages :**
- **Élégance** : Code court et lisible (15 lignes)
- **Optimalité** : Solution garantie en 2^n - 1 mouvements
- **Correction** : Algorithme mathématiquement prouvé
- **Simplicité** : Logique naturelle du problème

### ⚠️ **Complexité :**
- **Temporelle** : O(2^n) - exponentielle
- **Spatiale** : O(n) - pile de récursion
- **Appels récursifs** : Exactement 2^n - 1 appels

---

## 🔬 **SCRIPT DE DÉMONSTRATION**

Nous avons créé un script spécial pour visualiser la récursivité :

```bash
$ python demo_recursivite.py
```

Ce script montre **en détail** comment chaque appel récursif se décompose.

---

## 🎯 **POURQUOI LA RÉCURSIVITÉ EST PARFAITE ICI ?**

1. **Problème naturellement récursif** : La Tour de Hanoï se décompose naturellement
2. **Structure fractale** : Résoudre n disques = résoudre 2 fois (n-1) disques
3. **Élégance mathématique** : Correspond à la définition mathématique du problème
4. **Preuve de correction** : Plus facile à prouver qu'un algorithme itératif

---

## ✅ **CONCLUSION**

**OUI, notre programme utilise la récursivité de manière intensive et exclusive !**

- ✅ **Algorithme 100% récursif**
- ✅ **Cas de base clairement défini** (n=1)
- ✅ **Appels récursifs multiples** (2 par niveau)
- ✅ **Solution optimale garantie**
- ✅ **Code élégant et maintenable**

La récursivité n'est pas juste utilisée, elle **EST** l'essence même de notre algorithme de résolution de la Tour de Hanoï !

---

*Pour voir la récursivité en action, lancez `python demo_recursivite.py` 🚀*

