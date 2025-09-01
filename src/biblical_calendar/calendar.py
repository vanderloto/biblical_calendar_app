"""Biblical Lunisolar Calendar - Calendário Bíblico Lunissolar.

Este módulo implementa um calendário bíblico dinâmico baseado em cálculos
astronômicos precisos das luas novas em Jerusalém.

Funcionalidades:
    - Meses ancorados em luas novas astronômicas (Skyfield)
    - Heurística opcional para primeira crescente visível em Jerusalém
    - 10 festivais bíblicos completos com nomes hebraicos e traduções
    - Eventos de Yeshua com múltiplas hipóteses
    - Calendário visual interativo com navegação contínua
    - Painel de eventos expandido com descrições educativas
    - Fases lunares completas e estações astronômicas
    - Informações para ambos hemisférios (Jerusalém/São Paulo)
    - Exportação CSV e ICS para integração externa

Exemplo:
    >>> app = BiblicalCalendarApp()
    >>> app.mainloop()

Autor:
    Vander Loto - DATAMETRIA

Versão:
    1.3.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date, timedelta, timezone, time as dt_time
import pandas as pd
import pytz
import os
import math

# Astronomy
from skyfield import api, almanac
from skyfield.api import Topos
from astral import LocationInfo
from astral.sun import sun

# ICS
from icalendar import Calendar, Event

# Optional nicer widget
try:
    from tkcalendar import DateEntry
    TKCAL_AVAILABLE = True
except Exception:
    TKCAL_AVAILABLE = False

# ---------------- CONFIG ----------------
JERUSALEM = {"name": "Jerusalem", "region": "Israel", "lat": 31.7683, "lon": 35.2137, "tz": "Asia/Jerusalem"}
SAOPAULO  = {"name": "São Paulo",  "region": "Brazil", "lat": -23.5505, "lon": -46.6333, "tz": "America/Sao_Paulo"}

MONTH_NAMES = ["Nissan", "Iyar", "Sivan", "Tammuz", "Av", "Elul",
               "Tishrei", "Cheshvan", "Kislev", "Tevet", "Shevat", "Adar"]

# Cronologias para comparação de anos
def calculate_ussher_year(gregorian_year: int) -> int:
    """Calcula ano segundo cronologia de Ussher (Criação em 4004 AC).
    
    Args:
        gregorian_year (int): Ano gregoriano.
        
    Returns:
        int: Ano desde a criação segundo Ussher.
    """
    return gregorian_year + 4004

def calculate_hebrew_year(gregorian_year: int) -> int:
    """Calcula ano hebraico aproximado (AM - Anno Mundi).
    
    Args:
        gregorian_year (int): Ano gregoriano.
        
    Returns:
        int: Ano hebraico aproximado.
    """
    # Conversão aproximada: ano hebraico = gregoriano + 3760
    # Ajuste pode variar de 1 ano dependendo do mês
    return gregorian_year + 3760

FESTIVALS_DEF = {
    # Festas da Primavera
    "Pessach": (1, 15),                    # Páscoa - Nissan 15
    "Chag HaMatzot": (1, 16),             # Festa dos Pães Asmos - Nissan 16-21 (início)
    "Omer Reshit": (1, 17),               # Primícias - Nissan 17
    
    # Festa do Verão
    "Shavuot": (3, 6),                    # Pentecostes - Sivan 6
    
    # Festas do Outono
    "Rosh Hashaná": (7, 1),               # Festa das Trombetas - Tishrei 1
    "Yom Kippur": (7, 10),                # Dia da Expiação - Tishrei 10
    "Sukkot": (7, 15),                    # Festa dos Tabernáculos - Tishrei 15
    
    # Outras celebrações importantes
    "Chanucá": (9, 25),                   # Festa das Luzes - Kislev 25
    "Purim": (12, 14),                    # Livramento de Ester - Adar 14
}
YESHUA_EVENTS_DEF = {
    "Leidat Yeshua (Nissan)": (1, 15),
    "Leidat Yeshua (Tishrei)": (7, 15),
    "Mavet Yeshua (Tzliva)": (1, 14)
}

# Traduções para português
FESTIVAL_TRANSLATIONS = {
    # Festas da Primavera
    "Pessach": "Páscoa",
    "Chag HaMatzot": "Festa dos Pães Asmos",
    "Omer Reshit": "Primícias",
    
    # Festa do Verão
    "Shavuot": "Pentecostes",
    
    # Festas do Outono
    "Rosh Hashaná": "Festa das Trombetas",
    "Yom Kippur": "Dia da Expiação",
    "Sukkot": "Festa dos Tabernáculos",
    
    # Outras celebrações
    "Chanucá": "Festa das Luzes",
    "Purim": "Festa de Purim",
    
    # Eventos de Yeshua
    "Leidat Yeshua (Nissan)": "Nascimento de Jesus (hipótese Nissan)",
    "Leidat Yeshua (Tishrei)": "Nascimento de Jesus (hipótese Sukkot)",
    "Mavet Yeshua (Tzliva)": "Crucificação de Jesus"
}

# Descrições das festas e eventos
FESTIVAL_DESCRIPTIONS = {
    "Pessach": "Celebra a libertação do povo de Israel do Egito. Simboliza redenção e sacrifício.",
    "Chag HaMatzot": "Representa a purificação do pecado, com a retirada do fermento.",
    "Omer Reshit": "Marca o início da colheita e a consagração dos primeiros frutos a Deus.",
    "Shavuot": "Comemora a entrega da Torá no Sinai e também é associada à colheita do trigo.",
    "Rosh Hashaná": "Ano Novo judaico, marcado pelo toque do shofar e chamado ao arrependimento.",
    "Yom Kippur": "Dia solene de jejum e arrependimento, buscando perdão e purificação.",
    "Sukkot": "Celebra a proteção divina durante a travessia no deserto e a colheita final.",
    "Chanucá": "Comemora a dedicação do templo e o milagre do azeite.",
    "Purim": "Celebra o livramento dos judeus na história de Ester.",
    "Leidat Yeshua (Nissan)": "Hipótese do nascimento de Jesus em Nissan 15 (Páscoa). Alguns estudiosos sugerem esta data baseando-se na simbologia do 'Cordeiro Pascal' e na proximidade com a Páscoa. Esta teoria conecta o nascimento com o tema da redenção e libertação.",
    "Leidat Yeshua (Tishrei)": "Hipótese do nascimento de Jesus em Tishrei 15 (Sukkot). Muitos eruditos favorecem esta data considerando que Sukkot era época de peregrinação a Jerusalém, explicando a lotação das hospedarias. A festa simboliza a habitação de Deus entre os homens (João 1:14 - 'o Verbo se fez carne e habitou entre nós').",
    "Mavet Yeshua (Tzliva)": "Crucificação de Jesus em Nissan 14, véspera da Páscoa (30 ou 33 d.C.). Momento central da fé cristã, quando Jesus é sacrificado como 'Cordeiro Pascal' para redenção da humanidade. A data coincide simbolicamente com o sacrifício dos cordeiros pascais no Templo.",
    "Lua Nova": "Início do mês bíblico baseado na conjunção astronômica Sol-Lua.",
    "Lua Cheia": "Fase lunar quando a Lua está completamente iluminada pelo Sol.",
    "Quarto Crescente": "Fase lunar quando metade da Lua está visível e crescendo.",
    "Quarto Minguante": "Fase lunar quando metade da Lua está visível e diminuindo.",
    "Equinócio de Primavera": "Em Jerusalém, marca o início da primavera (Hemisfério Norte)\nEm São Paulo, marca o início do outono (Hemisfério Sul)",
    "Solstício de Verão": "Em Jerusalém, marca o início do verão (Hemisfério Norte)\nEm São Paulo, marca o início do inverno (Hemisfério Sul)",
    "Equinócio de Outono": "Em Jerusalém, marca o início do outono (Hemisfério Norte)\nEm São Paulo, marca o início da primavera (Hemisfério Sul)",
    "Solstício de Inverno": "Em Jerusalém, marca o início do inverno (Hemisfério Norte)\nEm São Paulo, marca o início do verão (Hemisfério Sul)"
}

# Skyfield ephemeris - Dynamic loading based on year
TS = api.load.timescale()

# Global ephemeris variable - will be set dynamically
Eph = None
CURRENT_EPHEMERIS = "none"

# Jerusalem Topos for positional checks
JER_TOPOS = Topos(latitude_degrees=JERUSALEM["lat"], longitude_degrees=JERUSALEM["lon"])

def load_optimal_ephemeris(year: int, force_academic: bool = False) -> tuple[object, str]:
    """Carrega a efeméride mais adequada para o ano especificado.
    
    Args:
        year (int): Ano para o qual calcular.
        force_academic (bool): Se True, força uso de DE440 para máxima precisão.
        
    Returns:
        tuple[object, str]: Objeto efeméride e nome da efeméride carregada.
        
    Raises:
        RuntimeError: Se nenhuma efeméride adequada puder ser carregada.
    """
    global Eph, CURRENT_EPHEMERIS
    
    # Modo acadêmico sempre usa DE440
    if force_academic:
        try:
            eph = api.load('de440.bsp')
            Eph = eph
            CURRENT_EPHEMERIS = "DE440 (Modo Acadêmico)"
            return eph, CURRENT_EPHEMERIS
        except Exception as e:
            # Fallback para DE430 se DE440 não disponível
            try:
                eph = api.load('de430.bsp')
                Eph = eph
                CURRENT_EPHEMERIS = "DE430 (Fallback Acadêmico)"
                return eph, CURRENT_EPHEMERIS
            except Exception:
                raise RuntimeError(f"Modo acadêmico requer DE440/DE430. Erro: {e}")
    
    # Seleção automática baseada no ano
    if year <= 2050:
        # DE421 para anos "normais" (1900-2050)
        try:
            eph = api.load('de421.bsp')
            Eph = eph
            CURRENT_EPHEMERIS = "DE421 (Padrão)"
            return eph, CURRENT_EPHEMERIS
        except Exception as e:
            # Fallback para DE440 se DE421 não disponível
            try:
                eph = api.load('de440.bsp')
                Eph = eph
                CURRENT_EPHEMERIS = "DE440 (Fallback)"
                return eph, CURRENT_EPHEMERIS
            except Exception:
                raise RuntimeError(f"Não foi possível carregar efeméride adequada. Erro: {e}")
    else:
        # DE440 para anos > 2050
        try:
            eph = api.load('de440.bsp')
            Eph = eph
            CURRENT_EPHEMERIS = "DE440 (Ano > 2050)"
            return eph, CURRENT_EPHEMERIS
        except Exception as e:
            # Fallback para DE430
            try:
                eph = api.load('de430.bsp')
                Eph = eph
                CURRENT_EPHEMERIS = "DE430 (Fallback)"
                return eph, CURRENT_EPHEMERIS
            except Exception:
                raise RuntimeError(f"Anos > 2050 requerem DE440/DE430. Erro: {e}")

# Initialize with default ephemeris
try:
    Eph, CURRENT_EPHEMERIS = load_optimal_ephemeris(datetime.now().year)
except Exception:
    # Ultimate fallback
    Eph = api.load('de421.bsp')
    CURRENT_EPHEMERIS = "DE421 (Fallback)"

# ---------------- Astronomical helpers ----------------

def get_march_equinox(year: int) -> date:
    """Obtém a data do equinócio de março.
    
    Args:
        year (int): Ano para calcular o equinócio.
        
    Returns:
        date: Data UTC do equinócio de março.
    """
    t0 = TS.utc(year, 1, 1)
    t1 = TS.utc(year, 12, 31)
    times, events = almanac.find_discrete(t0, t1, almanac.seasons(Eph))
    for ti, ev in zip(times, events):
        if ev == 0:
            return ti.utc_datetime().date()
    return date(year, 3, 20)

def find_new_moons_window(start_date: date, end_date: date) -> list[date]:
    """Encontra luas novas astronômicas em um período.
    
    Args:
        start_date (date): Data inicial (inclusiva).
        end_date (date): Data final (inclusiva).
        
    Returns:
        list[date]: Lista de datas UTC das luas novas.
    """
    t0 = TS.utc(start_date.year, start_date.month, start_date.day)
    t1 = TS.utc(end_date.year, end_date.month, end_date.day + 1)
    f = almanac.moon_phases(Eph)
    times, phases = almanac.find_discrete(t0, t1, f)
    out = []
    for ti, ph in zip(times, phases):
        if ph == 0:
            # convert to UTC date
            out.append(ti.utc_datetime().date())
    return out

def next_new_moon_on_or_after(start_date: date) -> date:
    """Próxima lua nova astronômica em ou após a data especificada.
    
    Args:
        start_date (date): Data inicial para busca.
        
    Returns:
        date: Data da próxima lua nova.
        
    Raises:
        RuntimeError: Se nenhuma lua nova for encontrada na janela de busca.
    """
    # search 2 years ahead
    t0 = TS.utc(start_date.year, start_date.month, start_date.day)
    t1 = TS.utc(start_date.year + 2, 12, 31)
    f = almanac.moon_phases(Eph)
    times, phases = almanac.find_discrete(t0, t1, f)
    for ti, ph in zip(times, phases):
        if ph == 0:
            dt = ti.utc_datetime().date()
            if dt >= start_date:
                return dt
    raise RuntimeError("No new moon found in search window.")

def sun_moon_elongation_and_altitude_at(city_cfg: dict, when_dt_utc: datetime) -> tuple[float, float]:
    """Calcula elongação e altitude da lua para uma cidade.
    
    Args:
        city_cfg (dict): Configuração da cidade com lat, lon.
        when_dt_utc (datetime): Momento UTC para cálculo.
        
    Returns:
        tuple[float, float]: Elongação em graus e altitude da lua em graus.
    """
    # when_dt_utc: timezone-aware UTC datetime
    t = TS.utc(when_dt_utc.year, when_dt_utc.month, when_dt_utc.day,
               when_dt_utc.hour, when_dt_utc.minute, when_dt_utc.second)
    sun = Eph['sun']
    moon = Eph['moon']
    earth = Eph['earth']
    # Observer location
    obs = earth + Topos(latitude_degrees=city_cfg["lat"], longitude_degrees=city_cfg["lon"])
    # Apparent positions
    astrometric_moon = obs.at(t).observe(moon).apparent()
    astrometric_sun = obs.at(t).observe(sun).apparent()
    # Separation
    sep = astrometric_moon.separation_from(astrometric_sun).degrees
    # Moon altitude
    alt, az, distance = astrometric_moon.altaz()
    alt_deg = alt.degrees
    return sep, alt_deg

def is_first_crescent_visible_heuristic(new_moon_date: date, city_cfg: dict) -> date | None:
    """Heurística para determinar visibilidade da primeira crescente.
    
    Verifica até 3 noites após a lua nova astronômica procurando por:
    - Elongação >= 10 graus
    - Altitude da lua >= 3 graus no pôr do sol local
    
    Args:
        new_moon_date (date): Data da lua nova astronômica.
        city_cfg (dict): Configuração da cidade.
        
    Returns:
        date | None: Data local quando a crescente é considerada visível, ou None.
    """
    tz = pytz.timezone(city_cfg["tz"])
    # candidate days: new_moon_date, new_moon_date+1, +2, +3
    for delta in range(0, 4):
        cand = new_moon_date + timedelta(days=delta)
        # compute local sunset time for the city on 'cand' date
        loc = LocationInfo(city_cfg["name"], city_cfg["region"], city_cfg["tz"], city_cfg["lat"], city_cfg["lon"])
        try:
            s = sun(loc.observer, date=cand)
            sunset_local = s['sunset']  # timezone-aware local
        except Exception:
            # fallback: use 18:00 local
            sunset_local = tz.localize(datetime.combine(cand, dt_time(hour=18, minute=0)))
        # convert sunset to UTC
        sunset_utc = sunset_local.astimezone(pytz.UTC)
        # compute elongation and altitude at 20-30 minutes after sunset (safer)
        check_time = sunset_utc + timedelta(minutes=30)
        sep, alt = sun_moon_elongation_and_altitude_at(city_cfg, check_time)
        # thresholds: elongation >= 7-10 deg, altitude >= 3 deg
        if sep >= 10 and alt >= 3:
            # return the local date cand as the month start (Nissan 1 = that evening -> local date)
            return cand
    return None

# ---------------- Month generation ----------------

def generate_biblical_months_dynamic(reference_year: int, use_visibility_heuristic: bool = False) -> tuple[pd.DataFrame, bool, date]:
    """Gera meses bíblicos dinâmicos para um ano.
    
    Constrói meses ancorados em Nissan = primeira lua nova em/após equinócio de março.
    Opcionalmente ajusta para primeira crescente visível em Jerusalém.
    Detecta ano embolísmico (13 meses lunares em ~370 dias).
    
    Args:
        reference_year (int): Ano de referência.
        use_visibility_heuristic (bool): Se deve usar heurística de visibilidade.
        
    Returns:
        tuple[pd.DataFrame, bool, date]: DataFrame dos meses, se é embolísmico, data início Nissan.
    """
    equinox = get_march_equinox(reference_year)
    # find first astronomical new moon on/after equinox
    nissan_astro = next_new_moon_on_or_after(equinox)
    # if using heuristic visibility, try to determine visible date for Nissan
    if use_visibility_heuristic:
        vis = is_first_crescent_visible_heuristic(nissan_astro, JERUSALEM)
        if vis is not None:
            nissan_start = vis
        else:
            nissan_start = nissan_astro
    else:
        nissan_start = nissan_astro

    # collect successive astronomical new moons (14+) to detect embolismic
    new_moons = [nissan_astro]
    cursor = nissan_astro + timedelta(days=1)
    for _ in range(14):
        nm = next_new_moon_on_or_after(cursor)
        new_moons.append(nm)
        cursor = nm + timedelta(days=1)

    # count new moons within ~370 days -> embolismic if >=13
    limit = nissan_astro + timedelta(days=370)
    count = sum(1 for nm in new_moons if nm <= limit)
    embolismic = (count >= 13)

    # Now build months using astronomical new moons, but shift start to visible date if heuristic True
    months = []
    # prepare names sequence
    if embolismic:
        # will have 13 months: Nissan..Shevat, Adar I, Adar II
        for i in range(13):
            astro_start = new_moons[i]
            # If using visibility rule, compute local visible date for this astro new moon
            if use_visibility_heuristic:
                vis = is_first_crescent_visible_heuristic(astro_start, JERUSALEM)
                start_date = vis if vis is not None else astro_start
            else:
                start_date = astro_start
            end_date = new_moons[i+1] - timedelta(days=1)
            # name mapping: 0..10 -> MONTH_NAMES[0..10]; 11->Adar I, 12->Adar II
            if i < 11:
                name = MONTH_NAMES[i]
            elif i == 11:
                name = "Adar I"
            else:
                name = "Adar II"
            months.append({"index": i+1, "name": name, "start": start_date, "end": end_date, "days": (end_date - start_date).days + 1})
    else:
        for i in range(12):
            astro_start = new_moons[i]
            if use_visibility_heuristic:
                vis = is_first_crescent_visible_heuristic(astro_start, JERUSALEM)
                start_date = vis if vis is not None else astro_start
            else:
                start_date = astro_start
            end_date = new_moons[i+1] - timedelta(days=1)
            name = MONTH_NAMES[i]
            months.append({"index": i+1, "name": name, "start": start_date, "end": end_date, "days": (end_date - start_date).days + 1})

    df = pd.DataFrame(months)
    # Ensure Nissan start returned is the mapped start (visible or astro)
    nissan_mapped_start = df.iloc[0]["start"] if not df.empty else nissan_start
    return df, embolismic, nissan_mapped_start

# ---------------- Festival mapping & ICS export ----------------

def map_festivals_to_dates(months_df: pd.DataFrame, festivals_dict: dict) -> list[dict]:
    """Mapeia festivais para datas específicas.
    
    Args:
        months_df (pd.DataFrame): DataFrame com os meses.
        festivals_dict (dict): Dicionário de festivais {nome: (mês, dia)}.
        
    Returns:
        list[dict]: Lista de eventos com nome e data.
    """
    out = []
    for fname, (midx, day) in festivals_dict.items():
        row = months_df[months_df["index"] == midx]
        if not row.empty:
            start = row.iloc[0]["start"]
            ev_date = start + timedelta(days=day-1)
            out.append({"name": fname, "date": ev_date})
    return out

def export_events_to_ics(event_list: list[dict], filename: str) -> None:
    """Exporta lista de eventos para arquivo ICS.
    
    Args:
        event_list (list[dict]): Lista de eventos com name, date, description.
        filename (str): Caminho do arquivo ICS a ser criado.
    """
    cal = Calendar()
    cal.add('prodid', '-//Biblical Lunisolar Calendar//')
    cal.add('version', '2.0')
    for ev in event_list:
        ical = Event()
        ical.add('summary', ev['name'])
        # all-day event
        dt = ev['date']
        ical.add('dtstart', dt)
        ical.add('dtend', dt + timedelta(days=1))
        if ev.get('description'):
            ical.add('description', ev['description'])
        cal.add_component(ical)
    with open(filename, 'wb') as f:
        f.write(cal.to_ical())

# ---------------- Seasons & sun events ----------------

def compute_seasons_for_year(year: int) -> list[dict]:
    """Calcula as estações astronômicas para um ano.
    
    Args:
        year (int): Ano para calcular as estações.
        
    Returns:
        list[dict]: Lista com eventos das estações e timestamps UTC.
    """
    t0 = TS.utc(year, 1, 1)
    t1 = TS.utc(year, 12, 31)
    times, events = almanac.find_discrete(t0, t1, almanac.seasons(Eph))
    mapping = {0: "March Equinox", 1: "June Solstice", 2: "September Equinox", 3: "December Solstice"}
    out = []
    for ti, ev in zip(times, events):
        out.append({"event": mapping[ev], "utc": ti.utc_datetime().replace(tzinfo=timezone.utc)})
    return out

def sunrise_sunset(location_cfg: dict, target_date: date) -> dict:
    """Calcula nascer e pôr do sol para uma localização e data.
    
    Args:
        location_cfg (dict): Configuração da localização.
        target_date (date): Data alvo.
        
    Returns:
        dict: Dicionário com sunrise e sunset (timezone-aware).
    """
    loc = LocationInfo(location_cfg["name"], location_cfg["region"], location_cfg["tz"], location_cfg["lat"], location_cfg["lon"])
    try:
        s = sun(loc.observer, date=target_date)
        return {"sunrise": s["sunrise"].astimezone(pytz.timezone(location_cfg["tz"])),
                "sunset": s["sunset"].astimezone(pytz.timezone(location_cfg["tz"]))}
    except Exception:
        return {"sunrise": None, "sunset": None}

# ---------------- GUI Application ----------------

class BiblicalCalendarApp(tk.Tk):
    """Aplicação GUI para Calendário Bíblico Lunissolar.
    
    Interface gráfica completa com abas para visualização de meses,
    festivais, estações astronômicas e calendário visual.
    
    Attributes:
        months_df (pd.DataFrame): DataFrame com os meses calculados.
        embolismic (bool): Se o ano é embolísmico (13 meses).
        nissan_start (date): Data de início do mês de Nissan.
        visual_index (int): Índice do mês sendo visualizado.
    """
    
    def __init__(self) -> None:
        """Inicializa a aplicação GUI."""
        super().__init__()
        self.title("Biblical Lunisolar Calendar (Dynamic) - Jerusalem anchored")
        self.geometry("1400x900")

        # Notebook
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True)

        # Tabs
        self.tab_months = ttk.Frame(self.nb)
        self.tab_festivals = ttk.Frame(self.nb)
        self.tab_seasons = ttk.Frame(self.nb)
        self.tab_visual = ttk.Frame(self.nb)

        self.nb.add(self.tab_visual, text="Calendário Visual")
        self.nb.add(self.tab_months, text="Meses (lista)")
        self.nb.add(self.tab_festivals, text="Festas & Yeshua")
        self.nb.add(self.tab_seasons, text="Estações (Jerusalém / São Paulo)")

        # Top controls
        ctrl = ttk.Frame(self)
        ctrl.pack(fill="x", padx=8, pady=6)
        
        # First row - Year and basic options
        row1 = ttk.Frame(ctrl)
        row1.pack(fill="x", pady=2)
        ttk.Label(row1, text="Ano referência:").pack(side="left")
        self.year_var = tk.IntVar(value=datetime.now().year)
        ttk.Entry(row1, width=6, textvariable=self.year_var).pack(side="left", padx=4)
        self.visual_visibility_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(row1, text="Heurística visibilidade (Jerusalém)", variable=self.visual_visibility_var).pack(side="left", padx=8)
        self.academic_mode_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(row1, text="🔬 Modo Pesquisa Acadêmica (DE440)", variable=self.academic_mode_var).pack(side="left", padx=8)
        
        # Second row - Actions and status
        row2 = ttk.Frame(ctrl)
        row2.pack(fill="x", pady=2)
        ttk.Button(row2, text="Gerar", command=self.generate_all).pack(side="left", padx=6)
        ttk.Button(row2, text="Exportar ICS", command=self.on_export_ics).pack(side="left", padx=6)
        ttk.Button(row2, text="Exportar CSV", command=self.on_export_csv).pack(side="left", padx=6)
        
        # Ephemeris status label
        self.ephemeris_status = ttk.Label(row2, text=f"Efeméride: {CURRENT_EPHEMERIS}", foreground="blue")
        self.ephemeris_status.pack(side="right", padx=8)

        # Build tab UIs
        self._build_months_tab()
        self._build_festivals_tab()
        self._build_seasons_tab()
        self._build_visual_tab()

        # state
        self.months_df = None
        self.embolismic = False
        self.nissan_start = None
        self.visual_index = 0
        self.current_ephemeris_name = CURRENT_EPHEMERIS

        # initial generate
        self.generate_all()
        
        # select visual calendar tab
        self.nb.select(self.tab_visual)

    def _build_months_tab(self) -> None:
        """Constrói a aba de listagem dos meses."""
        cols = ("index", "name", "start", "end", "days")
        self.tree_months = ttk.Treeview(self.tab_months, columns=cols, show="headings")
        for c in cols:
            self.tree_months.heading(c, text=c.capitalize())
            self.tree_months.column(c, width=130 if c in ("start","end") else 80)
        self.tree_months.pack(fill="both", expand=True, padx=6, pady=6)

    def _build_festivals_tab(self) -> None:
        """Constrói a aba de festivais e eventos."""
        left = ttk.Frame(self.tab_festivals)
        left.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        ttk.Label(left, text="Festividades e eventos (calculados):", font=("Arial", 12, "bold")).pack(anchor="w")
        self.txt_fest = tk.Text(left, width=70, height=25)
        self.txt_fest.pack(fill="both", expand=True)

    def _build_seasons_tab(self) -> None:
        """Constrói a aba de estações astronômicas."""
        frame = ttk.Frame(self.tab_seasons)
        frame.pack(fill="both", expand=True, padx=6, pady=6)
        left = ttk.Frame(frame)
        left.pack(side="left", fill="both", expand=True)
        right = ttk.Frame(frame)
        right.pack(side="left", fill="both", expand=True)

        ttk.Label(left, text="Estações astronômicas (UTC) - Jerusalém:", font=("Arial", 11, "bold")).pack(anchor="w")
        self.txt_seasons_jer = tk.Text(left, width=60, height=12)
        self.txt_seasons_jer.pack(fill="both", expand=True)

        ttk.Label(right, text="Estações astronômicas (UTC) - São Paulo:", font=("Arial", 11, "bold")).pack(anchor="w")
        self.txt_seasons_sp = tk.Text(right, width=60, height=12)
        self.txt_seasons_sp.pack(fill="both", expand=True)

        ttk.Label(frame, text="Exemplo: Nascer/Por do sol em Nissan 1 (Jerusalém / São Paulo):", font=("Arial", 10)).pack(anchor="w", padx=6, pady=4)
        self.txt_sun = tk.Text(frame, width=130, height=6)
        self.txt_sun.pack(fill="both", padx=6, pady=4)

    def _build_visual_tab(self) -> None:
        """Constrói a aba do calendário visual."""
        vf = ttk.Frame(self.tab_visual)
        vf.pack(fill="both", expand=True)
        hdr = ttk.Frame(vf)
        hdr.pack(fill="x", pady=4)
        self.lbl_visual = ttk.Label(hdr, text="Calendário Visual", font=("Arial", 12, "bold"))
        self.lbl_visual.pack(side="left")
        
        # Year comparisons label
        self.lbl_years = ttk.Label(hdr, text="", font=("Arial", 9), foreground="gray")
        self.lbl_years.pack(side="left", padx=(20, 0))
        btns = ttk.Frame(hdr)
        btns.pack(side="right")
        ttk.Button(btns, text="◀ Anterior", command=self.visual_prev).pack(side="left", padx=4)
        ttk.Button(btns, text="Hoje", command=self.visual_today).pack(side="left", padx=4)
        ttk.Button(btns, text="Próximo ▶", command=self.visual_next).pack(side="left", padx=4)

        main_frame = ttk.Frame(vf)
        main_frame.pack(fill="both", expand=True)
        
        self.grid_container = ttk.Frame(main_frame)
        self.grid_container.pack(side="left", fill="both", expand=True)
        
        right_panel = ttk.Frame(main_frame, width=450)
        right_panel.pack(side="right", fill="y", padx=(10, 0))
        right_panel.pack_propagate(False)
        
        ttk.Label(right_panel, text="Legenda:", font=("Arial", 10, "bold")).pack(anchor="w")
        ttk.Label(right_panel, text="🌑 Lua Nova").pack(anchor="w")
        ttk.Label(right_panel, text="🌓 Lua Crescente").pack(anchor="w")
        ttk.Label(right_panel, text="🌕 Lua Cheia").pack(anchor="w")
        ttk.Label(right_panel, text="🌗 Lua Minguante").pack(anchor="w")
        ttk.Label(right_panel, text="★ Festival").pack(anchor="w")
        ttk.Label(right_panel, text="🌍 Estação Astronômica").pack(anchor="w")
        ttk.Label(right_panel, text="Fundo azul = Hoje").pack(anchor="w")
        
        ttk.Separator(right_panel, orient="horizontal").pack(fill="x", pady=5)
        
        ttk.Label(right_panel, text="Cronologias:", font=("Arial", 10, "bold")).pack(anchor="w")
        ttk.Label(right_panel, text="Ussher: Desde Criação (4004 AC)", font=("Arial", 8)).pack(anchor="w")
        ttk.Label(right_panel, text="Hebraico: Anno Mundi (AM)", font=("Arial", 8)).pack(anchor="w")
        ttk.Label(right_panel, text="Gregoriano: Era Cristã (DC)", font=("Arial", 8)).pack(anchor="w")
        
        ttk.Separator(right_panel, orient="horizontal").pack(fill="x", pady=10)
        
        ttk.Label(right_panel, text="Eventos do Dia:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.day_events = tk.Text(right_panel, width=55, height=20, wrap="word")
        self.day_events.tag_configure("bold", font=("Arial", 9, "bold"))
        self.day_events.pack(fill="both", expand=True)

    def generate_all(self) -> None:
        """Gera todos os dados do calendário e atualiza a interface."""
        year = int(self.year_var.get())
        use_vis = bool(self.visual_visibility_var.get())
        academic_mode = bool(self.academic_mode_var.get())
        
        # Load optimal ephemeris for the year
        try:
            if academic_mode:
                messagebox.showinfo("Modo Acadêmico", 
                    "Modo Pesquisa Acadêmica ativado.\n\n"
                    "• Usando efeméride DE440 para máxima precisão\n"
                    "• Download de ~128MB pode ser necessário\n"
                    "• Dados exportados com precisão estendida")
            
            eph, eph_name = load_optimal_ephemeris(year, force_academic=academic_mode)
            self.current_ephemeris_name = eph_name
            self.ephemeris_status.config(text=f"Efeméride: {eph_name}")
            
        except Exception as e:
            messagebox.showerror("Erro de Efeméride", 
                f"Falha ao carregar efeméride adequada:\n{e}\n\n"
                f"Verifique sua conexão com internet.")
            return
        
        try:
            df, embol, nissan = generate_biblical_months_dynamic(year, use_visibility_heuristic=use_vis)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao calcular meses: {e}")
            return
        self.months_df = df
        self.embolismic = embol
        self.nissan_start = nissan

        # populate months tree
        for r in self.tree_months.get_children():
            self.tree_months.delete(r)
        for _, row in df.iterrows():
            self.tree_months.insert('', 'end', values=(int(row["index"]), row["name"], row["start"].isoformat(), row["end"].isoformat(), int(row["days"])))

        # festivals
        combined = FESTIVALS_DEF.copy()
        combined.update(YESHUA_EVENTS_DEF)
        fest_list = map_festivals_to_dates(df, combined)
        self.txt_fest.delete("1.0", tk.END)
        
        # Technical info for academic mode
        if academic_mode:
            self.txt_fest.insert(tk.END, "=== MODO PESQUISA ACADÊmica ===\n")
            self.txt_fest.insert(tk.END, f"Efeméride: {self.current_ephemeris_name}\n")
            self.txt_fest.insert(tk.END, f"Precisão: Máxima disponível\n")
            self.txt_fest.insert(tk.END, f"Ano: {year}\n\n")
        
        self.txt_fest.insert(tk.END, f"Nissan (início): {self.nissan_start.isoformat()}\n")
        self.txt_fest.insert(tk.END, f"Ano embolisímico: {'Sim' if embol else 'Não'} ({13 if embol else 12} meses)\n")
        self.txt_fest.insert(tk.END, f"Efeméride: {self.current_ephemeris_name}\n\n")
        self.txt_fest.insert(tk.END, "Festas e eventos:\n")
        for ev in fest_list:
            self.txt_fest.insert(tk.END, f" - {ev['name']}: {ev['date'].isoformat()}\n")

        # seasons (astronomical instants in UTC)
        self.seasons = compute_seasons_for_year(year)
        self.txt_seasons_jer.delete("1.0", tk.END)
        self.txt_seasons_sp.delete("1.0", tk.END)
        for s in self.seasons:
            self.txt_seasons_jer.insert(tk.END, f"{s['event']}: {s['utc'].isoformat()} UTC\n")
            self.txt_seasons_sp.insert(tk.END, f"{s['event']}: {s['utc'].isoformat()} UTC\n")
        
        # moon phases for the year
        self.moon_phases = self._get_moon_phases_for_year(year)

        # sample sunrise/sunset for Nissan 1
        try:
            sun_jer = sunrise_sunset(JERUSALEM, self.nissan_start)
            sun_sp = sunrise_sunset(SAOPAULO, self.nissan_start)
            self.txt_sun.delete("1.0", tk.END)
            self.txt_sun.insert(tk.END, f"Nissan 1 = {self.nissan_start.isoformat()}\n")
            self.txt_sun.insert(tk.END, f" - Jerusalém sunrise: {sun_jer['sunrise']}, sunset: {sun_jer['sunset']}\n")
            self.txt_sun.insert(tk.END, f" - São Paulo   sunrise: {sun_sp['sunrise']}, sunset: {sun_sp['sunset']}\n")
        except Exception:
            pass

        # find and render current month
        self._set_current_month()
        self.render_visual_month()

    def render_visual_month(self) -> None:
        """Renderiza o mês atual no calendário visual."""
        for w in self.grid_container.winfo_children():
            w.destroy()
        if self.months_df is None or len(self.months_df) == 0:
            ttk.Label(self.grid_container, text="Gere o calendário primeiro.").pack()
            return
        row = self.months_df.iloc[self.visual_index]
        idx = int(row["index"]); name = row["name"]; start = row["start"]; days = int(row["days"])
        
        # Update main title
        self.lbl_visual.config(text=f"Mês {idx} - {name} (start {start}, {days} dias)")
        
        # Update year comparisons
        gregorian_year = start.year
        ussher_year = calculate_ussher_year(gregorian_year)
        hebrew_year = calculate_hebrew_year(gregorian_year)
        
        year_text = f"Ussher: {ussher_year} AM | Hebraico: {hebrew_year} | Gregoriano: {gregorian_year}"
        self.lbl_years.config(text=year_text)

        days_week = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
        for c, dname in enumerate(days_week):
            lbl = ttk.Label(self.grid_container, text=dname, borderwidth=1, relief="solid", width=14)
            lbl.grid(row=0, column=c, sticky="nsew")

        py_wd = start.weekday()  # Mon=0..Sun=6
        start_col = (py_wd + 1) % 7

        combined = FESTIVALS_DEF.copy()
        combined.update(YESHUA_EVENTS_DEF)

        today = datetime.now().date()
        r = 1; c = start_col
        for d in range(1, days+1):
            cur = start + timedelta(days=d-1)
            greg_date = cur.strftime("%d/%m")
            text = f"{d}\n({greg_date})"
            # annotate festivals
            for fname, (midx, fday) in combined.items():
                if midx == idx and fday == d:
                    text += "\n★ " + fname
            if d == 1:
                text += "\n🌑"
            
            # annotate seasons
            for season in getattr(self, 'seasons', []):
                season_date = season['utc'].date()
                if season_date == cur:
                    text += "\n🌍"
            
            # annotate moon phases
            for phase in getattr(self, 'moon_phases', []):
                if phase['date'] == cur and phase['phase'] != 0:  # Skip new moon (already shown)
                    text += f"\n{phase['icon']}"
            
            # highlight today
            bg_color = "lightblue" if cur == today else "white"
            
            lbl = tk.Label(self.grid_container, text=text, borderwidth=1, relief="solid", width=14, height=4, anchor="n", justify="left", padx=4, pady=3, bg=bg_color, cursor="hand2", wraplength=100)
            lbl.bind("<Button-1>", lambda e, day=d, date=cur: self.on_day_click(day, date))
            lbl.grid(row=r, column=c, sticky="nsew", padx=1, pady=1)
            c += 1
            if c > 6:
                c = 0; r += 1

    def visual_next(self) -> None:
        """Navega para o próximo mês no calendário visual."""
        if self.months_df is None: return
        if self.visual_index < len(self.months_df) - 1:
            self.visual_index += 1
            self.render_visual_month()
        else:
            # Advance to next year
            current_year = int(self.year_var.get())
            if current_year < 2100:
                self.year_var.set(str(current_year + 1))
                self.generate_all()

    def visual_prev(self) -> None:
        """Navega para o mês anterior no calendário visual."""
        if self.months_df is None: return
        if self.visual_index > 0:
            self.visual_index -= 1
            self.render_visual_month()
        else:
            # Go back to previous year
            current_year = int(self.year_var.get())
            if current_year > 1:
                self.year_var.set(str(current_year - 1))
                self.generate_all()
                # Go to last month of previous year
                if self.months_df is not None:
                    self.visual_index = len(self.months_df) - 1
                    self.render_visual_month()

    def visual_today(self) -> None:
        """Navega para o mês que contém a data atual."""
        if self.months_df is None: return
        today = datetime.now().date()
        for i, (_, row) in enumerate(self.months_df.iterrows()):
            start_date = row["start"]
            end_date = row["end"]
            if start_date <= today <= end_date:
                self.visual_index = i
                self.render_visual_month()
                return
    
    def _get_moon_phases_for_year(self, year: int) -> list[dict]:
        """Obtém todas as fases da lua para um ano."""
        t0 = TS.utc(year, 1, 1)
        t1 = TS.utc(year, 12, 31)
        f = almanac.moon_phases(Eph)
        times, phases = almanac.find_discrete(t0, t1, f)
        phase_names = {0: "🌑", 1: "🌓", 2: "🌕", 3: "🌗"}
        phase_labels = {0: "Nova", 1: "Crescente", 2: "Cheia", 3: "Minguante"}
        out = []
        for ti, ph in zip(times, phases):
            out.append({
                "date": ti.utc_datetime().date(),
                "phase": ph,
                "icon": phase_names[ph],
                "name": phase_labels[ph]
            })
        return out
    
    def _set_current_month(self) -> None:
        """Define o índice para o mês que contém a data atual."""
        if self.months_df is None: 
            self.visual_index = 0
            return
        today = datetime.now().date()
        for i, (_, row) in enumerate(self.months_df.iterrows()):
            start_date = row["start"]
            end_date = row["end"]
            if start_date <= today <= end_date:
                self.visual_index = i
                return
        self.visual_index = 0
    
    def _get_current_season(self, target_date: date) -> dict:
        """Obtém a estação astronômica atual para ambas as localidades."""
        year = target_date.year
        seasons = getattr(self, 'seasons', [])
        
        # Find the current season based on the target date
        current_season = None
        for i, season in enumerate(seasons):
            season_date = season['utc'].date()
            if i < len(seasons) - 1:
                next_season_date = seasons[i + 1]['utc'].date()
                if season_date <= target_date < next_season_date:
                    current_season = season['event']
                    break
            else:
                # Last season of the year, check if date is after it
                if season_date <= target_date:
                    current_season = season['event']
                    break
        
        # If no season found, it might be before March equinox (winter from previous year)
        if not current_season and seasons:
            current_season = "December Solstice"  # Winter in Northern Hemisphere
        
        if current_season:
            season_map = {
                "March Equinox": {"jerusalem": "Primavera", "sao_paulo": "Outono"},
                "June Solstice": {"jerusalem": "Verão", "sao_paulo": "Inverno"},
                "September Equinox": {"jerusalem": "Outono", "sao_paulo": "Primavera"},
                "December Solstice": {"jerusalem": "Inverno", "sao_paulo": "Verão"}
            }
            return season_map.get(current_season, {"jerusalem": "N/A", "sao_paulo": "N/A"})
        
        return None

    def on_day_click(self, day: int, date: datetime.date) -> None:
        """Manipula clique em um dia do calendário."""
        if self.months_df is None: return
        
        row = self.months_df.iloc[self.visual_index]
        idx = int(row["index"])
        
        combined = FESTIVALS_DEF.copy()
        combined.update(YESHUA_EVENTS_DEF)
        
        events = []
        
        # Check for festivals
        for fname, (midx, fday) in combined.items():
            if midx == idx and fday == day:
                portuguese_name = FESTIVAL_TRANSLATIONS.get(fname, fname)
                events.append(f"★ {fname} ({portuguese_name})")
                # Store the original Hebrew name for description lookup
                events.append(("hebrew_name", fname))
        
        # Check for new moon
        if day == 1:
            events.append("🌑 Lua Nova")
        
        # Check for astronomical seasons
        for season in getattr(self, 'seasons', []):
            season_date = season['utc'].date()
            if season_date == date:
                events.append(f"🌍 {season['event']}")
        
        # Check for moon phases (skip new moon if day 1)
        for phase in getattr(self, 'moon_phases', []):
            if phase['date'] == date and not (phase['phase'] == 0 and day == 1):
                events.append(f"{phase['icon']} Lua {phase['name']}")
        
        # Check if today
        today = datetime.now().date()
        if date == today:
            events.append("📅 Hoje")
        
        # Update events display with descriptions
        self.day_events.delete("1.0", tk.END)
        self.day_events.insert(tk.END, f"Dia {day} ({date.strftime('%d/%m/%Y')})\n\n")
        
        # Add current astronomical season for both locations
        season_info = self._get_current_season(date)
        if season_info:
            self.day_events.insert(tk.END, f"🌍 Estação Astronômica:\n", "bold")
            self.day_events.insert(tk.END, f"   Jerusalém: {season_info['jerusalem']}\n")
            self.day_events.insert(tk.END, f"   São Paulo: {season_info['sao_paulo']}\n\n")
        
        # Add year comparisons
        gregorian_year = date.year
        ussher_year = calculate_ussher_year(gregorian_year)
        hebrew_year = calculate_hebrew_year(gregorian_year)
        
        self.day_events.insert(tk.END, f"📅 Cronologias do Ano:\n", "bold")
        self.day_events.insert(tk.END, f"   Ussher: {ussher_year} AM (desde Criação)\n")
        self.day_events.insert(tk.END, f"   Hebraico: {hebrew_year} AM (Anno Mundi)\n")
        self.day_events.insert(tk.END, f"   Gregoriano: {gregorian_year} DC (Era Cristã)\n\n")
        
        # Process events and their Hebrew names
        hebrew_names = {}
        display_events = []
        
        for item in events:
            if isinstance(item, tuple) and item[0] == "hebrew_name":
                # This is a Hebrew name storage, get the last display event
                if display_events:
                    hebrew_names[display_events[-1]] = item[1]
            else:
                display_events.append(item)
        
        if display_events:
            for event in display_events:
                # Insert event name in bold
                self.day_events.insert(tk.END, f"{event}\n", "bold")
                
                # Add description for festivals and other events in normal text
                if "★" in event:
                    # Get the stored Hebrew name for this event
                    hebrew_name = hebrew_names.get(event, "")
                    
                    # If no stored name, try to extract from event text
                    if not hebrew_name:
                        event_clean = event.replace("★ ", "")
                        if " (" in event_clean:
                            hebrew_name = event_clean.split(" (")[0]
                        else:
                            hebrew_name = event_clean
                    
                    description = FESTIVAL_DESCRIPTIONS.get(hebrew_name, "")
                    if description:
                        self.day_events.insert(tk.END, f"   {description}\n")
                elif "Lua" in event:
                    # Add descriptions for moon phases
                    if "Nova" in event:
                        description = FESTIVAL_DESCRIPTIONS.get("Lua Nova", "")
                    elif "Cheia" in event:
                        description = FESTIVAL_DESCRIPTIONS.get("Lua Cheia", "")
                    elif "Crescente" in event:
                        description = FESTIVAL_DESCRIPTIONS.get("Quarto Crescente", "")
                    elif "Minguante" in event:
                        description = FESTIVAL_DESCRIPTIONS.get("Quarto Minguante", "")
                    else:
                        description = ""
                    if description:
                        self.day_events.insert(tk.END, f"   {description}\n")
                elif "🌍" in event:
                    # Add descriptions for astronomical seasons
                    if "March Equinox" in event:
                        description = FESTIVAL_DESCRIPTIONS.get("Equinócio de Primavera", "")
                    elif "June Solstice" in event:
                        description = FESTIVAL_DESCRIPTIONS.get("Solstício de Verão", "")
                    elif "September Equinox" in event:
                        description = FESTIVAL_DESCRIPTIONS.get("Equinócio de Outono", "")
                    elif "December Solstice" in event:
                        description = FESTIVAL_DESCRIPTIONS.get("Solstício de Inverno", "")
                    else:
                        description = ""
                    if description:
                        self.day_events.insert(tk.END, f"   {description}\n")
                self.day_events.insert(tk.END, "\n")
        else:
            self.day_events.insert(tk.END, "Nenhum evento especial.")

    def on_export_csv(self) -> None:
        """Exporta os meses para arquivo CSV."""
        if self.months_df is None:
            messagebox.showwarning("Export", "Gere o calendário antes de exportar.")
            return
        fn = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")])
        if not fn: return
        try:
            # Add metadata for academic mode
            export_df = self.months_df.copy()
            if bool(self.academic_mode_var.get()):
                # Add precision metadata
                export_df.attrs['ephemeris'] = self.current_ephemeris_name
                export_df.attrs['academic_mode'] = True
                export_df.attrs['precision'] = 'maximum'
            
            export_df.to_csv(fn, index=False)
            messagebox.showinfo("Exportado", f"CSV salvo em {fn}\nEfeméride: {self.current_ephemeris_name}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar CSV: {e}")

    def on_export_ics(self) -> None:
        """Exporta os festivais para arquivo ICS."""
        if self.months_df is None:
            messagebox.showwarning("Export", "Gere o calendário antes de exportar.")
            return
        combined = FESTIVALS_DEF.copy(); combined.update(YESHUA_EVENTS_DEF)
        fest_list = map_festivals_to_dates(self.months_df, combined)
        events = []
        
        # Enhanced description for academic mode
        base_desc = "Calendário bíblico lunissolar"
        if bool(self.academic_mode_var.get()):
            base_desc += f" - {self.current_ephemeris_name} (Modo Acadêmico)"
        else:
            base_desc += f" - {self.current_ephemeris_name}"
        
        for ev in fest_list:
            events.append({"name": ev["name"], "date": ev["date"], "description": base_desc})
        
        fn = filedialog.asksaveasfilename(defaultextension=".ics", filetypes=[("iCalendar","*.ics")])
        if not fn: return
        try:
            export_events_to_ics(events, fn)
            messagebox.showinfo("Exportado", f"ICS salvo em {fn}\nEfeméride: {self.current_ephemeris_name}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao criar ICS: {e}")

# ---------------- Run ----------------

def main() -> None:
    """Função principal para execução da aplicação."""
    app = BiblicalCalendarApp()
    app.mainloop()

if __name__ == "__main__":
    main()