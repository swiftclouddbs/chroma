import gradio as gr
from langchain.vectorstores import Chroma

# Specify the directory where the Chroma vector data is stored
PERSIST_DIRECTORY = "./Map_jan03b"  # Update with your directory

def delete_by_source(collection_name, source_name):
    try:
        # Initialize Chroma vector store with the given collection name
        chroma_store = Chroma(
            collection_name=collection_name,
            persist_directory=PERSIST_DIRECTORY,
        )

        # Access the collection
        collection = chroma_store._collection

        # Retrieve all documents with metadata
        results = collection.get(include=["metadatas"])  # Fetch only metadata

        # Find document IDs with the matching "source" metadata
        ids_to_delete = [
            metadata["id"]
            for metadata in results["metadatas"]
            if metadata.get("source") == source_name
        ]

        if not ids_to_delete:
            return f"No documents found with source '{source_name}' in collection '{collection_name}'."

        # Delete the matching documents
        chroma_store.delete(ids=ids_to_delete)

        return f"Successfully deleted {len(ids_to_delete)} document(s) with source '{source_name}' from collection '{collection_name}'."

        collection.persist()

    except Exception as e:
        return f"An error occurred: {str(e)}"

# Create the Gradio interface
interface = gr.Interface(
    fn=delete_by_source,
    inputs=[
        gr.Textbox(label="Collection Name", placeholder="Enter the collection name here"),
        gr.Textbox(label="Source Metadata", placeholder="Enter the source filename here"),
    ],
    outputs="text",
    title="Delete Documents by Source Metadata",
    description="Enter the collection name and source metadata to delete all documents associated with the specified source.",
)

# Launch the Gradio app
interface.launch(server_name="0.0.0.0", server_port=7868)
