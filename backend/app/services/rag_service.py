import os
import shutil
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from app.core.config import settings

class RagService:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(
            model=settings.LLM_MODEL,
            base_url=settings.OLLAMA_BASE_URL
        )

        # Initialize the Vector DB
        # This connects to your local ChromaDB folder
        self.vector_store = Chroma(
            persist_directory=settings.CHROMA_DB_PATH,
            embedding_function=self.embeddings
        )

        # Initialize the LLM
        self.llm = ChatOllama(
            model=settings.LLM_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0
        )

    async def ingest_file(self, file_path: str, original_filename: str):
        """
        Reads a PDF, chops it up, and saves it to the vector database.
        """
        try:
            # Load the PDF
            loader = PyPDFLoader(file_path)
            documents = loader.load()

            # Split into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200, # Overlap helps keep context between chunks
                add_start_index=True
            )
            splits = text_splitter.split_documents(documents)

            # Add metadata
            for split in splits:
                split.metadata["source"] = original_filename

            # Save to DB
            self.vector_store.add_documents(documents=splits)
            
            return len(splits)

        except Exception as e:
            raise e

    def query(self, question: str):
        """
        Searches the database for answers to the user's question.
        """
        # Create the Chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 4}),
            return_source_documents=True
        )

        # Run the question
        result = qa_chain.invoke({"query": question})
        
        # Format the output
        return {
            "answer": result["result"],
            "sources": list(set([doc.metadata.get("source") for doc in result["source_documents"]]))
        }