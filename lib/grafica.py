# =====================================================================
# GRAFICA: Sistema de visualización para la Competencia de vida artificial
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

class Graficadora:
    """
    Clase Graficador para visualizar la simulación de vida artificial.
    """

    def __init__(self, headless=False):
        self.sin_graficos = headless
        self.petri = None
        self.figura = None
        self.eje_principal = None
        self.eje_datos = None
        self.animacion = None
        # Estado
        self.t = 0
        self.iniciado = False
        self.continuar = True
        self.fin_competencia = False
        self.competencia_completada = False
        self.col1_vivos = 0
        self.col2_vivos = 0
        self.col1_energia = 0.0
        self.col2_energia = 0.0
        self.total_nutrientes = 0.0
        self.nombre_col1 = ""
        self.nombre_col2 = ""
        self.autor_col1 = ""
        self.autor_col2 = ""
        self.eje_poblacion = None

    def crear_ventanas(self, petri_instance) -> None:
        self.petri = petri_instance
        # Usar API en castellano: `colonias`, `nombre_colonia`, `autor_colonia`
        if len(self.petri.colonias) >= 1:
            self.nombre_col1 = self.petri.nombre_colonia(1)
            self.autor_col1 = self.petri.autor_colonia(1)
        if len(self.petri.colonias) >= 2:
            self.nombre_col2 = self.petri.nombre_colonia(2)
            self.autor_col2 = self.petri.autor_colonia(2)

        if not self.sin_graficos:
            self.figura, (self.eje_principal, self.eje_datos) = plt.subplots(1, 2, figsize=(15, 7))
            self.eje_principal.set_title("Competencia de Vida Artificial - Plato de Petri")
            self.eje_principal.set_xlim(0, 2 * R)
            self.eje_principal.set_ylim(0, 2 * R)
            self.eje_principal.set_aspect('equal')
            self.eje_datos.set_title("Estadísticas de Colonias")
            self.eje_datos.set_xlabel("Tiempo")
            self.eje_datos.set_ylabel("Energía / Población")

        if self.sin_graficos:
            self.ejecutar_headless()
        else:
            self.animacion = animation.FuncAnimation(
                self.figura, self.actualizar_frame, interval=50, blit=False,
                cache_frame_data=False, save_count=100)
            try:
                plt.show()
            except KeyboardInterrupt:
                self.limpiar()
                raise

    def ejecutar_headless(self) -> None:
        print("Ejecutando simulación en modo headless...")
        self.iniciado = True
        max_iteraciones = 10000
        while not self.fin_competencia and self.t < max_iteraciones:
            # Usar la versión en castellano
            self.petri.mover_colonias()
            self.t += 1
            self.actualizar_estadisticas()
            if self.t % 100 == 0:
                print(f"  Tiempo: {self.t}, Col1: {self.col1_vivos}, Col2: {self.col2_vivos}")
        if self.fin_competencia:
            print(f"Simulación completada después de {self.t} pasos de tiempo")
        else:
            print(f"Simulación terminada en max_iteraciones ({max_iteraciones}) - Competencia incompleta")

    def limpiar(self):
        if self.animacion:
            self.animacion.event_source.stop()
        if self.eje_poblacion is not None:
            self.eje_poblacion.remove()
            self.eje_poblacion = None
        if self.figura:
            plt.close(self.figura)

    def actualizar_frame(self, frame) -> None:
        try:
            if not self.iniciado:
                self.iniciado = True
            if self.continuar and not self.fin_competencia:
                self.petri.mover_colonias()
                self.t += 1
                self.actualizar_estadisticas()
                if not self.sin_graficos:
                    self.refrescar_principal()
                    self.refrescar_datos()
        except Exception as e:
            print(f"Error durante actualización de frame: {e}")
            self.fin_competencia = True

    def actualizar_estadisticas(self) -> None:
        self.col1_vivos = 0
        self.col2_vivos = 0
        self.col1_energia = 0.0
        self.col2_energia = 0.0
        self.total_nutrientes = 0.0
        N = 2 * R
        M = 2 * R
        for i in range(N):
            for j in range(M):
                if agar.ocupacion(i, j) != VACIO:
                    mo_id = agar.ocupacion(i, j)
                    energia = agar.energia(i, j)
                    if mo_id == 1:
                        self.col1_vivos += 1
                        self.col1_energia += energia
                    elif mo_id == 2:
                        self.col2_vivos += 1
                        self.col2_energia += energia
                self.total_nutrientes += agar.nutrientes(i, j)
        colonias_vivas = 0
        ganador = None
        if self.col1_vivos > 0:
            colonias_vivas += 1
            ganador = self.nombre_col1
        if self.col2_vivos > 0:
            colonias_vivas += 1
            ganador = self.nombre_col2
        if colonias_vivas <= 1 and self.t > 10:
            self.fin_competencia = True
            self.competencia_completada = True
            if ganador:
                puntos_ganador = self.col1_vivos if ganador == self.nombre_col1 else self.col2_vivos
                print(f"\nSimulación finalizada: {ganador} gana con {puntos_ganador} organismos!")
            else:
                print("\nSimulación finalizada: ¡Todos los organismos murieron!")

    def refrescar_principal(self) -> None:
        if self.sin_graficos or not self.eje_principal:
            return
        self.eje_principal.clear()
        self.eje_principal.set_title("Competencia de Vida Artificial - Plato de Petri")
        self.eje_principal.set_xlim(0, 2 * R)
        self.eje_principal.set_ylim(0, 2 * R)
        self.eje_principal.set_aspect('equal')
        N = 2 * R
        M = 2 * R
        R2 = (R + 1) * (R + 1)
        nutrientes = np.zeros((N, M))
        rejilla_mo = np.zeros((N, M))
        for i in range(N):
            for j in range(M):
                rr = (R - i) * (R - i) + (R - j) * (R - j)
                if rr < R2:
                    nutrientes[i, j] = agar.nutrientes(i, j) / MAX_NUTRI
                    rejilla_mo[i, j] = agar.ocupacion(i, j)
        self.eje_principal.imshow(nutrientes, cmap='YlOrBr', alpha=0.6, extent=[0, N, 0, M], origin='lower')
        col1_x, col1_y = [], []
        col2_x, col2_y = [], []
        for i in range(N):
            for j in range(M):
                mo_id = rejilla_mo[i, j]
                if mo_id == 1:
                    col1_x.append(i)
                    col1_y.append(j)
                elif mo_id == 2:
                    col2_x.append(i)
                    col2_y.append(j)
        if col1_x:
            self.eje_principal.scatter(col1_x, col1_y, c='red', s=20, label=f'{self.nombre_col1} ({self.col1_vivos})')
        if col2_x:
            self.eje_principal.scatter(col2_x, col2_y, c='blue', s=20, label=f'{self.nombre_col2} ({self.col2_vivos})')
        circulo = plt.Circle((R, R), R, fill=False, color='black', linewidth=2)
        self.eje_principal.add_patch(circulo)
        handles, labels = self.eje_principal.get_legend_handles_labels()
        if handles:
            self.eje_principal.legend(loc='upper right')

    def refrescar_datos(self) -> None:
        if hasattr(self, 'hist_energia'):
            self.hist_energia.append((self.col1_energia, self.col2_energia))
            self.hist_poblacion.append((self.col1_vivos, self.col2_vivos))
        else:
            self.hist_energia = [(self.col1_energia, self.col2_energia)]
            self.hist_poblacion = [(self.col1_vivos, self.col2_vivos)]
        if self.sin_graficos or not self.eje_datos:
            return
        self.eje_datos.clear()
        if self.eje_poblacion is not None:
            self.eje_poblacion.remove()
            self.eje_poblacion = None
        self.eje_datos.set_title("Estadísticas de Colonias")
        self.eje_datos.set_xlabel("Tiempo")
        self.eje_datos.set_ylabel("Energía", color='black')
        if len(self.hist_energia) > 1:
            tiempos = list(range(len(self.hist_energia)))
            ener1 = [e[0] for e in self.hist_energia]
            ener2 = [e[1] for e in self.hist_energia]
            linea1 = self.eje_datos.plot(tiempos, ener1, 'r-', label=f'{self.nombre_col1} Energía')
            linea2 = self.eje_datos.plot(tiempos, ener2, 'b-', label=f'{self.nombre_col2} Energía')
            self.eje_poblacion = self.eje_datos.twinx()
            self.eje_poblacion.set_ylabel("Población (Organismos vivos)", color='gray')
            pop1 = [p[0] for p in self.hist_poblacion]
            pop2 = [p[1] for p in self.hist_poblacion]
            linea3 = self.eje_poblacion.plot(tiempos, pop1, 'r--', alpha=0.7, label=f'{self.nombre_col1} Población')
            linea4 = self.eje_poblacion.plot(tiempos, pop2, 'b--', alpha=0.7, label=f'{self.nombre_col2} Población')
            lineas = linea1 + linea2 + linea3 + linea4
            etiquetas = [l.get_label() for l in lineas]
            self.eje_datos.legend(lineas, etiquetas, loc='upper right')
        self.eje_datos.grid(True, alpha=0.3)

    def resultado_competencia(self) -> dict:
        ganador = None
        puntos_ganador = 0
        if self.col1_vivos > self.col2_vivos:
            ganador = self.nombre_col1
            puntos_ganador = self.col1_vivos
        elif self.col2_vivos > self.col1_vivos:
            ganador = self.nombre_col2
            puntos_ganador = self.col2_vivos
        else:
            ganador = "Empate"
            puntos_ganador = 0
        # Devolver resultados con claves en castellano. Los consumidores pueden
        # traducir a los nombres esperados por el sistema de ranking si es necesario.
        return {
            'enfrentamiento': f'{self.nombre_col1} vs {self.nombre_col2}',
            'ganador': ganador,
            'puntos': puntos_ganador,
            'col1_nombre': self.nombre_col1,
            'col2_nombre': self.nombre_col2,
            'col1_poblacion_final': self.col1_vivos,
            'col2_poblacion_final': self.col2_vivos,
            'col1_energia_final': self.col1_energia,
            'col2_energia_final': self.col2_energia,
            'duracion': self.t,
            'timestamp': datetime.now().isoformat(),
            'completada': self.competencia_completada
        }

