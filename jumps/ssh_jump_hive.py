from pyhive import hive
import pandas as  pd
import paramiko
import logging
import selectors
import socketserver
import threading
import time



class hive_client:

  def __init__(self,host,user,pwd,port=10000,database='fkdb',auth='LDAP'):
    self.host=host
    self.user=user
    self.pwd=pwd
    self.port=port
    self.database=database
    self.auth=auth

  def connhive(self,database='fkdb',auth='LDAP'):
    conn = hive.Connection(host=self.host, port=self.port, username=self.user, auth=self.auth, password=self.pwd,
      database=self.database)
    logger.info(msg="hive server connect sucessfully {hivehost:%s,hiveport:%d,hiveuser:%s,hivepwd:%s,hiveauth:%s,hivedatabase:%s}"%(
      self.host,self.port,self.user,self.pwd,self.auth,self.database
    ))
    return conn

  def query_AllFileds_Dataframe(self,conn,table,param_dict,limit=None):
    base_table = self.database + '.' + table
    query_part='select * from %s where '%base_table
    params = []
    for key, value in param_dict.items():
      params.append(' '+key + '= \'%s\' ' % value + 'and')
    paramstemp = ''.join(params)
    params = paramstemp[:-3]
    if limit==None:
      hsql = query_part + params
    else:
      hsql=query_part+params+' limit %d'%limit
    logger.info(msg="exec hsql : %s"%hsql)
    # cursor=conn.cursor()
    # cursor.execute(hsql)
    # dataframe=pd.DataFrame(cursor.fetchall())
    dataframe = pd.read_sql(hsql, conn)
    return dataframe

  def query_selectFileds_Dataframe(self,conn,table,filed_list,param_dict,limit=None):
    base_table = self.database + '.' + table
    fileds=','.join(filed_list)
    query_part='select %s  from %s where '%(fileds,base_table)
    params = []
    for key, value in param_dict.items():
      params.append(' '+key + '= \'%s\' ' % value + 'and')
    paramstemp = ''.join(params)
    params = paramstemp[:-3]
    if limit==None:
      hsql = query_part + params
    else:
      hsql=query_part+params+ ' limit %d'%limit
    logger.info(msg="exec hsql : %s" % hsql)
    cursor = conn.cursor()
    cursor.execute(hsql)
    #dataframe=pd.DataFrame(cursor.fetchall())
    dataframe=pd.read_sql(hsql,conn,columns=filed_list)
    return dataframe



  def drop_partition(self,cursor,table,partition_param):
    base_table=self.database+'.'+table
    hsql_part='alter table %s drop if  exists  partition ( '%base_table
    params=[]
    for key, value in partition_param.items():
      params.append(key+'= \'%s\''%value+',')
    paramstemp=''.join(params)
    params=paramstemp[:-1]
    hsql=hsql_part+params+');'
    logger.info(msg="exec hsql : %s" % hsql)
    cursor.execute(hsql)

  def queryby_hsql_df(self,conn,hsql):
    logger.info(msg="exec hsql : %s" % hsql)
    cursor = conn.cursor()
    cursor.execute(hsql)
    # dataframe=pd.DataFrame(cursor.fetchall())
    dataframe = pd.read_sql(hsql, conn)
    return dataframe

logger = logging.getLogger(
    name=__name__,
)


class SSH_Tunnel(
    socketserver.ThreadingTCPServer,
):
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
            except Exception :
              self.request.shutdown(2,)
              self.request.close()
      # except Exception :
      #   logger.error(" maybe socket has something wrong but maybe you can get data result ,it's just work")
      # finally:
      #   logger.info("do next program")

