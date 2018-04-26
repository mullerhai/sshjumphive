import paramiko
import logging
import selectors
import socketserver
import threading
import time
from .SSH_Tunnel import SSH_Tunnel

logger = logging.getLogger(
    name=__name__,
)

class Jump_Tunnel:

  def __init__(self,jumphost,jumpport,jumpuser,jumppwd,tunnelhost,tunnelAPPport,localhost,localbindport):
    self.jumphost=jumphost
    self.jumpport=jumpport
    self.jumpuser=jumpuser
    self.jumppwd=jumppwd
    self.tunnelhost=tunnelhost
    self.tunnelAPPport=tunnelAPPport
    self.localhost=localhost
    self.localBindport=localbindport

  def  jump_connect(self):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(
      paramiko.AutoAddPolicy(),
    )
    client.connect(
      hostname=self.jumphost,
      port=self.jumpport,
      username=self.jumpuser,
      password=self.jumppwd,
    )
    logger.info(msg="jump server info :{host: %s, port: %d,username: %s,password: %s}"%(self.jumphost,self.jumpport,self.jumpuser,self.jumppwd))

    return client
  def  jump_con_tunnel(self):
    client=self.jump_connect()
    tunnel=SSH_Tunnel(
            paramiko_session=client,
            remote_host=self.tunnelhost,
            remote_port=self.tunnelAPPport,
            bind_address_and_port=(self.localhost,self.localBindport),
    )
    logger.info(msg="the ssh tunnel  for jump server %s" %tunnel)
    return tunnel

  def  hold_ssh_tunnel_session(self,daemonSecond):
    jump_tunnel=Jump_Tunnel(self.jumphost,self.jumpport,self.jumpuser,self.jumppwd,self.tunnelhost,self.tunnelAPPport,self.localhost,self.localbindport)
    tunnel=jump_tunnel.jump_con_tunnel()
    try:
      with  tunnel:
        logger.info("ssh_tunnel_session create successfully ")
        time.sleep(daemonSecond)
    except:
      logger.error("ssh_tunnel_session create failed")