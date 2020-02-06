import matplotlib.pyplot as plt#约定俗成的写法plt
import subprocess
import re
def get_data(filename):
    with open(filename,'r',encoding='utf-8') as f:
        ans = f.readlines()
    datas = [an.strip() for an in ans]
    return datas
def get_ping_data(uploadRes):
    ress = uploadRes.split('\n')
    ans = re.findall('(\d*?)ms', ress[-1], re.S)
    return int(ans[0]),int(ans[1]),int(ans[2])
def draw_plot(name_data,max_data,ave_data,min_data):
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False

    x = [i for i in range(len(name_data))]

    fig, ax = plt.subplots(figsize=(15, 8))


    min_line, = ax.plot(x, min_data,color='green',linestyle='--')

    ave_line, = ax.plot(x, ave_data,color='r')
    max_line, = ax.plot(x, max_data,color='blue',linestyle='-.')
    ax.legend((min_line, ave_line,max_line), ("最小响应值","平均响应值","最大响应值"))

    for a, b in zip(x, ave_data):
        ax.text(a, b, b, ha='center', va='bottom', fontsize=10)


    plt.title("不同机房的不同相应位置折线图")
    plt.xlabel('机房位置')
    plt.ylabel('响应值：ms')

    plt.xticks(x,name_data, color='blue')
    plt.savefig('result.png')
if __name__ == '__main__':

    ip_list = get_data('ipList')
    name_data=[]
    max_data = []
    ave_data=[]
    min_data=[]
    for ipplace  in ip_list:

        ip,place = ipplace.split(' ',maxsplit=1)
        cmd = "ping %s -n   10"%(ip)
        (status, uploadRes) = subprocess.getstatusoutput(cmd)
        try:
            minda, maxda, aveda = get_ping_data(uploadRes)
        except:
            continue

        name_data.append(place)
        max_data.append(maxda)
        ave_data.append(aveda)
        min_data.append(minda)
    draw_plot(name_data,max_data,ave_data,ave_data)

