#!/usr/bin/env python3
"""
Script de démonstration pour le projet Tour de Hanoï
Montre toutes les fonctionnalités du projet
"""

import time
import sys
from solve import solve_hanoi, calculate_min_moves


def print_separator(title=""):
    """Affiche un séparateur avec titre optionnel"""
    print("\n" + "="*60)
    if title:
        print(f" {title} ".center(60, "="))
        print("="*60)


def demo_algorithm():
    """Démonstration de l'algorithme de résolution"""
    print_separator("DÉMONSTRATION DE L'ALGORITHME")
    
    print("🎯 L'algorithme récursif de la Tour de Hanoï")
    print("\nPrincipe:")
    print("1. Pour déplacer n disques de A vers C:")
    print("   - Déplacer n-1 disques de A vers B")
    print("   - Déplacer le disque n de A vers C")
    print("   - Déplacer n-1 disques de B vers C")
    print("\n2. Cas de base: 1 disque = déplacement direct")
    
    # Démonstration avec différents nombres de disques
    test_cases = [1, 2, 3, 4, 5]
    
    print(f"\n{'Disques':<8} {'Mouvements':<12} {'Formule 2^n-1':<15} {'Temps (s)':<10}")
    print("-" * 50)
    
    for n in test_cases:
        start_time = time.time()
        moves = solve_hanoi(n, 3, verbose=False)
        end_time = time.time()
        
        expected = calculate_min_moves(n)
        duration = end_time - start_time
        
        print(f"{n:<8} {len(moves):<12} {expected:<15} {duration:.6f}")
    
    print("\n📊 Complexité temporelle: O(2^n)")
    print("📊 Complexité spatiale: O(n) pour la pile de récursion")


def demo_solution_steps():
    """Démonstration détaillée d'une solution"""
    print_separator("SOLUTION DÉTAILLÉE - 3 DISQUES")
    
    n_disks = 3
    print(f"🎮 Résolution pour {n_disks} disques:")
    print(f"📈 Nombre minimum de mouvements: {calculate_min_moves(n_disks)}")
    
    print("\n🎯 État initial:")
    print("Bâtonnet 1: [3, 2, 1]  (du bas vers le haut)")
    print("Bâtonnet 2: []")
    print("Bâtonnet 3: []")
    print("Objectif: déplacer tous les disques vers le bâtonnet 3")
    
    print("\n📋 Séquence de mouvements:")
    moves = solve_hanoi(n_disks, 3, verbose=False)
    
    # Simuler l'état pour chaque mouvement
    rods = [list(range(n_disks, 0, -1)), [], []]
    
    print(f"État initial: {rods}")
    
    for i, move in enumerate(moves, 1):
        source, dest = map(int, move.split('->'))
        source -= 1  # Convertir en index 0-based
        dest -= 1
        
        disk = rods[source].pop()
        rods[dest].append(disk)
        
        print(f"Mouvement {i:2d}: {move} -> {rods}")
    
    print(f"\n✅ Solution terminée ! Tous les disques sont sur le bâtonnet 3.")


def demo_performance():
    """Démonstration des performances"""
    print_separator("ANALYSE DES PERFORMANCES")
    
    print("⚡ Test de performance pour différentes tailles:")
    print("(Arrêt automatique si le temps dépasse 1 seconde)")
    
    print(f"\n{'Disques':<8} {'Mouvements':<12} {'Temps (s)':<12} {'Croissance':<12}")
    print("-" * 50)
    
    prev_time = 0
    for n in range(1, 20):
        start_time = time.time()
        moves = solve_hanoi(n, 3, verbose=False)
        end_time = time.time()
        
        duration = end_time - start_time
        growth = f"x{duration/prev_time:.1f}" if prev_time > 0 else "-"
        
        print(f"{n:<8} {len(moves):<12} {duration:.6f}    {growth}")
        
        prev_time = duration
        
        # Arrêter si ça prend trop de temps
        if duration > 1.0:
            print(f"\n⏹️  Arrêt du test (temps > 1s pour {n} disques)")
            break
    
    print(f"\n📈 Observation: le temps double approximativement à chaque disque supplémentaire")
    print(f"📈 Ceci confirme la complexité exponentielle O(2^n)")


