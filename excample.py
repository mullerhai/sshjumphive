from ssh_jump_hive import Jump_Tunnel_HIVE
import pandas as pd

def gethive():
  jumphost = '***'
  jumpport = 2222
  jumpuser = 'dm'
  jumppwd = '****'
  tunnelhost = '****'
  tunnelhiveport = 10000
  localhost = '127.0.0.1'
  localbindport = 4800
  username = '****'
  auth = 'LDAP'
  password = "abc123."
  database = 'fkdb'
  table = 'tab_client_label'
  partions_param_dict = {'client_nmbr': 'AA75', 'batch': 'p1'}
  query_fileds_list = ['gid', 'realname', 'card']
  querylimit = 1000
  jump = Jump_Tunnel_HIVE(jumphost, jumpport, jumpuser, jumppwd, tunnelhost, tunnelhiveport, localhost, localbindport,
    username, password)
  return jump

def demo1():
    table = 'tab_client_label'
    partions_param_dict = {'client_nmbr': 'AA75', 'batch': 'p1'}
    query_fileds_list = ['gid', 'realname', 'card']
    querylimit = 1000
    jump=gethive()
    df2=jump.get_JumpTunnel_df(table,partions_param_dict,query_fileds_list,querylimit)
    return df2
def demo2():
  table = 'tab_client_label'
  partions_param_dict = {'client_nmbr': 'AA75', 'batch': 'p1'}
  jump =gethive()
  df2 = jump.get_JumpTunnel_table_partitions_df(table,partions_param_dict,1000)
  return df2

def demo3():
  jump = gethive()
  hsql="select * from fkdb.tab_client_label where  client_nmbr= 'AA75' and batch= 'p1' limit 500"
  df2=jump.get_JumpTunnel_hsql_df(hsql)
  return df2

df3=demo2()
print(df3.shape)
print(df3.columns)
print(df3.head(100))