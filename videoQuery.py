import youtube_query as yq

yt_url = 'https://www.youtube.com/watch?v=rWVAzS5duAs&ab_channel=Veritasium'
query = 'How long does it take for concrete to dry?'

docs = yq.VideoDocs(yt_url)

video_query = yq.VideoQuery()

print(video_query.ask(video_docs=docs, query=query))