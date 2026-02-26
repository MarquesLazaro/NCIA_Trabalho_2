import torch
import torch.nn as nn


class LSTMModel(nn.Module):
    def __init__(self, input_size=13, num_classes=2):
        super(LSTMModel, self).__init__()

        # Taxas de dropout separadas para evitar sobrescrita
        self.drop_10 = nn.Dropout(0.1)
        self.drop_20 = nn.Dropout(0.2)

        # Feature Extractors (LSTMs)
        self.lstm1 = nn.LSTM(input_size, 32, batch_first=True, bidirectional=True)
        self.lstm2 = nn.LSTM(64, 32, batch_first=True, bidirectional=True)
        self.lstm3 = nn.LSTM(64, 64, batch_first=True, bidirectional=True)

        # Camadas Densas
        self.fc1 = nn.Linear(128, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 64)
        self.fc4 = nn.Linear(64, 128)
        self.fc_final = nn.Linear(128, num_classes)

    def forward(self, x):
        # Bloco LSTM
        x, _ = self.lstm1(x)
        x = self.drop_10(x)  # Dropout 0.1 após LSTM 1

        x, _ = self.lstm2(x)
        x = self.drop_10(x)  # Dropout 0.1 após LSTM 2

        output, _ = self.lstm3(x)
        x = output[:, -1, :]  # Pega apenas o último timestep da sequência
        x = self.drop_20(x)  # Dropout 0.2 após LSTM 3

        # Bloco Denso (com ReLU para transformação não linear)
        x = torch.relu(self.fc1(x))
        x = self.drop_10(x)  # Dropout 0.1 após Dense 1

        x = torch.relu(self.fc2(x))
        x = self.drop_10(x)  # Dropout 0.1 após Dense 2

        x = torch.relu(self.fc3(x))
        x = self.drop_20(x)  # Dropout 0.2 após Dense 3

        x = torch.relu(self.fc4(x))
        x = self.drop_20(x)  # Dropout 0.2 após Dense 4

        # Retorna os logits brutos
        return self.fc_final(x)
