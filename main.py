#!/usr/bin/env python3
"""
Script principal pour le jeu de la Tour de Hanoï
Point d'entrée de l'application avec choix entre mode console et interface graphique
"""

import sys
import argparse
from typing import Optional

# Import des modules du projet
from solve import solve_hanoi, calculate_min_moves, parse_input
from graphics import main as graphics_main


def print_banner():
    """Affiche la bannière du jeu"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                        TOUR DE HANOÏ                         ║
    ║                                                              ║
    ║  Un jeu de réflexion classique avec résolution automatique  ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def console_mode(input_str: str):
    """
    Mode console pour résoudre la Tour de Hanoï
    
    Args:
        input_str: Chaîne d'entrée au format "n_disks,n_rods"
    """
    try:
        n_disks, n_rods = parse_input(input_str)
        
        print(f"\n🎯 Résolution de la Tour de Hanoï:")
        print(f"   • Nombre de disques: {n_disks}")
        print(f"   • Nombre de bâtonnets: {n_rods}")
        print(f"   • Nombre minimum de mouvements: {calculate_min_moves(n_disks)}")
        print("\n📋 Séquence de mouvements:")
        print("   " + "─" * 40)
        
        moves = solve_hanoi(n_disks, n_rods, verbose=True)
        
        print("   " + "─" * 40)
        print(f"\n✅ Résolution terminée en {len(moves)} mouvements.")
        
        if len(moves) == calculate_min_moves(n_disks):
            print("🏆 Solution optimale atteinte !")
        
    except ValueError as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Interruption par l'utilisateur")
        sys.exit(0)


def interactive_console():
    """Mode console interactif"""
    print_banner()
    print("Mode console interactif")
    print("Tapez 'quit' ou 'exit' pour quitter\n")
    
    while True:
        try:
            user_input = input("Entrez la configuration (format: n_disks,n_rods): ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Au revoir ! 👋")
                break
            
            if not user_input:
                continue
            
            console_mode(user_input)
            print("\n" + "="*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nAu revoir ! 👋")
            break
        except EOFError:
            print("\nAu revoir ! 👋")
            break


def show_help():
    """Affiche l'aide détaillée"""
    help_text = """
UTILISATION:
    python main.py [OPTIONS] [CONFIGURATION]

MODES:
    1. Interface graphique (par défaut):
       python main.py
       python main.py --gui
    
    2. Mode console avec configuration:
       python main.py "3,3"      # 3 disques, 3 bâtonnets
       python main.py "8,3"      # 8 disques, 3 bâtonnets
       python main.py "5,4"      # 5 disques, 4 bâtonnets
    
    3. Mode console interactif:
       python main.py --console

OPTIONS:
    -h, --help      Affiche cette aide
    -g, --gui       Lance l'interface graphique (par défaut)
    -c, --console   Mode console interactif
    -v, --version   Affiche la version

EXEMPLES:
    python main.py                    # Interface graphique
    python main.py "4,3"              # Résout 4 disques en mode console
    python main.py --console          # Mode console interactif
    python main.py --gui              # Force l'interface graphique

FORMAT DE CONFIGURATION:
    "n_disks,n_rods" où:
    - n_disks: nombre de disques (1-20)
    - n_rods: nombre de bâtonnets (3 minimum)

RÈGLES DU JEU:
    1. Un seul disque peut être déplacé à la fois
    2. Seul le disque du dessus peut être pris
    3. Un disque ne peut pas être placé sur un disque plus petit
    4. Objectif: déplacer tous les disques vers le dernier bâtonnet
    """
    print(help_text)


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description="Jeu de la Tour de Hanoï avec interface graphique et résolution automatique",
        add_help=False  # On gère l'aide manuellement
    )
    
    parser.add_argument('config', nargs='?', help='Configuration au format "n_disks,n_rods"')
    parser.add_argument('-h', '--help', action='store_true', help='Affiche l\'aide')
    parser.add_argument('-g', '--gui', action='store_true', help='Lance l\'interface graphique')
    parser.add_argument('-c', '--console', action='store_true', help='Mode console interactif')
    parser.add_argument('-v', '--version', action='store_true', help='Affiche la version')
    
    args = parser.parse_args()
    
    # Gestion des options spéciales
    if args.help:
        show_help()
        return
    
    if args.version:
        print("Tour de Hanoï v1.0")
        print("Développé comme projet éducatif")
        return
    
    # Déterminer le mode d'exécution
    if args.config:
        # Mode console avec configuration directe
        print_banner()
        console_mode(args.config)
    
    elif args.console:
        # Mode console interactif
        interactive_console()
    
    else:
        # Mode interface graphique (par défaut)
        try:
            print_banner()
            print("Lancement de l'interface graphique...")
            print("Fermez la fenêtre pour quitter.\n")
            graphics_main()
        except ImportError as e:
            print(f"❌ Erreur: Impossible de lancer l'interface graphique: {e}")
            print("💡 Suggestion: Utilisez le mode console avec --console")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()

