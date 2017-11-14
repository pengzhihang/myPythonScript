# /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'gu.yanfeng'

import time
import os
import sys
import shutil
import hashlib
import types
import pexpect
import logging
import xlrd
import xlwt
from xlutils.copy import copy
import subprocess
import ConfigParser
import heapq
import paramiko

reload(sys)
sys.setdefaultencoding('utf-8')
_cnpath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'workspace/moxian_m2ku_cn/配置文件/各项目包配置文件/moxiancn/'))
_betapath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'workspace/moxian_m2ku_cn/配置文件/各项目包配置文件/beta/'))
_productionpath = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'workspace/moxian_m2ku_cn/配置文件/各项目包配置文件/production/'))
_mossespath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'workspace/moxian_m2ku_cn/配置文件/各项目包配置文件/test/'))

_boss_branch_test = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'workspace/moxian_boss_branch_cn/配置文件/test/'))
_boss_branch_beta = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'workspace/moxian_boss_branch_cn/配置文件/beta/'))
_boss_branch_cn = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'workspace/moxian_boss_branch_cn/配置文件/moxiancn/'))
_boss_branch_online = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'workspace/moxian_boss_branch_cn/配置文件/production/'))

_boss_master_test = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'workspace/moxian_boss_master_cn/配置文件/test/'))
_boss_master_beta = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'workspace/moxian_boss_master_cn/配置文件/beta/'))
_boss_master_cn = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'workspace/moxian_boss_master_cn/配置文件/moxiancn/'))
_boss_master_online = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'workspace/moxian_boss_master_cn/配置文件/production/'))

_codeCNM2 = os.path.abspath(os.path.join(os.path.dirname(__file__), 'compilePath/m2/moxian_m2ku_cn'))
_codeCNBoss = os.path.abspath(os.path.join(os.path.dirname(__file__), 'compilePath/boss_master/moxian_boss_master'))
_codeCNBoss_v202 = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'compilePath/boss_branch/moxian_boss_branch_cn'))

_code_moxian_m2 = os.path.abspath(os.path.join(os.path.dirname(__file__), 'workspace/moxian_m2ku_cn'))
_code_moxian_boss = os.path.abspath(os.path.join(os.path.dirname(__file__), 'workspace/moxian_boss_master_cn'))
_code_moxian_boss_v202 = os.path.abspath(os.path.join(os.path.dirname(__file__), 'workspace/moxian_boss_branch_cn'))

_code_online = os.path.abspath(os.path.join(os.path.dirname(__file__), 'compilePath/build_online'))

_log_file = os.path.abspath(
    os.path.join(os.path.join(os.path.dirname(__file__), 'compileLog'), 'compileforjenkins_cn.log'))

_wars_path_online = os.path.abspath(os.path.join(os.path.dirname(__file__), 'compilewars/wars_online'))
_wars_path_beta = os.path.abspath(os.path.join(os.path.dirname(__file__), 'compilewars/wars_beta'))
_wars_path_test = os.path.abspath(os.path.join(os.path.dirname(__file__), 'compilewars/wars_test'))
_wars_path_cn = os.path.abspath(os.path.join(os.path.dirname(__file__), 'compilewars/wars_cn'))

# _wars_path_online = '/mnt/public/测试部/2.0版本编译/发包申请Excel/compilewars/wars_online'
# _wars_path_beta = '/mnt/public/测试部/2.0版本编译/发包申请Excel/compilewars/wars_beta'
# _wars_path_test = '/mnt/public/测试部/2.0版本编译/发包申请Excel/compilewars/wars_test'
# _wars_path_cn = '/mnt/public/测试部/2.0版本编译/发包申请Excel/compilewars/wars_cn'

_work_path = os.path.abspath(os.path.dirname(__file__))

_CFG_CN_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'setting.py'))
_CFG_TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'setting_test.py'))

_module_noneed = ['mo_admin', 'mo_common_permission']
_env_for_package = {'1.1': 'M2_CN', '1.2': 'BOSS_master_CN', '1.3': 'Boss_v2.0.3_CN',
                    '2.1': 'M2_Beta', '2.2': 'Boss_master_Beta', '2.3': 'Boss_v2.0.3_Beta',
                    '3.1': 'M2_Online', '3.2': 'Boss_master_Online', '3.3': 'Boss_v2.0.3_Online',
                    '4.1': 'M2_Test', '4.2': 'Boss_master_Test', '4.3': 'Boss_v2.0.3_Test'
                    }

isUpdateCode = 'Y'  # 是否需要更新代码文件
isALL = 'N'  # 是否拉全量代码打

ENV = '1'
_MODULE_NAME = dict()
_moudles = []
DESTFILES = ['version.txt', 'application.yml', 'log4j2.xml']
_envpath = _cnpath
cms = '1'
env_forpackage = ''
excel_models = dict()

cf = ''


def setconfig(path):
    cf = ConfigParser.ConfigParser()
    cf.read(path)
    return cf


