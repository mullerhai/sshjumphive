from ftplib import FTP
from ftplib import FTP_TLS

class  ftps_client:
  ##初始化的时候会把登录参数赋值初始化
  def __init__(self,host,user,pwd,port=21):
    self.host=host
    self.port=port
    self.user=user
    self.pwd=pwd
    #self._old_makepasv=FTP_TLS.makepasv

## ftp 登录项  含有闭包项
  def login(self,debug=2,set_pasv=True):
    _old_makepasv = FTP_TLS.makepasv
    def _new_makepasv(self):
      host, port = _old_makepasv(self)
      host = self.sock.getpeername()[0]
      return host, port
    FTP_TLS.makepasv = _new_makepasv
    ftps = FTP_TLS(self.host)
    ftps.set_debuglevel(debug)
    ftps.auth()
    ftps.login(self.user,self.pwd)
    ftps.makepasv()
    ftps.sendcmd('pbsz 0')
    ftps.set_pasv(set_pasv)
    ftps.prot_p()
    print("hello ")
    ftps.getwelcome()
    return ftps

  #显示  目录下的 文件列表
  def ftplistDir(self,ftps,sever_path):
    ftps.cwd("/")#首先切换得到根目录下，否则会出现问题
    ftps.cwd(sever_path)
    files = ftps.nlst()
    for f in files:
      print(f)

# 下载服务器文件
  def  ftpDownloadSeverFile(self,ftps,sever_path,sever_file,new_localfile,buffersize=1024):
    ftps.cwd("/")
    ftps.cwd(sever_path)
    with open(new_localfile , 'wb')as download_file:
      ftps.retrbinary('RETR %s' %sever_file , download_file.write, buffersize)

##上传文件
  def  ftpUploadLocalFile(self,ftps,local_filepath,sever_path,new_severfile,buffersize=1024):
    ftps.cwd("/")
    ftps.cwd(sever_path)
    with open(local_filepath,'rb') as  upload_file:
      ftps.storbinary('STOR ' + new_severfile, upload_file, buffersize)


##测试使用 通过
if __name__ == '__main__':
  host = 'ftps.baidu.com'
  port = '21'
  user = 'zh****eng'
  pwd = 'zz****mt.2'
  ip = '117.35.45.150'

  cli=ftp_client(host,user,pwd,port)
  fs= cli.login(2,True)
  #fs.makepasv()
  # files = []
  # files = fs.nlst()
  # for f in files:
  #   print(f)
  path='china'
  cli.ftplistDir(fs,path)