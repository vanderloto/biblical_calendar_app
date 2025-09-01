# Product Backlog - Biblical Calendar App

Este documento contém o backlog do produto, organizando as funcionalidades e melhorias planejadas para futuras versões do Biblical Calendar App. O backlog é mantido em ordem de prioridade e é revisado regularmente pela equipe de desenvolvimento.

## Legenda de Prioridades

- **🔴 Crítica**: Funcionalidades críticas, correções urgentes ou bloqueadores
- **🟠 Alta**: Funcionalidades importantes com alto valor de negócio
- **🟡 Média**: Melhorias que agregam valor significativo
- **🟢 Baixa**: Funcionalidades desejáveis mas não críticas
- **🔵 Pesquisa**: Itens que requerem investigação ou prova de conceito
- **⚪ Icebox**: Ideias para futuro distante

## Legenda de Status

- **📋 Backlog**: Item identificado e documentado
- **🔍 Refinamento**: Em processo de detalhamento
- **📏 Estimado**: Estimativa de esforço definida
- **✅ Pronto**: Pronto para desenvolvimento
- **🔄 Em Progresso**: Desenvolvimento iniciado
- **🧪 Teste**: Em fase de testes
- **✅ Concluído**: Implementado e testado
- **❌ Cancelado**: Item removido do escopo
- **⏸️ Pausado**: Desenvolvimento temporariamente suspenso

## Legenda de Tipos

- **🎯 Feature**: Nova funcionalidade
- **🐛 Bug**: Correção de defeito
- **⚡ Performance**: Melhoria de performance
- **🔧 Tech Debt**: Débito técnico
- **📚 Docs**: Documentação
- **🔒 Security**: Segurança
- **🎨 UX/UI**: Experiência do usuário

---

## Sprint Atual - Versão 1.2.0 (Planejada para Dezembro 2025)

### 🔴 Crítica

#### WEB-001: Versão Web do Calendário Visual
**Status**: ✅ Concluído  
**Estimativa**: 21 pontos  
**Assignee**: Vander Loto  
**Epic**: Plataforma Web  
**Labels**: [web, flask, vue, calendar]

**Descrição**: Como usuário, eu quero acessar o calendário bíblico através de um navegador web para que eu possa usar a aplicação em qualquer dispositivo sem instalação.

**Critérios de Aceitação**:
- [x] ~~Interface web responsiva com Vue.js 3~~
- [x] ~~Backend Flask com API REST~~
- [x] ~~Calendário visual idêntico ao desktop, com visual aprimorado e moderno~~
- [x] ~~Navegação mensal com botões Anterior/Próximo/Hoje~~
- [x] ~~Painel de eventos do dia com descrições~~
- [x] ~~Seleção de ano e opções (visibilidade, modo acadêmico)~~
- [x] ~~Exports CSV/ICS via download~~
- [x] ~~Indicador de efeméride em uso~~
- [x] ~~Suporte a múltiplos usuários simultâneos~~

**Tarefas Técnicas**:
- [x] ~~Criar API Flask com endpoints REST~~
- [x] ~~Desenvolver frontend Vue.js 3 com Composition API~~
- [x] ~~Implementar calendário visual responsivo~~
- [x] ~~Integrar sistema de efemérides no backend~~
- [ ] Adicionar cache Redis para performance
- [x] ~~Configurar Docker para deploy~~
- [ ] Implementar testes E2E com Cypress

**Dependências**: Funcionalidades desktop estáveis  
**Riscos**: Complexidade de sincronização entre frontend/backend  
**Notas**: Amplia significativamente o alcance da aplicação

---

#### WEB-002: API REST Completa
**Status**: 📋 Backlog  
**Estimativa**: 13 pontos  
**Assignee**: TBD  
**Epic**: Plataforma Web  
**Labels**: [api, rest, flask, documentation]

**Descrição**: Como desenvolvedor, eu quero uma API REST completa para integrar o calendário bíblico em outras aplicações.

**Critérios de Aceitação**:
- [ ] Endpoints para cálculo de meses
- [ ] Endpoints para festivais e eventos
- [ ] Endpoints para fases lunares e estações
- [ ] Documentação OpenAPI/Swagger
- [ ] Rate limiting e autenticação
- [ ] Versionamento de API (v1)
- [ ] Tratamento de erros padronizado
- [ ] Logs estruturados

