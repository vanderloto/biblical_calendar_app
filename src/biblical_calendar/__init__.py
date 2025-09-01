"""Biblical Calendar - Calendário Bíblico Lunissolar.

Este módulo implementa um calendário bíblico dinâmico baseado nas luas novas
em Jerusalém, com cálculos astronômicos precisos e exportação para formatos
padrão (CSV, ICS).

Funcionalidades:
    - 10 festivais bíblicos completos com nomes hebraicos
    - Calendário visual interativo com navegação contínua
    - Fases lunares completas e estações astronômicas
    - Suporte bilíngue (Hebraico/Português)
    - Exportação CSV e ICS

Exemplo:
    >>> from biblical_calendar import BiblicalCalendarApp
    >>> app = BiblicalCalendarApp()
    >>> app.mainloop()

Autor:
    Vander Loto - DATAMETRIA

Versão:
    1.0.0
"""

from .calendar import (
    BiblicalCalendarApp,
    generate_biblical_months_dynamic,
    map_festivals_to_dates,
    export_events_to_ics,
    compute_seasons_for_year,
    sunrise_sunset,
    main,
    FESTIVALS_DEF,
    YESHUA_EVENTS_DEF,
    MONTH_NAMES,
    JERUSALEM,
    SAOPAULO
)

__version__ = "1.2.0"
__author__ = "Vander Loto"
__email__ = "vander.loto@outlook.com"
__description__ = "Calendário bíblico-lunissolar dinâmico com cálculos astronômicos precisos"

__all__ = [
    "BiblicalCalendarApp",
    "generate_biblical_months_dynamic", 
    "map_festivals_to_dates",
    "export_events_to_ics",
    "compute_seasons_for_year",
    "sunrise_sunset",
    "main",
    "FESTIVALS_DEF",
    "YESHUA_EVENTS_DEF", 
    "MONTH_NAMES",
    "JERUSALEM",
    "SAOPAULO"
]