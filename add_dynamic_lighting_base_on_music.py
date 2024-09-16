import json
import os
import random
import librosa  # Library for audio analysis
import numpy as np

# Define the root folder (the folder containing all song subfolders)
root_folder = "."  # Change "." to the path of your root folder if not running in the same directory

# Configurable parameters for lighting dynamics
max_effect_duration = 2  # Maximum duration for lighting effects (in beats)
lighting_types = [0, 1, 2, 3, 4]  # Light types: Back Laser, Ring Light, etc.
colors = [1, 2, 3, 4, 5]  # Example colors: Different intensities or colors
effects = [0.5, 1.0, 1.5]  # Effects: Fade, Flash, etc.

# Function to generate lighting events based on beat timings
def generate_lighting_events_from_beats(beat_times, max_effect_duration, types, colors, effects):
    events = []
    
    for time in beat_times:
        # Randomly select lighting type, color, and effect
        light_type = random.choice(types)
        color = random.choice(colors)
        effect_duration = random.uniform(0.1, max_effect_duration)  # Random duration between 0.1 and max_effect_duration
        
        # Create the event
        event = {
            "_time": time,
            "_type": light_type,
            "_value": color,
            "_floatValue": effect_duration
        }
        # Add the event to the list
        events.append(event)
    
    return events

# Function to extract beat times from the audio file using librosa
def extract_beats_from_audio(audio_file):
    # Load the audio file
    y, sr = librosa.load(audio_file, sr=None)

    # Get the tempo (BPM) and beat timings
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    
    # Convert the beat frames to time (in seconds)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    
    print(f"Detected BPM: {tempo}")
    print(f"Detected Beat Times: {beat_times}")

    return beat_times

# Function to add lighting events to a specific .dat file
def add_lighting_to_dat_file(file_path, beat_times):
    # Load the existing .dat file
    with open(file_path, 'r') as f:
        map_data = json.load(f)

    # Clear existing lighting events
    map_data["_events"] = []

    # Generate lighting events from beat timings
    lighting_events = generate_lighting_events_from_beats(beat_times, max_effect_duration, lighting_types, colors, effects)

    # Add the new lighting events to the _events section of the map
    map_data["_events"].extend(lighting_events)

    # Save the updated .dat file
    with open(file_path, 'w') as f:
        json.dump(map_data, f, indent=4)

    print(f"Existing lighting events cleared and new music-synced events added to {file_path}")

# Main function to iterate over all song folders and process audio and .dat files
def process_all_songs(root_folder):
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            # Check for either song.ogg or song.egg audio file in the folder
            audio_file_path = None
            if os.path.exists(os.path.join(folder_path, "song.ogg")):
                audio_file_path = os.path.join(folder_path, "song.ogg")
            elif os.path.exists(os.path.join(folder_path, "song.egg")):
                audio_file_path = os.path.join(folder_path, "song.egg")
            
            if audio_file_path:
                print(f"Processing audio file: {audio_file_path}")
                # Extract beat times from the audio file
                beat_times = extract_beats_from_audio(audio_file_path)
                
                # Check for difficulty .dat files in the song folder
                difficulty_files = {
                    "Normal": os.path.join(folder_path, "Normal.dat"),
                    "Hard": os.path.join(folder_path, "Hard.dat"),
                    "Expert": os.path.join(folder_path, "Expert.dat"),
                    "ExpertPlus": os.path.join(folder_path, "ExpertPlus.dat")
                }

                # Process each difficulty file
                for difficulty, file_path in difficulty_files.items():
                    if os.path.exists(file_path):
                        add_lighting_to_dat_file(file_path, beat_times)
                    else:
                        print(f"File {file_path} not found, skipping...")
            else:
                print(f"No audio file found in {folder_path}, skipping...")

# Run the script on all song folders in the root directory
process_all_songs(root_folder)

print("Music-synced dynamic lighting events added to all available song difficulty files in the root folder!")