class Jump_Tunnel_HIVE:
  logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  logger = logging.getLogger(__name__)
  def __init__(self,jumphost,jumpport,jumpuser,jumppwd,tunnelhost,tunnelAPPport,localhost,localbindport,hiveusername, hivepassword):
    self.jumphost=jumphost
    self.jumpport=jumpport
    self.jumpuser=jumpuser
    self.jumppwd=jumppwd
    self.tunnelhost=tunnelhost
    self.tunnelAPPport=tunnelAPPport
    self.localhost=localhost
    self.localBindport=localbindport
    self.hiveusername=hiveusername
    self.hivepassword=hivepassword
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
  # 获取hive数据生成 pandas dataframe ，
  # 参数 ：表名  分区参数字典  要查询的字段名列表，查询数量 默认  ，查询数据库 默认  登录hive方式 默认
  # pip install paramiko paramiko_tunnel  pyhive
  def get_JUMP_df(self,table, partions_param_dict, query_fileds_list, query_limit=100, database='fkdb', auth='LDAP'):
    tun=self.jump_con_tunnel()
    with tun:
       hive_cli = hive_client(self.localhost, self.hiveusername,self.hivepassword,self.localBindport)
       conn = hive_cli.connhive(database, auth)
       pd_dataframe = hive_cli.query_selectFileds_Dataframe(conn, table, query_fileds_list, partions_param_dict, query_limit)
       return pd_dataframe


  def get_JumpTunnel_df(self,table, partions_param_dict, query_fileds_list, query_limit=100, database='fkdb', auth='LDAP'):
    client = self.jump_connect()
    with  SSH_Tunnel(
      paramiko_session=client,
      remote_host=self.tunnelhost,
      remote_port=self.tunnelAPPport,
      bind_address_and_port=(self.localhost, self.localBindport),
    ) as tunnel :
       logger.info(msg="the ssh tunnel  for jump server %s" % tunnel)
       hive_cli = hive_client(self.localhost, self.hiveusername,self.hivepassword,self.localBindport)
       conn = hive_cli.connhive(database, auth)
       pd_dataframe = hive_cli.query_selectFileds_Dataframe(conn, table, query_fileds_list, partions_param_dict, query_limit)
       return pd_dataframe
  def get_JumpTunnel_hsql_df(self,hsql, database='fkdb', auth='LDAP'):
    client = self.jump_connect()
    with  SSH_Tunnel(
            paramiko_session=client,
            remote_host=self.tunnelhost,
            remote_port=self.tunnelAPPport,
            bind_address_and_port=(self.localhost, self.localBindport),
    ) as tunnel:
      logger.info(msg="the ssh tunnel  for jump server %s" % tunnel)
      hive_cli = hive_client(self.localhost, self.hiveusername, self.hivepassword, self.localBindport)
      conn = hive_cli.connhive(database, auth)
      pd_dataframe=hive_cli.queryby_hsql_df(conn,hsql)
      return  pd_dataframe

  def get_JumpTunnel_table_partitions_df(self,table,param_dict,limit=None, database='fkdb', auth='LDAP'):
    client = self.jump_connect()
    with  SSH_Tunnel(
            paramiko_session=client,
            remote_host=self.tunnelhost,
            remote_port=self.tunnelAPPport,
            bind_address_and_port=(self.localhost, self.localBindport),
    ) as tunnel:
      logger.info(msg="the ssh tunnel  for jump server %s" % tunnel)
      hive_cli = hive_client(self.localhost, self.hiveusername, self.hivepassword, self.localBindport)
      conn = hive_cli.connhive(database, auth)
      pd_dataframe = hive_cli.query_AllFileds_Dataframe(conn,table,param_dict,limit)
      return pd_dataframe

  def alter_table_Tunnel_by_hsql(self,hsql, database='fkdb', auth='LDAP'):
    client = self.jump_connect()
    with  SSH_Tunnel(
            paramiko_session=client,
            remote_host=self.tunnelhost,
            remote_port=self.tunnelAPPport,
            bind_address_and_port=(self.localhost, self.localBindport),
    ) as tunnel:
      logger.info(msg="the ssh tunnel  for jump server %s" % tunnel)
      hive_cli = hive_client(self.localhost, self.hiveusername, self.hivepassword, self.localBindport)
      conn = hive_cli.connhive(database, auth)
      cursor=conn.cursor()
      try:
        cursor.execute(hsql)
        logger.info(msg="hive cursor exec  successfully for : [ %s ]"%hsql)
      except:
        logger.error(msg="hive cursor  exec failed for [ %s ]"%hsql)