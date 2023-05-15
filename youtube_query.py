from organizeTranscript import TranscriptDumper
from youtube_transcript_api import YouTubeTranscriptApi
import chromadb
import math
from urllib.parse import urlparse
from urllib.parse import parse_qs

# Creates the vector store given a youtube url
class VideoDocs:
    def __init__(self, video_url: str, embeddings=None):
        """
        Gets video transcript and converts it into a vector store

        video_url: A YouTube URL (must have a transcript)
        embeddings (optional): Different chromadb compatible embeddings. Uses Sentence Transformers by default
        """

        parsed_url = urlparse(video_url)
        video_id = parse_qs(parsed_url.query)['v'][0]

        self.video_url = video_url
        self.video_id = video_id
        self.transcript = YouTubeTranscriptApi.get_transcript(video_id=video_id)
        dumper = TranscriptDumper(transcript=self.transcript, doc_length=100)

        docs, meta, ids = dumper.dump_docs() # Gets the transcript split into an array of docs with corresponding metadata and ids

        client = chromadb.Client()

        if embeddings == None:
            self.collection = client.create_collection("documents")
        else:
            self.collection = client.create_collection("documents", embedding_function=embeddings)

        # Generate the chromadb collection
        self.collection.add(
            documents=docs,
            metadatas=meta,
            ids=ids,
        )

    def get_collection(self):
        return self.collection

    def get_video_id(self):
        return self.video_id


# Only holds the function for quering the vector store and return a timestamp url
class VideoQuery:
    def __init__(self) -> None:
        pass

    def ask(self, video_docs: VideoDocs, query:str) -> str:
        """
        Returns a youtube timestamp answering the query

        video_docs: Created from a YouTube URL
        query: The query to be answered 
        """

        collection = video_docs.get_collection()
        video_id = video_docs.get_video_id()

        results = collection.query(
            query_texts=[query],
            n_results=1,
        )

        timestamp = results['metadatas'][0][0]['start']

        # Puts the timestamp and video id into generic youtube url schema
        timestamp_url = f'https://youtu.be/{video_id}?t={math.floor(timestamp)}'
        return timestamp_url
    