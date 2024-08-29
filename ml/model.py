import multiprocessing

import datasets
import torch
from pytorch_lightning import LightningModule
from torch import nn as nn
from torch.nn import functional as F
from torch.utils.data import DataLoader
from ml.dataset import dataset_collate_function
import math

from torch.optim.lr_scheduler import StepLR

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super(PositionalEncoding, self).__init__()
        self.d_model = d_model
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe.unsqueeze(0))

    def forward(self, x):
        return x + self.pe[:, :x.size(1)].clone().detach()

class Transformer(LightningModule):
    def __init__(self, output_dim, data_path, signal_length, num_layers=6, dropout_rate=0.1):
        super(Transformer, self).__init__()
        self.save_hyperparameters()
        self.embedding = nn.Linear(signal_length, 512)
        self.encoder_layer = nn.TransformerEncoderLayer(
            d_model=512, nhead=8, dim_feedforward=2048, dropout=dropout_rate
        )
        self.transformer_encoder = nn.TransformerEncoder(self.encoder_layer, num_layers=num_layers)
        self.positional_encoding = PositionalEncoding(512, max_len=1500)
        self.output_layer = nn.Linear(512, output_dim)
        self.loss_func = nn.CrossEntropyLoss()

    def forward(self, x):
        # Print details for the first sample in the batch
        sample_index = 0
        
        print(f"Input x shape: {x.shape}")  # Input shape: [32, 1, 1500]
        print(f"Input x (sample {sample_index}): {x[sample_index]}")
        
        x = self.embedding(x)
        print(f"After embedding x shape: {x.shape}")  # Shape: [32, 1, 512]
        print(f"After embedding x (sample {sample_index}): {x[sample_index]}")

        x = self.positional_encoding(x)
        print(f"After positional encoding x shape: {x.shape}")  # Shape: [32, 1, 512]
        print(f"After positional encoding x (sample {sample_index}): {x[sample_index]}")

        x = self.transformer_encoder(x)
        print(f"After transformer encoder x shape: {x.shape}")  # Shape: [32, 1, 512]
        print(f"After transformer encoder x (sample {sample_index}): {x[sample_index]}")

        x = torch.mean(x, dim=1)
        print(f"After averaging x shape: {x.shape}")  # Shape: [32, 512]
        print(f"After averaging x (sample {sample_index}): {x[sample_index]}")

        x = self.output_layer(x)
        print(f"After output layer x shape: {x.shape}")  # Shape: [32, 17]
        print(f"After output layer x (sample {sample_index}): {x[sample_index]}")
        
        return x


    def training_step(self, batch, batch_idx):
        x, y = batch['feature'], batch['label']
        x = x.float()
        y = y.long()
        logits = self(x)
        loss = self.loss_func(logits, y)
        self.log('train_loss', loss)
        print("Logits:", logits)
        print("Loss:", loss.item())
        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=0.0001)
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)
        return [optimizer], [scheduler]

    def train_dataloader(self):
        dataset_dict = datasets.load_dataset(self.hparams.data_path)
        dataset = dataset_dict[list(dataset_dict.keys())[0]]
        try:
            num_workers = multiprocessing.cpu_count()
        except:
            num_workers = 1
        return DataLoader(
            dataset,
            batch_size=32,
            shuffle=True,
            num_workers=num_workers,
            collate_fn=dataset_collate_function
        )


# import multiprocessing

# import datasets
# import torch
# from pytorch_lightning import LightningModule
# from torch import nn as nn
# from torch.nn import functional as F
# from torch.utils.data import DataLoader
# from ml.dataset import dataset_collate_function
# import math

# from torch.optim.lr_scheduler import StepLR

# class Transformer(LightningModule):
#     def __init__(self, output_dim, data_path, signal_length, num_layers=6, dropout_rate=0.1):
#         super(Transformer, self).__init__()
#         self.save_hyperparameters()
#         self.embedding = nn.Linear(signal_length, 512)
#         self.encoder_layer = nn.TransformerEncoderLayer(
#             d_model=512, nhead=8, dim_feedforward=2048, dropout=dropout_rate
#         )
#         self.transformer_encoder = nn.TransformerEncoder(self.encoder_layer, num_layers=num_layers)
#         self.positional_encoding = PositionalEncoding(512, max_len=1500)
#         self.output_layer = nn.Linear(512, output_dim)
#         self.loss_func = nn.CrossEntropyLoss()

#     def forward(self, x):
#         x = self.embedding(x)
#         x = self.positional_encoding(x)
#         x = self.transformer_encoder(x)
#         x = torch.mean(x, dim=1)
#         x = self.output_layer(x)
#         return x

#     def training_step(self, batch, batch_idx):
#         x, y = batch['feature'], batch['label']
#         x = x.float()
#         y = y.long()
#         logits = self(x)
#         loss = self.loss_func(logits, y)
#         self.log('train_loss', loss)
#         return loss

#     def configure_optimizers(self):
#         optimizer = torch.optim.Adam(self.parameters(), lr=0.0001)
#         scheduler = StepLR(optimizer, step_size=10, gamma=0.1)
#         return [optimizer], [scheduler]

#     def train_dataloader(self):
#         dataset_dict = datasets.load_dataset(self.hparams.data_path)
#         dataset = dataset_dict[list(dataset_dict.keys())[0]]
#         try:
#             num_workers = multiprocessing.cpu_count()
#         except:
#             num_workers = 1
#         return DataLoader(
#             dataset,
#             batch_size=32,
#             shuffle=True,
#             num_workers=num_workers,
#             collate_fn=dataset_collate_function
#         )

# class PositionalEncoding(nn.Module):
#     def __init__(self, d_model, max_len=5000):
#         super(PositionalEncoding, self).__init__()
#         self.d_model = d_model
#         pe = torch.zeros(max_len, d_model)
#         position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
#         div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
#         pe[:, 0::2] = torch.sin(position * div_term)
#         pe[:, 1::2] = torch.cos(position * div_term)
#         self.register_buffer('pe', pe.unsqueeze(0))

#     def forward(self, x):
#         return x + self.pe[:, :x.size(1)].clone().detach()