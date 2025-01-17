import gradio as gr
from chromadb import HttpClient

# Function to list all collections using the Chroma HTTP client
def list_chroma_collections():
    try:
        # Initialize the Chroma HTTP client
        client = HttpClient(host='localhost', port=8000)

        # List all collections available on the server
        collection_objects = client.list_collections()  # Returns collection objects
        if not collection_objects:
            return "No collections found in the vectorstore."

        # Extract only collection names from the objects
        collection_names = [col.name if hasattr(col, 'name') else str(col) for col in collection_objects]

        collections = []
        debug_info = []  # To collect debug details

        # Process each collection name
        for name in collection_names:
            try:
                # Fetch collection metadata by name
                collection = client.get_collection(name=name)
                collections.append(collection)
                debug_info.append(f"Collection '{name}' fetched successfully.")
            except Exception as e:
                # Log errors for debugging
                debug_info.append(f"Collection '{name}' failed: {str(e)}")
                continue

        # Format the output
        if not collections:
            return f"No valid collections found. Debug Info:\n{'\n'.join(debug_info)}"

        result = [f"Number of valid collections: {len(collections)}"]
        for collection in collections:
            result.append(f"Collection Name: {collection.name}")
        
##        # Include debug info
##        result.append("\nDebug Information:")
##        result.extend(debug_info)
        
        return "\n".join(result)
    except Exception as e:
        return f"Error: {str(e)}"

theme = gr.themes.Glass().set(
    background_fill_primary='*secondary_200',
    block_background_fill='*primary_400',
    block_border_color='*primary500',
    block_border_width='3px',
    block_shadow='*primary_400',
    button_border_width='0px',
    button_transition='all 0.5s;'    
)

# Gradio app
def gradio_app():
    with gr.Blocks(title="Collections Summary", theme=theme) as app:
        gr.Markdown("## Collections Summary")
        gr.Markdown("Click the button to view all collections in the vectorstore.")

        result_output = gr.Textbox(label="Output", lines=15, interactive=False, value="Click the button to fetch collections.")
        fetch_button = gr.Button("List Collections")

        fetch_button.click(list_chroma_collections, inputs=[], outputs=result_output)
    return app

# Run the Gradio app
if __name__ == "__main__":
    app = gradio_app()
    app.launch(server_name="0.0.0.0", server_port=7864)
