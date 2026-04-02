import os
import sys
import warnings
import logging
from pathlib import Path

# Configure environment variables BEFORE importing other libraries to suppress warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["HF_HUB_DISABLE_WARNINGS"] = "1"
os.environ["huggingface_hub_VERBOSITY"] = "error"
os.environ["TQDM_DISABLE"] = "1" # Disable "Loading weights" progress bar

# Suppress Python/Langchain warnings
warnings.filterwarnings("ignore")

# Configure HuggingFace and Transformers loggers to be quiet
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)

try:
    from langchain_chroma import Chroma
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    print("Error: RAG dependencies are not installed. Run: pip install langchain-community langchain-huggingface chromadb sentence-transformers", file=sys.stderr)
    sys.exit(1)

def search_docs(query: str, k: int = 5):
    package_dir = Path(__file__).parent
    chroma_persist_dir = package_dir / "data" / "chroma_db"
    
    if not chroma_persist_dir.exists():
        print(f"Error: Packaged vector database not found in {chroma_persist_dir}.", file=sys.stderr)
        sys.exit(1)

    # Silently load the model and database
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
        print(f"Error querying the database: {str(e)}", file=sys.stderr)
        sys.exit(1)
        
    if not results:
        print("No relevant results found in the documentation.")
        return

    # Structured and clean print
    print(f"--- JOOMLA DOCUMENTATION SEARCH RESULTS FOR: '{query}' ---\n")
    for i, (doc, score) in enumerate(results):
        source_raw = doc.metadata.get('source', 'Unknown')
        # Rebuild absolute path based on installed package directory (for LLM reading)
        abs_source = package_dir / source_raw
        
        headers = " > ".join(v for k, v in doc.metadata.items() if k.startswith('Header'))
        
        print(f"[[ RESULT {i+1} | FILE: {abs_source} ]]")
        if headers:
            print(f"TOPIC: {headers}")
        print(f"CONTENT:\n{doc.page_content}\n")
        print("-" * 50 + "\n")