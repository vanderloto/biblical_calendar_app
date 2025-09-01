"""Testes para o módulo calendar.

Este módulo contém testes unitários para as principais funcionalidades
do calendário bíblico lunissolar.

Autor:
    Vander Loto - DATAMETRIA
"""

import pytest
from datetime import date
import pandas as pd

from biblical_calendar.calendar import (
    get_march_equinox,
    generate_biblical_months_dynamic,
    map_festivals_to_dates,
    FESTIVALS_DEF,
    MONTH_NAMES
)


class TestCalendarFunctions:
    """Testes para funções do calendário."""
    
    def test_get_march_equinox_2024(self):
        """Testa cálculo do equinócio de março para 2024."""
        equinox = get_march_equinox(2024)
        
        assert isinstance(equinox, date)
        assert equinox.month == 3
        assert 19 <= equinox.day <= 21  # Equinócio sempre entre 19-21 de março
    
    def test_generate_biblical_months_basic(self):
        """Testa geração básica de meses bíblicos."""
        df, embolismic, nissan_start = generate_biblical_months_dynamic(2024)
        
        # Verificar tipos de retorno
        assert isinstance(df, pd.DataFrame)
        assert isinstance(embolismic, bool)
        assert isinstance(nissan_start, date)
        
        # Verificar estrutura do DataFrame
        expected_columns = ["index", "name", "start", "end", "days"]
        assert list(df.columns) == expected_columns
        
        # Verificar número de meses (12 ou 13)
        assert len(df) in [12, 13]
        
        # Verificar se primeiro mês é Nissan
        assert df.iloc[0]["name"] == "Nissan"
        assert df.iloc[0]["index"] == 1
    
    def test_generate_biblical_months_embolismic_detection(self):
        """Testa detecção de anos embolísmicos."""
        # Testar alguns anos conhecidos
        for year in [2024, 2025, 2026]:
            df, embolismic, _ = generate_biblical_months_dynamic(year)
            
            if embolismic:
                assert len(df) == 13
                # Verificar presença de Adar I e Adar II
                names = df["name"].tolist()
                assert "Adar I" in names
                assert "Adar II" in names
            else:
                assert len(df) == 12
                # Verificar apenas Adar normal
                names = df["name"].tolist()
                assert "Adar" in names
                assert "Adar I" not in names
                assert "Adar II" not in names
    
    def test_map_festivals_to_dates(self):
        """Testa mapeamento de festivais para datas."""
        df, _, _ = generate_biblical_months_dynamic(2024)
        festivals = map_festivals_to_dates(df, FESTIVALS_DEF)
        
        # Verificar estrutura dos festivais
        assert isinstance(festivals, list)
        assert len(festivals) == len(FESTIVALS_DEF)
        
        for festival in festivals:
            assert "name" in festival
            assert "date" in festival
            assert isinstance(festival["date"], date)
        
        # Verificar se todos os festivais foram mapeados
        festival_names = [f["name"] for f in festivals]
        for expected_name in FESTIVALS_DEF.keys():
            assert expected_name in festival_names
    
    def test_month_names_consistency(self):
        """Testa consistência dos nomes dos meses."""
        df, embolismic, _ = generate_biblical_months_dynamic(2024)
        
        if not embolismic:
            # Ano normal: deve ter exatamente os 12 meses padrão
            expected_names = MONTH_NAMES
            actual_names = df["name"].tolist()
            assert actual_names == expected_names
        else:
            # Ano embolísmico: deve ter Adar I e Adar II
            actual_names = df["name"].tolist()
            assert len(actual_names) == 13
            assert "Adar I" in actual_names
            assert "Adar II" in actual_names
    
    def test_month_dates_consistency(self):
        """Testa consistência das datas dos meses."""
        df, _, _ = generate_biblical_months_dynamic(2024)
        
        for i in range(len(df) - 1):
            current_month = df.iloc[i]
            next_month = df.iloc[i + 1]
            
            # Fim do mês atual deve ser um dia antes do início do próximo
            expected_next_start = current_month["end"] + pd.Timedelta(days=1)
            assert next_month["start"] == expected_next_start.date()
            
            # Número de dias deve ser consistente
            calculated_days = (current_month["end"] - current_month["start"]).days + 1
            assert current_month["days"] == calculated_days


class TestCalendarEdgeCases:
    """Testes para casos extremos e edge cases."""
    
    def test_year_boundaries(self):
        """Testa anos nos limites (muito antigos/futuros)."""
        # Testar anos extremos (dentro do razoável para efemérides)
        for year in [1900, 2100]:
            df, embolismic, nissan_start = generate_biblical_months_dynamic(year)
            
            assert isinstance(df, pd.DataFrame)
            assert len(df) in [12, 13]
            assert isinstance(nissan_start, date)
    
    def test_visibility_heuristic_option(self):
        """Testa opção de heurística de visibilidade."""
        year = 2024
        
        # Sem heurística
        df1, _, nissan1 = generate_biblical_months_dynamic(year, use_visibility_heuristic=False)
        
        # Com heurística
        df2, _, nissan2 = generate_biblical_months_dynamic(year, use_visibility_heuristic=True)
        
        # Ambos devem retornar DataFrames válidos
        assert isinstance(df1, pd.DataFrame)
        assert isinstance(df2, pd.DataFrame)
        
        # Podem ter datas de início diferentes (heurística pode ajustar)
        # Mas estrutura deve ser similar
        assert len(df1) == len(df2)  # Mesmo número de meses


if __name__ == "__main__":
    pytest.main([__file__])