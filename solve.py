#!/usr/bin/env python3
"""
Module de résolution de la Tour de Hanoï
Implémente l'algorithme récursif pour résoudre le puzzle
"""

import sys
from typing import List, Tuple


def hanoi_recursive(n: int, source: int, destination: int, auxiliary: int, moves: List[str], verbose: bool = True) -> None: 
    if n == 1:
        move = f"{source}->{destination}"
        moves.append(move)
        if verbose:
            print(move)
        return
    
    # Déplacer n-1 disques de source vers auxiliaire
    hanoi_recursive(n-1, source, auxiliary, destination, moves, verbose)
    
    # Déplacer le disque le plus grand de source vers destination
    move = f"{source}->{destination}"
    moves.append(move)
    if verbose:
        print(move)
    
    # Déplacer n-1 disques d'auxiliaire vers destination
    hanoi_recursive(n-1, auxiliary, destination, source, moves, verbose)


def solve_hanoi(n_disks: int, n_rods: int = 3, verbose: bool = True) -> List[str]:
    """
    Résout le problème de la Tour de Hanoï et retourne la liste des mouvements
    
    Args:
        n_disks: Nombre de disques
        n_rods: Nombre de bâtonnets (par défaut 3)
        verbose: Si True, affiche les mouvements
    
    Returns:
        Liste des mouvements sous forme de chaînes "source->destination"
    """
    if n_disks <= 0:
        return []
    
    if n_rods < 3:
        raise ValueError("Il faut au moins 3 bâtonnets pour résoudre la Tour de Hanoï")
    
    moves = []
    
    # Pour l'instant, on implémente seulement le cas classique à 3 bâtonnets
    if n_rods == 3:
        hanoi_recursive(n_disks, 1, 3, 2, moves, verbose)
    else:
        # Pour plus de 3 bâtonnets, on utilise l'algorithme de Frame-Stewart
        # (implémentation simplifiée pour le moment)
        if verbose:
            print(f"Résolution avec {n_rods} bâtonnets non encore implémentée")
            print("Utilisation de l'algorithme classique à 3 bâtonnets")
        hanoi_recursive(n_disks, 1, 3, 2, moves, verbose)
    
    return moves


def calculate_min_moves(n_disks: int) -> int:
    """
    Calcule le nombre minimum de mouvements pour n disques
    
    Args:
        n_disks: Nombre de disques
    
    Returns:
        Nombre minimum de mouvements (2^n - 1)
    """
    return (2 ** n_disks) - 1


def parse_input(input_str: str) -> Tuple[int, int]:
    """
    Parse la chaîne d'entrée au format "n_disks,n_rods"
    
    Args:
        input_str: Chaîne d'entrée (ex: "8,3")
    
    Returns:
        Tuple (nombre de disques, nombre de bâtonnets)
    """
    try:
        parts = input_str.strip().split(',')
        if len(parts) != 2:
            raise ValueError("Format d'entrée invalide. Utilisez: 'n_disks,n_rods'")
        
        n_disks = int(parts[0])
        n_rods = int(parts[1])
        
        if n_disks <= 0:
            raise ValueError("Le nombre de disques doit être positif")
        if n_rods < 3:
            raise ValueError("Il faut au moins 3 bâtonnets")
        
        return n_disks, n_rods
    
    except ValueError as e:
        raise ValueError(f"Erreur de parsing: {e}")


def main():
    """
    Fonction principale pour exécuter le solveur en ligne de commande
    """
    if len(sys.argv) != 2:
        print("Usage: python solve.py 'n_disks,n_rods'")
        print("Exemple: python solve.py '8,3'")
        sys.exit(1)
    
    try:
        n_disks, n_rods = parse_input(sys.argv[1])
        
        print(f"Résolution de la Tour de Hanoï:")
        print(f"- Nombre de disques: {n_disks}")
        print(f"- Nombre de bâtonnets: {n_rods}")
        print(f"- Nombre minimum de mouvements: {calculate_min_moves(n_disks)}")
        print("\nSéquence de mouvements:")
        
        moves = solve_hanoi(n_disks, n_rods)
        
        print(f"\nRésolution terminée en {len(moves)} mouvements.")
        
    except ValueError as e:
        print(f"Erreur: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterruption par l'utilisateur")
        sys.exit(0)


if __name__ == "__main__":
    main()

