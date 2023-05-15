# youtube-context
Given a YouTube link and a query, find the place in the video where that query is answered.
Uses chromadb as a local vector store and by default uses sentence transformers for embeddings.

Two classes: VideoDocs and VideoQuery

VideoDocs constructor takes in a youtube video url and optionally different chromadb embeddings

VideoQuery constructor takes no parameters

The VideoQuery.ask method takes a query and a VideoDocs object.
The VideoDocs object holds the chromadb collection for actually performing
the similarity search as well as holding the video id for creating the timestamp url.
