import os
import shutil
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
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
        # Create the retriever
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 4})
        
        # Create the prompt template
        template = """Answer the question based only on the following context: {context}
                Question: {question}
                """
        prompt = ChatPromptTemplate.from_template(template)
        
        # Create the chain
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        answer = chain.invoke(question)
        
        docs = retriever.invoke(question)
        sources = list(set([doc.metadata.get("source") for doc in docs]))
        
        return {
            "answer": answer,
            "sources": sources
        }