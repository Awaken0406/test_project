import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as Data
import Selenium_Result_Update
import Selenium_DoubleBall
import random
import time

# 构建模型
class LinearRegression(nn.Module):
    def __init__(self):
        super(LinearRegression, self).__init__()
        self.linear = nn.Linear(7, 7)

    def forward(self, x):
        return self.linear(x)
    

def train(model,inputData,targetData):

    inputs = torch.tensor(inputData, dtype=torch.float32).to(device)
    targets = torch.tensor(targetData, dtype=torch.float32).to(device)

    # 训练模型
    num_epochs = 40000
    for epoch in range(num_epochs):

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = lossFunc(outputs, targets)
        loss.backward()
        optimizer.step()
        if (epoch+1) % 10 == 0:
            loss = loss.item()
            print('Epoch [{}/{}], Loss: {:.4f}'.format(epoch+1, num_epochs, loss))
            if loss < 1.0:
                 break


def Predicted(model,testData):
    # 设置模型为评估模式
    model.eval()
    x_test = torch.tensor(testData, dtype=torch.float32).to(device)
    with torch.no_grad():
        predicted = model(x_test)

    for i in range(len(x_test)):
            print("Input: {} Predicted: {}".format(x_test[i].tolist(), predicted[i].tolist()))


def TrainData(model):
        model = model.to(device)
        model.train()
        BallDataList = []
        AllDataMap = Selenium_Result_Update.GetFileDate('2020-01-01')#train date
        for data in AllDataMap.values():
            BallDataList.append(data)

        legth = len(BallDataList)
        inputData=[]
        targetData=[]   
        for i in range(legth):  
            #seed = int(time.time() * 10000000)
            random.seed(10086)     
            sliced_list = BallDataList[:i]
            redTopKeys,blueTopKeys = Selenium_DoubleBall.Analyse(sliced_list)
            AllDataList = Selenium_DoubleBall.DoRecommend(redTopKeys,blueTopKeys,0,0,1000,sliced_list,False,False)
            nextData = BallDataList[i]

            for data in AllDataList:
                inputData.append(data.front + data.back)
            targetData = nextData.red + [nextData.blue]
            train(model,inputData,[targetData])
        torch.save(model.state_dict(), 'model2.pth')

def PredictedData(model,dateStr):
        model = model.to(device)
        model.eval()
        BallDataList = []
        AllDataMap = Selenium_Result_Update.GetFileDate('2020-01-01')
        for data in AllDataMap.values():
            BallDataList.append(data)
            if(data.date == dateStr):
                 break
        legth = len(BallDataList)
        #seed = int(time.time() * 10000000)
        random.seed(10086)     
        testData = []
        last = legth - 1   
        sliced_list = BallDataList[:last]
        redTopKeys,blueTopKeys = Selenium_DoubleBall.Analyse(sliced_list)
        recList = Selenium_DoubleBall.DoRecommend(redTopKeys,blueTopKeys,0,0,5,sliced_list,False,False)
        for data in recList:
                testData.append(data.front + data.back)
        Predicted(model,testData)
        nextData = BallDataList[last]
        print(nextData.red + [nextData.blue])

if __name__ == "__main__":
        model = LinearRegression()
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {device}")
        model = LinearRegression()
        model.load_state_dict(torch.load('model2.pth'))
       
        # 定义损失函数和优化器
        lossFunc = nn.MSELoss()
        optimizer = optim.SGD(model.parameters(), lr=0.001)
        #训练数据
        #TrainData(model)

        #预测数据
        PredictedData(model,'2024-12-24')
        print(f"Using device: {device}")
      
        

            

