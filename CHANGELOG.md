# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [2.0.0] - 2025-09-01

### Added
- **Versão Web Completa**: Interface web moderna com Vue.js 3 + Flask API
- **Deploy Cloud**: Configuração para Render.com, Heroku, Vercel com Docker
- **Navegação Automática de Anos**: Transição automática entre anos (1-2100)
- **Estações Dinâmicas**: Atualização automática conforme mês/dia selecionado
- **Cronologias Organizadas**: Ussher, Hebraico e Gregoriano com descrições
- **Painel de Eventos Expandido**: 450px com descrições completas
- **Interface Ampliada**: 1400x900px para melhor visualização
- **Rótulos Formatados**: "Inicia em:", "Cronologias do Ano:", "Estação Astronômica:" em negrito
- **Indentação Visual**: Hierarquia clara nas cronologias
- **Seleção Automática**: Carrega no mês atual com dia atual selecionado

### Changed
- **Interface Desktop**: Aprimorada com melhor organização visual
- **Navegação**: Botão "Hoje" volta para ano atual quando necessário
- **Estações**: Jerusalém e São Paulo em linha única separados por "|"
- **Formatação**: Cronologias com descrições explicativas
- **Stack Tecnológica**: Adicionado Vue.js 3, Flask API, Docker

### Fixed
- **Fuso Horário**: Sincronização perfeita entre versões web e desktop
- **Navegação de Anos**: Transição automática no primeiro/último mês
- **Botão Hoje**: Funciona corretamente em qualquer ano
- **Datas Consistentes**: Web e desktop mostram mesmas datas

### Technical
- **Backend API**: Flask REST endpoints para calendário, festivais e estações
- **Frontend Web**: Vue.js 3 Composition API com Pinia state management
- **DevOps**: Docker multi-stage build com Nginx reverse proxy
- **UTC Management**: Correção completa de problemas de fuso horário

## [1.3.0] - 2025-08-20

### Added
- Suporte inicial ao Oracle Database
- Painel de monitoramento de conexões
- Fallback de CDN em redes restritas
- Validação de entrada implementada

### Changed
- Atualizado Vue Material para v3.0.1
- Melhorada gestão de sessões SQLAlchemy
- Otimizada performance de queries

### Fixed
- Falha no fallback de CDN
- Vazamento de sessões SQLAlchemy
- Problemas de conectividade em redes corporativas

## [1.2.0] - 2025-07-15

### Added
- Modo Pesquisa Acadêmica com DE440
- Seleção automática de efemérides por ano
- Cronologias comparativas (Ussher, Hebraico, Gregoriano)
- Exportação ICS para integração com calendários

### Changed
- Interface expandida para 1400x900px
- Painel de eventos ampliado para 450px
- Melhorada navegação entre meses

### Fixed
- Cálculos de anos embolísmicos
- Precisão de datas de festivais
- Performance em anos extremos

## [1.1.0] - 2025-06-10

### Added
- Heurística de visibilidade da primeira crescente
- Festivais bíblicos completos (10 festivais)
- Eventos de Yeshua com múltiplas hipóteses
- Estações astronômicas para Jerusalém e São Paulo

### Changed
- Interface visual aprimorada
- Navegação contínua entre meses
- Descrições educativas expandidas

### Fixed
- Cálculos de fases lunares
- Precisão de equinócios e solstícios
- Formatação de datas

## [1.0.0] - 2025-05-01

### Added
- Calendário bíblico-lunissolar dinâmico
- Cálculos astronômicos com Skyfield
- Interface Tkinter nativa
- Exportação CSV de meses
- Suporte a efemérides DE421
- Detecção automática de anos embolísmicos
- 10 festivais bíblicos principais
- Fases lunares completas
- Documentação completa

### Technical
- Python 3.11+ como runtime
- Poetry para gerenciamento de dependências
- Skyfield 1.45+ para astronomia
- Pandas para manipulação de dados
- iCalendar para exportação ICS

---

## Tipos de Mudanças

- `Added` para novas funcionalidades
- `Changed` para mudanças em funcionalidades existentes
- `Deprecated` para funcionalidades que serão removidas
- `Removed` para funcionalidades removidas
- `Fixed` para correções de bugs
- `Security` para correções de vulnerabilidades
- `Technical` para mudanças técnicas internas

## Links de Comparação

- [2.0.0]: https://github.com/vanderloto/biblical_calendar_app/compare/v1.3.0...v2.0.0
- [1.3.0]: https://github.com/vanderloto/biblical_calendar_app/compare/v1.2.0...v1.3.0
- [1.2.0]: https://github.com/vanderloto/biblical_calendar_app/compare/v1.1.0...v1.2.0
- [1.1.0]: https://github.com/vanderloto/biblical_calendar_app/compare/v1.0.0...v1.1.0
- [1.0.0]: https://github.com/vanderloto/biblical_calendar_app/releases/tag/v1.0.0