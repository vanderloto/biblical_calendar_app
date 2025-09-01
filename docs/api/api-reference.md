# API Reference - Biblical Calendar App

## Módulo Principal: biblical_calendar.calendar

### Funções Principais

#### `generate_biblical_months_dynamic(reference_year: int, use_visibility_heuristic: bool = False)`

Gera meses bíblicos dinâmicos para um ano.

**Parâmetros:**
- `reference_year` (int): Ano de referência
- `use_visibility_heuristic` (bool): Se deve usar heurística de visibilidade

**Retorna:**
- `tuple[pd.DataFrame, bool, date]`: DataFrame dos meses, se é embolísmico, data início Nissan

#### `map_festivals_to_dates(months_df: pd.DataFrame, festivals_dict: dict)`

Mapeia festivais para datas específicas.

**Parâmetros:**
- `months_df` (pd.DataFrame): DataFrame com os meses
- `festivals_dict` (dict): Dicionário de festivais {nome: (mês, dia)}

**Retorna:**
- `list[dict]`: Lista de eventos com nome e data

#### `export_events_to_ics(event_list: list[dict], filename: str)`

Exporta lista de eventos para arquivo ICS.

**Parâmetros:**
- `event_list` (list[dict]): Lista de eventos com name, date, description
- `filename` (str): Caminho do arquivo ICS a ser criado

### Constantes

#### `FESTIVALS_DEF`
Dicionário com definições dos festivais bíblicos.

#### `YESHUA_EVENTS_DEF`
Dicionário com eventos relacionados a Yeshua.

#### `MONTH_NAMES`
Lista com nomes dos meses hebraicos.

### Classe Principal

#### `BiblicalCalendarApp(tk.Tk)`

Aplicação GUI principal para o calendário bíblico.

**Métodos Principais:**
- `generate_all()`: Gera todos os dados do calendário
- `render_visual_month()`: Renderiza o mês atual no calendário visual
- `on_day_click(day: int, date: date)`: Manipula clique em um dia do calendário