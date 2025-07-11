#!/usr/bin/env python3
"""
Interface graphique finale pour le jeu de la Tour de Hanoï
Corrections finales :
- Solveur BFS pour résolution depuis n'importe quel état
- Affichage du coup recommandé
- Résolution automatique complètement fonctionnelle
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import time
import threading
from typing import List, Optional, Tuple, Dict
from collections import deque
from solve import solve_hanoi, calculate_min_moves


class HanoiGame:
    """Classe principale pour le jeu de la Tour de Hanoï avec interface graphique finale"""
    
    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.title("Tour de Hanoï - Version Finale")
        self.master.geometry("800x600")
        self.master.resizable(True, True)
        
        # Configuration du jeu
        self.n_disks = 3
        self.n_rods = 3
        self.disk_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
        
        # État du jeu
        self.rods = [[], [], []]  # Liste des disques sur chaque bâtonnet
        self.selected_rod = None
        self.move_count = 0
        self.is_solving = False
        self.solution_moves = []
        self.solution_index = 0
        self.initial_state = None  # Pour sauvegarder l'état initial
        
        # Variables d'interface
        self.canvas_width = 700
        self.canvas_height = 400
        self.rod_width = 10
        self.rod_height = 300
        self.disk_height = 20
        self.base_width = 150
        
        self.setup_ui()
        self.reset_game()
        
        # Afficher les coups possibles au démarrage
        self.print_possible_moves()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Frame principal
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration du redimensionnement
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Frame de contrôle
        control_frame = ttk.LabelFrame(main_frame, text="Contrôles", padding="5")
        control_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Configuration du jeu
        config_frame = ttk.Frame(control_frame)
        config_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(config_frame, text="Nombre de disques:").grid(row=0, column=0, padx=(0, 5))
        self.disk_var = tk.StringVar(value=str(self.n_disks))
        disk_spinbox = ttk.Spinbox(config_frame, from_=1, to=8, width=5, textvariable=self.disk_var)
        disk_spinbox.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(config_frame, text="Nouveau jeu", command=self.new_game).grid(row=0, column=2, padx=(0, 10))
        ttk.Button(config_frame, text="Réinitialiser", command=self.reset_game).grid(row=0, column=3, padx=(0, 10))
        
        # Boutons de résolution
        solve_frame = ttk.Frame(control_frame)
        solve_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        ttk.Button(solve_frame, text="Résoudre automatiquement", command=self.solve_auto).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(solve_frame, text="Étape suivante", command=self.next_step).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(solve_frame, text="Arrêter", command=self.stop_solving).grid(row=0, column=2, padx=(0, 10))
        
        # Informations
        info_frame = ttk.Frame(control_frame)
        info_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        self.move_label = ttk.Label(info_frame, text="Mouvements: 0")
        self.move_label.grid(row=0, column=0, padx=(0, 20))
        
        self.min_moves_label = ttk.Label(info_frame, text="Minimum: 7")
        self.min_moves_label.grid(row=0, column=1, padx=(0, 20))
        
        self.status_label = ttk.Label(info_frame, text="Prêt")
        self.status_label.grid(row=0, column=2)
        
        # Canvas pour le jeu
        self.canvas = tk.Canvas(main_frame, width=self.canvas_width, height=self.canvas_height, 
                               bg='white', relief=tk.SUNKEN, borderwidth=2)
        self.canvas.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Événements de la souris
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        
        # Instructions améliorées
        instructions = ttk.Label(main_frame, text="Cliquez sur un bâtonnet pour sélectionner/déplacer un disque. "
                                                 "Les coups possibles et le coup recommandé sont affichés dans le terminal. "
                                                 "Seul le disque du dessus peut être déplacé et ne peut pas être placé sur un disque plus petit.",
                                wraplength=700, justify=tk.CENTER)
        instructions.grid(row=2, column=0, columnspan=2, pady=(10, 0))
    
    def get_current_state(self) -> List[List[int]]:
        """Retourne l'état actuel du jeu"""
        return [rod.copy() for rod in self.rods]
    
    def set_state(self, state: List[List[int]]):
        """Définit l'état du jeu"""
        self.rods = [rod.copy() for rod in state]
    
    def state_to_tuple(self, state: List[List[int]]) -> Tuple:
        """Convertit un état en tuple pour utilisation comme clé de dictionnaire"""
        return tuple(tuple(rod) for rod in state)
    
    def tuple_to_state(self, state_tuple: Tuple) -> List[List[int]]:
        """Convertit un tuple en état"""
        return [list(rod) for rod in state_tuple]
    
    def is_goal_state(self, state: List[List[int]]) -> bool:
        """Vérifie si un état est l'état final (tous les disques sur le dernier bâtonnet)"""
        return len(state[2]) == self.n_disks and len(state[0]) == 0 and len(state[1]) == 0
    
    def get_possible_moves_from_state(self, state: List[List[int]]) -> List[Tuple[int, int]]:
        """Retourne la liste des mouvements possibles depuis un état donné"""
        possible_moves = []
        
        for from_rod in range(self.n_rods):
            if state[from_rod]:  # Si le bâtonnet n'est pas vide
                for to_rod in range(self.n_rods):
                    if from_rod != to_rod:
                        # Vérifier si le mouvement est valide
                        if not state[to_rod] or state[from_rod][-1] < state[to_rod][-1]:
                            possible_moves.append((from_rod + 1, to_rod + 1))  # Convertir en 1-based
        
        return possible_moves
    
    def apply_move_to_state(self, state: List[List[int]], from_rod: int, to_rod: int) -> List[List[int]]:
        """Applique un mouvement à un état et retourne le nouvel état"""
        new_state = [rod.copy() for rod in state]
        if new_state[from_rod]:
            disk = new_state[from_rod].pop()
            new_state[to_rod].append(disk)
        return new_state
    
    def solve_from_current_state_bfs(self) -> List[str]:
        """Utilise BFS pour trouver la solution optimale depuis l'état actuel"""
        current_state = self.get_current_state()
        
        if self.is_goal_state(current_state):
            return []
        
        # BFS pour trouver la solution optimale
        queue = deque([(current_state, [])])
        visited = {self.state_to_tuple(current_state)}
        
        while queue:
            state, moves = queue.popleft()
            
            # Générer tous les mouvements possibles
            possible_moves = self.get_possible_moves_from_state(state)
            
            for from_rod, to_rod in possible_moves:
                # Appliquer le mouvement
                new_state = self.apply_move_to_state(state, from_rod - 1, to_rod - 1)
                new_state_tuple = self.state_to_tuple(new_state)
                
                if new_state_tuple not in visited:
                    visited.add(new_state_tuple)
                    new_moves = moves + [f"{from_rod}->{to_rod}"]
                    
                    # Vérifier si c'est l'état final
                    if self.is_goal_state(new_state):
                        return new_moves
                    
                    queue.append((new_state, new_moves))
        
        # Si aucune solution trouvée (ne devrait pas arriver)
        return []
    
    def get_recommended_move(self) -> Optional[str]:
        """Retourne le coup recommandé (premier coup de la solution optimale)"""
        try:
            if self.is_game_won():
                return None
            
            # Utiliser BFS pour trouver la solution optimale
            optimal_moves = self.solve_from_current_state_bfs()
            
            if optimal_moves:
                return optimal_moves[0]
            else:
                return None
                
        except Exception as e:
            print(f"Erreur lors du calcul du coup recommandé: {e}")
            return None
    
    def get_possible_moves(self) -> List[Tuple[int, int]]:
        """Retourne la liste des mouvements possibles depuis l'état actuel"""
        return self.get_possible_moves_from_state(self.rods)
    
    def print_possible_moves(self):
        """Affiche les coups possibles dans le terminal avec coup recommandé"""
        possible_moves = self.get_possible_moves()
        recommended_move = self.get_recommended_move()
        
        print("\n" + "="*50)
        print("🎯 ÉTAT ACTUEL DU JEU:")
        print(f"   Mouvements effectués: {self.move_count}")
        print(f"   Minimum théorique: {calculate_min_moves(self.n_disks)}")
        
        # Afficher l'état des bâtonnets
        print("\n📊 ÉTAT DES BÂTONNETS:")
        for i, rod in enumerate(self.rods):
            if rod:
                disks_str = " ".join(str(d) for d in reversed(rod))
                print(f"   Bâtonnet {i+1}: [{disks_str}] (dessus: {rod[-1]})")
            else:
                print(f"   Bâtonnet {i+1}: [vide]")
        
        # Afficher le coup recommandé
        if recommended_move:
            from_rod, to_rod = map(int, recommended_move.split('->'))
            from_disk = self.rods[from_rod-1][-1] if self.rods[from_rod-1] else "?"
            print(f"\n⭐ COUP RECOMMANDÉ:")
            print(f"   🎯 {recommended_move} (déplacer disque {from_disk}) ← MEILLEUR CHOIX")
        
        # Afficher les coups possibles
        if possible_moves:
            print(f"\n🎮 TOUS LES COUPS POSSIBLES ({len(possible_moves)}):")
            for i, (from_rod, to_rod) in enumerate(possible_moves, 1):
                from_disk = self.rods[from_rod-1][-1] if self.rods[from_rod-1] else "?"
                move_str = f"{from_rod}->{to_rod}"
                
                # Marquer le coup recommandé
                if recommended_move and move_str == recommended_move:
                    print(f"   {i}. {move_str} (déplacer disque {from_disk}) ⭐ RECOMMANDÉ")
                else:
                    print(f"   {i}. {move_str} (déplacer disque {from_disk})")
        else:
            print("\n❌ AUCUN COUP POSSIBLE")
        
        # Vérifier si le jeu est gagné
        if self.is_game_won():
            print("\n🏆 FÉLICITATIONS ! JEU TERMINÉ !")
            print(f"   Résolu en {self.move_count} mouvements")
            if self.move_count == calculate_min_moves(self.n_disks):
                print("   🌟 SOLUTION OPTIMALE ATTEINTE !")
            else:
                print(f"   💡 Solution optimale: {calculate_min_moves(self.n_disks)} mouvements")
        
        print("="*50)
    
    def new_game(self):
        """Démarre un nouveau jeu avec le nombre de disques spécifié"""
        try:
            new_n_disks = int(self.disk_var.get())
            if new_n_disks < 1 or new_n_disks > 8:
                messagebox.showerror("Erreur", "Le nombre de disques doit être entre 1 et 8")
                return
            
            self.n_disks = new_n_disks
            self.reset_game()
            
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide")
    
    def reset_game(self):
        """Remet le jeu à l'état initial"""
        self.stop_solving()
        
        # Réinitialiser l'état
        self.rods = [[], [], []]
        self.selected_rod = None
        self.move_count = 0
        self.solution_moves = []
        self.solution_index = 0
        
        # Placer tous les disques sur le premier bâtonnet
        for i in range(self.n_disks, 0, -1):
            self.rods[0].append(i)
        
        # Sauvegarder l'état initial
        self.initial_state = self.get_current_state()
        
        # Mettre à jour l'affichage
        self.update_display()
        self.update_info()
        self.print_possible_moves()
    
    def update_display(self):
        """Met à jour l'affichage du canvas"""
        self.canvas.delete("all")
        
        # Calculer les positions des bâtonnets
        rod_spacing = self.canvas_width // 3
        rod_positions = [rod_spacing // 2 + i * rod_spacing for i in range(3)]
        
        # Dessiner la base
        base_y = self.canvas_height - 50
        for x in rod_positions:
            self.canvas.create_rectangle(x - self.base_width//2, base_y, 
                                       x + self.base_width//2, base_y + 20, 
                                       fill='brown', outline='black')
        
        # Dessiner les bâtonnets
        for i, x in enumerate(rod_positions):
            color = 'red' if i == self.selected_rod else 'black'
            self.canvas.create_rectangle(x - self.rod_width//2, base_y - self.rod_height, 
                                       x + self.rod_width//2, base_y, 
                                       fill=color, outline='black')
        
        # Dessiner les disques
        for rod_idx, rod in enumerate(self.rods):
            x = rod_positions[rod_idx]
            for disk_idx, disk_size in enumerate(rod):
                y = base_y - (disk_idx + 1) * self.disk_height
                disk_width = 20 + disk_size * 15
                color = self.disk_colors[(disk_size - 1) % len(self.disk_colors)]
                
                self.canvas.create_rectangle(x - disk_width//2, y - self.disk_height//2,
                                           x + disk_width//2, y + self.disk_height//2,
                                           fill=color, outline='black', width=2)
                
                # Numéro du disque
                self.canvas.create_text(x, y, text=str(disk_size), font=('Arial', 12, 'bold'))
    
    def update_info(self):
        """Met à jour les informations affichées"""
        self.move_label.config(text=f"Mouvements: {self.move_count}")
        self.min_moves_label.config(text=f"Minimum: {calculate_min_moves(self.n_disks)}")
        
        if self.is_solving:
            self.status_label.config(text="Résolution en cours...")
        elif self.is_game_won():
            self.status_label.config(text="Jeu terminé !")
        else:
            self.status_label.config(text="En cours")
    
    def get_rod_from_x(self, x: int) -> Optional[int]:
        """Détermine quel bâtonnet correspond à la position x"""
        rod_spacing = self.canvas_width // 3
        for i in range(3):
            rod_x = rod_spacing // 2 + i * rod_spacing
            if abs(x - rod_x) < rod_spacing // 2:
                return i
        return None
    
    def on_canvas_click(self, event):
        """Gère les clics sur le canvas"""
        if self.is_solving:
            return
        
        rod = self.get_rod_from_x(event.x)
        if rod is None:
            return
        
        if self.selected_rod is None:
            # Sélectionner un bâtonnet
            if self.rods[rod]:  # Seulement si le bâtonnet n'est pas vide
                self.selected_rod = rod
                self.update_display()
        else:
            # Déplacer vers le bâtonnet sélectionné
            if rod == self.selected_rod:
                # Désélectionner
                self.selected_rod = None
                self.update_display()
            else:
                # Tenter le mouvement
                if self.move_disk(self.selected_rod, rod):
                    self.move_count += 1
                    self.selected_rod = None
                    self.update_display()
                    self.update_info()
                    
                    # Afficher les nouveaux coups possibles
                    self.print_possible_moves()
                    
                    # Vérifier si le jeu est gagné
                    if self.is_game_won():
                        messagebox.showinfo("Félicitations !", 
                                          f"Vous avez résolu le puzzle en {self.move_count} mouvements !\n"
                                          f"Minimum théorique: {calculate_min_moves(self.n_disks)}")
                else:
                    messagebox.showwarning("Mouvement invalide", 
                                         "Ce mouvement n'est pas autorisé selon les règles du jeu.")
    
    def on_mouse_move(self, event):
        """Gère le mouvement de la souris pour le survol"""
        rod = self.get_rod_from_x(event.x)
        if rod is not None:
            self.canvas.config(cursor="hand2")
        else:
            self.canvas.config(cursor="")
    
    def can_move(self, from_rod: int, to_rod: int) -> bool:
        """Vérifie si un mouvement est valide"""
        if not self.rods[from_rod]:
            return False
        
        if not self.rods[to_rod]:
            return True
        
        return self.rods[from_rod][-1] < self.rods[to_rod][-1]
    
    def move_disk(self, from_rod: int, to_rod: int):
        """Déplace un disque d'un bâtonnet à un autre"""
        if self.can_move(from_rod, to_rod):
            disk = self.rods[from_rod].pop()
            self.rods[to_rod].append(disk)
            return True
        return False
    
    def is_game_won(self) -> bool:
        """Vérifie si le jeu est gagné"""
        return len(self.rods[2]) == self.n_disks
    
    def solve_auto(self):
        """Lance la résolution automatique depuis l'état actuel"""
        if self.is_solving:
            return
        
        if self.is_game_won():
            messagebox.showinfo("Jeu terminé", "Le jeu est déjà résolu !")
            return
        
        print("\n🤖 RÉSOLUTION AUTOMATIQUE DEPUIS L'ÉTAT ACTUEL")
        print("="*50)
        
        # Utiliser le solveur BFS pour calculer la solution optimale
        try:
            self.solution_moves = self.solve_from_current_state_bfs()
            self.solution_index = 0
            
            if self.solution_moves:
                print(f"🎯 Solution optimale calculée: {len(self.solution_moves)} mouvements")
                print(f"📋 Séquence: {' → '.join(self.solution_moves)}")
                
                self.is_solving = True
                
                # Démarrer la résolution automatique dans un thread séparé
                threading.Thread(target=self.auto_solve_thread, daemon=True).start()
            else:
                print("❌ Aucune solution trouvée (erreur)")
                
        except Exception as e:
            print(f"❌ Erreur lors du calcul de la solution: {e}")
            messagebox.showerror("Erreur", f"Impossible de calculer la solution: {e}")
    
    def auto_solve_thread(self):
        """Thread pour la résolution automatique"""
        while self.is_solving and self.solution_index < len(self.solution_moves):
            if not self.is_solving:
                break
            
            # Exécuter le mouvement suivant
            self.master.after(0, self.execute_next_move)
            time.sleep(1)  # Pause d'une seconde entre les mouvements
        
        if self.is_solving:
            self.master.after(0, self.stop_solving)
    
    def execute_next_move(self):
        """Exécute le mouvement suivant de la solution"""
        if self.solution_index < len(self.solution_moves):
            move = self.solution_moves[self.solution_index]
            from_rod, to_rod = map(int, move.split('->'))
            from_rod -= 1  # Convertir en index 0-based
            to_rod -= 1
            
            print(f"🤖 Mouvement automatique: {move}")
            
            if self.move_disk(from_rod, to_rod):
                self.move_count += 1
                self.solution_index += 1
                self.update_display()
                self.update_info()
                self.print_possible_moves()
    
    def next_step(self):
        """Exécute la prochaine étape de la solution"""
        if not self.solution_moves:
            # Calculer la solution depuis l'état actuel avec BFS
            try:
                self.solution_moves = self.solve_from_current_state_bfs()
                self.solution_index = 0
                
                if self.solution_moves:
                    print(f"💡 Solution calculée: {len(self.solution_moves)} mouvements restants")
                else:
                    print("❌ Aucune solution trouvée")
                    return
                    
            except Exception as e:
                print(f"❌ Erreur lors du calcul: {e}")
                return
        
        if self.solution_index < len(self.solution_moves):
            move = self.solution_moves[self.solution_index]
            print(f"👆 Étape suivante suggérée: {move}")
            self.execute_next_move()
        else:
            messagebox.showinfo("Solution terminée", "Toutes les étapes ont été exécutées !")
    
    def stop_solving(self):
        """Arrête la résolution automatique"""
        self.is_solving = False
        self.update_info()
        print("\n⏹️  Résolution automatique arrêtée")


def main():
    """Fonction principale pour lancer l'interface graphique finale"""
    print("🎮 TOUR DE HANOÏ - VERSION FINALE")
    print("="*50)
    print("✨ Fonctionnalités finales:")
    print("   • Affichage des coups possibles dans le terminal")
    print("   • Coup recommandé avec solveur BFS optimal")
    print("   • Résolution automatique 100% fonctionnelle")
    print("   • Informations détaillées sur l'état du jeu")
    print("="*50)
    
    root = tk.Tk()
    game = HanoiGame(root)
    
    # Centrer la fenêtre
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()

