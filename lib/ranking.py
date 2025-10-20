# =====================================================================
# RANKING: Sistema de ranking para la Competencia de vida artificial
# Procesa resultados de la Competencia y genera rankings
# =====================================================================

import os
import glob
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

class RankingSystem:
    """
    Sistema de ranking para procesar resultados de la Competencia y generar rankings.
    Procesa archivos YAML con marcas temporales y calcula las posiciones.
    """
    
    def __init__(self, results_dir: str = "results"):
        """
        Inicializar el sistema de ranking

        Args:
            results_dir: Directorio que contiene los archivos de resultados de la Competencia
        """
        self.results_dir = results_dir
        self.contests = []
        self.rankings = defaultdict(int)
        
    def load_contest_files(self, date_pattern: str = "*") -> int:
        """
        Cargar archivos de Competencia que coincidan con un patrón de fecha

        Args:
            date_pattern: Patrón de fecha para coincidencia de archivos (ej.: "241005" para una fecha, "*" para todo)

        Returns:
            Número de archivos de Competencia cargados
        """
        self.contests = []
        
        # Find all matching contest files
        pattern = os.path.join(self.results_dir, f"contests_{date_pattern}.yml")
        contest_files = glob.glob(pattern)
        
        for filepath in sorted(contest_files):
            try:
                self._parse_contest_file(filepath)
            except Exception as e:
                print(f"Error cargando {filepath}: {e}")
                
        return len(contest_files)
    
    def _parse_contest_file(self, filepath: str) -> None:
        """
        Analizar un archivo de Competencia y extraer resultados

        Args:
            filepath: Ruta al archivo YAML de la Competencia
        """
        try:
            with open(filepath, 'r') as f:
                content = f.read().strip()
                
            if not content:
                return
                
            # Split by document separators (---)
            documents = content.split('---')
            
            for doc in documents:
                doc = doc.strip()
                if not doc:
                    continue
                    
                # Parse YAML-like content manually (avoid dependency)
                contest = {}
                lines = doc.split('\n')
                
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                        
                    if line.startswith('- vs:'):
                        # New contest entry
                        contest = {}
                        value = line.replace('- vs:', '').strip().strip('"')
                        contest['vs'] = value
                    elif ':' in line and not line.startswith('-'):
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip().strip('"')
                        
                        # Convert numeric values
                        if key in ['points', 'col1_final_pop', 'col2_final_pop', 'duration']:
                            try:
                                contest[key] = int(value)
                            except ValueError:
                                contest[key] = 0
                        elif key in ['col1_final_energy', 'col2_final_energy']:
                            try:
                                contest[key] = float(value)
                            except ValueError:
                                contest[key] = 0.0
                        else:
                            contest[key] = value
                
                if contest and 'winner' in contest:
                    contest['file'] = os.path.basename(filepath)
                    self.contests.append(contest)
                    
        except Exception as e:
            print(f"Error analizando {filepath}: {e}")
    
    def calculate_rankings(self) -> Dict[str, Dict]:
        """
        Calcular rankings basados en las Competencias cargadas

        Returns:
            Diccionario con rankings y estadísticas por colonia
        """
        self.rankings = defaultdict(lambda: {
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'total_points': 0,
            'contests': 0,
            'avg_points': 0.0,
            'win_rate': 0.0
        })
        
        for contest in self.contests:
            col1 = contest.get('col1_name', 'Unknown1')
            col2 = contest.get('col2_name', 'Unknown2')
            winner = contest.get('winner', 'Draw')
            points = contest.get('points', 0)
            
            # Update contest counts
            self.rankings[col1]['contests'] += 1
            self.rankings[col2]['contests'] += 1
            
            # Update win/loss/draw counts
            if winner == col1:
                self.rankings[col1]['wins'] += 1
                self.rankings[col1]['total_points'] += points
                self.rankings[col2]['losses'] += 1
            elif winner == col2:
                self.rankings[col2]['wins'] += 1
                self.rankings[col2]['total_points'] += points
                self.rankings[col1]['losses'] += 1
            else:
                # Draw or no winner
                self.rankings[col1]['draws'] += 1
                self.rankings[col2]['draws'] += 1
        
        # Calculate averages and win rates
        for colony, stats in self.rankings.items():
            if stats['contests'] > 0:
                stats['avg_points'] = stats['total_points'] / stats['contests']
                stats['win_rate'] = (stats['wins'] / stats['contests']) * 100
        
        return dict(self.rankings)
    
    def generate_ranking_report(self, top_n: int = 10) -> str:
        """
        Generar un informe de ranking formateado

        Args:
            top_n: Número de colonias principales a incluir

        Returns:
            Cadena con el informe de ranking formateado
        """
        rankings = self.calculate_rankings()
        
        if not rankings:
            return "No hay datos de Competencias disponibles para generar ranking."
        
        # Sort by win rate, then by total points
        sorted_colonies = sorted(
            rankings.items(),
            key=lambda x: (x[1]['win_rate'], x[1]['total_points']),
            reverse=True
        )
        
        report = []
        report.append("=" * 80)
        report.append("COMPETENCIA DE VIDA ARTIFICIAL - INFORME DE RANKING")
        report.append("=" * 80)
        report.append(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total de Competencias analizadas: {len(self.contests)}")
        report.append(f"Total de colonias: {len(rankings)}")
        report.append("-" * 80)
        
        # Header
        report.append(f"{'Rank':<4} {'Colony':<20} {'W-L-D':<8} {'Win%':<6} {'Avg Pts':<8} {'Total Pts':<10}")
        report.append("-" * 80)
        
        # Rankings
        for i, (colony, stats) in enumerate(sorted_colonies[:top_n], 1):
            wld = f"{stats['wins']}-{stats['losses']}-{stats['draws']}"
            report.append(
                f"{i:<4} {colony:<20} {wld:<8} {stats['win_rate']:5.1f}% "
                f"{stats['avg_points']:7.1f} {stats['total_points']:>9}"
            )
        
        if len(sorted_colonies) > top_n:
            report.append(f"... and {len(sorted_colonies) - top_n} more colonies")
        
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def get_colony_stats(self, colony_name: str) -> Optional[Dict]:
        """
        Get detailed statistics for a specific colony
        
        Args:
            colony_name: Name of the colony
            
        Returns:
            Dictionary with colony statistics or None if not found
        """
        rankings = self.calculate_rankings()
        return rankings.get(colony_name)
    
    def get_recent_contests(self, limit: int = 10) -> List[Dict]:
        """
        Get most recent contests
        
        Args:
            limit: Maximum number of contests to return
            
        Returns:
            List of recent contest dictionaries
        """
        # Sort by timestamp if available, otherwise by order in file
        sorted_contests = sorted(
            self.contests,
            key=lambda x: x.get('timestamp', ''),
            reverse=True
        )
        
        return sorted_contests[:limit]
    
    def save_ranking_report(self, filepath: str, top_n: int = 20) -> None:
        """
        Save ranking report to file
        
        Args:
            filepath: Output file path
            top_n: Number of top colonies to include
        """
        try:
            report = self.generate_ranking_report(top_n)
            with open(filepath, 'w') as f:
                f.write(report)
            print(f"Ranking report saved to: {filepath}")
        except Exception as e:
            print(f"Error saving ranking report: {e}")
    
    def guardar_resultado_competencia(self, contest_data: dict) -> None:
        """Guardar resultado de la Competencia en formato YAML (archivo diario)."""
        try:
            # Create results directory if it doesn't exist
            import os
            os.makedirs(self.results_dir, exist_ok=True)

            # Generate timestamped filename
            from datetime import datetime
            timestamp = datetime.now().strftime('%y%m%d')
            filename = f'contests_{timestamp}.yml'
            filepath = os.path.join(self.results_dir, filename)

            # Load existing results or create new list
            contests = []
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r') as f:
                        content = f.read().strip()
                        contests = content.split('---\n') if content else []
                        contests = [c.strip() for c in contests if c.strip()]
                except:
                    contests = []

            # Append new result
            with open(filepath, 'a') as f:
                if contests:  # If file has content, add separator
                    f.write('\n---\n')
                f.write(f'- vs: "{contest_data["vs"]}"\n')
                f.write(f'  winner: "{contest_data["winner"]}"\n')
                f.write(f'  points: {contest_data["points"]}\n')
                f.write(f'  col1_name: "{contest_data["col1_name"]}"\n')
                f.write(f'  col2_name: "{contest_data["col2_name"]}"\n')
                f.write(f'  col1_final_pop: {contest_data["col1_final_pop"]}\n')
                f.write(f'  col2_final_pop: {contest_data["col2_final_pop"]}\n')
                f.write(f'  col1_final_energy: {contest_data["col1_final_energy"]:.2f}\n')
                f.write(f'  col2_final_energy: {contest_data["col2_final_energy"]:.2f}\n')
                f.write(f'  duration: {contest_data["duration"]}\n')
                f.write(f'  timestamp: "{contest_data["timestamp"]}"\n')

            print(f"Contest result saved to: {filepath}")

        except Exception as e:
            print(f"Error saving contest result: {e}")

    def generar_ranking_diario(self) -> None:
        """Generar ranking diario a partir de los resultados de Competencia de hoy."""
        try:
            from datetime import datetime

            # Get today's date for filename (YYMMDD only)
            today = datetime.now().strftime('%y%m%d')

            # Generate ranking for today only
            files_loaded = self.load_contest_files(today)

            if files_loaded == 0:
                print("No contests found for today - no ranking generated.")
                return

            # Generate and save daily ranking report (overwrite existing file for same day)
            import os
            output_file = os.path.join(self.results_dir, f"ranking_{today}.txt")
            report = self.generate_ranking_report()

            with open(output_file, 'w') as f:
                f.write(report)

            print(f"Daily ranking updated: {output_file}")

        except Exception as e:
            print(f"Error generating daily ranking: {e}")
    
    def update_global_ranking(self, global_ranking_file: str) -> int:
        """Update global ranking file with all available contest results
        
        Args:
            global_ranking_file: Name of the global ranking file to create/update
            
        Returns:
            0 on success, 1 on error
        """
        try:
            # Load all contest files
            files_loaded = self.load_contest_files("*")  # Load all files

            if files_loaded == 0:
                print("No contest files found to update global ranking.")
                return 1

            print(f"Loaded {files_loaded} contest file(s)")
            print(f"Total contests: {len(self.contests)}")

            # Generate comprehensive ranking report
            report = self.generate_ranking_report(top_n=50)  # Show more entries for global

            # Save to specified global ranking file in results directory
            import os
            import shutil

            bkp_dir = os.path.join(self.results_dir, "bkp")
            filepath = os.path.join(self.results_dir, global_ranking_file)

            # Create backup directory if it doesn't exist
            os.makedirs(bkp_dir, exist_ok=True)

            # Create backup of existing file if it exists
            if os.path.exists(filepath):
                timestamp = datetime.now().strftime('%y%m%d_%H%M%S')
                filename_base = os.path.splitext(global_ranking_file)[0]
                filename_ext = os.path.splitext(global_ranking_file)[1]
                backup_filename = f"{filename_base}_{timestamp}{filename_ext}"
                backup_filepath = os.path.join(bkp_dir, backup_filename)
                shutil.copy2(filepath, backup_filepath)
                print(f"Backup created: {backup_filepath}")

            # Write new ranking file
            with open(filepath, 'w') as f:
                f.write(report)
            print(f"Global ranking updated: {filepath}")

            # Also display the ranking
            print("\n" + report)

            return 0

        except Exception as e:
            print(f"Error updating global ranking: {e}")
            return 1

    # -----------------------------
    # Aliases for backward compatibility (English names)
    # These are placed at the end of the class and delegate to the
    # Spanish-named methods to preserve backward compatibility.
    def save_contest_result(self, contest_data: dict) -> None:
        """Backward-compatibility alias for `guardar_resultado_competencia`."""
        return self.guardar_resultado_competencia(contest_data)

    def generate_daily_ranking(self) -> None:
        """Backward-compatibility alias for `generar_ranking_diario`."""
        return self.generar_ranking_diario()


def main():
    """Command-line interface for ranking system.

    Usage:
      python lib/ranking.py [DATE_PATTERN]
    If DATE_PATTERN is provided, only contests matching that YYMMDD pattern are loaded.
    """
    import sys

    ranking = RankingSystem()

    if len(sys.argv) > 1:
        date_pattern = sys.argv[1]
    else:
        date_pattern = "*"

    files_loaded = ranking.load_contest_files(date_pattern)

    if files_loaded == 0:
        print(f"No contest files found matching pattern: contests_{date_pattern}.yml")
        return

    print(f"Loaded {files_loaded} contest file(s)")
    print(f"Total contests: {len(ranking.contests)}")
    print()

    # Generate and display ranking report
    report = ranking.generate_ranking_report()
    print(report)

    # Save to file with timestamp
    timestamp = datetime.now().strftime('%y%m%d_%H%M%S')
    output_file = f"results/ranking_{timestamp}.txt"
    ranking.save_ranking_report(output_file)


if __name__ == "__main__":
    main()

    # -----------------------------
    # Aliases for backward compatibility (English names)
    # These are placed at the end of the class and delegate to the
    # Spanish-named methods to preserve backward compatibility.
    def save_contest_result(self, contest_data: dict) -> None:
        """Backward-compatibility alias for `guardar_resultado_competencia`."""
        return self.guardar_resultado_competencia(contest_data)

    def generate_daily_ranking(self) -> None:
        """Backward-compatibility alias for `generar_ranking_diario`."""
        return self.generar_ranking_diario()


def main():
    """Command-line interface for ranking system.

    Usage:
      python lib/ranking.py [DATE_PATTERN]
    If DATE_PATTERN is provided, only contests matching that YYMMDD pattern are loaded.
    """
    import sys

    ranking = RankingSystem()

    if len(sys.argv) > 1:
        date_pattern = sys.argv[1]
    else:
        date_pattern = "*"

    files_loaded = ranking.load_contest_files(date_pattern)

    if files_loaded == 0:
        print(f"No contest files found matching pattern: contests_{date_pattern}.yml")
        return

    print(f"Loaded {files_loaded} contest file(s)")
    print(f"Total contests: {len(ranking.contests)}")
    print()

    # Generate and display ranking report
    report = ranking.generate_ranking_report()
    print(report)

    # Save to file with timestamp
    timestamp = datetime.now().strftime('%y%m%d_%H%M%S')
    output_file = f"results/ranking_{timestamp}.txt"
    ranking.save_ranking_report(output_file)


if __name__ == "__main__":
    main()