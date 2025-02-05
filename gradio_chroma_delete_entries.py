import gradio as gr
from chromadb import HttpClient
from chromadb.config import Settings

# Initialize Chroma DB client
chroma_client = HttpClient(host='localhost', port=8000)

# Function to retrieve document IDs by metadata (source file name)
def get_document_ids_by_source(db_name, source_file_name):
    try:
        # Select collection from Chroma DB
        collection = chroma_client.get_or_create_collection(name=db_name)

        # Retrieve document IDs with matching source file name metadata
        query_results = collection.get(where={"source_file": source_file_name})

        # Extract document IDs
        document_ids = query_results.get("ids", []) if query_results else []

        if not document_ids:
            return f"No documents found with source file: {source_file_name}."

        return f"Document IDs found: {', '.join(document_ids)}"

    except Exception as e:
        return f"Error: {str(e)}"

# Gradio Interface
def gradio_interface(db_name, source_file_name):
    return get_document_ids_by_source(db_name, source_file_name)

with gr.Blocks() as demo:
    with gr.Row():
        db_name_input = gr.Textbox(label="Database Name", placeholder="Enter the Chroma DB collection name")
        source_file_input = gr.Textbox(label="Source File Name", placeholder="Enter the source file name to fetch document IDs")

    fetch_button = gr.Button("Fetch Document IDs")
    output_text = gr.Textbox(label="Output", interactive=False)

    fetch_button.click(fn=gradio_interface, inputs=[db_name_input, source_file_input], outputs=output_text)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7878)






##import gradio as gr
##from chromadb import HttpClient
##from chromadb.config import Settings
##
### Initialize Chroma DB client
##chroma_client = HttpClient(host='localhost', port=8000)
##
### Function to delete documents by metadata (source file name)
##def delete_documents_by_source(db_name, source_file_name):
##    try:
##        # Select collection from Chroma DB
##        collection = chroma_client.get_or_create_collection(name=db_name)
##
##        # Retrieve document IDs with matching source file name metadata
##        query_results = collection.get(where={"source_file": source_file_name})
##
##        # Extract document IDs to delete
##        document_ids = query_results.get("ids", []) if query_results else []
##
##        if not document_ids:
##            return f"No documents found with source file: {source_file_name}."
##
##        # Delete the documents
##        collection.delete(ids=document_ids)
##        return f"Deleted {len(document_ids)} document(s) with source file: {source_file_name}."
##
##    except Exception as e:
##        return f"Error: {str(e)}"
##
### Gradio Interface
##def gradio_interface(db_name, source_file_name):
##    return delete_documents_by_source(db_name, source_file_name)
##
##with gr.Blocks() as demo:
##    with gr.Row(title="Delete Entries from Vectorstore"):
##        db_name_input = gr.Textbox(label="Database Name", placeholder="Enter the Chroma DB collection name")
##        source_file_input = gr.Textbox(label="Source File Name", placeholder="Enter the source file name for deletion")
##    
##    delete_button = gr.Button("Delete Documents")
##    output_text = gr.Textbox(label="Output", interactive=False)
##
##    delete_button.click(fn=gradio_interface, inputs=[db_name_input, source_file_input], outputs=output_text)
##
##if __name__ == "__main__":
##    demo.launch(server_name="0.0.0.0", server_port=7878)