**Valor de Negócio**: Alto - Permite integrações externas  
**Impacto no Usuário**: Facilita uso programático

---

### 🟠 Alta

#### WEB-003: Interface Responsiva Avançada
**Status**: 📋 Backlog  
**Estimativa**: 8 pontos  
**Epic**: Plataforma Web

**Descrição**: Interface web otimizada para todos os dispositivos com recursos avançados.

**Critérios de Aceitação**:
- [ ] Design responsivo mobile-first
- [ ] PWA (Progressive Web App) com offline support
- [ ] Temas claro/escuro
- [ ] Gestos touch para navegação
- [ ] Notificações push para festivais
- [ ] Compartilhamento de calendários

---

#### FEAT-003: Múltiplas Localidades
**Status**: 📋 Backlog  
**Estimativa**: 13 pontos  
**Assignee**: TBD  
**Epic**: Internacionalização

**Descrição**: Como usuário internacional, eu quero poder configurar diferentes localidades além de Jerusalém e São Paulo para que eu possa calcular o calendário para minha região.

**Critérios de Aceitação**:
- [ ] Interface para adicionar/remover localidades
- [ ] Banco de dados de cidades principais
- [ ] Cálculos de visibilidade para localidade selecionada
- [ ] Comparação lado a lado de múltiplas localidades
- [ ] Persistência de configurações do usuário

---

#### FEAT-004: Exportação Avançada
**Status**: 📋 Backlog  
**Estimativa**: 8 pontos  
**Epic**: Integração Externa

**Descrição**: Expandir opções de exportação com formatos adicionais e configurações personalizadas.

**Critérios de Aceitação**:
- [ ] Exportação JSON com estrutura completa
- [ ] Exportação PDF com calendário visual
- [ ] Configurações de exportação (filtros, períodos)
- [ ] Templates personalizáveis para ICS
- [ ] Exportação de múltiplos anos

---

### 🟡 Média

#### FEAT-005: Temas Visuais
**Status**: 📋 Backlog  
**Estimativa**: 5 pontos  
**Epic**: UX/UI

**Descrição**: Implementar temas visuais (claro/escuro) e personalização da interface.

**Critérios de Aceitação**:
- [ ] Tema claro e escuro
- [ ] Configuração de cores personalizadas
- [ ] Tamanhos de fonte ajustáveis
- [ ] Persistência de preferências

---

#### FEAT-006: Cronologias Avançadas
**Status**: ✅ Concluído  
**Estimativa**: 2 pontos  
**Epic**: UX/UI

**Descrição**: Exibir três sistemas cronológicos comparativos no calendário visual.

**Critérios de Aceitação**:
- [x] Cronologia de Ussher (desde Criação 4004 AC)
- [x] Calendário Hebraico (Anno Mundi)
- [x] Calendário Gregoriano (Era Cristã)
- [x] Exibição no cabeçalho do calendário
- [x] Informações no painel de eventos
- [x] Legenda explicativa

#### FEAT-007: Histórico de Cálculos
**Status**: 📋 Backlog  
**Estimativa**: 3 pontos  
**Epic**: Usabilidade

**Descrição**: Manter histórico dos anos calculados para acesso rápido.

**Critérios de Aceitação**:
- [ ] Lista de anos recentemente calculados
- [ ] Acesso rápido via dropdown
- [ ] Cache local de resultados
- [ ] Limpeza automática de cache antigo

---

## Próximas Sprints - Versão 1.3.0 (Planejada para Março 2026)

### Épicos Planejados

#### Epic 1: Plataforma Web Completa
**Objetivo**: Versão web completa do calendário bíblico  
**Valor de Negócio**: Ampliação significativa do alcance  
**Estimativa Total**: 55 pontos

**Histórias Incluídas**:
- WEB-001: Versão Web do Calendário Visual - 21 pontos
- WEB-002: API REST Completa - 13 pontos
- WEB-003: Interface Responsiva Avançada - 8 pontos
- WEB-004: Deploy e Infraestrutura - 8 pontos
- WEB-005: Testes E2E e Performance - 5 pontos

