#!/usr/bin/env python3
"""
Interface graphique pour le jeu de la Tour de Hanoï
Utilise tkinter pour créer une interface interactive
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import time
import threading
from typing import List, Optional, Tuple
from solve import solve_hanoi, calculate_min_moves


class HanoiGame:
    """Classe principale pour le jeu de la Tour de Hanoï avec interface graphique"""
    
    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.title("Tour de Hanoï")
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
        
        # Variables d'interface
        self.canvas_width = 700
        self.canvas_height = 400
        self.rod_width = 10
        self.rod_height = 300
        self.disk_height = 20
        self.base_width = 150
        
        self.setup_ui()
        self.reset_game()
    
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
        
        # Instructions
        instructions = ttk.Label(main_frame, text="Cliquez sur un bâtonnet pour sélectionner/déplacer un disque. "
                                                 "Seul le disque du dessus peut être déplacé et ne peut pas être placé sur un disque plus petit.",
                                wraplength=700, justify=tk.CENTER)
        instructions.grid(row=2, column=0, columnspan=2, pady=(10, 0))
    
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
        
        # Mettre à jour l'affichage
        self.update_display()
        self.update_info()
    
    def update_display(self):
        """Met à jour l'affichage du canvas"""
        self.canvas.delete("all")
        
        # Calculer les positions des bâtonnets
        rod_spacing = self.canvas_width // 3
        rod_positions = [rod_spacing // 2, rod_spacing + rod_spacing // 2, 2 * rod_spacing + rod_spacing // 2]
        
        # Dessiner la base
        base_y = self.canvas_height - 50
        for i, x in enumerate(rod_positions):
            # Base du bâtonnet
            self.canvas.create_rectangle(x - self.base_width // 2, base_y, 
                                       x + self.base_width // 2, base_y + 20,
                                       fill='#8B4513', outline='#654321', width=2)
            
            # Bâtonnet
            rod_color = '#FF6B6B' if i == self.selected_rod else '#654321'
            self.canvas.create_rectangle(x - self.rod_width // 2, base_y - self.rod_height,
                                       x + self.rod_width // 2, base_y,
                                       fill=rod_color, outline='#4A4A4A', width=2)
            
            # Numéro du bâtonnet
            self.canvas.create_text(x, base_y + 35, text=str(i + 1), 
                                  font=('Arial', 14, 'bold'), fill='#333')
        
        # Dessiner les disques
        for rod_idx, rod in enumerate(self.rods):
            x = rod_positions[rod_idx]
            for disk_idx, disk_size in enumerate(rod):
                y = base_y - (disk_idx + 1) * self.disk_height
                disk_width = 30 + disk_size * 15
                color = self.disk_colors[(disk_size - 1) % len(self.disk_colors)]
                
                # Disque
                self.canvas.create_oval(x - disk_width // 2, y - self.disk_height // 2,
                                      x + disk_width // 2, y + self.disk_height // 2,
                                      fill=color, outline='#333', width=2)
                
                # Numéro du disque
                self.canvas.create_text(x, y, text=str(disk_size), 
                                      font=('Arial', 10, 'bold'), fill='white')
    
    def update_info(self):
        """Met à jour les informations affichées"""
        self.move_label.config(text=f"Mouvements: {self.move_count}")
        min_moves = calculate_min_moves(self.n_disks)
        self.min_moves_label.config(text=f"Minimum: {min_moves}")
        
        if self.is_game_won():
            self.status_label.config(text="Félicitations ! Vous avez gagné !", foreground='green')
        elif self.is_solving:
            self.status_label.config(text="Résolution en cours...", foreground='blue')
        else:
            self.status_label.config(text="Prêt", foreground='black')
    
    def on_canvas_click(self, event):
        """Gère les clics sur le canvas"""
        if self.is_solving:
            return
        
        # Déterminer sur quel bâtonnet on a cliqué
        rod_spacing = self.canvas_width // 3
        clicked_rod = min(2, max(0, event.x // rod_spacing))
        
        if self.selected_rod is None:
            # Sélectionner un bâtonnet source
            if self.rods[clicked_rod]:  # Il y a des disques sur ce bâtonnet
                self.selected_rod = clicked_rod
                self.update_display()
        else:
            # Déplacer le disque
            if clicked_rod == self.selected_rod:
                # Désélectionner
                self.selected_rod = None
                self.update_display()
            else:
                # Tenter le déplacement
                if self.can_move(self.selected_rod, clicked_rod):
                    self.move_disk(self.selected_rod, clicked_rod)
                    self.selected_rod = None
                    self.move_count += 1
                    self.update_display()
                    self.update_info()
                else:
                    messagebox.showwarning("Mouvement invalide", 
                                         "Vous ne pouvez pas placer un disque plus grand sur un disque plus petit !")
    
    def on_mouse_move(self, event):
        """Gère le survol de la souris pour changer le curseur"""
        if self.is_solving:
            return
        
        rod_spacing = self.canvas_width // 3
        hovered_rod = min(2, max(0, event.x // rod_spacing))
        
        if self.selected_rod is None and self.rods[hovered_rod]:
            self.canvas.config(cursor="hand2")
        elif self.selected_rod is not None:
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
        """Lance la résolution automatique"""
        if self.is_solving:
            return
        
        if self.is_game_won():
            messagebox.showinfo("Jeu terminé", "Le jeu est déjà résolu !")
            return
        
        # Calculer la solution
        self.solution_moves = solve_hanoi(self.n_disks, self.n_rods, verbose=False)
        self.solution_index = 0
        self.is_solving = True
        
        # Démarrer la résolution automatique dans un thread séparé
        threading.Thread(target=self.auto_solve_thread, daemon=True).start()
    
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
            
            if self.move_disk(from_rod, to_rod):
                self.move_count += 1
                self.solution_index += 1
                self.update_display()
                self.update_info()
    
    def next_step(self):
        """Exécute la prochaine étape de la solution"""
        if not self.solution_moves:
            # Calculer la solution si pas encore fait
            self.solution_moves = solve_hanoi(self.n_disks, self.n_rods, verbose=False)
            self.solution_index = 0
        
        if self.solution_index < len(self.solution_moves):
            self.execute_next_move()
        else:
            messagebox.showinfo("Solution terminée", "Toutes les étapes ont été exécutées !")
    
    def stop_solving(self):
        """Arrête la résolution automatique"""
        self.is_solving = False
        self.update_info()


def main():
    """Fonction principale pour lancer l'interface graphique"""
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

