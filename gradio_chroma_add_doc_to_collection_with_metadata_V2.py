import gradio as gr
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_nomic.embeddings import NomicEmbeddings

# Initialize the embeddings model for vector search
embedding_model = NomicEmbeddings(model="nomic-embed-text-v1.5", inference_mode="local")

# Specify the directory where the Chroma vector data will be stored
PERSIST_DIRECTORY = "./Map_jan03b"  # Update with your desired directory

def get_next_id(collection):
    """Retrieve the highest existing ID and return the next ID."""
    results = collection.get(include=["metadatas"])
    existing_ids = [
        int(metadata["id"]) for metadata in results["metadatas"] if "id" in metadata
    ]
    return max(existing_ids, default=0) + 1

def process_pdf(collection_name, pdf_file):
    try:
        # Load the PDF file
        loader = PyPDFLoader(pdf_file.name)
        documents = loader.load()

        # Split the text into manageable chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=500)
        split_documents = text_splitter.split_documents(documents)

        # Initialize Chroma vector store with the given collection name
        chroma_store = Chroma(
            collection_name=collection_name,
            embedding_function=embedding_model,
            persist_directory=PERSIST_DIRECTORY,
        )
        
        # Access the existing collection to determine the next ID
        collection = chroma_store._collection
        next_id = get_next_id(collection)

        # Add unique IDs to documents
        documents_with_ids = []
        for doc in split_documents:
            documents_with_ids.append(
                Document(
                    page_content=doc.page_content,
                    metadata={
                        **doc.metadata,
                        "id": str(next_id),
                    },
                )
            )
            next_id += 1

        # Add documents to Chroma store and persist
        chroma_store.add_documents(documents_with_ids)
        chroma_store.persist()

        return f"PDF '{pdf_file.name}' successfully loaded into collection '{collection_name}' with unique IDs."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Create the Gradio interface
interface = gr.Interface(
    fn=process_pdf,
    inputs=[
        gr.Textbox(label="Collection Name", placeholder="Enter collection name here"),
        gr.File(label="Upload PDF File"),
    ],
    outputs="text",
    title="PDF to Chroma Store with Unique IDs",
)

# Launch the Gradio app
interface.launch(server_name="0.0.0.0", server_port=7865)
