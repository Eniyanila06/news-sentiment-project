from gtts import gTTS
import os

def generate_hindi_speech(text, output_filename="output.mp3"):
    try:
        # Convert text to speech in Hindi
        tts = gTTS(text=text, lang="hi")
        
        # Save the audio file
        tts.save(output_filename)
        print(f"✅ Hindi speech saved as {output_filename}")

        # Play the audio file (Optional: Uncomment this if you want it to play automatically)
        os.system(f"start {output_filename}")  # Works on Windows
        # os.system(f"afplay {output_filename}")  # Use this for Mac
        # os.system(f"mpg321 {output_filename}")  # Use this for Linux

    except Exception as e:
        print(f"⚠️ Error generating speech: {e}")

# Example usage
if __name__ == "__main__":
    sample_text = "यह एक उदाहरण है कि हम हिंदी में टेक्स्ट को स्पीच में कैसे बदल सकते हैं।"
    generate_hindi_speech(sample_text, "hindi_output.mp3")
