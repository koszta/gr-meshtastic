# GnuRadio Meshtastic Sink

Sends the decoded Lora packets to meshtasticd via the simulation port.

https://meshtastic.org/docs/software/meshtasticator/

In this case via the TCP or the HTTP api you can send packets to a device
that does not have an actual Lora radio. The meshtastic firmware has a simulated radio interface.
When you send a packet using ToRadio protobuf that has a port number SIMULATOR_APP,
it simulates that the interface has actually received the packet.

https://github.com/meshtastic/firmware/blob/master/src/platform/portduino/SimRadio.cpp

https://buf.build/meshtastic/protobufs/docs/main:meshtastic#meshtastic.ToRadio

https://buf.build/meshtastic/protobufs/file/main:meshtastic/portnums.proto#L173

## How to install

```sh
cd build
cmake ..
make
sudo make install
```

Install GNURadio and Lora SDR

https://github.com/tapparelj/gr-lora_sdr

Download a GNURadio file that is matching your area.

https://gitlab.com/crankylinuxuser/meshtastic_sdr/-/tree/master/gnuradio%20scripts/RX?ref_type=heads

Replace ZeroMQ sink with the meshtastic block.

Set the base64 encoded key and the url of your meshtastic device.

## Thanks

This project could not exist without Josh Conway's meshtastic_sdr project.

https://gitlab.com/crankylinuxuser/meshtastic_sdr
