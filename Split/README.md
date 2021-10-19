# Audio/Split / Nexss Programmer

Split audio to the separate tracks.

## Examples

Note: For the first run for each separation types, it can take a time to download predefined model.

```sh
nexss Audio/Split myfile.mp3 // --_tracks=2  - 2 is default Vocals (singing voice) / accompaniment separation
nexss Audio/Split myfile.mp3 --_tracks=4 // Vocals / drums / bass / other separation
nexss Audio/Split myfile.mp3 --_tracks=5 // Vocals / drums / bass / piano / other separation
```

## Licensing notes

With version 1.0 Nexss Programmer for the package Audio/Split uses great package [Spleeter](https://github.com/deezer/spleeter) (MIT License).
