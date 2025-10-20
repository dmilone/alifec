# Documentación del sistema de rankings diarios

## Resumen
El sistema genera archivos de ranking diarios con marcas de tiempo simplificadas (formato YYMMDD) que se actualizan cada vez que se agrega un nuevo concurso en la misma fecha.

## Convenciones de nombres de archivo

### Archivos de concursos
- `contests_YYMMDD.yml` - Contiene todos los concursos de una fecha específica
- Varios concursos del mismo día se agregan (append) al mismo archivo

### Archivos de ranking diario
- `ranking_YYMMDD.txt` - Ranking diario para una fecha específica (formato YYMMDD)
- **Se actualiza automáticamente** cada vez que se añade un concurso ese día
- **Sobrescribe** el archivo existente del mismo día

### Archivos de ranking global
- Nombre definido por el usuario (por ejemplo, `global_ranking.txt`)
- **Se guarda en**: `results/global_ranking.txt`
- **Backups automáticos**: versiones anteriores se guardan en `results/bkp/` con marca de tiempo completa
- Contiene estadísticas acumuladas de todos los archivos de concursos
- Se genera bajo demanda con la opción `--update-global`

## Ejemplo de flujo de trabajo

1. **Ejecutar el primer concurso del día:**
   ```bash
   python comvida.py --dist 4 --colonies 0 1
   ```
   - Crea: `results/contests_251005.yml`
   - Crea: `results/ranking_251005.txt`

2. **Ejecutar un segundo concurso el mismo día:**
   ```bash
   python comvida.py --dist 3 --colonies 2 4
   ```
   - Agrega (append) a: `results/contests_251005.yml`
   - **Actualiza**: `results/ranking_251005.txt` (sobrescribe con las nuevas estadísticas)

3. **Generar ranking global:**
   ```bash
   python comvida.py --update-global global_ranking.txt
   ```
   - Procesa todos los archivos `contests_*.yml`
   - Crea/actualiza: `results/global_ranking.txt`

## Ejemplo de estructura de archivos
```
results/
├── contests_251004.yml            # Concursos de ayer (4 Oct 2025)
├── contests_251005.yml            # Concursos de hoy (5 Oct 2025)
├── ranking_251004.txt             # Ranking de ayer
├── ranking_251005.txt             # Ranking de hoy (actualizado con cada concurso)
├── global_ranking.txt             # Ranking global (todos los tiempos)
├── season1_rankings.txt           # Archivo de ranking global personalizado
└── bkp/                           # Directorio de backups
    ├── global_ranking_251005_114710.txt    # Backup con marca de tiempo completa
    └── season1_rankings_251005_114739.txt  # Backup de ranking personalizado
```