def initLogging(logFilename):
    """Init for logging
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        filename=logFilename,
        filemode='a');
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler();
    console.setLevel(logging.DEBUG);
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(asctime)s %(filename)s LINE %(lineno)-2d : %(levelname)-s %(message)s');
    # tell the handler to use this format
    console.setFormatter(formatter);
    logging.getLogger('').addHandler(console);


class writeexcel(object):
    def __init__(self, iswrite=True):
        # self.xlsfile = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)),'excel_files/package_record.xls'))
        # self.xlsfile = 'C:\\Users\\Administrator\\.jenkins\\jobs\\发包记录-11.16之后发包记录.xls'
        self.xlsfile = '/opt/home/jenkins/excel_files/发包记录-11.16之后发包记录.xls'
        self.iswrite = iswrite

    # 返回读取指定表格的sheet对象
    def _getsheet(self):
        # sheetName = time.strftime("%Y%m%d",time.localtime())
        sheetName = 'Sheet3'
        logging.debug('excel file--%s, sheetName--%s' % (self.xlsfile, sheetName))
        excel = xlrd.open_workbook(self.xlsfile, formatting_info=True)
        sheetNames = excel.sheet_names()
        if sheetName not in sheetNames:
            logging.error('Error:No sheet named:%s,please sure,and progaram exit!' % sheetName)
            raise ValueError('Build Failed!')
        for sheet in sheetNames:
            if sheet == sheetName:
                table = excel.sheet_by_name(sheet)
                return table, sheetName

    def GetrowsAndData(self, modelname):
        table, sheetName = self._getsheet()
        lineNum = table.nrows
        datasList = []
        if lineNum < 1:
            data = ['包名', '申请时间', '后台包负责人', '测试环境', 'beta是否发包', 'CN是否发包', '是否打了线上包', '上线日期', 'beta是否验证', 'beta验证结果',
                    '解决问题', '是否涉及前端', '是否涉及数据库', '问题跟踪人', '备注']
            datasList.append(data)
        gete = getexcel(True, modelname)
        lines = gete._getContent()
        datasList.extend(lines)
        # logging.debug(table,lineNum,datasList)
        return sheetName, lineNum, datasList

    # 发包申请Excel中的数据：编号 修改内容描述 文件路径    配置文件是否需要更新    数据库是否需要更新   申请时间  是否涉及到前端 涉及到前端的人员    提交人员
    # 需要写入Excel中的数据：0-包名 1-申请时间 2-后台包负责人 4-beta是否发包 10-解决问题 11-是否涉及前端 12-是否涉及数据库
    # 对应发包Excel中的数据：2-     5-         8-                            1-          6-              4-
    def writeinexcel(self, sheetName, fromrows, datasList, modelname):
        # datasList=[list1[],list2[],...,listn[]]
        # list1--listn为每一行需要写入数据列表,n表示第几行，listn的内容即为每一列的数据
        if self.iswrite:
            logging.info('iswrite=%s,need write excel! from the %d row.' % (str(self.iswrite), fromrows))
            # logging.debug(datasList)
            oldWb = xlrd.open_workbook(self.xlsfile, formatting_info=True)
            newWb = copy(oldWb)
            newWs = newWb.get_sheet(0)
            sheets = oldWb.sheet_names()
            sheetnum = 0
            for i in range(len(sheets)):
                if sheets[i] == sheetName:
                    sheetnum = int(i)
            newWs = newWb.get_sheet(sheetnum)
            logging.debug('wirte in sheet--%s' % newWs.get_name())

            # 根据前面已经记录了多少行来判断从第几行写起
            if len(datasList) > 0:
                rowflag = 0
                for r in range(fromrows, len(datasList) + fromrows):
                    logging.debug('gggggggggggggggggggg row=%d,length=%d' % (r, len(datasList)))
                    datasListIndex = r
                    if fromrows > 0:
                        datasListIndex = datasListIndex - fromrows
                        # logging.debug('ggggggggg----datasListIndex=%s' % datasListIndex)
                    for c in range(15):
                        row = r
                        col = c
                        value = ''
                        modelname2 = ''
                        oldWb = xlrd.open_workbook(self.xlsfile, formatting_info=True)
                        newWb = copy(oldWb)
                        newWs = newWb.get_sheet(sheetnum)
                        if col == 10:
                            newWs.col(col).width = 20000
                            logging.debug('set col:%d width 20000' % col)
                        else:
                            newWs.col(col).width = 3500
                            logging.debug('set col:%d width 3500' % col)
                        if row == 0:
                            # 第一行写入标题
                            value = datasList[row][col]
                            modelname2 = 'title'
                        else:
                            if modelname in datasList[datasListIndex][2]:
                                modelname2 = 'need write'
                            if c == 0:
                                if modelname == 'mo_admin':
                                    value = 'mo_boss'
                                else:
                                    value = modelname
                            elif c == 1:
                                value = str(datasList[datasListIndex][5]) + '(real time:' + time.strftime(
                                    '%Y/%m/%d %H:%M', time.localtime()) + ')'
                                logging.debug('value type:%s' % type(value))
                                # value = value.encode('gbk')
                            elif c == 2:
                                value = datasList[datasListIndex][8]
                                # value = value.encode('gbk')
                            elif c == 3:
                                value = 'Y'
                            elif c == 10:
                                value = datasList[datasListIndex][1]
                                # value = value.encode('gbk')
                            elif c == 11:
                                value = datasList[datasListIndex][6]
                                # value = value.encode('gbk')
                            elif c == 12:
                                value = datasList[datasListIndex][4]
                                # value = value.encode('gbk')
                        if modelname2 == 'title' or modelname2 == 'need write':
                            # 从第几行开始写的值，需减去不需要写入的次数
                            newrow = row - rowflag
                            logging.debug('write at row:%d,col:%d,value:%s' % (newrow + 1, c, value))
                            newWs.write(newrow, col, value)
                            try:
                                # logging.debug('111-%s,222-%s' % (self.xlsfile,type(self.xlsfile)))
                                newWb.save(self.xlsfile)
                            except Exception as e:
                                logging.error('Exception:%s' % str(e))
                        else:
                            logging.warning('files do not need write --%s' % datasList[datasListIndex][2])
                            # 某模块不需要写的话就+1
                            rowflag += 1
                            break
            else:
                logging.warning('nothing to write excel,datasList is null(%s)' % datasList)
        else:
            logging.info('iswrite=%s,do not need write excel!' % str(self.iswrite))


class getexcel(object):
    # “是否涉及前端”为True时，要校验是否涉及，为False时，不进行校验
    def __init__(self, appflag, model):
        # logging.debug('gggggggggggg-%s' % type(appflag))
        if model == 'mo_admin':
            # self.xlsfile = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)),'excel_files/Boss后台每日test发包申请.xls'))
            self.xlsfile = '/opt/home/jenkins/excel_files/Boss后台每日CN发包申请.xls'
        else:
            # self.xlsfile = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)),'excel_files/Java后台每日test发包申请.xls'))
            self.xlsfile = '/opt/home/jenkins/excel_files/Java后台每日CN发包申请.xls'
        self.appflag = appflag == str(True)

    # 返回读取指定表格的sheet对象
    def _getsheet(self):
        sheetName = time.strftime("%Y%m%d", time.localtime())
        # sheetName = '20160105'
        excel = xlrd.open_workbook(self.xlsfile)
        sheetNames = excel.sheet_names()
        newsheetNames = sheetNames
        newsheetNames = [s for s in newsheetNames if s.isdigit()]
        largestSheet = heapq.nlargest(1, newsheetNames)[0]
        print largestSheet
        if sheetName not in largestSheet:
            logging.error(
                'Error:No sheet named startswith:%s,the latest table is %s, please sure,and progaram exit!' % (
                sheetName, str(largestSheet)))
            raise ValueError('Build Failed!')
        logging.debug('excel file--%s, sheetName--%s' % (self.xlsfile, str(largestSheet)))
        table = excel.sheet_by_name(largestSheet)
        return table

    # 获取Excel中所有的内容并返回
    def _getContent(self):
        table = self._getsheet()
        lineNum = table.nrows
        lines = []
        if lineNum == 0 or lineNum == 1:
            logging.warning('WARNING:the sheet is null!please sure,and progaram exit!')
            raise ValueError('Build Failed!')
        for i in range(1, lineNum):
            line = table.row_values(i)
            if line == '': pass
            lines.append(line)
        return lines

    # 解析文件路径
    # excel列结构
    # 编号 修改内容描述 文件路径    配置文件是否需要更新    数据库是否需要更新   申请时间  是否涉及到前端 涉及到前端的人员    提交人员
    def getfilepath(self):
        lines = self._getContent()
        filePaths = []
        repeatFiles = []
        models_dict = dict()
        model_name_list = []
        models_no = []
        for i in range(len(lines)):
            fs = ''
            if '\\' in lines[i][2].encode('utf-8'):
                fs = lines[i][2].encode('utf-8').replace('\\', '/')
            else:
                fs = lines[i][2].encode('utf-8')
            files = []
            ffs = fs.split('\n')
            for ff in ffs:
                if ff.strip() != '':
                    files.append(ff)
            # 判断是否涉及前端
            appf = '否'
            lsix = lines[i][6].decode('utf-8').encode('gbk')
            if lsix == appf:
                filePaths.append(files)
                logging.debug('get the %d row data:%s' % (i + 2, files))
                # if files in filePaths:
                #    repeatFiles.append(files)
                #    logging.warning("Repeated file :'%s' is exist already!" % files)
                for f in files:
                    # 获取模块名
                    m_name = f[0:f.find('/')]
                    if m_name not in model_name_list and m_name.strip() != '':
                        model_name_list.append(m_name.strip())
            else:
                if self.appflag:
                    names = lines[i][7].decode('utf-8').encode('gbk')
                    logging.warning('第%d行涉及到前端，不打包，请确认！文件：%s,涉及到前端的人员--%s' % (i + 2, files, names))
                    for f in files:
                        # 获取不需要打包的模块名
                        m_no = f[0:f.find('/')]
                        if m_no not in models_no and m_no != '':
                            models_no.append(m_no)
                            logging.debug("package name '%s' that involve the app client!" % m_no)
                else:
                    filePaths.append(files)
                    logging.debug('get the %d row data:%s' % (i + 2, files))
                    # if files in filePaths:
                    #    repeatFiles.append(files)
                    #    logging.warning("Repeated file :'%s' is exist already!" % files)
                    for f in files:
                        # 获取模块名
                        m_name = f[0:f.find('/')]
                        if m_name not in model_name_list and m_name != '':
                            model_name_list.append(m_name.strip())
        logging.info('Excel models that need compiled:%s----and models that don\'t need compile:%s' % (
        model_name_list, models_no))
        # 重新新整合数据，{modelname:files}
        for m in model_name_list:
            m_tmp = []
            for flist in filePaths:
                for f in flist:
                    if f.strip().startswith(m):
                        if f.strip() not in m_tmp:
                            m_tmp.append(f.strip())
                        else:
                            logging.warning("Repeated file :'%s' is exist already!" % f.strip())
                            repeatFiles.append(f.strip())
            models_dict[m] = m_tmp
        for key in models_dict.keys():
            for fs in models_dict[key]:
                logging.debug('models:%s , files: %s' % (key, fs))
        logging.info('there %d repeated files' % len(repeatFiles))
        for rf in repeatFiles:
            logging.info('Repeated file:%s' % rf)
        global excel_models
        excel_models = models_dict
        return models_dict


class FilesOperations(object):
    def copycodetobuild(self, buildmodule):
        if buildmodule == '3.1':
            if os.path.isdir(_code_online + '/moxian_m2'):
                shutil.rmtree(_code_online + '/moxian_m2')
            r = os.system('cp -rf %s %s' % (_codeCNM2, _code_online + '/moxian_m2'))
            if r == 0:
                logging.info('cmd: cp -rf %s %s  sucessful' % (_codeCNM2, _code_online + '/moxian_m2'))
            else:
                logging.error('cp failed--result:%d' % r)
                raise ValueError('Build Failed!')
        elif buildmodule == '3.2':
            if os.path.isdir(_code_online + '/moxian_boss'):
                shutil.rmtree(_code_online + '/moxian_boss')
            r = os.system('cp -rf %s %s' % (_codeCNBoss, _code_online + '/moxian_boss'))
            if r == 0:
                logging.info('cmd: cp -rf %s %s  sucessful' % (_codeCNBoss, _code_online + '/moxian_boss'))
            else:
                logging.error('cp failed--result:%d' % r)
                raise ValueError('Build Failed!')
        elif buildmodule == '3.3':
            if os.path.isdir(_code_online + '/moxian_boss'):
                shutil.rmtree(_code_online + '/moxian_boss')
            r = os.system('cp -rf %s %s' % (_codeCNBoss_v202, _code_online + '/moxian_boss'))
            if r == 0:
                logging.info('cmd: cp -rf %s %s  sucessful' % (_codeCNBoss_v202, _code_online + '/moxian_boss'))
            else:
                logging.error('cp failed--result:%d' % r)
                raise ValueError('Build Failed!')

    def deletefiles(self, path):
        filepaths = findfile(path)
        dirlist = []
        for f in filepaths:
            if 'api-docs' in f:
                docsdir = f.split('api-docs')[0].strip() + 'api-docs'
                # logging.debug(f.split('api-docs')[0].strip()+'api-docs')
                dirlist.append(docsdir)
                break
        if len(dirlist) > 0:
            for dl in dirlist:
                logging.debug('>>>>>delete dir:%s' % dl)
                shutil.rmtree(dl)
        else:
            logging.warning('error:there no \"api-docs\" directory!')

    def getMd5(self, filename):
        myMd5 = hashlib.md5()
        f = file(filename, 'rb')
        while True:
            b = f.read(8096)
            if not b:
                break
            myMd5.update(b)
            myMd5_Digest = myMd5.hexdigest()
        return myMd5_Digest

    def findwar(self, path):
        filepaths = findfile(path)
        warslist = []
        logging.debug('war path:%s' % _wars_path)
        for war in filepaths:
            if '.war' in war:
                modulewarname = war[war.rfind('/') + 1:]
                mwn = modulewarname[:modulewarname.find('.')]
                if mwn not in _module_noneed:
                    logging.debug('>>>>>find war package:%s' % war)
                    warslist.append(war)
                else:
                    logging.debug('>>>>>%s don not need!' % war)
        if len(warslist) > 0:
            for war in warslist:
                warname = war[war.rfind('/') + 1:]
                if warname in os.listdir(_wars_path):
                    os.rename(_wars_path + '/' + warname, _wars_path + '/' + warname + '.bak')
                # deletewar(_wars_path+'/'+warname)
                logging.info('>>>>>copy \"%s\" to %s' % (war, _wars_path))
                shutil.copy2(war, _wars_path)
            return warslist
        else:
            logging.warning('WARNNING:No war package in :%s' % (path,))
            raise ValueError('Build Failed!')

    def writeMd5(self):
        wars = os.listdir(_wars_path)
        md5Dict = dict()
        for war in wars:
            if war.endswith('.war'):
                warpath = _wars_path + '/' + war
                md5Dict[war] = self.getMd5(warpath)
        md5file = _wars_path + '/md5list.txt'
        if os.path.exists(md5file):
            shutil.copy2(md5file, md5file + '_bak')
        fp = open('%s/md5list.txt' % _wars_path, 'w+')
        fp.write('====================' + time.strftime('%Y-%m-%d-%H-%M', time.localtime()) + '====================\n')
        i = 1
        for key in md5Dict.keys():
            fp.write('%d - %s   %s\n' % (i, key, md5Dict[key]))
            i += 1
        # print 'total files:%s need copy.' % str(len(files))
        logging.debug('there %s files are copied sucessfully' % str(len(md5Dict)))


# copy file
class Move(object):
    def __init__(self, i, env):
        self.env = env
        self.module = switchmodule(i)

    @property
    def copy(self):
        module = self.module
        self._deletePkg()
        if type(module) == types.StringType:
            if module == "mo_common_permission": module = "mo_permission"
            if module == "mo_admin": module = "mo_boss"
            if module == "mo_game_mining": module = "mo_mining"
            if module == 'mo_push': module = 'mo_common_push'
            switch_test_cn_path(self.env)
            srcfile = os.path.join(os.getcwd(), module + '.war')
            destpath = os.path.join(_work_path, 'compileBack_Pkg/cn')
            if self.env == '4':
                destpath = os.path.join(_work_path, 'compileBack_Pkg/test')
            elif self.env == '3':
                destpath = os.path.join(_work_path, 'compileBack_Pkg/online')
            elif self.env == '2':
                destpath = os.path.join(_work_path, 'compileBack_Pkg/beta')
            pkg_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
            if not os.path.exists(destpath + '/%s' % module):
                os.mkdir(destpath + '/%s' % module)
            destpath = os.path.join(destpath, module)
            shutil.copy2(srcfile, (destpath + '/%s.war_' + pkg_time) % module)
            logging.info('>>>>> BackUp %s file finished!' % module)
        elif type(module) == types.ListType:
            pkg_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
            onlinepath = os.path.join(_work_path, 'compileBack_Pkg/cn')
            if self.env == '4':
                onlinepath = os.path.join(_work_path, 'compileBack_Pkg/test')
            elif self.env == '3':
                onlinepath = os.path.join(_work_path, 'compileBack_Pkg/online')
            elif self.env == '2':
                onlinepath = os.path.join(_work_path, 'compileBack_Pkg/beta')
            # os.mkdir(destpath)
            for m in module:
                if m == "mo_common_permission": m = "mo_permission"
                if m == "mo_admin": m = "mo_boss"
                if m == "mo_game_mining": m = "mo_mining"
                if m == "mo_push": m = "mo_common_push"
                if not os.path.exists(onlinepath + '/%s' % m):
                    os.mkdir(onlinepath + '/%s' % m)
                destpath = os.path.join(onlinepath, m)
                switch_test_cn_path(self.env)
                try:
                    srcfile = os.path.join(os.getcwd(), m + '.war')
                    shutil.copy2(srcfile, (destpath + '/%s.war_' + pkg_time) % m)
                    logging.info('>>>>> BackUp %s file finished!' % m)
                except Exception as e:
                    logging.error('>>>>> BackUp %s file Failed!' % m)
                    logging.error(e)

    def _deletePkg(self):
        curtime = time.time()
        destpath = os.path.join(_work_path, 'compileBack_Pkg/cn')
        if self.env == '4':
            destpath = os.path.join(_work_path, 'compileBack_Pkg/test')
        elif self.env == '3':
            destpath = os.path.join(_work_path, 'compileBack_Pkg/online')
        elif self.env == '2':
            destpath = os.path.join(_work_path, 'compileBack_Pkg/beta')
        dirlist = os.listdir(destpath)
        if len(dirlist) < 0:
            logging.debug('No backup files!')
        else:
            for i in dirlist:
                if i.startswith('mo_'):
                    mo_dirlist = os.listdir(destpath + '/' + i)
                    for md in mo_dirlist:
                        md_mtime = os.stat(destpath + '/' + i + '/' + md).st_mtime
                        if curtime - md_mtime >= 1296000:
                            os.remove(destpath + '/' + i + '/' + md)
                            logging.info(
                                'Delete the backup files that time greater than 15 days:' + destpath + '/' + i + '/' + md)
                mtime = os.path.getmtime(destpath + '/' + i)
                # need time in 15 days
                ntime = 1296000  # seconds
                if curtime - mtime >= ntime:
                    shutil.rmtree(destpath + '/' + i)
                    logging.info('Delete the backup files that time greater than 15 days:' + destpath + '/' + i)


def deletewar(warfile):
    if os.path.exists(warfile):
        os.remove(warfile)


# scp upload file
class SCP(object):
    def __init__(self, i, env):
        self.module = switchmodule(i)
        self.env = env

    @property
    def scpsend(self):
        module = self.module
        if type(module) == types.StringType:
            if module == "mo_push": module = "mo_common_push"
            scpip = cf.get(module, 'IP')
            scpport = cf.get(module, 'Port')
            scppath = cf.get(module, 'Root_Respostiory_Path')
            switch_test_cn_path(self.env)
            try:
                if module == "mo_common_permission":
                    module = "mo_permission"
                if module == "mo_admin":
                    module = "mo_boss"
                if module == "mo_game_mining": module = "mo_mining"
                modulewar = module + '.war'
                CMD = "scp -P {scpport} {warpackage} root@{scpip}:{scppath}/{model}".format(scpport=scpport,
                                                                                            warpackage=modulewar,
                                                                                            scpip=scpip,
                                                                                            scppath=scppath,
                                                                                            model=module)
                logging.debug('excute cmd:%s,transfering file,please wait...' % CMD)
                pp = subprocess.Popen(CMD, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                stdout, stderr = pp.communicate()
                pp.wait()
                logging.error(stderr)
                logging.debug(stdout)
                # child = pexpect.spawn(CMD)
                # child.expect('%s.*100*' % module,timeout=900)
                # child.interact()
                # child.close()
            except Exception, e:
                logging.error(e)
                logging.error('>>>>>%s SCP FAILED！' % module)
                raise ValueError('Build Failed!')
            else:
                logging.info(">>>>>%s SCP Success" % module)
        elif type(module) == types.ListType:
            for m in module:
                if m == "mo_push": m = "mo_common_push"
                scpip = cf.get(m, 'IP')
                scpport = cf.get(m, 'Port')
                scppath = cf.get(m, 'Root_Respostiory_Path')
                try:
                    switch_test_cn_path(self.env)
                    if m == "mo_common_permission":
                        m = "mo_permission"
                    if m == "mo_admin":
                        m = "mo_boss"
                    if m == "mo_game_mining": m = "mo_mining"
                    modulewar = m + '.war'
                    CMD = "scp -P {scpport} {warpackage} root@{scpip}:{scppath}/{model}".format(scpport=scpport,
                                                                                                warpackage=modulewar,
                                                                                                scpip=scpip,
                                                                                                scppath=scppath,
                                                                                                model=m)
                    logging.debug('excute cmd:%s,transfering file,please wait...' % CMD)
                    pp = subprocess.Popen(CMD, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                    stdout, stderr = pp.communicate()
                    pp.wait()
                    logging.error(stderr)
                    logging.debug(stdout)
                except Exception, e:
                    logging.error(e)
                    logging.error('>>>>> %s SCP FAILED！' % m)
                else:
                    logging.info('>>>>> %s SCP Success' % m)


# make a new directory for .war package
class MkDir(object):
    def __init__(self, i):
        self.module = switchmodule(i)

    @property
    def new(self):
        module = self.module
        if type(module) == types.StringType:
            if module == 'mo_push': module = 'mo_common_push'
            sship = cf.get(module, 'IP')
            sshport = cf.get(module, 'Port')
            sshpath = cf.get(module, 'Root_Respostiory_Path')
            try:
                CMD = "ssh -p {sshport} {sship}".format(sshport=sshport, sship=sship)
                logging.debug('excute cmd:%s' % CMD)
                child = pexpect.spawn(CMD)
                child.expect('Last login:*', timeout=30)
                child.expect('.*')
                CMD1 = "cd {path}".format(path=sshpath)
                child.sendline(CMD1)
                child.expect('.*')
                if module == "mo_common_permission": module = "mo_permission"
                if module == "mo_admin": module = "mo_boss"
                if module == "mo_game_mining": module = "mo_mining"
                child.sendline('rm -rf %s' % module)
                child.expect('.*')
                child.sendline('mkdir %s' % module)
                index = child.expect('.*')
                child.sendline("exit")
                child.expect(".*")
                # child.interact()
                child.close()
            except pexpect.EOF as e:
                logging.error(e)
                child.close()
                logging.warning('>>>>> Mkdir %s FAILED！' % module)
            else:
                logging.info('>>>>> Mkdir %s Success.' % module)
        elif type(module) == types.ListType:
            for m in module:
                if m == 'mo_push': m = 'mo_common_push'
                sship = cf.get(m, 'IP')
                sshport = cf.get(m, 'Port')
                sshpath = cf.get(m, 'Root_Respostiory_Path')
                try:
                    CMD = "ssh -p {sshport} {sship}".format(sshport=sshport, sship=sship)
                    child = pexpect.spawn(CMD)
                    child.expect('Last login:*', timeout=30)
                    child.expect('.*')
                    CMD1 = "cd {path}".format(path=sshpath)
                    child.sendline(CMD1)
                    child.expect('.*')
                    if m == "mo_common_permission": m = "mo_permission"
                    if m == "mo_admin": m = "mo_boss"
                    if m == "mo_game_mining": m = "mo_mining"
                    child.sendline('rm -rf %s' % m)
                    child.expect('.*')
                    child.sendline('mkdir %s' % m)
                    child.expect('.*')
                    child.sendline("exit")
                    child.expect(".*")
                    # child.interact()
                    child.close()
                except pexpect.EOF as e:
                    logging.error(e)
                    child.close()
                    logging.warning('>>>>> Mkdir %s FAILED！' % m)
                else:
                    logging.info('>>>>> Mkdir %s Success.' % m)


def monitorlog(ip, port, user, logpath, module):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, int(port), user, '')
    cmd = 'tail -f %s/logs/catalina.out' % logpath
    stdin, stdout, stderr = ssh.exec_command(cmd)
    curtime = time.time()
    logging.info('\n#############以下为 %s模块重启tomcat日志，请注意tomcat启动是否报错#############\n' % module)
    while True:
        line = stdout.readline()
        logging.info(line)
        newtime = time.time()
        if line.strip().startswith('INFO: Server startup in'):
            if newtime - curtime > 5:
                break
        if newtime - curtime > 120:
            logging.warning('>>>>read log time out, > 120s')
            break
    ssh.close()
    logging.info('#############以上为 %s模块重启tomcat日志，请注意tomcat启动是否报错#############\n\n' % module)


# restart tomcat
class TomCat(object):
    def __init__(self, i):
        self.module = switchmodule(i)

    @property
    def restart(self):
        module = self.module
        sucessModules = []
        failedModules = []
        if type(module) == types.StringType:
            if module == 'mo_push': module = 'mo_common_push'
            scpip = cf.get(module, 'IP')
            scpport = cf.get(module, 'Port')
            scppath = cf.get(module, 'Root_Respostiory_Path')
            os.chdir(_work_path)
            if module == "mo_common_permission":
                module = "mo_permission"
            if module == "mo_admin":
                module = "mo_boss"
            if module == "mo_game_mining": module = "mo_mining"
            try:
                # scp
                CMD = "scp -P {scpport} tomcat.sh root@{scpip}:{scppath}".format(scpport=scpport, scpip=scpip,
                                                                                 scppath=scppath)
                logging.debug('excute cmd:%s' % CMD)
                pp = subprocess.Popen(CMD, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                stdout, stderr = pp.communicate()
                pp.wait()
                logging.error(stderr)
                logging.debug(stdout)
                # ssh login
                CMD1 = "ssh -p {sshport} {sship}".format(sshport=scpport, sship=scpip)
                logging.debug('excute cmd:%s' % CMD1)
                child1 = pexpect.spawn(CMD1)
                child1.expect('Last login:*', timeout=30)
                CMD2 = 'cd {path}'.format(path=scppath)
                child1.sendline(CMD2)
                child1.expect('.*')
                CMD4 = 'chmod +x tomcat.sh'
                child1.sendline(CMD4)
                child1.expect('.*')
                child1.logfile = sys.stdout
                CMD3 = './tomcat.sh %s' % module
                child1.sendline(CMD3)
                child1.expect('tomcat start Success.*')
                # monitorlog(scpip,scpport,'root',scppath)
                child1.logfile = None
                child1.sendline("exit")
                child1.expect(".*")
                child1.close()
            except Exception, e:
                logging.error(e)
                logging.error('>>>>>restart tomcat.sh FAILED！')
                raise ValueError('Build Failed!')
            else:
                logging.info('>>>>>restart tomcat.sh Success')
            try:
                monitorlog(scpip, scpport, 'root', scppath, module)
            except Exception, e:
                logging.error(e)
                logging.warning('打印tomcat重启日志失败!')

        elif type(module) == types.ListType:
            for m in module:
                if m == 'mo_push': m = 'mo_common_push'
                scpip = cf.get(m, 'IP')
                scpport = cf.get(m, 'Port')
                scppath = cf.get(m, 'Root_Respostiory_Path')
                os.chdir(_work_path)
                if m == "mo_common_permission":
                    m = "mo_permission"
                if m == "mo_admin":
                    m = "mo_boss"
                if m == "mo_game_mining": m = "mo_mining"
                try:
                    # scp
                    CMD = "scp -P {scpport} tomcat.sh root@{scpip}:{scppath}".format(scpport=scpport, scpip=scpip,
                                                                                     scppath=scppath)
                    pp = subprocess.Popen(CMD, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                    stdout, stderr = pp.communicate()
                    pp.wait()
                    logging.error(stderr)
                    logging.debug(stdout)
                    # ssh login
                    CMD1 = "ssh -p {sshport} {sship}".format(sshport=scpport, sship=scpip)
                    child1 = pexpect.spawn(CMD1)
                    child1.expect('Last login:*', timeout=30)
                    CMD2 = 'cd {path}'.format(path=scppath)
                    child1.sendline(CMD2)
                    child1.expect('.*')
                    CMD4 = 'chmod +x tomcat.sh'
                    child1.sendline(CMD4)
                    child1.expect('.*')
                    child1.logfile = sys.stdout
                    time.sleep(10)
                    CMD3 = './tomcat.sh %s' % m
                    child1.sendline(CMD3)
                    child1.expect('tomcat start Success.*')
                    # monitorlog(scpip,scpport,'root',scppath)
                    child1.logfile = None
                    # child1.sendline('rm -rf tomcat.sh')
                    # child1.expect('.*')
                    child1.sendline("exit")
                    child1.expect(".*")
                    child1.close()
                except Exception, e:
                    logging.error(e)
                    logging.error('>>>>>module:%s -- restart tomcat.sh FAILED！' % m)
                    failedModules.append(m)
                    # child.close()
                    # child1.close()
                else:
                    logging.info('>>>>>module:%s -- restart tomcat.sh Success' % m)
                    sucessModules.append(m)
                try:
                    monitorlog(scpip, scpport, 'root', scppath, m)
                except Exception, e:
                    logging.error(e)
                    logging.warning('打印tomcat重启日志失败!')
            logging.info('modules that tomcat restart sucessful :%s, failed:%s' % (sucessModules, failedModules))
            if len(failedModules) > 0:
                raise ValueError('请注意，有重启tomcat失败的模块-- failed:%s' % failedModules)


# 获取指定目录下的所有文件
def findfile(fpath):
    if not os.path.exists(fpath):
        logging.error('path:\"%s\" is not exists!' % fpath)
        raise ValueError('Build Failed!')
    dirlist = []
    filepaths = []
    reasult = os.walk(fpath)
    for dirs in reasult:
        dirlist.append(dirs)
    for i in range(0, len(dirlist)):
        if len(dirlist[i][2]) > 0:
            for files in dirlist[i][2]:
                filepath = os.path.join(dirlist[i][0], files)
                if 'build' in filepath and 'gradle' not in filepath and 'build_online' not in filepath:
                    if 'war' in filepath:
                        filepaths.append(filepath)
                        filepath = ''
                    else:
                        pass
                else:
                    filepaths.append(filepath)
                    filepath = ''
    return filepaths


# 根据文件名获取指定文件的全路径
def getfile(filename, fpath):
    systemType = sys.platform
    filelist = []
    files = findfile(fpath)
    for f in files:
        # print f
        absfile = ''
        if systemType == 'win32':
            absfile = f[f.rfind('\\') + 1:]
        else:
            absfile = f[f.rfind('/') + 1:]
        if filename == absfile:
            filelist.append(f)
    if len(filelist) == 0:
        logging.warning('\"%s\" file:%s not found!' % (fpath, filename))
        raise ValueError('Build Failed!')
    else:
        return filelist


# 获取打包目录下的对应的配置文件
def destfile():
    filepaths = []
    for f in DESTFILES:
        files = getfile(f, _codeCNM2)
        filepaths.extend(files)
    for f in DESTFILES:
        files = getfile(f, _codeCNBoss)
        filepaths.extend(files)
    for f in DESTFILES:
        files = getfile(f, _codeCNBoss_v202)
        filepaths.extend(files)
    destfileList = []
    for m in _MODULE_NAME.values():
        for f in filepaths:
            if m == 'mo_push':
                m = 'mo_common_push'
            elif m == 'mo_boss':
                m = 'mo_admin'
            if m in f:
                destfileList.append(f)
    destfileList = list(set(destfileList))
    mnamelist = []
    for df in destfileList:
        mname = df.split('/')[9]
        if mname not in mnamelist:
            mnamelist.append(mname)
    return destfileList


# 打包目录与源目录下相对应的文件组成字典
def singleSrcAndDest(moudleName):
    destfileList = destfile()
    destf = []
    filedict = dict()
    if type(moudleName) == types.StringType:
        moudleName = [moudleName]
    for moudle in moudleName:
        for df in destfileList:
            # logging.debug('00000000000000000------%s' % df)
            if df[0:df.rfind('/') + 1] not in destf and '配置文件' not in df and 'main' in df:
                # logging.debug('111111111111------test:%s' % df[0:df.rfind('/')+1])
                destf.append(df[0:df.rfind('/') + 1])
        if moudle == 'mo_boss':
            moudle = 'mo_admin'
        elif moudle == 'mo_push':
            moudle = 'mo_common_push'
        for df in destf:
            # logging.debug('222222222222------moudle=%s,df=%s' % (moudle,df.split('/')[7]))
            if moudle == df.split('/')[7]:  # or moudle == df.split('\\')[10]:
                # logging.debug('33333333333333--------df=%s' % df)
                if cms == '3' or cms == '6':
                    if _codeCNBoss_v202 in df:
                        if moudle == 'mo_admin':
                            moudle = 'mo_boss'
                        filedict[os.path.join(_envpath, moudle)] = df
                        break
                elif cms == '2' or cms == '1' or cms == '4' or cms == '5':
                    if moudle == 'mo_admin':
                        moudle = 'mo_boss'
                    elif moudle == 'mo_common_push':
                        moudle = 'mo_push'
                    filedict[os.path.join(_envpath, moudle)] = df
                    break
    return filedict


def getMd5(filename):
    try:
        myMd5 = hashlib.md5()
        f = file(filename, 'rb')
        while True:
            b = f.read(8096)
            if not b:
                break
            myMd5.update(b)
            myMd5_Digest = myMd5.hexdigest()
        return myMd5_Digest
    except Exception as e:
        logging.warning('WARNING:%s' % e)


def compareMd5_config(moudleName):
    filedict = singleSrcAndDest(moudleName)
    for key in filedict.keys():
        for i in range(len(DESTFILES)):
            srcmd5 = getMd5(os.path.join(key, DESTFILES[i]))
            destmd5 = getMd5(os.path.join(filedict[key], DESTFILES[i]))
            if srcmd5 != destmd5:
                logging.error('------md5 not equal!copy failed,please sure!-------')
                logging.error('%s:%s' % (os.path.join(key, DESTFILES[i]), srcmd5))
                logging.error('%s:%s' % (os.path.join(filedict[key], DESTFILES[i]), destmd5))
                raise ValueError('Build Failed!')
        logging.debug('MD5 check correctly!')


def compareMd5_code(sdfDict):
    for key in sdfDict.keys():
        if os.path.isfile(key):
            srcmd5 = getMd5(key)
            # 有些新增文件只会有路径在sdfDict中，因此判断md5时需要重新拼接一个包含文件名的路径
            if '.' not in sdfDict[key] and 'gradlew' not in sdfDict[key]:
                sdfDict[key] = os.path.join(sdfDict[key], os.path.basename(key))
            destmd5 = getMd5(sdfDict[key])
            if srcmd5 != destmd5:
                logging.error('------md5 not equal!copy failed,please sure!-------')
                logging.error('%s:%s' % (key, srcmd5))
                logging.error('%s:%s' % (sdfDict[key], destmd5))
                raise ValueError('Build Failed!')
            logging.debug('MD5 check correctly!')
        elif os.path.isdir(key):
            logging.info("'%s' is director,don't need compareMd5!" % key)


def copyfile(srcpath, destpath):
    for f in os.listdir(srcpath):
        fpath = os.path.abspath(os.path.join(srcpath, f))
        shutil.copy2(fpath, destpath)


def copyfile_code(srcpath, destpath):
    shutil.copy2(srcpath, destpath)


def copyfile_code_all(srcpath, destpath):
    logging.info("copyfile_code_all--copy dir '%s' to dir '%s'" % (srcpath, destpath))
    if os.path.isdir(destpath):
        shutil.rmtree(destpath)
    r = os.system('cp -rf %s %s' % (srcpath, destpath))
    if r == 0:
        logging.info('cmd: cp -rf %s %s  sucessful' % (srcpath, destpath))
    else:
        logging.error('cp failed--result:%d' % r)
        raise ValueError('Build Failed!')


def switchmodule(i):
    if i.isdigit():
        module = _MODULE_NAME[int(i)]
        if i == '0':
            module = _MODULE_NAME.values()[1:len(_MODULE_NAME)]
    else:
        modulelist = []
        for k in i.split(','):
            module = _MODULE_NAME[int(k)]
            modulelist.append(module)
        module = modulelist
    return module


def switchpath(module):
    if env_forpackage == '1.1' or env_forpackage == '2.1' or env_forpackage == '4.1':
        os.chdir(_codeCNM2)
        os.chdir("%s" % module)
    elif env_forpackage == '1.2' or env_forpackage == '2.2' or env_forpackage == '4.2':
        os.chdir(_codeCNBoss)
        os.chdir("%s" % module)
    elif env_forpackage == '1.3' or env_forpackage == '2.3' or env_forpackage == '4.3':
        os.chdir(_codeCNBoss_v202)
        os.chdir("%s" % module)
    elif env_forpackage == '3.1':
        os.chdir(_code_online + '/moxian_m2')
        os.chdir("%s" % module)
    elif env_forpackage == '3.2' or env_forpackage == '3.3':
        os.chdir(_code_online + '/moxian_boss')
        os.chdir("%s" % module)


def switch_test_cn_path(env):
    if env == '1':
        os.chdir(_wars_path_cn)
    elif env == '4':
        os.chdir(_wars_path_test)
    elif env == '2':
        os.chdir(_wars_path_beta)
    elif env == '3':
        os.chdir(_wars_path_online)


def env_select(*args):
    logging.info("#####################################################################")
    logging.info("########        Moxian_Config(ENV_SELECT)                   ########")
    logging.info("#####################################################################")
    env_dict = {'1': 'CN', '2': 'Beta', '3': 'Production', '4': 'Test'}
    global ENV
    # ENV = raw_input(">>>>>Please Choose:")
    for k in env_dict.keys():
        logging.info('%s--%s' % (k, env_dict[k]))
    ENV = args[0]
    if str(ENV) in env_dict.keys():
        logging.info('The enviroment is：%s -- %s' % (str(ENV), env_dict[str(ENV)]))
        return True
    else:
        logging.error('Enviroment must in %s,and your chois is %s' % (env_dict, str(ENV)))
        logging.error('progaram exit!!')
        raise ValueError('Build Failed!')


def getCodefiles(srcpath, destpath, model, isClinet=True):
    # logging.debug('gggggggg:%s,%s,%s' % (isUpdateCode,isALL,model))
    # raise ValueError('Build Failed!')
    if model == 'mo_push': model = 'mo_common_push'
    if model == 'mo_boss': model = 'mo_admin'
    excel = getexcel(isClinet, model)
    models_dict = excel.getfilepath()
    if isUpdateCode == 'Y' and isALL == 'N':
        srcfiles = findfile(srcpath)
        destfiles = findfile(destpath)
        sdfDict = dict()
        # model-根据模块名来区分更新哪些模块下的文件，如果model==excel_all，则更新本次所有获取到的文件
        # model = args[0]
        # isClinet = args[1]
        filelist = []

        files_notexist = []
        if model.upper() == 'EXCEL_ALL' or model.upper() == 'START_ALL':
            logging.info('Models that need update file:--%s' % models_dict.keys())
            for key in models_dict.keys():
                for f in models_dict[key]:
                    filelist.append(f)
        elif model not in models_dict.keys() and isUpdateCode == 'Y' and isALL == 'N':
            logging.warning("Model '%s' have no files in excel! and progaram exit!" % model)
            raise ValueError('Build Failed!')
        else:
            logging.info('Models that need update file:--%s' % model)
            filelist = models_dict[model]
        # 获取某个目录下的所有文件，以"*"标记
        for fl in filelist:
            if '*' in fl:
                fnewp = os.path.join(srcpath, fl.strip('*'))
                fname = ''
                fnewl = findfile(fnewp)
                if fl.startswith('/'):
                    fname = fl[0:fl.strip('/').find('/')]
                else:
                    fname = fl[0:fl.find('/')]
                fnewtmp = []
                for fn in fnewl:
                    fn = fname + fn.split(fname)[1]
                    fnewtmp.append(fn)
                filelist.remove(fl)
                filelist.extend(fnewtmp)
        if len(filelist) > 0:
            # 更新整个模块的文件
            # if filelist[0].endswith('all') or filelist 'ALL':
            #    return filelist[0].upper()
            # 需要更新文件
            # else:
            for i in range(len(filelist)):
                srcf = os.path.join(srcpath, filelist[i])
                destf = os.path.join(destpath, filelist[i])
                # print destf
                if srcf in srcfiles:
                    if destf in destfiles:
                        sdfDict[srcf] = destf
                    # 新增加的文件就只取路径,并创建路径
                    else:
                        destf = destf[0:destf.rfind('/') + 1]
                        if os.path.exists(destf):
                            pass
                        else:
                            os.makedirs(destf)
                        sdfDict[srcf] = destf
                else:
                    # 对不存在的文件进行处理
                    if srcf not in files_notexist:
                        files_notexist.append(srcf)
            if files_notexist:
                logging.warning('Files not exist,and progaram exit!')
                for fnot in files_notexist:
                    logging.warning('Warning:File \"%s\" is not exist!!!!!please sure!!!' % fnot)
                raise ValueError('Build Failed!')
            else:
                return sdfDict
        else:
            logging.error('excel content is none!')
            raise ValueError('Build Failed!')
    elif isUpdateCode == 'Y' and isALL == 'Y' and model.startswith('mo_'):
        sdfDict = dict()
        # if model == 'mo_boss':
        #    model = 'mo_admin'
        key = os.path.join(srcpath, model)
        value = os.path.join(destpath, model)
        sdfDict[key] = value
        return sdfDict
    elif isUpdateCode == 'Y' and isALL == 'Y' and model.upper() == 'START_ALL':
        sdfDict = dict()
        for v in _MODULE_NAME.values():
            if v == 'mo_boss' or v == 'START_ALL':
                pass
            else:
                if v == 'mo_push':
                    v = 'mo_common_push'
                key = os.path.join(srcpath, v)
                value = os.path.join(destpath, v)
                sdfDict[key] = value
        return sdfDict
    elif isUpdateCode == 'Y' and isALL == 'Y' and model.upper() == 'EXCEL_ALL':
        sdfDict = dict()
        for k in models_dict.keys():
            key = os.path.join(srcpath, k)
            value = os.path.join(destpath, k)
            sdfDict[key] = value
        return sdfDict
    else:
        logging.debug('do not need update isUpdateCode=%s,isALL=%s,model=%s' % (isUpdateCode, isALL, model))
        return False


def code_modoule_select(*args):
    # args[0]-选择代码库  args[1]-模块名  args[2]-是否涉及前端
    logging.info("#####################################################################")
    logging.info("########        Moxian_Modoule(ENV_SELECT)                   ########")
    logging.info("#####################################################################")
    logging.info("Please choose the Environment(One Limited)")
    modoule_env_dict = {'1': 'M2', '2': 'Boss_master', '3': 'Boss_v2.0.3', '4': 'Test_M2', '5': 'Test_Boss_master',
                        '6': 'Test_Boss_v2.0.3'}
    for k in modoule_env_dict.keys():
        logging.info('%s -- %s' % (k, modoule_env_dict[k]))
    global cms
    cms = args[0]
    logging.info('your choicse is %s-%s' % (cms, modoule_env_dict[cms]))
    model = args[1]
    isClinet = args[2]
    # 如果是Mosses环境，则生成一个临时文件
    if str(cms) == '4' or str(cms) == '5' or str(cms) == '6':
        # f = open('/home/moxian_package/mosses.tmp','w')
        time.sleep(1)
        # f.close()
        print 'mosses.tmp ================='
    if str(cms) == '1' or str(cms) == '4':
        sdfDict = getCodefiles(_code_moxian_m2, _codeCNM2, model, isClinet=isClinet)
        return sdfDict
    elif str(cms) == '2' or str(cms) == '5':
        sdfDict = getCodefiles(_code_moxian_boss, _codeCNBoss, model, isClinet=isClinet)
        return sdfDict
    elif str(cms) == '3' or str(cms) == '6':
        sdfDict = getCodefiles(_code_moxian_boss_v202, _codeCNBoss_v202, model, isClinet=isClinet)
        return sdfDict
    else:
        print 'Input Wrong!'
        raise ValueError('Build Failed!')


def env_select_forpackage(*args):
    logging.info("#####################################################################")
    logging.info("########        Moxian_Package(ENV_SELECT)                   ########")
    logging.info("#####################################################################")
    for k in _env_for_package.keys():
        logging.info('%s--%s' % (k, _env_for_package[k]))
    global env_forpackage
    env_forpackage = args[0]
    logging.info('your choicse is %s--%s' % (env_forpackage, _env_for_package[env_forpackage]))


_wars_path = _wars_path_online


class Compile(object):
    def __init__(self, i, iswriteExcel):
        self.module = switchmodule(i)
        self.i = i
        if iswriteExcel == 'EY':
            self.w_excel_flag = True
        else:
            self.w_excel_flag = False

    @property
    def gradle(self):
        global _wars_path
        module = self.module
        if module == 'mo_push': module = 'mo_common_push'
        if module == 'mo_boss': module = 'mo_admin'
        fo = FilesOperations()
        if type(module) == types.StringType:
            buildpath = os.getcwd()
            if env_forpackage.startswith('3'):
                _wars_path = _wars_path_online
                fo.copycodetobuild(env_forpackage)
                switchpath(module)
                fo.deletefiles(os.getcwd())
            elif env_forpackage.startswith('2'):
                _wars_path = _wars_path_beta
            elif env_forpackage.startswith('1'):
                _wars_path = _wars_path_cn
            elif env_forpackage.startswith('4'):
                _wars_path = _wars_path_test
            switchpath(module)
            buildpath = os.getcwd()
            logging.debug('>>>>>build path is:%s' % buildpath)
            logging.info('>>>>>current path:%s' % os.getcwd())
            logging.info(">>>>>%s Module compileing...,please wait" % module)
            logging.debug('excute cmd:gradle clean war')
            pp = subprocess.Popen("gradle clean war", shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            # 解决Popen进程卡住的问题
            stdout, stderr = pp.communicate()
            pp.wait()
            logging.debug(20 * '=' + 'module ' + module + '\'s results begin' + 20 * '=')
            logging.error(stderr)
            logging.debug(stdout)
            logging.debug(20 * '=' + 'module ' + module + '\'s results end' + 20 * '=')
            if module == "mo_common_permission": module = "mo_permission"
            if module == "mo_admin": module = "mo_boss"
            if module == "mo_game_mining": module = "mo_mining"
            if module == "mo_page": module = "mo_page"
            if os.path.exists("build/libs/%s.war" % module):
                logging.info(">>>>>%s Module,Build Success." % module)
                war = fo.findwar(buildpath)
                logging.info('excute gradle clean !')
                # 执行gradle clean 命令以便清理掉前面编译后产生的build文件夹
                os.system("gradle clean")
                logging.info('begin write the result to excel!')
                if module == "mo_permission": module = "mo_common_permission"
                if module == "mo_boss": module = "mo_admin"
                if module == "mo_mining": module = "mo_game_mining"
                if module == "mo_page": module = "mo_page"
                writeExcel = writeexcel(iswrite=self.w_excel_flag)
                sheetName, lineNum, datasList = writeExcel.GetrowsAndData(module)
                writeExcel.writeinexcel(sheetName, lineNum, datasList, module)
                logging.info('write the result to excel finished!')
            else:
                logging.error(">>>>>%s Module,Build Failed!" % module)
                logging.error(">>>>>请注意，模块:%s 编译失败，以上为编译日志，请截取给开发定位！" % module)
                raise ValueError('Build Failed!')
        elif type(module) == types.ListType:
            build_sucess = []
            build_failed = []
            n = 1
            for m in module:
                buildpath = ''
                logging.debug(20 * '=' + 'the ' + str(n) + ' module ' + m + '\'s results begin' + 20 * '=')
                fo = FilesOperations()
                if env_forpackage.startswith('3'):
                    _wars_path = _wars_path_online
                    fo.copycodetobuild(ENV)
                    switchpath(m)
                    fo.deletefiles(os.getcwd())
                elif env_forpackage.startswith('2'):
                    _wars_path = _wars_path_beta
                elif env_forpackage.startswith('1'):
                    _wars_path = _wars_path_cn
                elif env_forpackage.startswith('4'):
                    _wars_path = _wars_path_test
                if m == 'mo_push': m = 'mo_common_push'
                if m == 'mo_boss': m = 'mo_admin'
                switchpath(m)
                # if ENV in ['11','12','13']:
                buildpath = os.getcwd()
                logging.debug('>>>>>build path is:%s' % buildpath)
                logging.info('>>>>>current path:--%s' % os.getcwd())
                logging.info(">>>>>%s Module compileing...,please wait" % m)
                logging.debug('excute cmd:gradle clean war')
                pp = subprocess.Popen("gradle clean war", shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                # out = pp.stdout.readlines()
                # err = pp.stderr.readlines()
                stdout, stderr = pp.communicate()
                pp.wait()
                logging.debug(20 * '=' + 'module ' + m + '\'s results begin' + 20 * '=')
                logging.error(stderr)
                logging.debug(stdout)
                logging.debug(20 * '=' + 'module ' + m + '\'s results end' + 20 * '=')
                logging.debug(20 * '=' + 'the ' + str(n) + ' module ' + m + '\'s results end' + 20 * '=')
                n += 1
                # os.popen("gradle clean war >> %s 2>&1" % _log_file)
                if m == "mo_common_permission": m = "mo_permission"
                if m == "mo_admin": m = "mo_boss"
                if m == "mo_game_mining": m = "mo_mining"
                if module == "mo_page": module = "mo_page"
                if os.path.exists("build/libs/%s.war" % m):
                    logging.info(">>>>>%s Module,Build Success." % m)
                    build_sucess.append(m)
                    war = fo.findwar(buildpath)
                    logging.info('excute gradle clean !')
                    os.system("gradle clean")
                    logging.info('begin write the result to excel!')
                    if m == "mo_permission": m = "mo_common_permission"
                    if m == "mo_boss": m = "mo_admin"
                    if m == "mo_mining": m = "mo_game_mining"
                    if module == "mo_page": module = "mo_page"
                    writeExcel = writeexcel(iswrite=self.w_excel_flag)
                    sheetName, lineNum, datasList = writeExcel.GetrowsAndData(m)
                    writeExcel.writeinexcel(sheetName, lineNum, datasList, m)
                else:
                    logging.error("********************Failed********************")
                    logging.error(">>>>>Error:%s Module,Build Failed!" % m)
                    logging.error(">>>>>请注意，模块:%s 编译失败，以上为编译日志，请截取给开发定位！" % m)
                    logging.error("********************Failed********************\n\n\n")
                    if ENV == '1' or ENV == '4': deletewar(_wars_path + '/' + m + '.war')
                    build_failed.append(m)
            logging.info('build sucessful number:%d,details:%s' % (len(build_sucess), build_sucess))
            logging.warning('build failed number:%d,details:%s' % (len(build_failed), build_failed))
            logging.info(">>>>>请注意，以上两行日志为编译结果，请注意是否有编译失败的包！\n\n")


def main(*args):
    # 更新的代码文件相关操作
    # *args参数：args[0]--选择代码库：1.M2 2.Boss_master 3.Boss_v2.0.3 4.Test_M2 5.Test_Boss_master 6.Test_Boss_v2.0.3
    #           args[1]--模块名
    #           args[2]--选择环境：1.CN 2.Beta 3.Production 4.Test
    #           args[3]--是否校验“是否涉及前端” True:校验，False:不校验
    #           args[4]--选择打哪个环境的包：1.1 M2_CN     1.2 BOSS_master_CN     1.3 Boss_v2.0.3_CN;
    #                                      2.1 M2_Beta   2.2 Boss_master_Beta   2.3 Boss_v2.0.3_Beta;
    #                                      3.1 M2_Online 3.2 Boss_master_Online 3.3 Boss_v2.0.3_Online;
    #                                      4.1 M2_Test   4.2 Boss_master_Test   4.3 Boss_v2.0.3_Test.
    #           args[5]--是否需要更新代码文件：Y:需要更新，N:不需要更新
    #           args[6]--是否拉全量代码打:   Y :是，N:否
    #           args[7]-是否写结果到excel： EY :是，EN:否
    logging.debug('main args: ' + len(args) * '-%s' % args)
    if args[1].upper() == 'EXCEL_ALL' and args[5].upper() == 'N':
        excel = getexcel(args[3], args[1])
        set_excel_models = excel.getfilepath()
    envs = args[2]
    e = env_select(envs)
    if not e:
        raise ValueError('Build Failed!')
    global _moudles
    global _envpath
    # logging.debug('-------ENV:%s' % ENV)
    if ENV == '1':
        if args[0] == '3':
            _moudles = os.listdir(_boss_branch_cn)
            _envpath = _boss_branch_cn
        elif args[0] == '2':
            _moudles = os.listdir(_boss_master_cn)
            _envpath = _boss_master_cn
        else:
            _moudles = os.listdir(_cnpath)
            _envpath = _cnpath
    elif ENV == '2':
        if args[0] == '3':
            logging.debug(_boss_branch_beta)
            _moudles = os.listdir(_boss_branch_beta)
            _envpath = _boss_branch_beta
        elif args[0] == '2':
            _moudles = os.listdir(_boss_master_beta)
            _envpath = _boss_master_beta
        else:
            _moudles = os.listdir(_betapath)
            _envpath = _betapath
    elif ENV == '3':
        if args[0] == '3':
            _moudles = os.listdir(_boss_branch_online)
            _envpath = _boss_branch_online
        elif args[0] == '2':
            _moudles = os.listdir(_boss_master_online)
            _envpath = _boss_master_online
        else:
            _moudles = os.listdir(_productionpath)
            _envpath = _productionpath
    elif ENV == '4':
        if args[0] == '3':
            _moudles = os.listdir(_boss_branch_test)
            _envpath = _boss_branch_test
        elif args[0] == '2':
            _moudles = os.listdir(_boss_master_test)
            _envpath = _boss_master_test
        else:
            _moudles = os.listdir(_mossespath)
            _envpath = _mossespath
    logging.info('Enviroment path:%s' % _envpath)

    for index, key in enumerate(_moudles):
        _MODULE_NAME[index + 1] = key
    _MODULE_NAME[0] = 'START_ALL'
    # _MODULE_NAME[len(_moudles)+1] = 'Exit'

    allModel = _MODULE_NAME.values()
    allModel.append('EXCEL_ALL')
    if args[1].upper() not in ['START_ALL', 'EXCEL_ALL']:
        if args[1] not in allModel:
            logging.error('script arg2-model name wrong:%s,it must be in %s' % (args[1], allModel))
            raise ValueError('Build Failed!')

    global isUpdateCode
    global isALL
    isUpdateCode = args[5].upper()
    isALL = args[6].upper()
    sdfDict = code_modoule_select(args[0], args[1], args[3])
    if isinstance(sdfDict, dict):
        logging.info('>>>>>Total File:%d' % len(sdfDict))
        n = 1
        for key in sdfDict.keys():
            logging.info('---------- copy time:%d ----------' % n)
            if os.path.isfile(key):
                logging.info('copye \"%s\" to \"%s\"' % (key, sdfDict[key]))
                copyfile_code(key, sdfDict[key])
                n += 1
            elif os.path.isdir(key):
                copyfile_code_all(key, sdfDict[key])
                n += 1
            else:
                logging.error('unknow path:%s' % key)
        compareMd5_code(sdfDict)
    else:
        logging.info('isUpdateCode=%s,do not need update code' % isUpdateCode)

    logging.info('###################################################################')
    logging.info('########            Moxian_Package(send)                   ########')
    logging.info('###################################################################')
    for key in _MODULE_NAME.keys():
        logging.info("{a}.{b}".format(a=key, b=_MODULE_NAME[key]))
    i = ''
    if args[1].upper() == 'EXCEL_ALL':
        # excel = getexcel(args[3],args[1])
        # excel_models = excel.getfilepath()
        global excel_models
        for ek in excel_models.keys():
            if ek == 'mo_admin':
                ek = 'mo_boss'
            elif ek == 'mo_common_push':
                ek = 'mo_push'
            for k in _MODULE_NAME.keys():
                if _MODULE_NAME[k] == ek and len(excel_models) > 1:
                    i = i + str(k) + ','
                elif _MODULE_NAME[k] == ek and len(excel_models) < 2:
                    i = str(k)
    elif args[1].upper() == 'START_ALL':
        # i = '0'
        for k in _MODULE_NAME.keys():
            if str(args[0]) in ['1', '4']:
                if _MODULE_NAME[k] == 'mo_boss':
                    logging.debug('env M2,do not need mo_boss.')
                elif _MODULE_NAME[k] == 'START_ALL':
                    pass
                else:
                    i = i + str(k) + ','
            else:
                i = 0
    else:
        for k in _MODULE_NAME.keys():
            if _MODULE_NAME[k] == args[1]:
                i = str(k)

    if str(i).endswith(','):
        i = i.strip(',')
        logging.info('your chois:%s' % i)
    if len(i.split(',')) < 2:
        logging.info(">>>>>Your choose is %s-%s" % (str(i), _MODULE_NAME[int(i)]))
    module = switchmodule(i)
    # 如果是m2的，则屏蔽掉boss模块
    logging.debug('--------moudule name:%s' % module)
    # 配置文件相关操作
    filedict = singleSrcAndDest(module)
    logging.info('>>>>>Total modules:%d' % len(filedict))
    if len(filedict) == 0:
        logging.error('no module\'s config files found,please sure!')
        raise ValueError('Build Failed!')
    for key in filedict.keys():
        logging.info('copy \"%s\" to \"%s\"' % (key, filedict[key]))
        copyfile(key, filedict[key])
    compareMd5_config(module)
    # 编译war包
    env_select_forpackage(args[4])
    cmp = Compile(i, args[7])
    cmp.gradle
    move = Move(i, ENV)
    move.copy
    # global cf
    # if ENV == '1':
    #     #logging.debug('eeeeeeeeeeeeeeeeeee---%s' % _CFG_CN_PATH)
    #     cf = setconfig(_CFG_CN_PATH)
    # elif ENV == '4':
    #     logging.debug('eeeeeeeeeeeeeeeeeee---%s' % _CFG_TEST_PATH)
    #     cf = setconfig(_CFG_TEST_PATH)
    # if ENV == '1' or ENV == '4':
    #     mkdir = MkDir(i)
    #     mkdir.new
    #     scp = SCP(i,ENV)
    #     scp.scpsend
    #     tomcat = TomCat(i)
    #     tomcat.restart


if __name__ == '__main__':
    # 各环境下对应的选择
    # value值（如:1-1-1.1）分别对应main方法中的arg0、arg2、arg4
    initLogging(_log_file)
    allselect = {
        'cnm2': '1-1-1.1',
        'cnbossmaster': '2-1-1.2',
        'cnbossv': '3-1-1.3',
        'betam2': '1-2-2.1',
        'betabossmaster': '2-2-2.2',
        'betabossv': '3-2-2.3',
        'onlinem2': '1-3-3.1',
        'onlinebossmaster': '2-3-3.2',
        'onlinebossv': '3-3-3.3',
        'testm2': '1-4-4.1',
        'testbossmaster': '2-4-4.2',
        'testbossv': '3-4-4.3'
    }
    # 脚本参数：arg1-选择对应的环境（allselect的keys）
    #          arg2-模块名(其中-EXCEL_ALL表示从Excel文件中获取所有模块，START_ALL表示所有模块)
    #          arg3-是否校验“是否涉及前端”
    #          arg4-是否需要更新代码文件：Y:需要更新，N:不需要更新
    #          arg5-是否拉全量代码打:   Y :是，N:否
    #          arg6-是否写结果到excel： EY :是，EN:否
    args = sys.argv
    # print args
    if len(args) != 7:
        logging.error('script arg number error!')
        raise ValueError('Build Failed!')
    if args[1] in allselect.keys():
        main_arg0 = allselect[args[1]].split('-')[0]
        main_arg2 = allselect[args[1]].split('-')[1]
        main_arg4 = allselect[args[1]].split('-')[2]
    else:
        logging.error('script arg1-%s not correct! this mast be in %s' % (args[1], allselect.keys()))
        raise ValueError('Build Failed!')
    main_arg1 = args[2]
    if 'boss' in args[1]:
        if main_arg1 != 'mo_boss':
            logging.warning(
                "selected boss,so script arg2 must be 'mo_boss'(your given '%s'),and i will set it as 'mo_boss'" % main_arg1)
            main_arg1 = 'mo_boss'
    main_arg3 = args[3]
    if main_arg3 not in ['True', 'False']:
        logging.error('script arg3-%s not correct! this mast be %s'(main_arg3, 'True or False'))
        raise ValueError('Build Failed!')
    ny = ['y', 'Y', 'n', 'N']
    main_arg5 = args[4].upper()
    if main_arg5 not in ny:
        logging.error('script arg4-%s not correct! this mast be in %s' % (main_arg5, ny))
        raise ValueError('Build Failed!')
    main_arg6 = args[5].upper()
    if main_arg6 not in ny:
        logging.error('script arg5-%s not correct! this mast be in %s' % (main_arg6, ny))
        raise ValueError('Build Failed!')
    main_arg7 = args[6].upper()
    if main_arg7 not in ['EN', 'EY']:
        logging.error('script arg5-%s not correct! this mast be in %s' % (main_arg6, ['EN', 'EY']))
        raise ValueError('Build Failed!')
    logging.info("script's args:arg1=%s,arg2=%s,arg3=%s,arg4=%s,arg5=%s,arg6=%s" % (
    args[1], args[2], args[3], args[4], args[5], args[6]))
    main(main_arg0, main_arg1, main_arg2, main_arg3, main_arg4, main_arg5, main_arg6, main_arg7)

    # writeexcel = writeexcel(iswrite=True)
    # sheetName,lineNum,datasList = writeexcel.GetrowsAndData('mo_order')
    # writeexcel.writeinexcel(sheetName,lineNum,datasList,'mo_order')