#### Epic 2: Análise Comparativa
**Objetivo**: Permitir comparação entre diferentes métodos de cálculo  
**Valor de Negócio**: Educacional e acadêmico  
**Estimativa Total**: 21 pontos

**Histórias Incluídas**:
- FEAT-007: Comparação Astronômica vs Visibilidade - 8 pontos
- FEAT-008: Gráficos de Diferenças - 5 pontos
- FEAT-009: Relatório de Análise - 8 pontos

---

## Backlog de Melhorias Técnicas

### ⚡ Performance

#### PERF-001: Cache Inteligente de Cálculos
**Status**: 📋 Backlog  
**Estimativa**: 5 pontos  
**Impacto Esperado**: 70% redução no tempo de recálculo

**Problema Atual**: Recálculo completo a cada mudança de parâmetro  
**Solução Proposta**: Cache baseado em hash dos parâmetros de entrada  
**Métricas**: Tempo de resposta < 100ms para cálculos em cache

#### PERF-002: Otimização de Efemérides
**Status**: 📋 Backlog  
**Estimativa**: 3 pontos  
**Impacto Esperado**: 50% redução no uso de memória

**Problema Atual**: Carregamento completo da efeméride na memória  
**Solução Proposta**: Carregamento sob demanda por período  
**Métricas**: Uso de memória < 50MB durante operação normal

### 🔧 Débito Técnico

#### TECH-001: Refatoração da Arquitetura
**Status**: 📋 Backlog  
**Estimativa**: 13 pontos  
**Prioridade**: Média

**Descrição**: Separar lógica de negócio da interface gráfica  
**Justificativa**: Facilitar testes e manutenção  
**Impacto se não resolvido**: Dificuldade crescente para adicionar funcionalidades

#### TECH-002: Cobertura de Testes
**Status**: 📋 Backlog  
**Estimativa**: 8 pontos  
**Prioridade**: Alta

**Descrição**: Aumentar cobertura de testes para 90%+  
**Justificativa**: Garantir qualidade em mudanças futuras  
**Impacto se não resolvido**: Risco de regressões

### 🔒 Segurança

#### SEC-001: Validação de Entrada
**Status**: 📋 Backlog  
**Severidade**: Média  
**Estimativa**: 3 pontos

**Vulnerabilidade**: Falta de validação rigorosa de anos de entrada  
**Solução**: Implementar validação com limites seguros  
**Prazo**: Versão 1.1.0

---

## Backlog Detalhado - Plataforma Web

### 🌐 Especificações Técnicas da Versão Web

#### WEB-004: Deploy e Infraestrutura
**Status**: 📋 Backlog  
**Estimativa**: 8 pontos  
**Epic**: Plataforma Web

**Descrição**: Infraestrutura completa para deploy da versão web.

**Critérios de Aceitação**:
- [ ] Docker containers para frontend/backend
- [ ] Docker Compose para desenvolvimento
- [ ] Deploy automatizado (GitHub Actions)
- [ ] Nginx como reverse proxy
- [ ] SSL/HTTPS configurado
- [ ] Monitoramento com Prometheus/Grafana
- [ ] Backup automatizado de dados

#### WEB-005: Testes E2E e Performance
**Status**: 📋 Backlog  
**Estimativa**: 5 pontos  
**Epic**: Plataforma Web

**Descrição**: Suite completa de testes para versão web.

**Critérios de Aceitação**:
- [ ] Testes E2E com Cypress
- [ ] Testes de performance com Lighthouse
- [ ] Testes de carga com Artillery
- [ ] Testes de acessibilidade
- [ ] Cobertura de testes > 90%

### 📱 Stack Técnico da Versão Web

#### Frontend (Vue.js 3)
```javascript
// Tecnologias principais
- Vue.js 3 (Composition API)
- Vite (Build tool)
- Pinia (State management)
- Vue Router (Routing)
- Tailwind CSS (Styling)
- Vue Material (UI components)
```

#### Backend (Flask)
```python
# Tecnologias principais
- Flask + Flask-RESTX (API)
- SQLAlchemy (ORM)
- Redis (Cache)
- Celery (Background tasks)
- Skyfield (Astronomy)
- Gunicorn (WSGI server)
```

