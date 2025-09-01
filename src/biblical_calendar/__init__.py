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

# Import GUI version (with tkinter)
try:
    from .calendar import BiblicalCalendarApp, main
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

# Import core version (web-compatible)
from .calendar_core import (
    BiblicalCalendarCore,
    generate_biblical_months_dynamic,
    map_festivals_to_dates,
    export_events_to_ics,
    compute_seasons_for_year,
    sunrise_sunset,
    FESTIVALS_DEF,
    YESHUA_EVENTS_DEF,
    MONTH_NAMES,
    JERUSALEM,
    SAOPAULO
)

__version__ = "2.0.0"
__author__ = "Vander Loto"
__email__ = "vander.loto@outlook.com"
__description__ = "Calendário bíblico-lunissolar dinâmico com cálculos astronômicos precisos"

__all__ = [
    "BiblicalCalendarCore",
    "generate_biblical_months_dynamic", 
    "map_festivals_to_dates",
    "export_events_to_ics",
    "compute_seasons_for_year",
    "sunrise_sunset",
    "FESTIVALS_DEF",
    "YESHUA_EVENTS_DEF", 
    "MONTH_NAMES",
    "JERUSALEM",
    "SAOPAULO",
    "GUI_AVAILABLE"
]

# Add GUI exports if available
if GUI_AVAILABLE:
    __all__.extend(["BiblicalCalendarApp", "main"])