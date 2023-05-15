"""
Takes a transcript array of dictionaries and splits it up into docs of n length each.
It doesn't have to be a youtube transcript. Future plans include transcription and parsing of regular audio

transcript dictionary structure:

    [
        {
            'start': 0.0,
            'text': '...hello there...'  
        },
    
        {
            'start': 5.0,
            'text': '...General Kenobi...'  
        }
    ]
    
"""

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