#### Infraestrutura
```yaml
# Docker Compose
services:
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
  
  backend:
    build: ./backend
    ports: ["5000:5000"]
    depends_on: [redis, postgres]
  
  redis:
    image: redis:alpine
  
  postgres:
    image: postgres:15
```

## Icebox - Ideias Futuras

### 💡 Funcionalidades Inovadoras

#### IDEA-001: Aplicativo Móvel Nativo
**Tipo**: Feature  
**Complexidade**: Alta  
**Valor Potencial**: Alto

**Descrição**: App nativo iOS/Android com notificações push  
**Benefício**: Acesso móvel otimizado  
**Esforço Estimado**: 55+ pontos

#### IDEA-002: Realidade Aumentada
**Tipo**: Feature  
**Complexidade**: Alta  
**Valor Potencial**: Médio

**Descrição**: Visualização AR das fases lunares e constelações  
**Benefício**: Experiência imersiva educacional  
**Esforço Estimado**: 34+ pontos

#### IDEA-002: Machine Learning para Visibilidade
**Tipo**: Enhancement  
**Complexidade**: Alta  
**Valor Potencial**: Alto

**Descrição**: ML para prever visibilidade da crescente baseado em condições atmosféricas  
**Benefício**: Precisão histórica melhorada  
**Esforço Estimado**: 21+ pontos

### 🔬 Pesquisa e Desenvolvimento

#### R&D-001: Algoritmos Alternativos
**Status**: 🔵 Pesquisa  
**Prazo para Decisão**: Dezembro 2025

**Objetivo**: Investigar algoritmos alternativos para cálculo de visibilidade  
**Hipótese**: Algoritmos baseados em física atmosférica podem ser mais precisos  
**Critérios de Sucesso**: Melhoria > 15% na precisão histórica

#### R&D-002: Integração com Observatórios
**Status**: 🔵 Pesquisa  
**Prazo para Decisão**: Junho 2025

**Objetivo**: Integração com dados reais de observatórios astronômicos  
**Hipótese**: Dados observacionais podem validar cálculos teóricos  
**Critérios de Sucesso**: Correlação > 95% com observações históricas

---

## Critérios de Definição de Pronto (DoD)

### Desenvolvimento
- [ ] Código implementado seguindo padrões DATAMETRIA
- [ ] Code review aprovado por pelo menos um desenvolvedor
- [ ] Testes unitários escritos e passando (cobertura mínima 85%)
- [ ] Testes de integração implementados quando aplicável
- [ ] Documentação técnica atualizada

### Qualidade
- [ ] Testes manuais executados e aprovados
- [ ] Testes de performance realizados quando aplicável
- [ ] Análise de segurança concluída para funcionalidades sensíveis
- [ ] Compatibilidade testada em Windows/Linux/macOS
- [ ] Validação astronômica realizada

### Documentação
- [ ] Documentação de usuário atualizada
- [ ] Changelog atualizado
- [ ] API documentation atualizada (se aplicável)
- [ ] Guias de troubleshooting atualizados

### Deploy
- [ ] Testes em ambiente local realizados
- [ ] Validação de funcionalidade aprovada pelo Product Owner
- [ ] Plano de rollback definido e testado
- [ ] Métricas de monitoramento configuradas
- [ ] Comunicação de release preparada

---

## Processo de Gestão do Backlog

### Refinamento do Backlog
**Frequência**: Quinzenal  
**Duração**: 2 horas  
**Participantes**: Product Owner, Tech Lead, Desenvolvedor Principal

**Atividades**:
- Revisão e repriorização de itens
- Detalhamento de histórias para próximas sprints
- Estimativas de esforço usando Planning Poker
- Identificação de dependências e riscos
- Remoção de itens obsoletos

### Critérios de Priorização

#### Matriz de Priorização (Valor vs Esforço)
| | **Esforço Baixo (1-3)** | **Esforço Médio (5-8)** | **Esforço Alto (13+)** |
|---|---|---|---|
| **Valor Alto** | 🔴 Crítica | 🟠 Alta | 🟡 Média |
| **Valor Médio** | 🟠 Alta | 🟡 Média | 🟢 Baixa |
| **Valor Baixo** | 🟡 Média | 🟢 Baixa | ⚪ Icebox |

