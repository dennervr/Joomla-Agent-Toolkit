import os
import sys
import warnings
import logging
from pathlib import Path

# Configurar variáveis de ambiente ANTES de importar outras bibliotecas para suprimir avisos
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["HF_HUB_DISABLE_WARNINGS"] = "1"
os.environ["huggingface_hub_VERBOSITY"] = "error"
os.environ["TQDM_DISABLE"] = "1" # Desabilita a barra de progresso "Loading weights"

# Suprimir avisos do Python/Langchain
warnings.filterwarnings("ignore")

# Configurar loggers do HuggingFace e Transformers para calarem a boca
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)

try:
    from langchain_chroma import Chroma
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    print("Erro: As dependências do RAG não estão instaladas. Rode: pip install langchain-community langchain-huggingface chromadb sentence-transformers", file=sys.stderr)
    sys.exit(1)

def search_docs(query: str, k: int = 5):
    package_dir = Path(__file__).parent
    chroma_persist_dir = package_dir / "data" / "chroma_db"
    
    if not chroma_persist_dir.exists():
        print(f"Erro: Banco de dados vetorial empacotado não encontrado em {chroma_persist_dir}.", file=sys.stderr)
        sys.exit(1)

    # Carrega silenciosamente o modelo e o banco
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'local_files_only': True}
        )
        
        vectorstore = Chroma(
            persist_directory=str(chroma_persist_dir),
            embedding_function=embeddings
        )
        
        results = vectorstore.similarity_search_with_score(query, k=k)
    except Exception as e:
        print(f"Erro ao consultar o banco de dados: {str(e)}", file=sys.stderr)
        sys.exit(1)
        
    if not results:
        print("Nenhum resultado relevante encontrado na documentação.")
        return

    # Print estruturado e limpo
    print(f"--- RESULTADOS DA BUSCA NA DOCUMENTAÇÃO DO JOOMLA PARA: '{query}' ---\n")
    for i, (doc, score) in enumerate(results):
        source_raw = doc.metadata.get('source', 'Unknown')
        # Reconstrói o caminho absoluto baseando-se no diretório do pacote instalado (para leitura do LLM)
        abs_source = package_dir / source_raw
        
        headers = " > ".join(v for k, v in doc.metadata.items() if k.startswith('Header'))
        
        print(f"[[ RESULTADO {i+1} | ARQUIVO: {abs_source} ]]")
        if headers:
            print(f"TÓPICO: {headers}")
        print(f"CONTEÚDO:\n{doc.page_content}\n")
        print("-" * 50 + "\n")