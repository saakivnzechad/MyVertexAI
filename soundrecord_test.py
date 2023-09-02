import struct
import pygame
import pyaudio
import asyncio
from asyncio import Queue

class MicrophoneListener:
    def __init__(self, queue):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        self.queue = queue
        self.amplitude = 0

    async def listen(self):
        data = self.stream.read(1024)
        self.amplitude = max(abs(sample) for sample in struct.unpack('<' + 'h' * 1024, data))
        print(self.amplitude)
        await self.queue.put(self.amplitude)

async def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600))
    queue = Queue()
    listener = MicrophoneListener(queue)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        await listener.listen()

        if not queue.empty():
            amplitude = await queue.get()
            pygame.draw.rect(screen, (255, 255, 255), (10, 10, amplitude, 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

asyncio.run(main())
