import whisper_timestamped as whisper


model = whisper.load_model("base", device='cuda')
result = model.transcribe("test2.mp3")

print(result['segments'][0:3])