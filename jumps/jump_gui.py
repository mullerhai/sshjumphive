import sys
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtWidgets import QWidget,QInputDialog,QMainWindow,QDialog,QLabel,QLineEdit,QGridLayout,  QToolTip,QPushButton, QApplication
from jumps.Jump_Tunnel import Jump_Tunnel
import click
import  time
import  logging


jumphost = '117.48.195.186'
jumpport = 2222
jumpuser = 'dm'
jumppwd = 'Vts^pztbvE339@Rw'
tunnelhost = '172.16.16.32'
tunnelappport = 10000
localhost = '127.0.0.1'
localbindport = 4800
daemonsecond=2000
logger = logging.getLogger('ssh-jump-hive-gui')
class JumpTunnel(QWidget):

  def __init__(self):
    super().__init__()

    self.my_UI()


  def my_UI(self):


    jhLabel=QLabel("JumpHost:")
    jpLabel=QLabel("JumpPort:")
    juLable=QLabel("JumpUser:")
    jpwdLabel=QLabel("JumpPwd:")
    thLabel=QLabel("TunnelHost:")
    tpLabel=QLabel("TunnelPort:")
    lhLabel=QLabel("LocalHost:")
    lpLabel=QLabel("LocalPort:")
    gitLabel = QLabel("GithubRepo:")
    dtLabel=QLabel("DaemonSecond:")

    self.jumpHost=QLineEdit()
    self.jumpPort=QLineEdit()
    self.jumpUser=QLineEdit()
    self.jumpPwd=QLineEdit()
    self.tunnelHost=QLineEdit()
    self.tunnelPort=QLineEdit()
    self.localHost=QLineEdit()
    self.localPort=QLineEdit()
    self.daemonSecond=QLineEdit("21600")
    github=QLineEdit("https://github.com/mullerhai/sshjumphive")
    self.btnConn = QPushButton("Trun ON", self)
    self.btnClose=QPushButton("Trun Off",self)
    grid=QGridLayout()
    grid.setSpacing(10)
    grid.addWidget(jhLabel,2,0)
    grid.addWidget(self.jumpHost,2,1)
    grid.addWidget(jpLabel,2,2)
    grid.addWidget(self.jumpPort,2,3)
    grid.addWidget(juLable,3,0)
    grid.addWidget(self.jumpUser,3,1)
    grid.addWidget(jpwdLabel,3,2)
    grid.addWidget(self.jumpPwd,3,3)
    grid.addWidget(thLabel,5,0)
    grid.addWidget(self.tunnelHost,5,1)
    grid.addWidget(tpLabel,5,2)
    grid.addWidget(self.tunnelPort,5,3)
    grid.addWidget(lhLabel,7,0)
    grid.addWidget(self.localHost,7,1)
    grid.addWidget(lpLabel,7,2)
    grid.addWidget(self.localPort,7,3)
    grid.addWidget(gitLabel,8,0)
    grid.addWidget(github,8,1)
    grid.addWidget(dtLabel,8,2)
    grid.addWidget(self.daemonSecond,8,3)
    grid.addWidget(self.btnConn,9,0)
    grid.addWidget(self.btnClose,9,3)
    pixmap = QPixmap("../img/guilogo.jpg")
    pixmap=pixmap.scaledToHeight(80)
    pixmap=pixmap.scaledToWidth(180)
    lbl = QLabel(self)
    lbl.setFixedHeight(80)
    lbl.setFixedWidth(180)
    lbl.setPixmap(pixmap)
    grid.addWidget(lbl,10,1)
    pixfox = QPixmap("../img/tunnel.jpg")
    pixfox=pixfox.scaledToHeight(90)
    pixfox=pixfox.scaledToWidth(90)
    lblfox = QLabel(self)
    lblfox.setFixedHeight(90)
    lblfox.setFixedWidth(90)
    lblfox.setPixmap(pixfox)
    grid.addWidget(lblfox,10,2)
    self.btnConn.clicked.connect(self.buttonClicked)
    self.btnClose.clicked.connect(self.btnCloseSession)
    self.setLayout(grid)
    self.setWindowTitle('SSH-Jump-Hive')
    self.setGeometry(300, 300, 490, 450)
    self.show()

  def btnCloseSession(self):
    text, ok = QInputDialog.getText(self, 'Turn Off',
      'Please Input 1 then Trun off tunnel :')
    logging.warn(msg="Will kill recently ssh tunnle process")
    if ok and text=='1':
      try:
        self.jump_tunnel.client.close()
        logging.info(msg="ssh_tunnel turn off  successfully")
        text, ok = QInputDialog.getText(self, 'Success',
          'ssh_tunnel turn off  successfully close dialog ok')
      except:
        text, ok = QInputDialog.getText(self, 'Failed',
          'ssh_tunnel turn off  failed check the config')
        logging.error(msg="ssh_tunnel turn off failed,please try again")
    else:
      text, ok = QInputDialog.getText(self, 'Failed',
        'ssh_tunnel turn off  failed check the config')
  def buttonClicked(self):  # 在buttonClikced()方法中，我们调用sender()方法来判断哪一个按钮是我们按下的
    jumphost=self.jumpHost.text()
    jumpuser=self.jumpUser.text()
    jumppwd=self.jumpPwd.text()
    tunnelhost=self.tunnelHost.text()
    localhost=self.localHost.text()

    logging.info(msg=self.jumpHost.text()+"%%"+self.jumpUser.text()+"%%"+self.jumpPwd.text())
    try:
      jumpport = (int(self.jumpPort.text()) if self.jumpPort.text() != None else 2222)
      tunnelappport = (int(self.tunnelPort.text()) if self.tunnelPort.text() != None else 10000)
      localbindport = (int(self.localPort.text()) if self.localPort.text() != None else 4320)
      daemonsecond = (int(self.daemonSecond.text()) if self.daemonSecond.text() != None else 21600)

      self.jump_tunnel=Jump_Tunnel(jumphost,jumpport,jumpuser,jumppwd,tunnelhost,tunnelappport,localhost,localbindport)
      tunnel_conn=self.jump_tunnel.jump_con_tunnel()
      with  tunnel_conn:
        logging.info(msg="启动成功")
        text, ok = QInputDialog.getText(self, 'Success',
          'connect ssh tunnel successfully close dialog ok')
        time.sleep(daemonsecond)
    except:
      logging.info(msg="启动失败")
      text, ok = QInputDialog.getText(self, 'Failed',
        'connect ssh tunnel failed check the config')

    #sender = self.sender()
    # self.showMessage(sender.text() + ' 是发送者')

def main():
  app = QApplication(sys.argv)
  jtGui = JumpTunnel()
  sys.exit(app.exec_())


if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = JumpTunnel()
  sys.exit(app.exec_())
