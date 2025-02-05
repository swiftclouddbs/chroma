import gradio as gr
from chromadb import HttpClient

# Initialize the Chroma HTTP client
client = HttpClient(host='localhost', port=8000)

def get_collection_source_files(collection_name):
    try:
        # Fetch the collection by name
        collection = client.get_collection(name=collection_name)
        if not collection:
            return f"No collection found with the name '{collection_name}'."

        # Fetch all documents from the collection
        results = collection.get(include=["metadatas"])
        if not results or "metadatas" not in results:
            return "No documents found in the selected collection."

        # Extract unique source filenames from metadata
        unique_sources = set()
        for metadata in results["metadatas"]:
            if "source" in metadata:
                unique_sources.add(metadata["source"])

        if not unique_sources:
            return "No source files found in the collection metadata."

        return "\n".join(f"Source File: {source}" for source in unique_sources)
    except Exception as e:
        return f"Error: {str(e)}"

def gradio_app():
    with gr.Blocks(title="Collection Source Files Viewer") as app:
        gr.Markdown("## Collection Source Files Viewer")
        gr.Markdown("Enter the collection name to list unique source files.")

        collection_input = gr.Textbox(label="Collection Name", placeholder="Enter collection name")
        result_output = gr.Textbox(label="Source Files", lines=10, interactive=False)
        fetch_button = gr.Button("Fetch Source Files")

        fetch_button.click(get_collection_source_files, inputs=[collection_input], outputs=result_output)
        
    return app

if __name__ == "__main__":
    app = gradio_app()
    app.launch(server_name="0.0.0.0", server_port=7866)
