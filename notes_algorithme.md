# Notes sur l'algorithme de la Tour de Hanoï

## Règles du jeu
1. Un seul disque peut être déplacé à la fois
2. Seul le disque du dessus d'une pile peut être déplacé
3. Un disque ne peut pas être placé sur un disque plus petit

## Algorithme récursif
L'algorithme récursif pour déplacer n disques de la source vers la destination :

1. **Cas de base** : Si n = 1, déplacer directement le disque de la source vers la destination
2. **Cas récursif** :
   - Déplacer les n-1 disques du dessus de la source vers l'auxiliaire
   - Déplacer le disque le plus grand de la source vers la destination
   - Déplacer les n-1 disques de l'auxiliaire vers la destination

## Formule du nombre minimum de mouvements
Pour n disques : **2^n - 1** mouvements

## Complexité
- **Temps** : O(2^n)
- **Espace** : O(n) pour la pile de récursion

## Exemple d'implémentation Python
```python
def TowerOfHanoi(n, source, destination, auxiliary):
    if n == 1:
        print(f"Move disk 1 from {source} to {destination}")
        return
    TowerOfHanoi(n-1, source, auxiliary, destination)
    print(f"Move disk {n} from {source} to {destination}")
    TowerOfHanoi(n-1, auxiliary, destination, source)
```

## Format de sortie requis
- Format : "1->3" pour déplacer un disque du bâtonnet 1 au bâtonnet 3
- Paramètres d'entrée : "8,3" pour 8 disques et 3 bâtonnets

