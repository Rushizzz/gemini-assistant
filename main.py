import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import sounddevice as sd
from OpenGL.GLUT import glutInit, glutWireSphere
import math
from speech_to_text import SpeechToText
from assistant import ask_gemini
from audio import text_to_speech
import sys
import traceback
import time

# Global variables
volume = 0
beat_detected = False
history_energy = []
rotation = 0
spheres = []  # Store sphere positions and states
current_response = None  # Store the latest Gemini response
recording = False
last_recording_time = 0
is_speaking = False  # Track if audio is being played
audio_stream = None  # Store the audio input stream

def init_opengl():
    """Initialize OpenGL with proper error handling"""
    try:
        pygame.init()
        glutInit()
        
        # Set OpenGL attributes before creating the display
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 2)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 1)
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)
        pygame.display.gl_set_attribute(pygame.GL_DOUBLEBUFFER, 1)
        
        display = (1920, 1080) #resolution of screen
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        
        gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -6)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        return True
    except Exception as e:
        print(f"Error initializing OpenGL: {e}")
        print(traceback.format_exc())
        return False

class Sphere:
    def __init__(self, position, color):
        self.position = position  # (x, y, z)
        self.color = color
        self.scale = 1.0
        self.target_scale = 1.0
        self.rotation = 0
        self.rotation_speed = 1.0

    def update(self, beat_detected, is_speaking):
        # Smooth scaling animation
        self.scale += (self.target_scale - self.scale) * 0.1
        
        # Only respond to beats when not speaking
        if not is_speaking:
            if beat_detected:
                self.target_scale = 1.3
            else:
                self.target_scale = 1.0
        else:
            # Gentle pulsing while speaking
            self.target_scale = 1.0 + 0.1 * math.sin(time.time() * 2)
        
        # Continuous rotation
        self.rotation += self.rotation_speed

    def draw(self):
        try:
            glPushMatrix()
            glTranslatef(*self.position)
            glRotatef(self.rotation, 1, 1, 1)  # Rotate on all axes
            glScalef(self.scale, self.scale, self.scale)
            glColor3f(*self.color)
            glutWireSphere(0.3, 20, 20)  # Radius, slices, stacks
            glPopMatrix()
        except Exception as e:
            print(f"Error drawing sphere: {e}")

def audio_callback(indata, frames, time, status):
    global volume, beat_detected, history_energy, is_speaking

    # Skip beat detection while speaking
    if is_speaking:
        return

    try:
        samples = indata[:, 0]
        energy = np.sum(samples ** 2) / len(samples)
        volume = np.linalg.norm(samples) * 10

        history_energy.append(energy)
        if len(history_energy) > 43:
            history_energy.pop(0)

        local_avg = np.mean(history_energy)
        beat_detected = energy > 1.3 * local_avg if local_avg > 0 else False
    except Exception as e:
        print(f"Error in audio callback: {e}")

def init_spheres():
    global spheres
    try:
        # Define positions for the four spheres at the center of each side
        positions = [
            (0, 2, 0),    # Top
            (0, -2, 0),   # Bottom
            (-2, 0, 0),   # Left
            (2, 0, 0)     # Right
        ]
        color = (0.1, 0.7, 1.0)  # Neon blue color
        spheres = [Sphere(pos, color) for pos in positions]
    except Exception as e:
        print(f"Error initializing spheres: {e}")

def draw_text(text, x, y):
    """Draw text on the screen using pygame"""
    try:
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, (255, 255, 255))
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        width = text_surface.get_width()
        height = text_surface.get_height()

        glWindowPos2d(x, y)
        glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    except Exception as e:
        print(f"Error drawing text: {e}")

def process_speech(text):
    """Process the recognized speech with Gemini and speak the response"""
    global current_response, is_speaking, audio_stream
    try:
        print(f"\nYou said: {text}")
        print("Processing with Gemini...")
        response = ask_gemini(text)
        current_response = response
        print(f"\nGemini's response: {response}")
        
        # Stop the audio input stream while speaking
        if audio_stream:
            audio_stream.stop()
        
        # Speak the response
        print("Speaking response...")
        is_speaking = True
        
        def on_speech_complete():
            global is_speaking, audio_stream
            is_speaking = False
            # Restart audio input
            if audio_stream:
                audio_stream.start()
        
        # Start speech playback with callback
        text_to_speech(response, callback=on_speech_complete)
        
    except Exception as e:
        print(f"Error processing speech: {e}")
        current_response = None
        is_speaking = False
        if audio_stream:
            audio_stream.start()

def main():
    global rotation, current_response, recording, last_recording_time, is_speaking, audio_stream

    try:
        if not init_opengl():
            print("Failed to initialize OpenGL. Exiting...")
            return

        # Initialize spheres
        init_spheres()

        # Initialize speech recognition
        stt = SpeechToText()

        # Start audio input
        audio_stream = sd.InputStream(callback=audio_callback)
        audio_stream.start()

        clock = pygame.time.Clock()

        print("Press SPACE to start/stop recording")
        print("Press ESC to exit")

        while True:
            current_time = time.time()
            
            # Check for recording timeout
            if recording and current_time - last_recording_time > 5:
                recording = False
                stt.stop_recording()
                text = stt.get_text()
                if text:
                    process_speech(text)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if audio_stream:
                        audio_stream.stop()
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if audio_stream:
                            audio_stream.stop()
                        pygame.quit()
                        return
                    elif event.key == pygame.K_SPACE:
                        if not recording:
                            recording = True
                            last_recording_time = current_time
                            stt.start_recording()
                        else:
                            recording = False
                            stt.stop_recording()
                            # Wait a short moment for the recognition to complete
                            time.sleep(0.5)
                            text = stt.get_text()
                            if text:
                                process_speech(text)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Update and draw all spheres
            for sphere in spheres:
                sphere.update(beat_detected, is_speaking)
                sphere.draw()

            # # Draw the latest response if available
            # if current_response:
            #     # Split response into lines to fit on screen
            #     lines = current_response.split('\n')
            #     for i, line in enumerate(lines[:3]):  # Show first 3 lines
            #         draw_text(line, 10, 750 - (i * 30))

            pygame.display.flip()
            clock.tick(60)

    except Exception as e:
        print(f"Error in main loop: {e}")
        print(traceback.format_exc())
        if audio_stream:
            audio_stream.stop()
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
