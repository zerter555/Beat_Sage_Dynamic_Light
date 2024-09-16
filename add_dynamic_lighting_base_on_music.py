import json
import os
import random

# Define the root folder (the folder containing all song subfolders)
root_folder = "."  # Change "." to the path of your root folder if not running in the same directory

# Configurable parameters for lighting dynamics
max_effect_duration = 2  # Maximum duration for lighting effects (in beats)
lighting_types = [0, 1, 2, 3, 4]  # Light types: Back Laser, Ring Light, etc.
colors = [1, 2, 3, 4, 5]  # Example colors: Different intensities or colors
effects = [0.5, 1.0, 1.5]  # Effects: Fade, Flash, etc.

# Parameters for atmospheric lighting
atmospheric_lighting_duration = 4  # Duration of atmospheric lighting effects (in beats)
atmospheric_lighting_count = 5  # Number of atmospheric lighting events

# Function to generate atmospheric lighting events
def generate_atmospheric_lighting_events(start_time, duration, types, colors):
    events = []
    for _ in range(atmospheric_lighting_count):
        # Randomly select timing, type, and color for atmospheric effects
        time = start_time + random.uniform(0, duration)
        light_type = random.choice(types)
        color = random.choice(colors)
        effect_duration = random.uniform(0.5, 1.5)  # Duration of the atmospheric lighting effect
        
        # Create the event
        event = {
            "_time": time,
            "_type": light_type,
            "_value": color
        }
        # Add the event to the list
        events.append(event)
    
    return events

# Function to generate lighting events based on note times
def generate_lighting_events_from_notes(note_times, max_effect_duration, types, colors):
    events = []
    
    for time in note_times:
        # Randomly select lighting type and color
        light_type = random.choice(types)
        color = random.choice(colors)
        effect_duration = random.uniform(0.1, max_effect_duration)  # Random duration between 0.1 and max_effect_duration

        # Ensure the effect does not extend beyond the end time
        if time + effect_duration > max(note_times):
            effect_duration = max(note_times) - time

        # Create the event
        event = {
            "_time": time,
            "_type": light_type,
            "_value": color
        }
        # Add the event to the list
        events.append(event)
    
    return events

# Function to extract note times from the difficulty .dat file
def extract_note_times_from_dat(file_path):
    with open(file_path, 'r') as f:
        map_data = json.load(f)
    
    note_times = [note["_time"] for note in map_data.get("_notes", [])]
    
    print(f"Extracted Note Times: {note_times}")
    return note_times

# Function to add lighting events to a specific .dat file
def add_lighting_to_dat_file(file_path, note_times):
    if not note_times:
        print(f"No note times found in {file_path}, skipping...")
        return

    # Load the existing .dat file
    with open(file_path, 'r') as f:
        map_data = json.load(f)

    # Clear existing lighting events
    map_data["_events"] = []

    # Get the start time for the atmospheric lighting events
    start_time = 0  # Start at the beginning of the song

    # Generate and add atmospheric lighting events
    atmospheric_events = generate_atmospheric_lighting_events(start_time, atmospheric_lighting_duration, lighting_types, colors)
    map_data["_events"].extend(atmospheric_events)
    
    # Generate lighting events from note timings
    lighting_events = generate_lighting_events_from_notes(note_times, max_effect_duration, lighting_types, colors)
    map_data["_events"].extend(lighting_events)

    # Save the updated .dat file
    with open(file_path, 'w') as f:
        json.dump(map_data, f, indent=4)

    print(f"Existing lighting events cleared and new music-synced events with atmospheric intro added to {file_path}")

# Main function to iterate over all song folders and process .dat files
def process_all_songs(root_folder):
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
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
                    note_times = extract_note_times_from_dat(file_path)
                    add_lighting_to_dat_file(file_path, note_times)
                else:
                    print(f"File {file_path} not found, skipping...")

# Run the script on all song folders in the root directory
process_all_songs(root_folder)

print("Music-synced dynamic lighting events with atmospheric intro added to all available song difficulty files in the root folder!")
