"""Biblical Calendar Web API - Flask Backend.

API REST para o calendário bíblico lunissolar com endpoints
para cálculos astronômicos, festivais e exportações.

Autor:
    Vander Loto - DATAMETRIA

Versão:
    1.0.0
"""

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from datetime import datetime, date
import sys
import os
import tempfile
import io

# Add src to path for imports
src_path = os.path.join(os.path.dirname(__file__), '..', '..', 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from biblical_calendar.calendar_core import (
    BiblicalCalendarCore,
    generate_biblical_months_dynamic,
    map_festivals_to_dates,
    export_events_to_ics,
    compute_seasons_for_year,
    load_optimal_ephemeris,
    FESTIVALS_DEF,
    YESHUA_EVENTS_DEF,
    FESTIVAL_TRANSLATIONS,
    FESTIVAL_DESCRIPTIONS,
    CURRENT_EPHEMERIS
)

def get_current_season_for_date(target_date, seasons):
    """Obtém a estação astronômica atual para ambas as localidades."""
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

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/calendar/<int:year>', methods=['GET'])
def get_calendar(year):
    """Get biblical calendar for a specific year."""
    try:
        use_visibility = request.args.get('visibility', 'false').lower() == 'true'
        academic_mode = request.args.get('academic', 'false').lower() == 'true'
        
        # Load optimal ephemeris
        eph, eph_name = load_optimal_ephemeris(year, force_academic=academic_mode)
        
        # Generate months
        months_df, embolismic, nissan_start = generate_biblical_months_dynamic(
            year, use_visibility_heuristic=use_visibility
        )
        
        # Convert DataFrame to dict
        months = []
        for _, row in months_df.iterrows():
            months.append({
                'index': int(row['index']),
                'name': row['name'],
                'start': row['start'].isoformat(),
                'end': row['end'].isoformat(),
                'days': int(row['days'])
            })
        
        # Get festivals
        combined = FESTIVALS_DEF.copy()
        combined.update(YESHUA_EVENTS_DEF)
        festivals = map_festivals_to_dates(months_df, combined)
        
        festivals_data = []
        for fest in festivals:
            hebrew_name = fest['name']
            portuguese_name = FESTIVAL_TRANSLATIONS.get(hebrew_name, hebrew_name)
            description = FESTIVAL_DESCRIPTIONS.get(hebrew_name, '')
            
            festivals_data.append({
                'name': hebrew_name,
                'portuguese_name': portuguese_name,
                'date': fest['date'].isoformat(),
                'description': description
            })
        
        # Get seasons
        seasons = compute_seasons_for_year(year)
        seasons_data = []
        for season in seasons:
            seasons_data.append({
                'event': season['event'],
                'utc': season['utc'].isoformat()
            })
        
        # Get current season for today
        current_season = get_current_season_for_date(datetime.now().date(), seasons)
        current_season_data = {
            'jerusalem': current_season['jerusalem'] if current_season else 'N/A',
            'sao_paulo': current_season['sao_paulo'] if current_season else 'N/A'
        }
        
        return jsonify({
            'year': year,
            'ephemeris': eph_name,
            'embolismic': embolismic,
            'nissan_start': nissan_start.isoformat(),
            'months': months,
            'festivals': festivals_data,
            'seasons': seasons_data,
            'current_season': current_season_data,
            'use_visibility': use_visibility,
            'academic_mode': academic_mode
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export/csv/<int:year>', methods=['GET'])
def export_csv(year):
    """Export calendar data as CSV."""
    try:
        use_visibility = request.args.get('visibility', 'false').lower() == 'true'
        academic_mode = request.args.get('academic', 'false').lower() == 'true'
        
        # Generate months
        months_df, _, _ = generate_biblical_months_dynamic(
            year, use_visibility_heuristic=use_visibility
        )
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        months_df.to_csv(temp_file.name, index=False)
        temp_file.close()
        
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=f'biblical_calendar_{year}.csv',
            mimetype='text/csv'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export/ics/<int:year>', methods=['GET'])
def export_ics(year):
    """Export festivals as ICS."""
    try:
        use_visibility = request.args.get('visibility', 'false').lower() == 'true'
        academic_mode = request.args.get('academic', 'false').lower() == 'true'
        
        # Generate months and festivals
        months_df, _, _ = generate_biblical_months_dynamic(
            year, use_visibility_heuristic=use_visibility
        )
        
        combined = FESTIVALS_DEF.copy()
        combined.update(YESHUA_EVENTS_DEF)
        festivals = map_festivals_to_dates(months_df, combined)
        
        events = []
        for fest in festivals:
            events.append({
                'name': fest['name'],
                'date': fest['date'],
                'description': f'Calendário bíblico lunissolar - {CURRENT_EPHEMERIS}'
            })
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='wb', suffix='.ics', delete=False)
        export_events_to_ics(events, temp_file.name)
        
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=f'biblical_festivals_{year}.ics',
            mimetype='text/calendar'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)