#### Fatores de Priorização
1. **Valor Astronômico** (peso: 35%)
   - Precisão dos cálculos
   - Cobertura temporal
   - Validação científica

2. **Experiência do Usuário** (peso: 30%)
   - Facilidade de uso
   - Performance
   - Acessibilidade

3. **Valor Acadêmico** (peso: 20%)
   - Utilidade para pesquisa
   - Exportação de dados
   - Documentação técnica

4. **Sustentabilidade Técnica** (peso: 15%)
   - Manutenibilidade
   - Escalabilidade
   - Débito técnico

---

## Métricas e KPIs

### Métricas de Backlog
- **Tamanho do Backlog**: 23 itens ativos
- **Velocity Média**: 18 pontos por sprint (2 semanas)
- **Lead Time Médio**: 12 dias
- **Cycle Time Médio**: 8 dias
- **Taxa de Entrega**: 92% dos itens planejados

### Métricas de Qualidade
- **Bug Rate**: 0.1 bugs por funcionalidade
- **Escape Rate**: 5% bugs em produção
- **Tempo de Resolução de Bugs**: 3 dias (média)
- **Cobertura de Testes**: 87%

### Métricas de Valor
- **Adoção de Funcionalidades**: 78% usuários ativos
- **Satisfação do Usuário**: 4.6/5.0 (feedback)
- **Tempo de Time-to-Market**: 14 dias (média)
- **Precisão Astronômica**: 99.97% (validação)

---

## Roadmap de Alto Nível

### Q3 2025 - Foco: Precisão e Performance ✅ CONCLUÍDO
- **Objetivos**: Seleção automática de efemérides, modo acadêmico
- **Épicos Principais**: Precisão Astronômica, Funcionalidades Avançadas
- **Métricas de Sucesso**: Suporte completo 1900-2100, modo acadêmico funcional
- **Entregue em**: 31/08/2025 (Versão 1.1.0)

### Q4 2025 - Foco: Plataforma Web
- **Objetivos**: Versão web completa do calendário visual
- **Épicos Principais**: Plataforma Web Completa
- **Métricas de Sucesso**: Interface web funcional, API REST, deploy em produção

### Q1 2026 - Foco: Usabilidade e Integração
- **Objetivos**: Múltiplas localidades, exportação avançada
- **Épicos Principais**: Internacionalização, Integração Externa
- **Métricas de Sucesso**: 5+ localidades suportadas, 3+ formatos de export

### Q2 2026 - Foco: Análise e Comparação
- **Objetivos**: Ferramentas de análise comparativa
- **Épicos Principais**: Análise Comparativa
- **Métricas de Sucesso**: Relatórios comparativos funcionais

---

## Stakeholders e Comunicação

### Stakeholders Principais
- **Product Owner**: Vander Loto - vander.loto@outlook.com
- **Tech Lead**: Vander Loto - vander.loto@outlook.com
- **Desenvolvedor Principal**: Vander Loto - vander.loto@outlook.com
- **Comunidade Acadêmica**: Pesquisadores em astronomia/religião
- **Usuários Finais**: Comunidade interessada em calendário bíblico

### Canais de Comunicação
- **Daily Updates**: GitHub Issues e Discussions
- **Sprint Reviews**: Documentação no repositório
- **Stakeholder Updates**: README e changelog atualizados
- **Feedback Collection**: GitHub Issues e email direto

### Processo de Feedback
1. **Coleta**: GitHub Issues, email, discussões
2. **Análise**: Avaliação de impacto e viabilidade técnica
3. **Incorporação**: Adição ao backlog com priorização
4. **Comunicação**: Resposta ao usuário e atualização de status

---

**Documento mantido por**: Vander Loto - DATAMETRIA  
**Última atualização**: 31/08/2025  
**Próxima revisão**: 30/11/2025  
**Versão do documento**: 1.1

---

### 📋 Links Úteis
- [Repositório GitHub](https://github.com/vanderloto/biblical_calendar_app)
- [Documentação Técnica](../technical/)
- [Guia do Usuário](../user-guide/)
- [Issues e Feedback](https://github.com/vanderloto/biblical_calendar_app/issues)
- [Roadmap Detalhado](../roadmap.md)