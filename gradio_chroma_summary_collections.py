import gradio as gr
from chromadb import HttpClient

# Function to list all collections using the Chroma HTTP client
def list_chroma_collections():
    try:
        # Initialize the Chroma HTTP client
        client = HttpClient(host='localhost', port=8000)

        # List all collections available on the server
        collections = client.list_collections()

        # Format the output
        result = [f"Number of collections: {len(collections)}"]
        for collection in collections:
            result.append(f"Collection Name: {collection.name}")
        
        return "\n".join(result)
    except Exception as e:
        return f"Error: {str(e)}"

# Gradio app
def gradio_app():
    with gr.Blocks() as app:
        gr.Markdown("## Collections Summary")
        gr.Markdown("Click the button to view all collections in the vectorstore.")

        result_output = gr.Textbox(label="Output", lines=10, interactive=False)
        fetch_button = gr.Button("List Collections")

        fetch_button.click(list_chroma_collections, inputs=[], outputs=result_output)

    return app

# Run the Gradio app
if __name__ == "__main__":
    app = gradio_app()
    app.launch(server_name="0.0.0.0", server_port=7864)
