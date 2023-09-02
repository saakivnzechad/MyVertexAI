import struct
import pyaudio

class MicrophoneListener:
    def __init__(self, queue):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        self.queue = queue
        self.amplitude = 0

    async def listen(self):
        data = self.stream.read(1024)
        self.amplitude = max(abs(sample) for sample in struct.unpack('<' + 'h' * 1024, data))
        await self.queue.put(self.amplitude)