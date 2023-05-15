from youtube_transcript_api import YouTubeTranscriptApi

# https://www.youtube.com/watch?v=SsrWgwCxTaM

transcript = YouTubeTranscriptApi.get_transcript('SsrWgwCxTaM')
for text in transcript[0:5]:
    print(text)