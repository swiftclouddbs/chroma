import gradio as gr
from langchain.vectorstores import Chroma


# Specify the directory where the Chroma vector data is stored
PERSIST_DIRECTORY = "./Map_jan03b"  # Update with your directory

def get_collection_info(collection_name):
    try:
        # Initialize the Chroma vector store with the provided collection name
        chroma_store = Chroma(
            collection_name=collection_name,
            persist_directory=PERSIST_DIRECTORY,
        )

        # Access the collection
        collection = chroma_store._collection

        # Retrieve all documents with metadata
        results = collection.get(include=["metadatas", "documents"])

        # Prepare the summary of the collection
        num_documents = len(results["documents"])
        summary = f"Number of documents in collection '{collection_name}': {num_documents}\n\n"

        for idx, (document, metadata) in enumerate(zip(results["documents"], results["metadatas"])):
            summary += f"Document {idx + 1}:\n"
            summary += f"  Content: {document[:100]}...\n"  # Print first 100 characters for brevity
            summary += f"  Metadata: {metadata}\n"
            summary += "-" * 40 + "\n"

        return summary

    except Exception as e:
        return f"An error occurred: {str(e)}"

# Gradio Interface
interface = gr.Interface(
    fn=get_collection_info,
    inputs=gr.Textbox(label="Enter Collection Name", placeholder="Type the collection name here"),
    outputs="text",
    title="Chroma Collection Info",
    description="Enter a collection name to retrieve information about its documents and metadata.",
)

# Launch Gradio app
interface.launch(server_name="0.0.0.0", server_port=7866)
