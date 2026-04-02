# Configuração de Agentes e "Skills" (OpenCode / Anthropic)

Este projeto foi desenhado com uma arquitetura baseada em **Agent Skills**, com o objetivo de otimizar a janela de contexto de agentes de IA e fornecer as ferramentas necessárias para que operem como **Desenvolvedores Full-Stack Joomla**.

## A Visão do Joomla Agent Toolkit

Em vez de focar apenas na pesquisa de documentação (RAG), este projeto almeja fornecer um ecossistema completo de habilidades para que a IA consiga:
- Criar e gerenciar Artigos, Categorias e Menus diretamente no banco de dados ou via API.
- Scaffoldar e desenvolver Módulos, Componentes (MVC) e Plugins do zero.
- Compreender as diferenças arquitetônicas entre Joomla 3, 4 e 5.
- Empacotar extensões prontas para instalação.

## O Modelo "Agent Skills"

No OpenCode e em agentes baseados na Anthropic (como Claude Desktop), manter servidores locais (como o Model Context Protocol - MCP) em execução contínua consome muitos recursos. A abordagem via "Agent Skill" é mais leve e eficiente:
- Funciona como instruções dinâmicas injetadas via `.opencode/skills/` (ou `~/.config/opencode/skills/`).
- Possui um frontmatter YAML com `name` e `description`.
- O agente lê as instruções e ferramentas disponíveis **apenas** quando o usuário precisa trabalhar com o Joomla.

### Funcionamento Atual: O Módulo RAG para o Agente

A primeira "Skill" implementada é a de pesquisa de documentação inteligente (RAG):

1. **O Agente Recebe o Prompt:** O usuário solicita, por exemplo, "Como criar um componente MVC no Joomla 5?".
2. **Ativação da Skill:** A IA detecta o contexto "Joomla" e carrega a skill `joomla-docs`.
3. **Execução Autônoma:** O arquivo de skill instrui o agente a executar a ferramenta de CLI empacotada:
   ```bash
   joomla-rag search "Como criar um componente MVC no Joomla 5"
   ```
4. **Extração Silenciosa e Offline:** O banco vetorial local (ChromaDB) é consultado e retorna instantaneamente os trechos mais relevantes da documentação oficial do Joomla, sem requerer chamadas de API externas e sem poluir o terminal com logs desnecessários.
5. **Aprofundamento (Opcional):** A resposta da busca inclui os caminhos absolutos dos arquivos Markdown. Se o agente precisar de mais contexto, ele pode usar ferramentas de leitura para consultar o documento completo antes de gerar o código final.
