import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as Data

# 准备数据
x_train = torch.randn(33)
y_train = 3*x_train + 2 + 0.4*torch.randn(33)

# 构建模型
class LinearRegression(nn.Module):
    def __init__(self):
        super(LinearRegression, self).__init__()
        self.linear = nn.Linear(3, 3)

    def forward(self, x):
        return self.linear(x)

model = LinearRegression()

# 定义损失函数和优化器
lossFunc = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# 模拟一些数据
base = 1.0
list1 = []
for i in range(33):
    list1.append(base + i)


#inputs = torch.tensor(list1, dtype=torch.float32)
#targets = torch.tensor(y_train, dtype=torch.float32)
data1 = [[1,2,3], [7,8,9]]
data2 = [[4,5,6]]

inputs = torch.tensor(data1, dtype=torch.float32)
targets = torch.tensor(data2, dtype=torch.float32)

# 训练模型
num_epochs = 100
for epoch in range(num_epochs):

    optimizer.zero_grad()
    outputs = model(inputs)
    loss = lossFunc(outputs, targets)
    loss.backward()
    optimizer.step()

    if (epoch+1) % 10 == 0:
        print('Epoch [{}/{}], Loss: {:.4f}'.format(epoch+1, num_epochs, loss.item()))

torch.save(model.state_dict(), 'model.pth')

model = LinearRegression()  # 实例化模型
model.load_state_dict(torch.load('model.pth'))
#model.eval()  # 确保模型处于评估模式

#训练模式
#model.train()
              
# 设置模型为评估模式
model.eval()

# 准备测试数据
x_test = torch.tensor([[1,2,3], [2,4,9]], dtype=torch.float32)

with torch.no_grad():
    predicted = model(x_test)

for i in range(len(x_test)):
        print("Input: {} Predicted: {}".format(x_test[i].tolist(), predicted[i].tolist()))



