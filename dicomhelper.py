import os
import sys
import shutil
import pydicom
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import QEvent
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog, QMessageBox
from PyQt5.QtCore import QStringListModel, QPoint
from ui import Ui_MainWindow
from cipher import Cipher


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(Main, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._init_variables()
        self._init_models()
        self._bind_actions()

    def _init_variables(self):
        self.exclude_extensions = [
            # 过滤某些特殊后缀的文件名
            "py", "gz", "rar", "ini", "nii",
        ]
        self.exclude_filenames = [
            ".DS_Store",
            "VERSION",
        ]
        # 全局的一个秘钥串
        self.secret_seed = ""
        self.checksmap = {
            "PatientID": False,
            "PatientName": False,
            "PatientBirthDate": False,
            "PatientSex": False,
            "InstitutionName": False,
            # "PatientAddress": True,
            # "PatientTelephoneNumbers": True,
        }
        self.PREFIX = "Anonymous_"
        self.cipher = Cipher()
        self.CIPHER_METHOD_ENCRYPT = "encrypt"
        self.CIPHER_METHOD_DECRYPT = "decrypt"
        self.CIPHER_METHOD_CUSTOM = "custom"
        self.DCM_EXTENSION = ".dcm"
        self.CUSTOM_SUFFIX = ""
        self.CHECK_OPTION_SOURCE_CUSTOM = "custom"
        self.CHECK_OPTION_SOURCE_COMMON = "common"
        self.keyProperties = [
            # 机构信息
            "InstitutionName",
            # 患者信息
            "PatientName", "PatientID", "IssuerOfPatientID", "PatientBirthDate", "PatientSex", "OtherPatientIDs",
            "PatientAge", "PatientSize", "PatientWeight", "AdditionalPatientHistory",
            # 症状描述
            "ContrastBolusAgent", "BodyPartExamined",
        ]

    # listview 中用到的俩模型
    def _init_models(self):
        self.undolist = []
        self.donelist = []
        self.undomodel = QStringListModel()
        self.donemodel = QStringListModel()

    def _bind_actions(self):
        # 绑定文件选项
        self.actionwenjian.triggered.connect(self._get_file_path)
        self.actionwenjianjia.triggered.connect(self._get_folder_path)

        # listview-model 的事件监听

        # 绑定秘钥选取处理
        self.actionmiyao.triggered.connect(self._get_secret_string)
        # 绑定关于菜单
        self.actionabout.triggered.connect(self._about)

        # 绑定文件夹切割窗口
        self.actionfoldersplit.triggered.connect(self._file_split)

        # 绑定按钮事件
        self.niming.clicked.connect(self._handle_niming)
        self.customniminghua.clicked.connect(self._handle_customniming)
        self.adddcm.clicked.connect(self._handle_add_dcmextension)
        self.deletedcm.clicked.connect(self._handle_delete_dcmextension)
        self.doneclean.clicked.connect(self._handle_clean_donelistview)

    def _handle_clean_donelistview(self):
        self.donelist = []
        self._update_listview()

    def _update_listview(self):
        self.undolist = list(set(self.undolist) - set(self.donelist))
        self.undomodel.setStringList(self.undolist)
        self.listViewundo.setModel(self.undomodel)
        self.donemodel.setStringList(self.donelist)
        self.listViewdone.setModel(self.donemodel)

    def _handle_add_dcmextension(self):
        self.changed_filenames = []
        for filename in self.undolist:
            newname = filename + self.DCM_EXTENSION
            try:
                os.rename(filename, newname)
            except:
                continue
            self.changed_filenames.append(newname)
        succ = len(self.changed_filenames)
        if succ == 0:
            msg = "暂时没有文件要修改"
        else:
            msg = "成功修改了{}个文件！".format(succ)

        # 更新 UI
        self.undolist = list(set(self.undolist) - set(self.changed_filenames))
        self.donelist = self.changed_filenames
        self._update_listview()
        self.statusbar.showMessage(msg)
        QMessageBox.information(self, "处理结果", msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    def _handle_delete_dcmextension(self):
        self.undolist = []
        succ = 0
        for filename in self.changed_filenames:
            filename = str(filename)
            if not filename.endswith(self.DCM_EXTENSION):
                continue
            newname = os.path.splitext(filename)[0]
            try:
                os.rename(filename, newname)
            except:
                continue
            succ += 1
        # 将改动展示到状态栏
        if succ == 0:
            msg = "暂时没有文件要撤销"
        else:
            msg = "成功撤销了{}个文件！".format(succ)
        # 更新 UI
        self.undolist = [item.strip(self.DCM_EXTENSION) for item in self.changed_filenames]
        self.donelist = []
        self._update_listview()
        self.statusbar.showMessage(msg)
        QMessageBox.information(self, "处理结果", msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    def _check_options(self, source):
        if self.secret_seed == "" and source == self.CHECK_OPTION_SOURCE_COMMON:
            QMessageBox.critical(self, "警告", "请先进行加解密秘钥的填写:\n 菜单栏->功能->秘钥", QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.Yes)
            return False
        return True
        ######
        # 暂以名单机制进行匿名化，不提供可选项。
        ######
        # 检查匿名化选项
        checks = [
            self.PatientID, self.PatientName, self.PatientBirthDate, self.PatientSex, self.InstitutionName,
        ]
        # check Checked
        allUnChecked = True
        for check in checks:
            if check.isChecked():
                allUnChecked = False
                self.checksmap[check.objectName()] = True
        print(self.checksmap)
        if allUnChecked:
            QMessageBox.critical(self, "警告", "请先进行匿名化选项的选择", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            return False
        # 初次校验通过
        return True

    # DICOM 文件匿名化处理，返回 True 或者 False，以便于后续追溯
    def dcmrewrite(self, filename, method):
        if method == "" or (not method in [
            self.CIPHER_METHOD_ENCRYPT, self.CIPHER_METHOD_DECRYPT, self.CIPHER_METHOD_CUSTOM
        ]):
            return False
        try:
            print("当前已选择 Options:", self.checksmap)
            ds = pydicom.dcmread(filename)
            print("handling: ", filename)
            for key in self.keyProperties:

                val = str(ds.data_element(key).value)
                print("key={}, val={}, method={}".format(key, val, method))
                # 对于匿名化处理过或者该项为空的，可以直接跳过
                if val == "":
                    continue
                if method == self.CIPHER_METHOD_ENCRYPT:
                    if not val.startswith(self.PREFIX):
                        val = self.PREFIX + self.cipher.encrypt(self.secret_seed, val)
                elif method == self.CIPHER_METHOD_DECRYPT:

                    if not val.startswith(self.PREFIX):
                        continue
                    val = self.cipher.decrypt(self.secret_seed, val).lstrip(self.PREFIX)
                elif method == self.CIPHER_METHOD_CUSTOM:
                    val = "{}{}".format(self.PREFIX, self.CUSTOM_SUFFIX)
                else:
                    print("竟然走到了这里？")

                ds.data_element(key).value = val
                # print(ds.data_element(key))
                ds.save_as(filename)
        except Exception as e:
            print(e)
            return True
        return True

    def _handle_niming(self):
        if not self._check_options(self.CHECK_OPTION_SOURCE_COMMON):
            return
        if len(self.undolist) <= 0:
            QMessageBox.information(self, "处理结果", "暂无要处理的数据", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            return
        total = len(self.undolist)
        # 对待处理列表进行序列处理
        print("secret_seed: ", self.secret_seed)
        succNum = 0
        for filename in self.undolist:
            # 匿名化信息读取
            succ = self.dcmrewrite(filename, self.CIPHER_METHOD_ENCRYPT)
            if succ:
                self.donelist.append(filename)
                succNum += 1

        # 更新 UI
        self._update_listview()

        msg = "【匿名化】共扫描到: {}个，成功处理: {}个，如有错误请重试！".format(total, succNum)
        QMessageBox.information(self, "处理结果", msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        self.statusbar.showMessage(msg)

    def _handle_customniming(self):
        text, ok = QInputDialog.getText(self, "自定义匿名化后缀", "请输入自定义的匿名化后缀，如:\n 1、abc 等\n 为空则随机生成后缀。\n")
        if ok:
            self.CUSTOM_SUFFIX = text
        if not self._check_options(self.CHECK_OPTION_SOURCE_CUSTOM):
            return
        # 对待处理列表进行序列处理
        succNum = 0
        for filename in self.undolist:
            # 匿名化信息读取
            ret = self.dcmrewrite(filename, self.CIPHER_METHOD_CUSTOM)
            print("decrypt_ret=", ret)
            if ret:
                self.donelist.append(filename)
                succNum += 1

        # 更新 UI
        self._update_listview()
        msg = "【自定义匿名化】成功处理: {}个，失败: {}个，如有错误请重试！".format(succNum, len(self.undolist))
        QMessageBox.information(self, "处理结果", msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        self.statusbar.showMessage(msg)

    def _get_file_path(self):
        self.filenames = []
        files, succ = QFileDialog.getOpenFileNames(self, "多文件选择", "~", "All Files (*);;Text Files (*.txt)")
        if not succ:
            self.statusbar.showMessage("文件路径选择失败，请重新选择")
            return
        self.undolist = files
        # 将文件选中到展示区
        self.undomodel.setStringList(self.undolist)
        self.listViewundo.setModel(self.undomodel)

    def _reset_variables(self):
        self.undolist = []
        self.donelist = []
        self.filenames = []

    def _get_folder_path(self):
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹", "~")
        print(directory)
        if not os.path.isdir(directory):
            self.statusbar.showMessage("{} 不是合法文件夹".format(directory))
            return
        # 重置文件夹信息
        self._reset_variables()
        self._read_all_filenames(directory)

        # 将 self.filenames全部追加到待处理区域
        self.undolist = self.filenames
        self.undomodel.setStringList(self.undolist)
        self.listViewundo.setModel(self.undomodel)

    def _read_all_filenames(self, path):
        self.filenames = []
        # 判断路径有效性
        if not os.path.isdir(path):
            self.statusbar.showMessage("当前路径：{} 不合法，请重新选择".format(path))
            return
        for root, dir, files in os.walk(path):
            for file in files:
                print(file)
                filename = str(os.path.join(root, file))
                if os.path.isfile(filename) == False:
                    continue
                if file in self.exclude_filenames:
                    continue
                # 判断是否有拓展名，对有拓展名的进行特殊过滤
                if "." in str(file):
                    row = str(file).split(".")
                    if len(row) >= 1 and row[-1] in self.exclude_extensions:
                        continue
                # 加入待更换列表
                self.filenames.append(filename)
        # 将扫描到的文件内容显示到状态栏
        self.statusbar.showMessage("当前目录扫描到{}个文件！".format(len(self.filenames)))

    def _get_secret_string(self):
        text, ok = QInputDialog.getText(self, "秘钥选择", "请输入匿名化/反匿名化用到的加密字符串")
        if ok:
            self.secret_seed = text
        else:
            self.statusbar.showMessage("匿名化操作之前需设置加密秘钥串")
        print(text, ok)

    def _about(self):
        msg = """
        使用说明书:
        
        1) .dcm后缀添加与撤销:
            添加步骤：菜单->选择文件/文件夹->添加.dcm后缀
            撤销步骤：添加结束后未关闭此软件时，可有一次撤销处理
        
        2) 匿名化与自定义匿名化处理:
            匿名化：菜单->秘钥->输入自定义加密字符串->主页面->选择匿名处理项->点击匿名按钮
            自定义匿名化: 支持自定义匿名化后缀，未选择时则随机生成后缀，如：Anonymous_xxx
            
        3）注意：
            当前版本匿名化为对称加密算法的处理，一定要保管好加解密字符串，以防泄露或者用于后续反匿名化操作
            撤销.dcm 后缀的添加，只有上一个操作步骤为添加.dcm 后缀，且软件未关闭时有效
            
        4）免责声明:
            在使用本软件之前，请您备份好源数据文件，以免因程序故障造成不必要的损失。
            因使用此软件造成的任何信息、版权问题均由操作者本人承担。
            
            copyright@2021, 泰戈尔
        """
        QMessageBox.information(self, "关于", msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    def _file_split(self):
        root = os.path.expanduser("~")
        # 选择文件夹
        dirchoose = QFileDialog.getExistingDirectory(self, "选择文件夹", root)
        if dirchoose == "":
            self.statusbar.showMessage("文件路径选择失败，请重新选择")
            return
        # 对页内的文件进行过滤处理
        files = [item for item in os.listdir(dirchoose) if item not in self.exclude_filenames]
        self.statusbar.showMessage("当前选择路径为：{}, 文件数量：{}".format(dirchoose, len(files)))

        # 获取每页数量
        sub_count = 0
        text, ok = QInputDialog.getText(self, "切割因子", "请输入每个子目录包含的文件数")
        if ok and str(text).isdigit():
            sub_count = int(text)
        if sub_count == 0:
            self.statusbar.showMessage("必须设置下切割因子的大小，每页数量应大于 0且为数值类型！")
            return


        self.statusbar.showMessage("目录[{}] 包含{}个文件！".format(dirchoose, len(files)))
        if len(files) <= 0:
            self.statusbar.showMessage("所选文件夹下文件为空，不是目标文件夹")
            return
        if len(files) % sub_count != 0:
            self.statusbar.showMessage("切割因子非法，切割因子应为文件夹下总文件的除数。[切割因子/总文件数={}/{}]".format(len(files), sub_count))
            return
        self.statusbar.showMessage("当前选择 [切割因子/总文件数={}/{}]".format(len(files), sub_count))

        # 执行文件夹分类
        # 创建子文件夹，并执行复制操作
        for index in range(1, int(len(files)/sub_count)+1):
            subfolder = "{}/{}".format(dirchoose, index)
            if not os.path.exists(subfolder):
                os.makedirs(subfolder)
            # 迁移文件到新文件夹下
            start = sub_count * (index -1)
            end = start + sub_count
            print("start={}, end={}".format(start, end))
            for file in files[start:end]:
                oldfilename = "{}/{}".format(dirchoose, file)
                newfilename = "{}/{}".format(subfolder, file)
                shutil.copy(oldfilename, newfilename)
        # 提示已完成
        msg = "所选文件夹已切割为{}份，每页切割数量为{}个".format(int(len(files)/sub_count), sub_count)
        self.statusbar.showMessage(msg)
        QMessageBox.information(self, "处理结果", msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    iconPath = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'gastric.icns')
    app.setWindowIcon(QIcon(iconPath))
    win = Main()
    win.setWindowTitle("DICOM匿名化小助手🔧")
    win.show()
    sys.exit(app.exec_())
