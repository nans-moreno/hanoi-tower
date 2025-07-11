#!/usr/bin/env python3
"""
Démonstration de la récursivité dans l'algorithme de la Tour de Hanoï
Ce script montre clairement comment la récursivité est utilisée
"""

def hanoi_recursive_demo(n: int, source: int, destination: int, auxiliary: int, level: int = 0):
    """
    Version démonstrative de l'algorithme récursif avec affichage des niveaux
    
    Args:
        n: Nombre de disques à déplacer
        source: Bâtonnet source
        destination: Bâtonnet destination  
        auxiliary: Bâtonnet auxiliaire
        level: Niveau de récursion (pour l'indentation)
    """
    indent = "  " * level
    print(f"{indent}📞 APPEL RÉCURSIF: hanoi({n} disques, {source}->{destination}, aux={auxiliary})")
    
    # CAS DE BASE (condition d'arrêt de la récursivité)
    if n == 1:
        print(f"{indent}✅ CAS DE BASE: Déplacer 1 disque {source}->{destination}")
        return
    
    # DÉCOMPOSITION RÉCURSIVE
    print(f"{indent}🔄 DÉCOMPOSITION en 3 étapes:")
    print(f"{indent}   1️⃣ Déplacer {n-1} disques de {source} vers {auxiliary}")
    print(f"{indent}   2️⃣ Déplacer le gros disque de {source} vers {destination}")
    print(f"{indent}   3️⃣ Déplacer {n-1} disques de {auxiliary} vers {destination}")
    print()
    
    # ÉTAPE 1: Récursion pour déplacer n-1 disques vers auxiliaire
    print(f"{indent}🚀 ÉTAPE 1:")
    hanoi_recursive_demo(n-1, source, auxiliary, destination, level + 1)
    
    # ÉTAPE 2: Déplacer le disque le plus grand
    print(f"{indent}🚀 ÉTAPE 2:")
    print(f"{indent}  ✅ Déplacer le gros disque: {source}->{destination}")
    
    # ÉTAPE 3: Récursion pour déplacer n-1 disques vers destination
    print(f"{indent}🚀 ÉTAPE 3:")
    hanoi_recursive_demo(n-1, auxiliary, destination, source, level + 1)
    
    print(f"{indent}✅ TERMINÉ: hanoi({n} disques, {source}->{destination})")
    if level > 0:
        print()


def demo_principe_recursivite():
    """Démontre le principe de récursivité"""
    print("=" * 80)
    print("🎯 DÉMONSTRATION DE LA RÉCURSIVITÉ - TOUR DE HANOÏ")
    print("=" * 80)
    print()
    
    print("📚 PRINCIPE DE LA RÉCURSIVITÉ:")
    print("   • Une fonction qui s'appelle elle-même")
    print("   • Avec un CAS DE BASE pour arrêter les appels")
    print("   • Décompose un problème complexe en sous-problèmes plus simples")
    print()
    
    print("🏗️ STRUCTURE DE L'ALGORITHME RÉCURSIF:")
    print("   1. CAS DE BASE: Si n=1, déplacer directement le disque")
    print("   2. CAS RÉCURSIF: Si n>1, décomposer en 3 étapes:")
    print("      a) Déplacer n-1 disques vers bâtonnet auxiliaire (RÉCURSION)")
    print("      b) Déplacer le gros disque vers destination")
    print("      c) Déplacer n-1 disques vers destination finale (RÉCURSION)")
    print()
    
    print("🔢 EXEMPLE AVEC 3 DISQUES:")
    print("=" * 50)
    hanoi_recursive_demo(3, 1, 3, 2)
    
    print("\n" + "=" * 80)
    print("✅ CONCLUSION:")
    print("   • L'algorithme utilise la RÉCURSIVITÉ PURE")
    print("   • Chaque appel se décompose en sous-problèmes plus petits")
    print("   • La récursion s'arrête quand n=1 (cas de base)")
    print("   • Solution optimale garantie: 2^n - 1 mouvements")
    print("=" * 80)


if __name__ == "__main__":
    demo_principe_recursivite()

