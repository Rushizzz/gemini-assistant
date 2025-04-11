# 3D Pulse Ring Visualizer with Holographic Illusion

A real-time 3D visualization system that responds to audio input and integrates with speech recognition and AI-powered responses. The system features:

- Real-time audio beat detection
- 3D holographic sphere visualization
- Speech-to-text input
- AI-powered responses using Google's Gemini
- Text-to-speech output
- Interactive controls

## Features

- **Audio Visualization**: Real-time 3D spheres that pulse and rotate in response to audio input
- **Speech Recognition**: Convert speech to text for interaction
- **AI Integration**: Process queries using Google's Gemini AI
- **Voice Output**: Convert AI responses to speech
- **Interactive Controls**: Use spacebar to start/stop recording and ESC to exit

## Requirements

### Python Packages

Install the required packages using pip:

```bash
pip install -r requirements.txt
```

The following packages are required:

- `pygame` - For 3D visualization and window management
- `PyOpenGL` - For 3D graphics rendering
- `numpy` - For numerical operations and audio processing
- `sounddevice` - For audio input/output
- `pydub` - For audio file handling
- `requests` - For HTTP requests
- `murf` - For text-to-speech conversion
- `google-generativeai` - For Gemini AI integration
- `speech_recognition` - For speech-to-text conversion

### System Requirements

- Python 3.8 or higher
- OpenGL-compatible graphics card
- Microphone for speech input
- Speakers for audio output

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Set up your API keys:
   - Create a `.env` file in the project root
   - Add your API keys:
     ```
     MURF_API_KEY=your_murf_api_key
     GEMINI_API_KEY=your_gemini_api_key
     ```

## Usage

1. Run the main program:
```bash
python ncs.py
```

2. Controls:
   - Press `SPACE` to start/stop recording
   - Press `ESC` to exit the program

3. Interaction:
   - When recording is active, speak your query
   - The system will process your speech, get a response from Gemini AI
   - The response will be played back through text-to-speech
   - The 3D visualization will continue running during the entire process

## Project Structure

- `ncs.py` - Main program file with 3D visualization and audio processing
- `audio.py` - Audio handling and text-to-speech functionality
- `speech_to_text.py` - Speech recognition implementation
- `assistant.py` - Gemini AI integration
- `requirements.txt` - List of required Python packages

## Troubleshooting

1. If you encounter audio issues:
   - Check your microphone and speaker settings
   - Ensure sounddevice is properly installed
   - Verify your audio input/output devices are correctly configured

2. If the visualization is not working:
   - Verify OpenGL is properly installed
   - Check your graphics card drivers
   - Ensure all required Python packages are installed

3. If speech recognition is not working:
   - Check your microphone permissions
   - Verify internet connection (required for speech recognition)
   - Ensure the speech_recognition package is properly installed

## License

[Your chosen license]

## Acknowledgments

- Google Gemini AI for natural language processing
- Murf for text-to-speech capabilities
- PyOpenGL and Pygame for 3D visualization
- All other open-source libraries used in this project 