import python_artnet as Artnet
from logger_settings import Logger
from Hyperdeck_controller import Hyperdeck

verbose=5
logger = Logger(name=__name__, level=verbose).get_logger()

def main():
    logger.debug("Starting")
    hyperdeck = Hyperdeck(port=9993, host_ip='192.168.197.22')
    artNet = Artnet.Artnet(DEBUG=True, SYSIP="192.168.111.246")
    
    while True:
        artNetPacket = artNet.readBuffer()[0]
        dmxPacket = artNetPacket.data
        if dmxPacket is not None:
            logger.debug(f"Data: {dmxPacket}")
    
    


if __name__ == "__main__":
    main()