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

    # 定义损失函数和优化器
    lossFunc = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001)
    inputs = torch.tensor(inputData, dtype=torch.float32)
    targets = torch.tensor(targetData, dtype=torch.float32)

    # 训练模型
    num_epochs = 400000
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
    x_test = torch.tensor(testData, dtype=torch.float32)
    with torch.no_grad():
        predicted = model(x_test)

    for i in range(len(x_test)):
            print("Input: {} Predicted: {}".format(x_test[i].tolist(), predicted[i].tolist()))


if __name__ == "__main__":
        model = LinearRegression()
        BallDataList = []
        AllDataMap = Selenium_Result_Update.GetFileDate('2024-01-01')#recommend number date
        for data in AllDataMap.values():
            BallDataList.append(data)
        redTopKeys,blueTopKeys = Selenium_DoubleBall.Analyse(BallDataList)
        legth = len(BallDataList)

        inputData=[]
        targetData=[]
        random.seed(10086)

        for i in range(legth - 10, legth-1):  
            #seed = int(time.time() * 10000000)
            #random.seed(seed)     
            sliced_list = BallDataList[:i]
            AllDataList = Selenium_DoubleBall.DoRecommend(redTopKeys,blueTopKeys,0,0,100,sliced_list,False,False)
            nextData = BallDataList[i]

            for data in AllDataList:
                inputData.append(data.front + data.back)
            targetData = nextData.red + [nextData.blue]
            train(model,inputData,[targetData])

        #seed = int(time.time() * 10000000)
       # random.seed(seed)     
        testData = []
        last = legth - 1   
        sliced_list = BallDataList[:last]
        recList = Selenium_DoubleBall.DoRecommend(redTopKeys,blueTopKeys,0,0,5,sliced_list,False,False)
        for data in recList:
                testData.append(data.front + data.back)
        nextData = BallDataList[last]

        Predicted(model,testData)
        print(nextData.red + [nextData.blue])

            

