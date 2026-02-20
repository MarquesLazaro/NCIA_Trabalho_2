import torch
from torch import nn


class LSTMModel(nn.Module):
    def __init__(self, input_size=13, num_classes=2):
        super(LSTMModel, self).__init__()

        self.lstm1 = nn.LSTM(input_size, 32, batch_first=True, bidirectional=True)
        self.dropout = nn.Dropout(0.1)

        self.lstm2 = nn.LSTM(64, 32, batch_first=True, bidirectional=True)
        self.dropout = nn.Dropout(0.1)

        self.lstm3 = nn.LSTM(64, 64, batch_first=True, bidirectional=True)
        self.dropout = nn.Dropout(0.2)

        self.fc1 = nn.Linear(128, 64)
        self.dropout = nn.Dropout(0.1)

        self.fc2 = nn.Linear(64, 64)
        self.dropout = nn.Dropout(0.1)

        self.fc3 = nn.Linear(64, 64)
        self.dropout = nn.Dropout(0.2)

        self.fc4 = nn.Linear(64, 128)
        self.dropout = nn.Dropout(0.2)

        self.fc_final = nn.Linear(128, num_classes)

    def forward(self, x):
        x, _ = self.lstm1(x)
        x = self.dropout(x)

        x, _ = self.lstm2(x)
        x = self.dropout(x)

        output, _ = self.lstm3(x)
        x = output[:, -1, :]
        x = self.dropout(x)

        x = torch.relu(self.fc1(x))
        x = self.dropout(x)

        x = torch.relu(self.fc2(x))
        x = self.dropout(x)

        x = torch.relu(self.fc3(x))
        x = self.dropout(x)

        x = torch.relu(self.fc4(x))
        x = self.dropout(x)

        return self.fc_final(x)
