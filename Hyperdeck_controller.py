import sys
import os
import time
import socket
import ipaddress
from typing import Optional
from logger_settings import Logger


def validate_ipaddress(host_string):
    try:
        ip_object = ipaddress.ip_address(host_string)
        return ip_object
    except ValueError:
        print(f'ERROR: Could not validate ip: {host_string}')
        return 0
    
    
    
class Hyperdeck:
    def __init__(self, port: int, host_ip: str, verbose=5) -> None:
        self.logger = Logger(name=__name__, level=verbose).get_logger()
        if validate_ipaddress:
            self._location = (host_ip, port)
            self.logger.debug(f'Will use HOST IP: {self._location}')
        else:
            self.logger.error(f'ERROR: {host_ip} is not a valid IP')
            return False 
    
    def _connect(self):
        try:
            self.logger.debug("Trying connection")
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.settimeout(30)
            self._sock.connect(self._location)
        except:
            self.logger.debug("Connection failed")
            return False
        response_key = self._receive_response()
        self.logger.debug(response_key)
        return True
        
        
    def _close_connection(self):
        self._sock.close()
        
    def _send_command(self, command: str) -> Optional[str]:
        ## First we make the connection
        if not self._connect():
            error_dict = {"ERROR": "Could not make connection to device"}
            self.logger.debug(error_dict)
            return error_dict

        ## Now send command
        command = f'{command}\r\n'
        command_binary = str.encode(command, "utf-8")
        self.logger.debug(f'Sending command: {command_binary}')
        
        self._sock.send(command_binary)
        self.logger.debug(self._sock)
        try:
            response = self._receive_response()
            self.logger.debug(f"Response: {response}")
        except:
            response = []
        return {"Sending": command, "Response": response}    
    
    
    def _receive_response(self) -> Optional[dict]:
        response_payload = ""
        while True:
            try:
                # # We read 32 bytes at the time
                response = self._sock.recv(2048)
                # # Now add to our response_payload
                response_payload = f"{response_payload}{response.decode('utf-8')}"
                self.logger.debug(response)
                if response_payload.endswith('\r\n'):
                    self.logger.debug(response_payload)
                    return response_payload
                else: 
                    self.logger.debug(response_payload)
                    return response_payload

            except socket.timeout:
                self.logger.error("Could not get answer")
                break
            
    def play_clip_single(self, clip_id):
        ## First we do a goto
        command = f"goto: clip id: {clip_id}"
        self._send_command(command=command)
        ## Now we play
        command = "play: single clip: true"
        self._send_command(command=command)
    
    
if __name__ == "__main__":
    print("Starting")
    hyperdeck = Hyperdeck(port=9993, host_ip='192.168.197.22')
    hyperdeck.play_clip_single(clip_id=2)
    
    hyperdeck._send_command("transport info")
    time.sleep(3)
    hyperdeck._send_command("transport info")
    
    
    print("End")
    