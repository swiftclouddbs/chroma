#  Here is a client looking for a chroma server:  chroma run --path .
#
#
#
from chromadb import HttpClient

# Initialize the Chroma HTTP client
client = HttpClient(host='localhost', port=8000)

# List all collections available on the server
collections = client.list_collections()
print(f"Number of collections: {len(collections)}")

for collection in collections:
    print(f"Collection Name: {collection.name}")

    # Access the specific collection
    col = client.get_collection(collection.name)

    # Retrieve documents and their metadata
    results = col.get(include=["metadatas", "documents"])

    # Display the number of documents in the collection
    print(f"Number of documents in collection '{collection.name}': {len(results['documents'])}")

    # Iterate through the documents and their metadata
    for idx, (document, metadata) in enumerate(zip(results["documents"], results["metadatas"])):
        print(f"Document {idx + 1}:")
        print(f"  Content: {document[:50]}...")  # Print first 50 characters for brevity
        print(f"  Metadata: {metadata}")
        page_number = metadata.get("page_number", "Unknown")
        print(f"  Page Number: {page_number}")
        print("-" * 40)
