import gradio as gr
from chromadb import HttpClient

# Initialize the Chroma HTTP client
client = HttpClient(host='localhost', port=8000)

def delete_documents_by_source(collection_name, source_file):
    try:
        # Fetch the collection by name
        collection = client.get_collection(name=collection_name)
        if not collection:
            return f"No collection found with the name '{collection_name}'."

        # Retrieve all documents with metadata
        results = collection.get(include=["metadatas", "documents"])
        if not results or "metadatas" not in results:
            return "No documents found in the selected collection."

        # Identify documents with matching source file
        documents_to_delete = []
        for metadata, document_content in zip(results["metadatas"], results["documents"]):
            if metadata.get("source") == source_file:
                documents_to_delete.append(document_content)

        if not documents_to_delete:
            return f"No documents found with source file '{source_file}' in collection '{collection_name}'."

        # Perform deletion by querying for matching documents
        collection.delete(where={"source": source_file})

        return f"Successfully deleted {len(documents_to_delete)} document(s) with source file '{source_file}' from collection '{collection_name}'."
    except Exception as e:
        return f"Error: {str(e)}"

def gradio_app():
    with gr.Blocks(title="Delete Documents by Source File") as app:
        gr.Markdown("## Delete Documents by Source File")
        gr.Markdown("Enter the collection name and source file to delete all associated documents.")

        collection_input = gr.Textbox(label="Collection Name", placeholder="Enter collection name")
        source_input = gr.Textbox(label="Source File Name", placeholder="Enter exact source file name (case-sensitive)")
        result_output = gr.Textbox(label="Result", lines=5, interactive=False)
        delete_button = gr.Button("Delete Documents")

        delete_button.click(delete_documents_by_source, inputs=[collection_input, source_input], outputs=result_output)

    return app

if __name__ == "__main__":
    app = gradio_app()
    app.launch(server_name="0.0.0.0", server_port=7867)
