import pytest
from unittest.mock import patch, MagicMock
from joomla_rag.search import search_docs

def test_search_docs_success():
    # Mock the embeddings and vectorstore
    mock_embeddings = MagicMock()
    mock_vectorstore = MagicMock()
    mock_results = [
        (MagicMock(page_content="Content 1", metadata={'source': 'file1.md', 'Header 1': 'Topic 1'}), 0.9),
        (MagicMock(page_content="Content 2", metadata={'source': 'file2.md'}), 0.8)
    ]
    mock_vectorstore.similarity_search_with_score.return_value = mock_results

    with patch('joomla_rag.search.HuggingFaceEmbeddings', return_value=mock_embeddings) as mock_embeddings_class, \
         patch('joomla_rag.search.Chroma', return_value=mock_vectorstore) as mock_chroma_class, \
         patch('pathlib.Path.exists', return_value=True), \
         patch('builtins.print') as mock_print:

        search_docs("test query", k=2)

    # Assert classes were called
    mock_embeddings_class.assert_called_once()
    mock_chroma_class.assert_called_once()

    # Assert similarity_search_with_score was called
    mock_vectorstore.similarity_search_with_score.assert_called_once_with("test query", k=2)

    # Assert print was called multiple times
    assert mock_print.call_count > 0

def test_search_docs_no_db():
    with patch('pathlib.Path.exists', return_value=False), \
         patch('sys.stderr') as mock_stderr, \
         patch('sys.exit') as mock_exit:

        search_docs("query")

    mock_stderr.write.assert_called()
    mock_exit.assert_called_once_with(1)

def test_search_docs_no_results():
    mock_embeddings = MagicMock()
    mock_vectorstore = MagicMock()
    mock_vectorstore.similarity_search_with_score.return_value = []

    with patch('joomla_rag.search.HuggingFaceEmbeddings', return_value=mock_embeddings), \
         patch('joomla_rag.search.Chroma', return_value=mock_vectorstore), \
         patch('pathlib.Path.exists', return_value=True), \
         patch('builtins.print') as mock_print:

        search_docs("query")

    mock_print.assert_called_with("No relevant results found in the documentation.")