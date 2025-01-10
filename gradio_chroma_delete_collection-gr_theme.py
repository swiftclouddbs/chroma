import gradio as gr
from langchain.vectorstores import Chroma

# Specify the directory where the Chroma vector data is stored
PERSIST_DIRECTORY = "./Map_jan03b"  # Update with your directory

def delete_collection(collection_name):
    try:
        # Initialize the Chroma vector store
        chroma_store = Chroma(
            collection_name=collection_name,
            persist_directory=PERSIST_DIRECTORY,
        )

        # Attempt to delete the collection
        chroma_store.delete_collection()

        return f"Collection '{collection_name}' has been successfully deleted."

    except Exception as e:
        return f"An error occurred while attempting to delete the collection: {str(e)}"

import gradio as gr

#
#Citrus theme is built-in
#Try and create a rose theme, a green theme, etc.
#

theme = gr.themes.Glass().set(
    background_fill_primary='*secondary_200',
    block_background_fill='*primary_400',
    block_border_color='*primary500',
    block_border_width='3px',
    block_shadow='*primary_400',
    button_border_width='0px',
    button_transition='all 0.5s;'
    
)

# Gradio Interface
interface = gr.Interface(
    theme=theme,
    fn=delete_collection,
    inputs=gr.Textbox(label="Enter Collection Name", placeholder="Type the collection name to delete here"),
    outputs="text",
    title="Collection Deletion",
    description="Enter a collection name to delete from the vector database.  Use with caution!",
    css="footer{display:none !important}",
    flagging_options=[],
)

# Launch Gradio app
interface.launch(server_name="0.0.0.0", server_port=7867)
