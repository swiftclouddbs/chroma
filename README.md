AI Portal:  Next video - portal mgmt, projects, plans for chroma collection layout
  Chart course for next set of videos - using task list functionality
  we want to load multiple 10Ks and query them.  show how they are in the "Research" Collection.  View collections for the business units.
  Citations.  
  How RAG addresses the LLM issues of hallucinations and groundedness.  Citations.
  D&D a dataset and perform linear regression
  Loading multiple datasets and creating graphs - drawing conclusions from the data
  SVM graphs
  
Build an HTML editor:  https://netbeans.apache.org/tutorial/main/tutorials/nbm-htmleditor/

Upgrade to latest chroma:
remove ALL installed chroma packages:
pip uninstall .............

pip install chromadb
pip install -U langchain-chroma

chroma run --path ./VS_name

dig up old script that fetches 10-K/Q and start loading them into a vectorstore.  Run queries...
