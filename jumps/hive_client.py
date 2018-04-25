from pyhive import hive
import pandas as  pd
import logging




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

