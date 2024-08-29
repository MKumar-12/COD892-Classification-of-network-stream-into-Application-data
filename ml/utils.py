from pathlib import Path

import numpy as np
import torch
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import EarlyStopping
from pytorch_lightning.loggers import TensorBoardLogger
from pytorch_lightning import seed_everything

from ml.model import Transformer  

def train_transformer(
    output_dim, data_path, epoch, model_path, signal_length, logger
):
    if model_path:
        model_path = Path(model_path)
        model_path.parent.mkdir(parents=True, exist_ok=True)

    seed_everything(seed=9876, workers=True)

    model = Transformer(
        output_dim=output_dim,
        data_path=data_path,
        signal_length=signal_length,
    ).float()
    trainer = Trainer(
        max_epochs=epoch,
        devices="auto",
        accelerator="auto",
        logger=logger,
        callbacks=[
            EarlyStopping(
                monitor="train_loss", mode="min", check_on_train_epoch_end=True,patience=5, verbose=True
            )
        ],
    )
    trainer.fit(model)

    # save model
    trainer.save_checkpoint(str(model_path.absolute()))

def train_application_classification_transformer_model(data_path, model_path):
    logger = TensorBoardLogger(
        "application_classification_transformer_logs",
        "application_classification_transformer"
    )
    train_transformer(
        output_dim=17, 
        data_path=data_path,
        epoch=20,
        model_path=model_path,
        signal_length=1500, 
        logger=logger,
    )

def train_traffic_classification_transformer_model(data_path, model_path):
    logger = TensorBoardLogger(
        "traffic_classification_transformer_logs",
        "traffic_classification_transformer"
    )
    train_transformer(
        output_dim=12,  
        data_path=data_path,
        epoch=20,
        model_path=model_path,
        signal_length=1500, 
        logger=logger,
    )

def load_transformer_model(model_path, gpu):
    if gpu:
        device = "cuda"
    else:
        device = "cpu"
    model = (
        Transformer.load_from_checkpoint(
            str(Path(model_path).absolute()), map_location=torch.device(device)
        )
        .float()
        .to(device)
    )

    model.eval()

    return model

def load_application_classification_transformer_model(model_path, gpu=True):
    return load_transformer_model(model_path=model_path, gpu=gpu)

def load_traffic_classification_transformer_model(model_path, gpu=True):
    return load_transformer_model(model_path=model_path, gpu=gpu)

def normalise_cm(cm):
    with np.errstate(all="ignore"):
        normalised_cm = cm / cm.sum(axis=1, keepdims=True)
        normalised_cm = np.nan_to_num(normalised_cm)
        return normalised_cm