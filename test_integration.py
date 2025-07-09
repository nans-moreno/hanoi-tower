#!/usr/bin/env python3
"""
Tests d'intégration pour le projet Tour de Hanoï
Teste l'intégration entre tous les modules
"""

import unittest
import sys
import io
from unittest.mock import patch, MagicMock
import tempfile
import os

# Import des modules du projet
from solve import solve_hanoi, calculate_min_moves, parse_input
import main


class TestIntegration(unittest.TestCase):
    """Tests d'intégration pour l'ensemble du projet"""
    
    def setUp(self):
        """Configuration avant chaque test"""
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
    
    def capture_output(self):
        """Capture la sortie standard"""
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()
        return sys.stdout, sys.stderr
    
    def test_solve_integration(self):
        """Test d'intégration du module solve"""
        # Test avec différentes configurations
        test_cases = [
            (1, 3, 1),
            (2, 3, 3),
            (3, 3, 7),
            (4, 3, 15),
        ]
        
        for n_disks, n_rods, expected_moves in test_cases:
            with self.subTest(n_disks=n_disks, n_rods=n_rods):
                moves = solve_hanoi(n_disks, n_rods, verbose=False)
                self.assertEqual(len(moves), expected_moves)
                
                # Vérifier que tous les mouvements sont valides
                for move in moves:
                    self.assertRegex(move, r'^\d+->\d+$')
                    source, dest = map(int, move.split('->'))
                    self.assertGreaterEqual(source, 1)
                    self.assertLessEqual(source, n_rods)
                    self.assertGreaterEqual(dest, 1)
                    self.assertLessEqual(dest, n_rods)
                    self.assertNotEqual(source, dest)
    
    def test_main_console_mode(self):
        """Test du mode console du script principal"""
        stdout, stderr = self.capture_output()
        
        # Simuler les arguments de ligne de commande
        test_args = ['main.py', '3,3']
        with patch.object(sys, 'argv', test_args):
            main.console_mode('3,3')
        
        output = stdout.getvalue()
        self.assertIn('Résolution de la Tour de Hanoï', output)
        self.assertIn('Nombre de disques: 3', output)
        self.assertIn('Nombre de bâtonnets: 3', output)
        self.assertIn('1->3', output)
        self.assertIn('Solution optimale atteinte', output)
    
    def test_main_help(self):
        """Test de l'affichage de l'aide"""
        stdout, stderr = self.capture_output()
        
        main.show_help()
        
        output = stdout.getvalue()
        self.assertIn('UTILISATION:', output)
        self.assertIn('MODES:', output)
        self.assertIn('OPTIONS:', output)
        self.assertIn('EXEMPLES:', output)
    
    def test_main_version(self):
        """Test de l'affichage de la version"""
        stdout, stderr = self.capture_output()
        
        test_args = ['main.py', '--version']
        with patch.object(sys, 'argv', test_args):
            main.main()
        
        output = stdout.getvalue()
        self.assertIn('Tour de Hanoï v1.0', output)
    
    def test_parse_input_integration(self):
        """Test d'intégration du parsing d'entrée"""
        valid_inputs = [
            ('3,3', (3, 3)),
            ('8,3', (8, 3)),
            ('172,5', (172, 5)),
            (' 4 , 4 ', (4, 4)),
        ]
        
        for input_str, expected in valid_inputs:
            with self.subTest(input_str=input_str):
                result = parse_input(input_str)
                self.assertEqual(result, expected)
    
    def test_error_handling(self):
        """Test de la gestion d'erreurs"""
        # Test avec entrée invalide
        stdout, stderr = self.capture_output()
        
        with self.assertRaises(SystemExit):
            main.console_mode('invalid')
        
        # Test avec nombre de disques invalide
        with self.assertRaises(ValueError):
            parse_input('0,3')
        
        # Test avec nombre de bâtonnets invalide
        with self.assertRaises(ValueError):
            parse_input('3,2')
    
    def test_algorithm_correctness(self):
        """Test de la correction de l'algorithme"""
        # Simuler l'exécution des mouvements pour vérifier la correction
        def simulate_moves(n_disks, moves):
            """Simule l'exécution des mouvements et vérifie la validité"""
            # État initial: tous les disques sur le premier bâtonnet
            rods = [list(range(n_disks, 0, -1)), [], []]
            
            for move in moves:
                source, dest = map(int, move.split('->'))
                source -= 1  # Convertir en index 0-based
                dest -= 1
                
                # Vérifier que le mouvement est valide
                if not rods[source]:
                    return False, f"Tentative de déplacement depuis un bâtonnet vide: {move}"
                
                disk = rods[source][-1]
                if rods[dest] and disk > rods[dest][-1]:
                    return False, f"Tentative de placer un disque plus grand sur un plus petit: {move}"
                
                # Effectuer le mouvement
                rods[dest].append(rods[source].pop())
            
            # Vérifier l'état final
            if len(rods[2]) == n_disks and not rods[0] and not rods[1]:
                return True, "Solution correcte"
            else:
                return False, f"État final incorrect: {rods}"
        
        # Tester pour différents nombres de disques
        for n_disks in range(1, 6):
            with self.subTest(n_disks=n_disks):
                moves = solve_hanoi(n_disks, 3, verbose=False)
                is_valid, message = simulate_moves(n_disks, moves)
                self.assertTrue(is_valid, f"Algorithme incorrect pour {n_disks} disques: {message}")
    
    def test_performance_reasonable(self):
        """Test que les performances sont raisonnables"""
        import time
        
        # Test avec 10 disques (1023 mouvements)
        start_time = time.time()
        moves = solve_hanoi(10, 3, verbose=False)
        end_time = time.time()
        
        # Doit se terminer en moins d'une seconde
        self.assertLess(end_time - start_time, 1.0, "Algorithme trop lent")
        self.assertEqual(len(moves), 1023, "Nombre de mouvements incorrect")


