
import pandas as pd
from jumps.Jump_Tunnel_HIVE import Jump_Tunnel_HIVE
from jumps.SSH_Tunnel import  SSH_Tunnel
from jumps.hive_client import hive_client

username = 'zhuzheng'
password = "abc123."
localhost=""
localbindport=""
cli = hive_client(localhost, username, password, localbindport)
conn = cli.connhive()
table = 'tab_client_label'
partions_param_dict = {'client_nmbr': 'AA75', 'batch': 'p1'}
query_fileds_list = ['gid', 'realname', 'card']
querylimit = 1000
df = cli.query_selectFileds_Dataframe(conn, table, query_fileds_list, partions_param_dict, querylimit)
print(df.shape)

def gethive(localport):
  jumphost = '117.48.195.186'
  jumpport = 2222
  jumpuser = 'dm'
  jumppwd = 'Vts^pztbvE339@Rw'
  tunnelhost = '172.16.16.32'
  tunnelhiveport = 10000
  localhost = '127.0.0.1'
  localbindport =localport
  username = 'zhuzheng'
  password = "abc123."
  jump = Jump_Tunnel_HIVE(jumphost, jumpport, jumpuser, jumppwd, tunnelhost, tunnelhiveport, localhost, localbindport,
    username, password)
  return jump

def demo1():
    table = 'tab_client_label'
    partions_param_dict = {'client_nmbr': 'AA75', 'batch': 'p1'}
    query_fileds_list = ['gid', 'realname', 'card']
    querylimit = 1000
    jump=gethive(4100)
    df2=jump.get_JumpTunnel_df(table,partions_param_dict,query_fileds_list,querylimit)
    return df2
def demo2():
  table = 'tab_client_label'
  partions_param_dict = {'client_nmbr': 'AA75', 'batch': 'p1'}
  jump =gethive(4322)
  df2 = jump.get_JumpTunnel_table_partitions_df(table,partions_param_dict,1000)
  return df2

def demo3():
  jump = gethive(4534)
  hsql="select * from fkdb.tab_client_label where  client_nmbr= 'AA75' and batch= 'p1' limit 500"
  df2=jump.get_JumpTunnel_hsql_df(hsql)
  return df2

df3=demo1()
print(df3.shape)
print(df3.columns)
print(df3.head(100))
# df3=demo2()
# print(df3.shape)
# print(df3.columns)
# print(df3.head(100))
# df3=demo3()
# print(df3.shape)
# print(df3.columns)
# print(df3.head(100))