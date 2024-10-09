import yaml

def generate_liquidsoap_script(station_name, directories, music_directories, shuffle, podcast_volume=0.7, music_volume=0.3):
    playlists = [f'playlist("{dir}", reload_mode="watch")' for dir in directories]
    
    if shuffle:
        podcast_source = f'random(weights=[{",".join(["1" for _ in directories])}], [{", ".join(playlists)}])'
    else:
        podcast_source = f'fallback([{", ".join(playlists)}])'
    
    music_playlists = [f'playlist("{dir}", reload_mode="watch")' for dir in music_directories]
    music_source = f'random(weights=[{",".join(["1" for _ in music_directories])}], [{", ".join(music_playlists)}])'
    
    script = f"""
# Radio station: {station_name}

# Podcast source
podcast = {podcast_source}

# Music source
music = {music_source}

# Audio processing
def process(source)
  # Normalize audio
  source = normalize(source)
  # Compress audio for radio-style sound
  source = compress(source, threshold=-15., ratio=3., attack=20., release=150.)
  source
end

# Mixing function
def mix(podcast, music)
  # Adjust volume of podcast and music
  podcast = amplify({podcast_volume}, podcast)
  music = amplify({music_volume}, music)
  
  # Mix podcast and music
  mixed = add([podcast, music])
  
  # Process the mixed audio
  process(mixed)
end

# Create the mixed source
radio = mix(podcast, music)

# Handle fallible source
radio = mksafe(radio)

# Harbor output (built-in HTTP streaming)
output.harbor(
  %opus,
  mount = "/{station_name}",
  port = 8000,
  radio)
"""
    return script

def main():
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

    liquidsoap_scripts = []

    for station in config["stations"]:
        name = station["name"]
        directories = station["directories"]
        music_directories = station.get("music_directories", [])
        shuffle = station.get("shuffle", False)
        podcast_volume = station.get("podcast_volume", 0.7)
        music_volume = station.get("music_volume", 0.3)

        script = generate_liquidsoap_script(name, directories, music_directories, shuffle, podcast_volume, music_volume)
        liquidsoap_scripts.append(script)

    # Write the combined Liquidsoap script
    with open("radio_stations.liq", "w") as output_file:
        output_file.write("\n".join(liquidsoap_scripts))

    print("Liquidsoap script generated: radio_stations.liq")
    print(f"Created {len(config['stations'])} radio stations.")
    print("All stations are accessible on port 8000 with their respective mount points.")
    for station in config["stations"]:
        print(f"  http://localhost:8000/{station['name']}")

if __name__ == "__main__":
    main()
