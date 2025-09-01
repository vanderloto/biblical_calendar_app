# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.2.0] - 2025-01-03

### ✨ Adicionado
- **Interface Expandida**: Janela aumentada para 1400x900px para melhor experiência visual
- **Painel de Eventos Ampliado**: Área "Eventos do Dia" expandida (450px largura, 20 linhas altura)
- **Descrições Completas dos Eventos de Yeshua**: Contexto histórico e teológico detalhado
- **Correção de Bug**: Descrições dos eventos de Yeshua agora aparecem corretamente no painel

### 🔧 Melhorado
- **Legibilidade**: Mais espaço para exibição de descrições educativas
- **Experiência do Usuário**: Interface mais confortável e menos comprimida
- **Proporções Visuais**: Melhor equilíbrio entre calendário e painel informativo

### 🐛 Corrigido
- **Bug de Descrições**: Eventos de Yeshua não exibiam descrições ao clicar nos dias
- **Lookup de Eventos**: Melhoria na associação entre nomes hebraicos e descrições

## [1.1.0] - 2025-01-02

### ✨ Adicionado
- **Calendário Visual Interativo**: Navegação mensal com clique em dias
- **Painel "Eventos do Dia"**: Detalhes expandidos com descrições educativas
- **Navegação Contínua**: Botões Anterior/Próximo com transição automática de anos (1-2100)
- **Botão "Hoje"**: Navegação rápida para o mês atual
- **Cronologias Comparativas**: Ussher (Criação), Hebraico (AM) e Gregoriano (DC)
- **Festivais Bíblicos Completos**: 10 festivais com nomes hebraicos e traduções
- **Eventos de Yeshua**: Nascimento (2 hipóteses) e crucificação com contexto
- **Fases Lunares Completas**: Nova, Crescente, Cheia, Minguante
- **Estações Astronômicas**: Para Jerusalém e São Paulo
- **Gerenciamento Inteligente de Efemérides**: Seleção automática DE421/DE440
- **Modo Pesquisa Acadêmica**: Força DE440 para máxima precisão
- **Exportação ICS**: Integração com Google Calendar, Outlook
- **Legenda Visual**: Símbolos para fases lunares, festivais e estações

### 🔧 Melhorado
- **Estrutura do Projeto**: Reorganização seguindo padrões DATAMETRIA
- **Documentação**: Estrutura completa com guias técnicos e de usuário
- **Qualidade de Código**: Type hints, docstrings Google Style, testes

### 🐛 Corrigido
- **Duplicação de Eventos**: Lua Nova não aparece mais duplicada
- **Nomes de Festivais**: Correções em hebraico (Chag HaMatzot, Omer Reshit)

## [1.0.0] - 2025-01-01

### ✨ Adicionado
- **Calendário Bíblico Dinâmico**: Meses baseados em luas novas astronômicas
- **Heurística de Visibilidade**: Primeira crescente visível em Jerusalém
- **Detecção Automática**: Anos embolísmicos (13 meses) com Adar I/II
- **Cálculos Astronômicos**: Skyfield com efemérides DE421
- **Interface Tkinter**: GUI nativa multiplataforma
- **Exportação CSV**: Dados tabulares para análise
- **Festivais Básicos**: Principais festas bíblicas
- **Estações**: Equinócios e solstícios

### 🏗️ Arquitetura
- **Python 3.11+**: Runtime moderno
- **Poetry**: Gerenciamento de dependências
- **Skyfield**: Cálculos astronômicos precisos
- **Pandas**: Manipulação de dados
- **Astral**: Cálculos solares

---

## Tipos de Mudanças

- `✨ Adicionado` para novas funcionalidades
- `🔧 Melhorado` para mudanças em funcionalidades existentes
- `🐛 Corrigido` para correção de bugs
- `🗑️ Removido` para funcionalidades removidas
- `🔒 Segurança` para vulnerabilidades corrigidas
- `📚 Documentação` para mudanças na documentação
- `🏗️ Arquitetura` para mudanças estruturais

---

**Mantido por**: Vander Loto - DATAMETRIA  
**Próxima versão planejada**: 1.3.0 (Web Version MVP)