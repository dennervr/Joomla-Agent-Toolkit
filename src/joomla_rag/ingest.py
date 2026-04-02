import os
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def ingest_docs(docs_path: str = None):
    package_dir = Path(__file__).parent
    
    if not docs_path:
        docs_dir = package_dir / "data" / "docs"
    else:
        docs_dir = Path(docs_path).resolve()
        
    chroma_persist_dir = package_dir / "data" / "chroma_db"
    
    if not docs_dir.exists():
        print(f"Erro: O diretório {docs_dir} não existe.")
        return
        
    print(f"Lendo arquivos markdown de: {docs_dir}")
    loader = DirectoryLoader(str(docs_dir), glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()
    print(f"Carregados {len(documents)} documentos.")
    
    headers_to_split_on = [("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    
    all_splits = []
    for doc in documents:
        md_splits = markdown_splitter.split_text(doc.page_content)
        for split in md_splits:
            abs_path = Path(doc.metadata.get("source", ""))
            try:
                # Salva o caminho relativo para que seja portátil entre computadores
                rel_path = abs_path.relative_to(package_dir)
                split.metadata["source"] = str(rel_path)
            except ValueError:
                split.metadata["source"] = str(abs_path)
            
        final_splits = text_splitter.split_documents(md_splits)
        all_splits.extend(final_splits)
        
    print(f"Criados {len(all_splits)} chunks. Inicializando modelo de embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'local_files_only': False} # Na ingestão inicial precisamos baixar da web
    )
    
    print(f"Criando Vector DB empacotado em {chroma_persist_dir}...")
    vectorstore = Chroma.from_documents(
        documents=all_splits,
        embedding=embeddings,
        persist_directory=str(chroma_persist_dir)
    )
    print("Ingestão concluída. O banco de dados agora faz parte do pacote Python!")