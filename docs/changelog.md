# Changelog - Biblical Calendar App

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [1.1.0] - 2025-08-31

### ✨ Adicionado
- **Seleção Automática de Efemérides**: Sistema inteligente que escolhe DE421 (1900-2050) ou DE440 (>2050) automaticamente
- **Modo Pesquisa Acadêmica**: Checkbox para forçar uso de DE440 com máxima precisão científica
- **Status de Efeméride**: Indicador visual mostrando qual efeméride está sendo usada
- **Metadados de Precisão**: Exports CSV/ICS incluem informações sobre efeméride utilizada
- **Fallbacks Robustos**: Sistema de fallback DE430 se DE440 não disponível
- **Avisos Informativos**: Notificação sobre download de 128MB no modo acadêmico
- **Cronologias Comparativas**: Exibição de três sistemas cronológicos (Ussher, Hebraico, Gregoriano)
- **Product Backlog**: Roadmap completo com funcionalidades futuras planejadas
- **Documentação Técnica**: Guia completo sobre gerenciamento de efemérides

### 🔧 Melhorado
- **Interface Reorganizada**: Layout em duas linhas para melhor organização
- **Exports Aprimorados**: Informações técnicas adicionais nos arquivos exportados
- **Tratamento de Erros**: Mensagens mais claras para falhas de download
- **Documentação**: Atualização completa com novas funcionalidades

### 🐛 Corrigido
- **Carregamento de Efemérides**: Inicialização mais robusta com fallbacks
- **Compatibilidade**: Suporte melhorado para anos extremos (>2050)

---

## [1.0.0] - 2025-08-30

### ✨ Adicionado
- **Calendário Visual Interativo**: Navegação mensal com clique em dias
- **10 Festivais Bíblicos**: Pessach, Chag HaMatzot, Omer Reshit, Shavuot, Rosh Hashaná, Yom Kippur, Sukkot, Chanucá, Purim
- **Eventos de Yeshua**: Nascimento (2 hipóteses) e crucificação
- **Navegação Contínua**: Botões Anterior/Próximo com transição automática de anos (1-2100)
- **Botão "Hoje"**: Navegação rápida para o mês atual
- **Painel de Eventos**: Detalhes expandidos ao clicar em qualquer dia
- **Nomes Bilíngues**: Hebraico e português para festivais
- **Descrições Educativas**: Contexto histórico e religioso para todos os eventos
- **Estação Atual**: Mostra estação astronômica para Jerusalém e São Paulo
- **Fases Lunares Completas**: Nova, Crescente, Cheia, Minguante
- **Exportação CSV**: Dados tabulares dos meses
- **Exportação ICS**: Integração com Google Calendar, Outlook, etc.
- **Heurística de Visibilidade**: Primeira crescente visível em Jerusalém
- **Cálculos Astronômicos**: Baseado em Skyfield com efemérides DE421
- **Anos Embolísmicos**: Detecção automática de anos com 13 meses
- **Interface Multilíngue**: Suporte completo a português

### 🔧 Funcionalidades Técnicas
- **Skyfield Integration**: Cálculos precisos com efemérides NASA/JPL
- **Astral Library**: Cálculos de nascer/pôr do sol
- **Pandas DataFrames**: Manipulação eficiente de dados
- **iCalendar Support**: Padrão RFC 5545 para exports
- **Tkinter GUI**: Interface nativa multiplataforma

---

## Tipos de Mudanças

- **✨ Adicionado** para novas funcionalidades
- **🔧 Melhorado** para mudanças em funcionalidades existentes
- **🐛 Corrigido** para correções de bugs
- **❌ Removido** para funcionalidades removidas
- **🔒 Segurança** para vulnerabilidades corrigidas
- **⚡ Performance** para melhorias de performance
- **📚 Documentação** para mudanças na documentação

---

## Links de Comparação

- [1.1.0 vs 1.0.0](https://github.com/vanderloto/biblical_calendar_app/compare/v1.0.0...v1.1.0)
- [Unreleased](https://github.com/vanderloto/biblical_calendar_app/compare/v1.1.0...HEAD)

---

**Mantido por**: Vander Loto - DATAMETRIA  
**Última atualização**: 31/08/2025