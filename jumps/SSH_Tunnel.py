import paramiko
import logging
import selectors
import socketserver
import threading
import time

logger = logging.getLogger(
    name=__name__,
)


class SSH_Tunnel(
  socketserver.ThreadingTCPServer,
):
  logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  logger = logging.getLogger(__name__)
  daemon_threads = True
  allow_reuse_address = True

  def __init__(
          self,
          paramiko_session,
          remote_host,
          remote_port,
          bind_address_and_port=(
                  '',
                  0,
          ),
  ):
    self.paramiko_session = paramiko_session
    self.remote_host = remote_host
    self.remote_port = remote_port

    super().__init__(
      server_address=bind_address_and_port,
      RequestHandlerClass=SSHForwardingHandler,
      bind_and_activate=True,
    )
    self.bind_address, self.bind_port = self.server_address
    self.server_thread = threading.Thread(
      target=self.serve_forever,
      daemon=True,
    )

  def __str__(
          self,
  ):
    return 'Tunnel to \'{remote_host}:{remote_port}\', bound at \'{bind_address}:{bind_port}\'.'.format(
      remote_host=self.remote_host,
      remote_port=self.remote_port,
      bind_address=self.bind_address,
      bind_port=self.bind_port,
    )

  def start(
          self,
  ):
    self.server_thread.start()

  def __enter__(
          self,
  ):
    self.start()

    return self

  def __exit__(
          self,
          exc_type,
          exc_val,
          exc_tb,
  ):
    self.shutdown()


class SSHForwardingHandler(
  socketserver.BaseRequestHandler,
):
  buffer_size = 1024

  def __init__(
          self,
          request,
          client_address,
          server,
  ):
    self.selector = selectors.DefaultSelector()
    self.ssh_channel = None
    super().__init__(request, client_address, server)

  def _read_from_client(
          self,
          socket_obj,
          mask,
  ):
    self._transfer_data(
      src_socket=socket_obj,
      dest_socket=self.ssh_channel,
    )

  def _read_from_channel(
          self,
          socket_obj,
          mask,
  ):
    self._transfer_data(
      src_socket=socket_obj,
      dest_socket=self.request,
    )

  def _transfer_data(
          self,
          src_socket,
          dest_socket,
  ):
    src_socket.setblocking(
      False,
    )
    data = src_socket.recv(
      self.buffer_size,
    )
    if len(data):
      try:
        dest_socket.send(
          data,
        )
      except BrokenPipeError:
        self.finish()

  def handle(
          self,
  ):
    peer_name = self.request.getpeername()
    try:
      self.ssh_channel = self.server.paramiko_session.get_transport().open_channel(
        kind='direct-tcpip',
        dest_addr=(
          self.server.remote_host,
          self.server.remote_port,
        ),
        src_addr=peer_name,
      )
    except Exception as error:
      logger.error(
        msg='Incoming request to {host}:{port} failed.'.format(
          host=self.server.remote_host,
          port=self.server.remote_port,
        ),
      )

      raise paramiko.SSHException(
        error,
      )
    else:
      self.selector.register(
        fileobj=self.ssh_channel,
        events=selectors.EVENT_READ,
        data=self._read_from_channel,
      )
      self.selector.register(
        fileobj=self.request,
        events=selectors.EVENT_READ,
        data=self._read_from_client,
      )
      if self.ssh_channel is None:
        logger.warning(
          msg='Incoming request to {host}:{port} was rejected by the SSH server.'.format(
            host=self.server.remote_host,
            port=self.server.remote_port,
          ),
        )

        self.finish()

      while True:
        events = self.selector.select()
        for key, mask in events:
          callback = key.data
          callback(
            socket_obj=key.fileobj,
            mask=mask,
          )
          if self.server._BaseServer__is_shut_down.is_set():
            self.finish()
        time.sleep(0)

  def finish(
          self,
  ):

    if self.ssh_channel is not None:
      try:
        self.ssh_channel.shutdown(
          how=2,
        )
        self.ssh_channel.close()
      except Exception:
        self.request.shutdown(2, )
        self.request.close()
  # except Exception :
  #   logger.error(" maybe socket has something wrong but maybe you can get data result ,it's just work")
  # finally:
  #   logger.info("do next program")
