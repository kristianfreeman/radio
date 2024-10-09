# Radio

Tools for creating radio stations at home, based on podcasts and music.

This project allows you to configure and run customizable media stations for podcasts and music using [Liquidsoap](https://www.liquidsoap.info/). Stations can shuffle media, combine podcasts with background music, and more.

## Features

- **Custom Stations:** Define stations to play music, podcasts, or a mix of both.
- **Shuffle:** Enable shuffle mode for random playback within a station.
- **Mixed Stations:** Combine podcasts with background music, adjusting volume levels for each.

## Quick Start

1. Install dependencies:
   - [Liquidsoap](https://www.liquidsoap.info/) - installing Liquidsoap is not easy. I recommend using `opam` to install it, including opus support
   - [FFmpeg](https://ffmpeg.org/)

2. Clone this repository and create your configuration file:
   ```bash
   cp config.yaml.example config.yaml
   ```

3. Edit `config.yaml` to define your stations and media directories.

4. Build and run the radio station:
   ```bash
   make
   ```

## Configuration Example

```yaml
stations:
  # Podcasts
  - name: business
    directories:
      - "/podcasts/business-podcast"
      - "/podcasts/business-podcast2"
    shuffle: true
  - name: business_focus
    directories:
      - "/podcasts/business-podcast"
      - "/podcasts/business-podcast2"
    music_directories:
      - "/music/bgm"
    podcast_volume: 0.7
    music_volume: 0.3
    shuffle: true
  # Music
  - name: edm
    directories:
      - "/music/techno"
```

## License

Open-source. Modify and distribute freely.