def demo_edge_cases():
    """Démonstration des cas limites"""
    print_separator("CAS LIMITES ET GESTION D'ERREURS")
    
    print("🧪 Test des cas limites:")
    
    # Cas valides
    print("\n✅ Cas valides:")
    valid_cases = [
        (1, 3, "Cas minimal"),
        (8, 3, "Cas standard"),
        (5, 4, "Avec 4 bâtonnets"),
    ]
    
    for n_disks, n_rods, description in valid_cases:
        moves = solve_hanoi(n_disks, n_rods, verbose=False)
        print(f"   {description}: {n_disks} disques, {n_rods} bâtonnets -> {len(moves)} mouvements")
    
    # Cas d'erreur
    print("\n❌ Cas d'erreur (gestion appropriée):")
    error_cases = [
        ("0,3", "Zéro disque"),
        ("-1,3", "Nombre négatif"),
        ("3,2", "Pas assez de bâtonnets"),
        ("abc,3", "Caractères non numériques"),
        ("3", "Format incorrect"),
    ]
    
    from solve import parse_input
    
    for input_str, description in error_cases:
        try:
            parse_input(input_str)
            print(f"   {description}: ERREUR - devrait échouer!")
        except ValueError as e:
            print(f"   {description}: ✅ Erreur correctement gérée")
        except Exception as e:
            print(f"   {description}: ⚠️  Erreur inattendue: {e}")


def demo_features():
    """Démonstration des fonctionnalités"""
    print_separator("FONCTIONNALITÉS DU PROJET")
    
    features = [
        "🎮 Interface graphique interactive avec tkinter",
        "🖥️  Mode console avec résolution automatique",
        "🔄 Résolution étape par étape",
        "📊 Calcul du nombre minimum de mouvements",
        "🎯 Validation des mouvements en temps réel",
        "🧪 Suite de tests complète (unitaires + intégration)",
        "📚 Documentation détaillée",
        "⚡ Performances optimisées",
        "🛡️  Gestion robuste des erreurs",
        "🎨 Interface utilisateur intuitive",
    ]
    
    print("✨ Fonctionnalités implémentées:")
    for feature in features:
        print(f"   {feature}")
    
    print("\n🚀 Modes d'utilisation:")
    print("   1. Interface graphique: python main.py")
    print("   2. Mode console: python main.py '3,3'")
    print("   3. Mode interactif: python main.py --console")
    print("   4. Aide: python main.py --help")
    
    print("\n📁 Structure du projet:")
    files = [
        ("solve.py", "Algorithme de résolution récursif"),
        ("graphics.py", "Interface graphique avec tkinter"),
        ("main.py", "Point d'entrée principal"),
        ("test_solve.py", "Tests unitaires"),
        ("test_integration.py", "Tests d'intégration"),
        ("demo.py", "Script de démonstration"),
        ("README.md", "Documentation du projet"),
    ]
    
    for filename, description in files:
        print(f"   📄 {filename:<20} - {description}")


def main():
    """Fonction principale de démonstration"""
    print("🎪 DÉMONSTRATION COMPLÈTE - TOUR DE HANOÏ")
    print("Projet développé comme souvenir de voyage au Vietnam")
    
    try:
        demo_algorithm()
        input("\n⏸️  Appuyez sur Entrée pour continuer...")
        
        demo_solution_steps()
        input("\n⏸️  Appuyez sur Entrée pour continuer...")
        
        demo_performance()
        input("\n⏸️  Appuyez sur Entrée pour continuer...")
        
        demo_edge_cases()
        input("\n⏸️  Appuyez sur Entrée pour continuer...")
        
        demo_features()
        
        print_separator("FIN DE LA DÉMONSTRATION")
        print("🎉 Merci d'avoir suivi cette démonstration !")
        print("🚀 Lancez 'python main.py' pour essayer l'interface graphique")
        print("📚 Consultez README.md pour plus d'informations")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Démonstration interrompue par l'utilisateur")
        print("Au revoir ! 👋")


if __name__ == "__main__":
    main()

