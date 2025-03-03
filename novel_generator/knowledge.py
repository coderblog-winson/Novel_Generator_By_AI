#novel_generator/knowledge.py
# -*- coding: utf-8 -*-
"""
Import knowledge files into vector library (advanced_split_content, import_knowledge_file)
"""
import os
import logging
import re
import traceback
import nltk
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from utils import read_file
from novel_generator.vectorstore_utils import load_vector_store, init_vector_store
from langchain.docstore.document import Document


def advanced_split_content(content: str, similarity_threshold: float = 0.7, max_length: int = 500) -> list:
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    sentences = nltk.sent_tokenize(content)
    if not sentences:
        return []
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embeddings = model.encode(sentences)
    merged_paragraphs = []
    current_sentences = [sentences[0]]
    current_embedding = embeddings[0]
    for i in range(1, len(sentences)):
        sim = cosine_similarity([current_embedding], [embeddings[i]])[0][0]
        if sim >= similarity_threshold:
            current_sentences.append(sentences[i])
            current_embedding = (current_embedding + embeddings[i]) / 2.0
        else:
            merged_paragraphs.append(" ".join(current_sentences))
            current_sentences = [sentences[i]]
            current_embedding = embeddings[i]
    if current_sentences:
        merged_paragraphs.append(" ".join(current_sentences))
    final_segments = []
    for para in merged_paragraphs:
        if len(para) > max_length:
            sub_segments = []
            start_idx = 0
            while start_idx < len(para):
                end_idx = min(start_idx + max_length, len(para))
                segment = para[start_idx:end_idx].strip()
                sub_segments.append(segment)
                start_idx = end_idx
            final_segments.extend(sub_segments)
        else:
            final_segments.append(para)
    return final_segments

def import_knowledge_file(
    embedding_api_key: str,
    embedding_url: str,
    embedding_interface_format: str,
    embedding_model_name: str,
    file_path: str,
    filepath: str
):
    logging.info(f"Start importing knowledge base files: {file_path}, interface format: {embedding_interface_format}, model: {embedding_model_name}")
    if not os.path.exists(file_path):
        logging.warning(f"The knowledge base file does not exist: {file_path}")
        return
    content = read_file(file_path)
    if not content.strip():
        logging.warning("The content of the knowledge base file is empty.")
        return
    paragraphs = advanced_split_content(content)
    from embedding_adapters import create_embedding_adapter
    embedding_adapter = create_embedding_adapter(
        embedding_interface_format,
        embedding_api_key,
        embedding_url if embedding_url else "http://localhost:11434/api",
        embedding_model_name
    )
    store = load_vector_store(embedding_adapter, filepath)
    if not store:
        logging.info("Vector store does not exist or load failed. Initializing a new one for knowledge import...")
        store = init_vector_store(embedding_adapter, paragraphs, filepath)
        if store:
            logging.info("Knowledgebase file has been successfully imported to the vector library (new initialization).")
        else:
            logging.warning("Knowledge base import failed, skip.")
    else:
        try:
            docs = [Document(page_content=str(p)) for p in paragraphs]
            store.add_documents(docs)
            logging.info("Knowledge base file has been successfully imported to vector library (append mode).")
        except Exception as e:
            logging.warning(f"Knowledge Base import failed: {e}")
            traceback.print_exc()