class TestModuleImports(unittest.TestCase):
    """Test que tous les modules peuvent être importés"""
    
    def test_solve_import(self):
        """Test d'importation du module solve"""
        import solve
        self.assertTrue(hasattr(solve, 'solve_hanoi'))
        self.assertTrue(hasattr(solve, 'calculate_min_moves'))
        self.assertTrue(hasattr(solve, 'parse_input'))
    
    def test_graphics_import(self):
        """Test d'importation du module graphics"""
        try:
            import graphics
            self.assertTrue(hasattr(graphics, 'HanoiGame'))
            self.assertTrue(hasattr(graphics, 'main'))
        except ImportError as e:
            self.skipTest(f"Interface graphique non disponible: {e}")
    
    def test_main_import(self):
        """Test d'importation du module main"""
        import main
        self.assertTrue(hasattr(main, 'main'))
        self.assertTrue(hasattr(main, 'console_mode'))
        self.assertTrue(hasattr(main, 'show_help'))


def run_all_tests():
    """Exécute tous les tests et affiche un rapport"""
    print("=" * 60)
    print("TESTS D'INTÉGRATION - TOUR DE HANOÏ")
    print("=" * 60)
    
    # Créer la suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Ajouter tous les tests
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestModuleImports))
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Afficher le résumé
    print("\n" + "=" * 60)
    print("RÉSUMÉ DES TESTS")
    print("=" * 60)
    print(f"Tests exécutés: {result.testsRun}")
    print(f"Échecs: {len(result.failures)}")
    print(f"Erreurs: {len(result.errors)}")
    print(f"Ignorés: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("✅ TOUS LES TESTS SONT PASSÉS !")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        
        if result.failures:
            print("\nÉCHECS:")
            for test, traceback in result.failures:
                print(f"- {test}: {traceback}")
        
        if result.errors:
            print("\nERREURS:")
            for test, traceback in result.errors:
                print(f"- {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

