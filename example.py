import youtube_query as yq

yt_url = 'https://www.youtube.com/watch?v=vSNtifE0Z2Q&ab_channel=Veritasium'

# Compile a doc store and vector store of the transcript of the given youtube video
docs = yq.VideoDocs(yt_url)

video_query = yq.VideoQuery()

query = 'What happens when you stretch a material?'

# Ask a question about the video and return the link to the timestamp
timestamp_url = video_query.ask(video_docs=docs, query=query)

# Ask a question about the video and return only the timestamp
timestamp_only = video_query.ask_time_only(video_docs=docs, query=query)

print()

print(f'Query: {query}')
print(f'URL: {timestamp_url}')
print(f'Timestamp: {timestamp_only}')