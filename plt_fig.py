import matplotlib.pyplot as plt
def plt_fig(title, xlabel,ylabel,xlst,ylst,legend='default'):
    plt.plot(xlst,ylst,label=legend)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()
    plt.close()

    
def pd_show(value):
    mongo_client = pymongo.MongoClient('127.0.0.1', 27017)
    mongo_db = mongo_client['股票']
    mongo_collection = mongo_db['指数']
    select_item = mongo_collection.find({'名称':value},{'_id':0,'名称':0,'涨跌幅':0})
    df.rename(columns={'最新价':'上证指数'},inplace=False)
    df.plot()
