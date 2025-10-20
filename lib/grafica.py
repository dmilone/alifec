# =====================================================================
# GRAFICA: Sistema de visualización para la Competencia de vida artificial
# Archivo principal con nombres en castellano (Grafica)
# =====================================================================

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from typing import Optional
import time
import os
from datetime import datetime
from .defs import *
from .agar import agar

class Grafica:
    """
    Clase Grafica para visualizar la simulación de vida artificial.
    Usa matplotlib en lugar de OpenGL para compatibilidad con Python.
    """

    def __init__(self, headless=False):
        self.headless = headless
        self.petri = None
        self.fig = None
        self.ax_main = None
        self.ax_data = None
        self.animation = None
        # Estado
        self.t = 0
        self.started = False
        self.cont = True
        self.end_contest = False
        self.contest_completed = False
        self.col1_vivos = 0
        self.col2_vivos = 0
        self.col1_ener = 0.0
        self.col2_ener = 0.0
        self.total_nutrients = 0.0
        self.cyname1 = ""
        self.cyname2 = ""
        self.author1 = ""
        self.author2 = ""
        self.ax_pop = None

    def create_windows(self, petri_instance) -> None:
        self.petri = petri_instance
        if len(self.petri.colonies) >= 1:
            self.cyname1 = self.petri.nombre_colonia(1)
            self.author1 = self.petri.autor_colonia(1)
        if len(self.petri.colonies) >= 2:
            self.cyname2 = self.petri.nombre_colonia(2)
            self.author2 = self.petri.autor_colonia(2)

        if not self.headless:
            self.fig, (self.ax_main, self.ax_data) = plt.subplots(1, 2, figsize=(15, 7))
            self.ax_main.set_title("Competencia de Vida Artificial - Plato de Petri")
            self.ax_main.set_xlim(0, 2 * R)
            self.ax_main.set_ylim(0, 2 * R)
            self.ax_main.set_aspect('equal')
            self.ax_data.set_title("Estadísticas de Colonias")
            self.ax_data.set_xlabel("Tiempo")
            self.ax_data.set_ylabel("Energía / Población")

        if self.headless:
            self.run_headless_simulation()
        else:
            self.animation = animation.FuncAnimation(
                self.fig, self.update_frame, interval=50, blit=False,
                cache_frame_data=False, save_count=100)
            try:
                plt.show()
            except KeyboardInterrupt:
                self.cleanup()
                raise

    def run_headless_simulation(self) -> None:
        print("Ejecutando simulación en modo headless...")
        self.started = True
        max_iterations = 10000
        while not self.end_contest and self.t < max_iterations:
            self.petri.move_colonies()
            self.t += 1
            self.update_statistics()
            if self.t % 100 == 0:
                print(f"  Tiempo: {self.t}, Col1: {self.col1_vivos}, Col2: {self.col2_vivos}")
        if self.end_contest:
            print(f"Simulación completada después de {self.t} pasos de tiempo")
        else:
            print(f"Simulación terminada en max_iterations ({max_iterations}) - Competencia incompleta")

    def cleanup(self):
        if self.animation:
            self.animation.event_source.stop()
        if self.ax_pop is not None:
            self.ax_pop.remove()
            self.ax_pop = None
        if self.fig:
            plt.close(self.fig)

    def update_frame(self, frame) -> None:
        try:
            if not self.started:
                self.started = True
            if self.cont and not self.end_contest:
                self.petri.move_colonies()
                self.t += 1
                self.update_statistics()
                if not self.headless:
                    self.refresh_main()
                    self.refresh_data()
        except Exception as e:
            print(f"Error during frame update: {e}")
            self.end_contest = True

    def update_statistics(self) -> None:
        self.col1_vivos = 0
        self.col2_vivos = 0
        self.col1_ener = 0.0
        self.col2_ener = 0.0
        self.total_nutrients = 0.0
        N = 2 * R
        M = 2 * R
        for i in range(N):
            for j in range(M):
                if agar.ocupacion(i, j) != VACIO:
                    mo_id = agar.ocupacion(i, j)
                    energy = agar.energia(i, j)
                    if mo_id == 1:
                        self.col1_vivos += 1
                        self.col1_ener += energy
                    elif mo_id == 2:
                        self.col2_vivos += 1
                        self.col2_ener += energy
                self.total_nutrients += agar.nutrientes(i, j)
        colonies_alive = 0
        winner = None
        if self.col1_vivos > 0:
            colonies_alive += 1
            winner = self.cyname1
        if self.col2_vivos > 0:
            colonies_alive += 1
            winner = self.cyname2
        if colonies_alive <= 1 and self.t > 10:
            self.end_contest = True
            self.contest_completed = True
            if winner:
                winner_points = self.col1_vivos if winner == self.cyname1 else self.col2_vivos
                print(f"\nSimulación finalizada: {winner} gana con {winner_points} organismos!")
            else:
                print("\nSimulación finalizada: ¡Todos los organismos murieron!")

    def refresh_main(self) -> None:
        if self.headless or not self.ax_main:
            return
        self.ax_main.clear()
        self.ax_main.set_title("Competencia de Vida Artificial - Plato de Petri")
        self.ax_main.set_xlim(0, 2 * R)
        self.ax_main.set_ylim(0, 2 * R)
        self.ax_main.set_aspect('equal')
        N = 2 * R
        M = 2 * R
        R2 = (R + 1) * (R + 1)
        nutrients_grid = np.zeros((N, M))
        microorg_grid = np.zeros((N, M))
        for i in range(N):
            for j in range(M):
                rr = (R - i) * (R - i) + (R - j) * (R - j)
                if rr < R2:
                    nutrients_grid[i, j] = agar.nutrientes(i, j) / MAX_NUTRI
                    microorg_grid[i, j] = agar.ocupacion(i, j)
        self.ax_main.imshow(nutrients_grid, cmap='YlOrBr', alpha=0.6, extent=[0, N, 0, M], origin='lower')
        colony1_x, colony1_y = [], []
        colony2_x, colony2_y = [], []
        for i in range(N):
            for j in range(M):
                mo_id = microorg_grid[i, j]
                if mo_id == 1:
                    colony1_x.append(i)
                    colony1_y.append(j)
                elif mo_id == 2:
                    colony2_x.append(i)
                    colony2_y.append(j)
        if colony1_x:
            self.ax_main.scatter(colony1_x, colony1_y, c='red', s=20, label=f'{self.cyname1} ({self.col1_vivos})')
        if colony2_x:
            self.ax_main.scatter(colony2_x, colony2_y, c='blue', s=20, label=f'{self.cyname2} ({self.col2_vivos})')
        circle = plt.Circle((R, R), R, fill=False, color='black', linewidth=2)
        self.ax_main.add_patch(circle)
        handles, labels = self.ax_main.get_legend_handles_labels()
        if handles:
            self.ax_main.legend(loc='upper right')

    def refresh_data(self) -> None:
        if hasattr(self, 'energy_history'):
            self.energy_history.append((self.col1_ener, self.col2_ener))
            self.pop_history.append((self.col1_vivos, self.col2_vivos))
        else:
            self.energy_history = [(self.col1_ener, self.col2_ener)]
            self.pop_history = [(self.col1_vivos, self.col2_vivos)]
        if self.headless or not self.ax_data:
            return
        self.ax_data.clear()
        if self.ax_pop is not None:
            self.ax_pop.remove()
            self.ax_pop = None
        self.ax_data.set_title("Estadísticas de Colonias")
        self.ax_data.set_xlabel("Tiempo")
        self.ax_data.set_ylabel("Energía", color='black')
        if len(self.energy_history) > 1:
            times = list(range(len(self.energy_history)))
            energies1 = [e[0] for e in self.energy_history]
            energies2 = [e[1] for e in self.energy_history]
            line1 = self.ax_data.plot(times, energies1, 'r-', label=f'{self.cyname1} Energy')
            line2 = self.ax_data.plot(times, energies2, 'b-', label=f'{self.cyname2} Energy')
            self.ax_pop = self.ax_data.twinx()
            self.ax_pop.set_ylabel("Población (Organismos vivos)", color='gray')
            pops1 = [p[0] for p in self.pop_history]
            pops2 = [p[1] for p in self.pop_history]
            line3 = self.ax_pop.plot(times, pops1, 'r--', alpha=0.7, label=f'{self.cyname1} Population')
            line4 = self.ax_pop.plot(times, pops2, 'b--', alpha=0.7, label=f'{self.cyname2} Population')
            lines = line1 + line2 + line3 + line4
            labels = [l.get_label() for l in lines]
            self.ax_data.legend(lines, labels, loc='upper right')
        self.ax_data.grid(True, alpha=0.3)

    def resultado_competencia(self) -> dict:
        winner = None
        winner_points = 0
        if self.col1_vivos > self.col2_vivos:
            winner = self.cyname1
            winner_points = self.col1_vivos
        elif self.col2_vivos > self.col1_vivos:
            winner = self.cyname2
            winner_points = self.col2_vivos
        else:
            winner = "Empate"
            winner_points = 0
        return {
            'vs': f'{self.cyname1} vs {self.cyname2}',
            'winner': winner,
            'points': winner_points,
            'col1_name': self.cyname1,
            'col2_name': self.cyname2,
            'col1_final_pop': self.col1_vivos,
            'col2_final_pop': self.col2_vivos,
            'col1_final_energy': self.col1_ener,
            'col2_final_energy': self.col2_ener,
            'duration': self.t,
            'timestamp': datetime.now().isoformat(),
            'completed': self.contest_completed
        }

    # Aliases en inglés para compatibilidad (se colocan al final de la clase)
    def get_contest_result(self) -> dict:
        return self.resultado_competencia()
