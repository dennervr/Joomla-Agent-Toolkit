# Joomla Agent Toolkit (ragJoomla)

O Joomla Agent Toolkit é uma suíte de ferramentas projetada para capacitar agentes de IA (como OpenCode e Claude) a desenvolver sites Joomla completos de forma autônoma. 

Nosso objetivo é fornecer as "skills" necessárias para que a IA possa atuar como um desenvolvedor Full-Stack Joomla, sendo capaz de:
- Criar e gerenciar Artigos, Categorias e Menus.
- Desenvolver Módulos, Componentes e Plugins do zero.
- Compreender e aplicar a arquitetura MVC do Joomla (versões 3, 4 e 5).
- Integrar extensões e gerenciar o ecossistema do CMS.

Atualmente, o projeto conta com um módulo inicial robusto de **RAG (Retrieval-Augmented Generation)**. Essa ferramenta permite aos agentes de IA consultarem a documentação oficial do Joomla em tempo real e de forma autônoma, garantindo que o código gerado siga as melhores práticas e os padrões mais recentes da plataforma.

## Funcionalidades

- **Consulta Inteligente (RAG):** Banco de dados vetorial embutido com a documentação oficial do Joomla. A IA busca o contexto necessário de forma dinâmica para resolver problemas complexos.
- **Integração Global:** Pode ser instalado globalmente no sistema e utilizado em qualquer projeto ou diretório local.

## Como Instalar

```bash
# Instala o CLI globalmente no seu sistema usando pipx
pipx install git+https://github.com/seu-usuario/joomla-rag.git

# Garante que a pasta do pipx esteja no seu PATH
pipx ensurepath

# Injeta a Skill no seu ambiente (ex: OpenCode)
joomla-rag setup
```

## Comandos Disponíveis (CLI)

- `joomla-rag setup`: Instala os arquivos de instrução (Skills) globalmente no ambiente do agente (ex: `~/.config/opencode/skills/`).
- `joomla-rag search "query"`: Comando utilizado autonomamente pela IA para buscar conhecimentos específicos na documentação do Joomla.
- `joomla-rag ingest [path]`: (Opcional) Comando administrativo para reprocessar a documentação e atualizar o banco de dados vetorial interno.
