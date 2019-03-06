import urllib.request
import os

#-----------------------------------------------------------------------------

#访问url并返回html数据

def url_open(url):

    #创建一个req对象，把url传进去
    req = urllib.request.Request(url)
    
    #在req之后加入header,伪装成浏览器访问页面
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')
    
    #判断访问页面是否存在，如果存在返回页面数据，如果不存在返回0
    try:
        response = urllib.request.urlopen(url)
        html = response.read()


    #如果返回错误为404，返回0
    except urllib.error.HTTPError as e:
        
        if e.code == 404:
            return 0

    return html


#-----------------------------------------------------------------------------


def get_imgs_url(url):
    #定义一个数组存放当前页面所有图集的地址
    imgs_url = []

    #对网页进行编码处理
    html = url_open(url).decode('utf-8')


    #定位数字的具体索引并存入数组

    a = html.find('<a href="http://www.win4000.com/meinv')
    #遍历获取当前页面图集的数字
    while(a!=-1):
        
        b = html.find('.html"',a)

        if b!=-1:
            if len(html[a+37:b])==6:
                imgs_url.append(html[a+9:b+5])
        else:
            b=a+10
        a = html.find('<a href="http://www.win4000.com/meinv',b)

    return imgs_url


#-----------------------------------------------------------------------------

#查找每张图片的地址并存入数组
def find_imgs(imgs_url):#一个图集的传到这里
    #定义一个数组把图集中所有图片所在页面的地址存入
    img_addrs = []
    #遍历所有图片地址并存入数组
    for i in range(1,50):
        img_url=imgs_url[:-5]+'_'+str(i)+'.html'
        if url_open(img_url)!=0:
            img_addrs.append(img_url)
        else:
            break

    

        
    #定义一个数组把图片地址存入
    imgs_jpgs = []
    #遍历所有图片所在页面地址
    for img_addr in img_addrs:
        
        #对网页进行编码处理
        html = url_open(img_addr).decode('utf-8')
                

        #定位到图片前后索引
        a = html.find('data-original')
        b = html.find('.jpg' ,a,a+255)

        #将图片地址存入数组
        imgs_jpgs.append(html[a+15:b+4])

    return imgs_jpgs
        


#-----------------------------------------------------------------------------
                     


#将图片全部保存到文件夹
def save_imgs(imgs_jpgs,url,root_addr):
    #对网页进行编码处理
    html = url_open(url).decode('utf-8')
    #获得当前下载的图集名称
    a = html.find('<div class="ptitle"><h1>')
    b = html.find('</h1>',a)

    
    #新建文件夹存入图片
    
    folders = root_addr+'\\'+html[a+24:b]
    #创建文件夹，如果存在结束程序
    if not os.path.exists(folders):
        #os.makedirs(folder)
        os.mkdir(folders)
        #改变当前工作目录到此文件夹
        os.chdir(folders)
    else:
        try:
            return 0

        except:
            print('Error')

    print("正在下载-->"+html[a+24:b]+',请稍等哦。。。^_^')
    #将图片写入
    i=1
    #遍历图片并保存
    for img in imgs_jpgs:
        filename = html[a+24:b]+'_'+str(i)+'.jpg'
        with open(filename,'wb') as f:
            img = url_open(img)
            f.write(img)    
        i=i+1
    print(html[a+24:b]+'已下载完成，快去享受吧^_^')
    print("------------------------------------------------")
    return 1


#-----------------------------------------------------------------------------

    
def download_mm(folder='小姐姐'):

    #在exe目录下创建文件夹，如果文件夹不存在，创建文件夹，如果文件夹不存在，将工作目录改变到此文件夹
    print('欢迎电脑前的帅锅美女访问本软件，非常荣幸为你们服务^_^')
    print('本软件支持多次下载，第二次运行可以继续下载哦，请放心使用^_^')
    print('那么让我们马上开始欣赏小姐姐们吧^_^')

    while True:
        go_num = input('请输入 go 开始我们的视觉盛宴吧----->')
        if go_num == 'go':
            break
        else:
            print('你输入错误了哦，请重新输入吧^_^')
            
        
    if not os.path.exists(folder):
        #创建文件夹
        os.mkdir(folder)
        #改变当前工作目录到此文件夹
        os.chdir(folder)
    else:
        #改变当前工作目录到此文件夹
        os.chdir(folder)

    #保存根目录位置
    root_addr = os.getcwd()

    
    #定义一个数组存放图集的六位数编号
    imgs_url = []
    
    #定义当前访问页数
    now_page=1
          
    while now_page<=5:

        #要访问的url地址
        url = "http://www.win4000.com/meinvtag346_"+str(now_page)+".html"

        #将所有图集的地址存入数组
        imgs_url=imgs_url+get_imgs_url(url)
        #指向下一页面
        now_page=now_page+1
    #定义一个数字存放本次更新数
    updata_num = 0
    #遍历所有图集的地址
    for each in imgs_url:
        #定义一个数组存放图片的地址
        imgs_jpg = []
        imgs_jpg = find_imgs(each)
        #保存图片到计算机
        num = save_imgs(imgs_jpg,each,root_addr)
        if num == 0:
            continue
        else:
            updata_num+=1
    print('本次共更新%s个图集，棒棒哒^_^'%updata_num)
    
    while True:
        exit_num = input("已经下载完毕了哦，如果还满意的话就刷个  666  吧----->")
        if exit_num == '666':
            exit()
        else:
            print('你输入错误了哦^_^,请重新输入吧')

            
        




if __name__ =='__main__':
    download_mm()
