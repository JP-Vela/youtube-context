from youtube_transcript_api import YouTubeTranscriptApi

# https://www.youtube.com/watch?v=SsrWgwCxTaM
video_id = 'SsrWgwCxTaM'

#transcript = YouTubeTranscriptApi.get_transcript(video_id)


class TranscriptDumper():
    def __init__(self, transcript, doc_length=100) -> None:
        self.doc_length = doc_length
        self.transcript = transcript

    def dump_docs(self):
        documents = ['']
        ids = ['doc0']
        metadata = [
            {
                'start':0.0
            }
        ]

        cur_doc = 0

        for i in range(len(self.transcript)):
            timestamp = self.transcript[i]

            text = timestamp['text']
            time = timestamp['start']

            word_count = len(documents[cur_doc].split(' '))

            if word_count<self.doc_length:
                documents[cur_doc] += ' '+text

            else:
                cur_doc+=1
                i -= int(self.doc_length/2)
                entry = {
                    'start':time
                }
                documents.append(text)
                metadata.append(entry)
                ids.append(f'doc{cur_doc}')

        return documents, metadata, ids
