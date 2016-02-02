# APT demodulator 
This is a POC to demodulate and show the radar images from NOAA satellites, with the APT protocol. 

There's a sample signal avalaible from [gnuradio](https://gnuradio.org/redmine/projects/gnuradio/wiki/SampleData). The scripts search in the current working directory for `noaa-12_256k.dat`.

End goal is to visualize images line by line as the satellite passes, with rolling corrections for Doppler shift.
