import multiprocessing
from pathlib import Path

import datasets
import numpy as np
import torch
import pandas as pd
from torch.nn import functional as F
from torch.utils.data import DataLoader
from sklearn.metrics import precision_recall_curve, roc_curve, auc, classification_report


from ml.dataset import dataset_collate_function

import matplotlib.pyplot as plt

from ml.dataset import dataset_collate_function

# def confusion_matrix(data_path, model, num_class):
#     data_path = Path(data_path)
#     model.eval()

#     cm = np.zeros((num_class, num_class), dtype=np.float64)

#     dataset_dict = datasets.load_dataset(str(data_path.absolute()))
#     dataset = dataset_dict[list(dataset_dict.keys())[0]]
#     dataloader = DataLoader(
#         dataset,
#         batch_size=4096,
#         num_workers=multiprocessing.cpu_count(),
#         collate_fn=dataset_collate_function,
#     )
    
#     y_true, y_pred, y_scores = [], [], []
#     for batch in dataloader:
#         x = batch["feature"].float().to(model.device)
#         y = batch["label"].long()
#         logits = model(x)
#         y_hat = torch.argmax(F.log_softmax(logits, dim=1), dim=1)
        
#         y_true.extend(y.cpu().numpy())
#         y_pred.extend(y_hat.cpu().numpy())
#         y_scores.extend(F.softmax(logits, dim=1).detach().cpu().numpy())  # Detach before converting to NumPy

#         for i in range(len(y)):
#             cm[y[i], y_hat[i]] += 1

#     return cm, y_true, y_pred, y_scores

def confusion_matrix(data_path, model, num_class):
    data_path = Path(data_path)
    model.eval()

    cm = np.zeros((num_class, num_class), dtype=np.float64)

    print(cm)

    dataset_dict = datasets.load_dataset(str(data_path.absolute()))
    dataset = dataset_dict[list(dataset_dict.keys())[0]]
    try:
        num_workers = multiprocessing.cpu_count()
    except:
        num_workers = 1
    dataloader = DataLoader(
        dataset,
        batch_size=4096,
        num_workers=0,
        collate_fn=dataset_collate_function,
    )
    for batch in dataloader:
        x = batch["feature"].float().to(model.device)
        y = batch["label"].long()
        y_hat = torch.argmax(F.log_softmax(model(x), dim=1), dim=1)

        for i in range(len(y)):
            cm[y[i], y_hat[i]] += 1

    return cm


def get_precision(cm, i):
    tp = cm[i, i]
    tp_fp = cm[:, i].sum()
    return tp / tp_fp if tp_fp != 0 else 0

def get_recall(cm, i):
    tp = cm[i, i]
    p = cm[i, :].sum()
    return tp / p if p != 0 else 0

def get_f1_score(precision, recall):
    return 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0

def get_accuracy(cm):
    total_correct = np.trace(cm)  
    total_samples = cm.sum()      
    return total_correct / total_samples


def get_classification_report(cm, y_true, y_pred, labels):
    rows = []
    total_samples = cm.sum()
    total_precision, total_recall, total_f1, weighted_sum = 0, 0, 0, 0

    accuracy = np.trace(cm) / total_samples
    class_report = classification_report(y_true, y_pred, target_names=labels, output_dict=True)
    
    for i, label in enumerate(labels):
        precision = class_report[label]['precision']
        recall = class_report[label]['recall']
        f1 = class_report[label]['f1-score']
        support = class_report[label]['support']

        row = {
            "label": label,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "support": support
        }
        rows.append(row)

    report_df = pd.DataFrame(rows)
    
    weighted_avg_precision = class_report['weighted avg']['precision']
    weighted_avg_recall = class_report['weighted avg']['recall']
    weighted_avg_f1 = class_report['weighted avg']['f1-score']

    print("Overall Accuracy: {:.2f}%".format(accuracy * 100))
    print(f"Weighted Avg Precision: {weighted_avg_precision:.2f}")
    print(f"Weighted Avg Recall: {weighted_avg_recall:.2f}")
    print(f"Weighted Avg F1 Score: {weighted_avg_f1:.2f}")

    return report_df
# def get_classification_report(cm, labels=None):
#     rows = []
#     total_samples = cm.sum()
#     total_precision, total_recall, total_f1, weighted_sum = 0, 0, 0, 0

#     accuracy = get_accuracy(cm)  
#     for i in range(cm.shape[0]):
#         precision = get_precision(cm, i)
#         recall = get_recall(cm, i)
#         f1 = get_f1_score(precision, recall)
#         support = cm[i, :].sum() 
#         weighted_sum += support

#         if labels:
#             label = labels[i]
#         else:
#             label = str(i)

#         total_precision += precision * support
#         total_recall += recall * support
#         total_f1 += f1 * support

#         row = {
#             "label": label,
#             "precision": precision,
#             "recall": recall,
#             "f1_score": f1,
#             "support": support
#         }
#         rows.append(row)

#     weighted_avg_precision = total_precision / weighted_sum if weighted_sum != 0 else 0
#     weighted_avg_recall = total_recall / weighted_sum if weighted_sum != 0 else 0
#     weighted_avg_f1 = total_f1 / weighted_sum if weighted_sum != 0 else 0

#     print("Overall Accuracy: {:.2f}%".format(accuracy * 100))
#     print(f"Weighted Avg Precision: {weighted_avg_precision:.2f}")
#     print(f"Weighted Avg Recall: {weighted_avg_recall:.2f}")
#     print(f"Weighted Avg F1 Score: {weighted_avg_f1:.2f}")

#     return pd.DataFrame(rows)
    