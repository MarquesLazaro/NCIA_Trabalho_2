import torch
import torch.nn as nn


class GRUModel(nn.Module):
    def __init__(self, input_size=13, num_classes=2):
        super(GRUModel, self).__init__()

        # --- BLOCO RECORRENTE (BIDIRECIONAL) ---

        # Camada 1: Bidirectional GRU (32 unidades) -> Saída por direção: 32. Total: 64.
        self.gru1 = nn.GRU(input_size, 32, batch_first=True, bidirectional=True)
        # Camada 2: Dropout (0.1)
        self.dropout1 = nn.Dropout(0.1)

        # Camada 3: Bidirectional GRU (32 unidades) -> Saída: 64.
        self.gru2 = nn.GRU(64, 32, batch_first=True, bidirectional=True)
        # Camada 4: Dropout (0.1)
        self.dropout2 = nn.Dropout(0.1)

        # Camada 5: Bidirectional GRU (64 unidades) -> Saída: 128.
        self.gru3 = nn.GRU(64, 64, batch_first=True, bidirectional=True)
        # Camada 6: Dropout (0.2)
        self.dropout3 = nn.Dropout(0.2)

        # --- BLOCO DENSO (FULLY CONNECTED) ---

        # Camada 7: Dense (64)
        self.fc1 = nn.Linear(128, 64)
        # Camada 8: Dropout (0.1)
        self.dropout4 = nn.Dropout(0.1)

        # Camada 9: Dense (64)
        self.fc2 = nn.Linear(64, 64)
        # Camada 10: Dropout (0.1)
        self.dropout5 = nn.Dropout(0.1)

        # Camada 11: Dense (64)
        self.fc3 = nn.Linear(64, 64)
        # Camada 12: Dropout (0.2)
        self.dropout6 = nn.Dropout(0.2)

        # Camada 13: Dense (128)
        self.fc4 = nn.Linear(64, 128)
        # Camada 14: Dropout (0.2)
        self.dropout7 = nn.Dropout(0.2)

        # Camada Final de Classificação (Anomalia vs Normal)
        self.fc_final = nn.Linear(128, num_classes)

    def forward(self, x):
        # x esperado: (batch, tempo, características)

        # Processamento Recorrente
        x, _ = self.gru1(x)
        x = self.dropout1(x)

        x, _ = self.gru2(x)
        x = self.dropout2(x)

        # Na última camada GRU, pegamos apenas o output do último passo temporal
        # para alimentar as camadas densas (saída tamanho 128)
        output, _ = self.gru3(x)
        x = output[:, -1, :]
        x = self.dropout3(x)

        # Processamento Denso com ativação ReLU
        x = torch.relu(self.fc1(x))
        x = self.dropout4(x)

        x = torch.relu(self.fc2(x))
        x = self.dropout5(x)

        x = torch.relu(self.fc3(x))
        x = self.dropout6(x)

        x = torch.relu(self.fc4(x))
        x = self.dropout7(x)

        # Saída final (Logits)
        return self.fc_final(x)
