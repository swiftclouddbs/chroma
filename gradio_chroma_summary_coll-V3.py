import gradio as gr
from chromadb.config import Settings
from chromadb.client import Client
#from chromadb import HttpClient
from chromadb.api.models.Collection import Collection
from langchain.embeddings import OpenAIEmbeddings  # Update based on your embedding source

# Function to list all collections using the Chroma HTTP client
def list_chroma_collections():
    try:
        # Initialize the Chroma client with HTTP settings
        client = Client(Settings(chroma_api_impl="rest", chroma_server_host="localhost", chroma_server_http_port=8000))
        
        # List all collections available on the server
        collection_names = client.list_collections()
        
        # Format the output
        result = [f"Number of collections: {len(collection_names)}"]
        for collection in collection_names:
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
