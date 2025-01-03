from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_nomic.embeddings import NomicEmbeddings

# Initialize the embeddings model for vector search
embedding_model = NomicEmbeddings(model="nomic-embed-text-v1.5", inference_mode="local")

# Specify the directory where the Chroma vector data will be stored
PERSIST_DIRECTORY = "./Map_jan03b"

# Initialize the Chroma vector store
chroma_store = Chroma(
    collection_name="Old_Map_jan03b", 
    embedding_function=embedding_model,
    persist_directory=PERSIST_DIRECTORY  # Specify persistent directory
)

# Load the PDF file(s)
pdf_file_path = "America.pdf"  # Replace with your PDF file path
loader = PyPDFLoader(pdf_file_path)
documents = loader.load()

# Split the text into manageable chunks and retain metadata
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=500)
split_documents = []
for doc in documents:
    chunks = text_splitter.split_text(doc.page_content)
    for chunk in chunks:
        split_documents.append(
            Document(
                page_content=chunk,
                metadata={
                    "page_number": doc.metadata.get("page_number", -1),
                    "source": pdf_file_path,}
                )
        )


# Initialize the Chroma vector store
chroma_store.add_documents(split_documents)
chroma_store.persist()

print("PDF content with page numbers successfully loaded into Chroma vector store.")
