import os
import requests

# ElevenLabs Production Voice Connection Configuration
ELEVENLABS_API_KEY = "YOUR_ELEVENLABS_API_KEY_HERE"  # <-- Swap in your API key string
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Default clean 'Rachel' voice profile token

def speak_briefing_update(text_to_speak):
    """Compiles local RAG intelligence profiles into fluid audio text-to-speech."""
    if ELEVENLABS_API_KEY == "YOUR_ELEVENLABS_API_KEY_HERE":
        print(f"🔊 [MOCK AUDIO LOG] Voice Engine Standby: '{text_to_speak}'")
        return

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    data = {
        "text": text_to_speak,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    print("📡 Contacting ElevenLabs Neural Arrays for Voice Synthesis compilation...")
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        output_audio_file = "icarus_morning_briefing.mp3"
        with open(output_audio_file, "wb") as f:
            f.write(response.content)
        print(f"🎵 [AUDIO GENERATION COMPLETE] Playable file saved cleanly to: {output_audio_file}")
        # To auto-play native sounds through Windows terminal directly:
        # os.system(f"start {output_audio_file}")
    else:
        print(f"❌ ElevenLabs Cloud Connection Refused: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Test Verification Loop
    speak_briefing_update("Systems fully operational, Caleb. Watchdog automated harvest arrays are actively tracking your desktop workspace.")