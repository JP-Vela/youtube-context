from organizeTranscript import TranscriptDumper
from youtube_transcript_api import YouTubeTranscriptApi
import chromadb
import math
#import whisper_timestamped as whisper

#Youtube
#https://www.youtube.com/watch?v=rWVAzS5duAs&ab_channel=Veritasium
vid_id = 'rWVAzS5duAs'
transcript = YouTubeTranscriptApi.get_transcript(video_id=vid_id)

#Whisper instead of Youtube transcript
#model = whisper.load_model("base", device='cuda')
#transcript = model.transcribe("test2.mp3")['segments']

print("Transcription done")

dumper = TranscriptDumper(transcript=transcript, doc_length=80)

docs, meta, ids = dumper.dump_docs()

client = chromadb.Client()

# Create collection. get_collection, get_or_create_collection, delete_collection also available!
collection = client.create_collection("documents")

# Add docs to the collection. Can also update and delete. Row-based API coming soon!
collection.add(
    documents=docs, # we handle tokenization, embedding, and indexing automatically. You can skip that and add your own embeddings as well
    metadatas=meta, # filter on these!
    ids=ids, # unique for each doc
)


def get_timestamp_href(query, video_id):
    results = collection.query(
    query_texts=[query],
    n_results=1,
    # where={"metadata_field": "is_equal_to_this"}, # optional filter
    # where_document={"$contains":"search_string"}  # optional filter
    )

    timestamp = results['metadatas'][0][0]['start']
    #content = results['documents'][0][0]

    href = f'https://youtu.be/{video_id}?t={math.floor(timestamp)}'
    return href


def get_timestamp(query):
    results = collection.query(
    query_texts=[query],
    n_results=1,
    # where={"metadata_field": "is_equal_to_this"}, # optional filter
    # where_document={"$contains":"search_string"}  # optional filter
    )

    timestamp = results['metadatas'][0][0]['start']
    #content = results['documents'][0][0]

    return timestamp

#url = get_timestamp_href("Is the car too expensive?")
#print(url)

time = get_timestamp_href('How long does it take for concrete to dry?', video_id=vid_id)
print(time)