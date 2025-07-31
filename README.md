# GnuRadio Meshtastic Sink

A GNU Radio Out-of-Tree (OOT) module that bridges Software-Defined Radio (SDR) with Meshtastic mesh networks by sending decoded LoRa packets to a Meshtastic device via its simulation interface.

## Overview

This module enables you to receive LoRa radio transmissions using an SDR receiver, decode them with GNU Radio, and forward them to Meshtastic firmware through its simulation port. This allows for:

- Monitoring Meshtastic mesh network traffic without a dedicated LoRa radio
- Testing and debugging Meshtastic applications
- Creating hybrid SDR/Meshtastic systems
- Learning about LoRa packet structure and Meshtastic protocol

## How It Works

1. Your SDR hardware receives LoRa radio signals
2. GNU Radio + gr-lora_sdr processes and decodes the LoRa modulation
3. This module (gr-meshtastic) takes the decoded packets, wraps them in a simulation packet and sends them via HTTP API.

The Meshtastic firmware has a simulated radio interface that can receive packets without actual LoRa hardware. When you send a packet using ToRadio protobuf with port number SIMULATOR_APP, it simulates that the interface has actually received the packet.

## Prerequisites

- GNU Radio 3.X
- gr-lora_sdr (https://github.com/tapparelj/gr-lora_sdr)
- A working Meshtastic installation with meshtasticd
- Python libraries: cryptography, requests, protobuf
- Meshtastic Python API (`pip install meshtastic`)

## Installation

```sh
cd build
cmake ..
make
sudo make install
```

After installation, restart GNU Radio Companion to see the new Meshtastic block.

## Usage

1. Download a GNU Radio flowgraph that matches your region's LoRa settings:
   - [Meshtastic SDR Examples](https://gitlab.com/crankylinuxuser/meshtastic_sdr/-/tree/master/gnuradio%20scripts/RX?ref_type=heads)

2. Open the flowgraph in GNU Radio Companion

3. Replace the ZeroMQ sink with the Meshtastic block

4. Configure the Meshtastic block:
   - Set the `key` parameter to your base64-encoded Meshtastic channel key
   - Set the `url` parameter to your Meshtastic device's API endpoint (e.g., "http://localhost:4403" or "http://192.168.4.1")

5. Run the flowgraph to start receiving and forwarding packets

## Block Parameters

- **key** (string): Base64-encoded encryption key for your Meshtastic channel
- **url** (string): HTTP URL for your Meshtastic device's API endpoint

## Relevant Documentation

- [Meshtastic Project](https://meshtastic.org/)
- [Meshtastic Python API](https://meshtastic.org/docs/software/python/api/)
- [Meshtastic Protocol Buffers](https://buf.build/meshtastic/protobufs/docs/main:meshtastic)
- [Meshtastic Simulation Interface](https://github.com/meshtastic/firmware/blob/master/src/platform/portduino/SimRadio.cpp)
- [ToRadio Protocol](https://buf.build/meshtastic/protobufs/docs/main:meshtastic#meshtastic.ToRadio)
- [Port Numbers Reference](https://buf.build/meshtastic/protobufs/file/main:meshtastic/portnums.proto#L173)

## Troubleshooting

- Ensure your SDR is properly tuned to the correct frequency for your region's Meshtastic network
- Verify that your Meshtastic device is running and accessible at the specified URL
- Check that you're using the correct channel encryption key
- For HTTP connection issues, check if your meshtasticd is running and the API is enabled

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## Acknowledgements

This project could not exist without Josh Conway's meshtastic_sdr project:
- https://gitlab.com/crankylinuxuser/meshtastic_sdr

## License

GPLv3 - See LICENSE file for details

## Author

Peter Pal Koszta
