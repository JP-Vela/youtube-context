from organizeTranscript import TranscriptDumper
from youtube_transcript_api import YouTubeTranscriptApi
import chromadb
from chromadb.utils import embedding_functions
import math
from urllib.parse import urlparse
from urllib.parse import parse_qs

#import whisper_timestamped as whisper

#Youtube
#https://www.youtube.com/watch?v=rWVAzS5duAs&ab_channel=Veritasium

#Whisper instead of Youtube transcript
#model = whisper.load_model("base", device='cuda')
#transcript = model.transcribe("test2.mp3")['segments']

class Word2Time_Youtube():
    def __init__(self, url=None):
        self.url = url

        if url==None:
            raise Exception("Expected a url got None")

        parsed_url = urlparse(url)
        self.vid_id = parse_qs(parsed_url.query)['v'][0]
        print(f'Using video id: {self.vid_id}')

        self.transcript = YouTubeTranscriptApi.get_transcript(video_id=self.vid_id)

        self.docstore = TranscriptDumper(transcript=self.transcript, doc_length=100)

        """self.openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key="OPENAI_KEY",
            model_name="text-embedding-ada-002"
        )"""

        self.client = chromadb.Client()
        self.collection = self.client.create_collection("documents")#, embedding_function=self.openai_ef)

        docs, meta, ids = self.docstore.dump_docs()

        # Add docs to the collection. Can also update and delete. Row-based API coming soon!
        self.collection.add(
            documents=docs, # we handle tokenization, embedding, and indexing automatically. You can skip that and add your own embeddings as well
            metadatas=meta, # filter on these!
            ids=ids, # unique for each doc
        )

    def get_timestamp(self,query):
        results = self.collection.query(
        query_texts=[query],
        n_results=1,
        )

        timestamp = results['metadatas'][0][0]['start']

        url = f'https://youtu.be/{self.vid_id}?t={math.floor(timestamp)}'
        return timestamp, url



class Word2Time():
    def __init__(self, transcript=None):
        self.transcript=transcript

        if self.transcript==None:
            raise Exception("Expected a url got None")


        self.docstore = TranscriptDumper(transcript=self.transcript, doc_length=80)

        self.client = chromadb.Client()
        self.collection = self.client.create_collection("documents")

        docs, meta, ids = self.docstore.dump_docs()

        # Add docs to the collection. Can also update and delete. Row-based API coming soon!
        self.collection.add(
            documents=docs,
            metadatas=meta,
            ids=ids,
        )

    def get_timestamp(self,query):
        results = self.collection.query(
        query_texts=[query],
        n_results=1,
        )

        timestamp = results['metadatas'][0][0]['start']

        return timestamp
        

word2time = Word2Time_Youtube('https://www.youtube.com/watch?v=K5UU0GA5GAU&ab_channel=JoeScott')
print("Vectorstore made")
time,url = word2time.get_timestamp("How long will it be until we use nuclear engines?")
print(url)