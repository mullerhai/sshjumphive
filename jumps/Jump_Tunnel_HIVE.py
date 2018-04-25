from pyhive import hive
import pandas as  pd
import paramiko
import logging
import selectors
import socketserver
import threading
import time
from jumps.hive_client import hive_client
from jumps.SSH_Tunnel import  SSH_Tunnel

logger = logging.getLogger(
    name=__name__,
)

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
        logger.error(msg="hive cursor  exec failed for [ %s ]" % hsql)