import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

from ml.utils import load_application_classification_transformer_model, normalise_cm
from ml.metrics import confusion_matrix, get_classification_report
from utils import  ID_TO_APP

def main():
    mpl.rcParams['figure.dpi'] = 100
    traffic_classification_transformer_model_path = r'D:\minorProject\2git\Deep-Packet\model\oversamp_application_classification.cnn.model'

    traffic_classification_transformer = load_application_classification_transformer_model(traffic_classification_transformer_model_path, gpu=True)

    traffic_classification_test_data_path = r'D:\minorProject\1git\Deep-Packet\train_test_data\application_classification\test'
    traffic_transformer_cm = confusion_matrix(
        data_path=traffic_classification_test_data_path,
        model=traffic_classification_transformer,
        num_class=len(ID_TO_APP)

    )

    print(traffic_transformer_cm)
    traffic_labels = [ID_TO_APP[i] for i in sorted(ID_TO_APP.keys())]

    plot_confusion_matrix(traffic_transformer_cm, traffic_labels)
    classification_report = get_classification_report(traffic_transformer_cm, traffic_labels)
    print(classification_report)

def plot_confusion_matrix(cm, labels):
    normalised_cm = normalise_cm(cm)
    fig, ax = plt.subplots(figsize=(8, 8))
    sns.heatmap(
        data=normalised_cm, cmap='YlGnBu',
        xticklabels=labels, yticklabels=labels,
        annot=True, ax=ax, fmt='.2f'
    )
    ax.set_xlabel('Predict labels')
    ax.set_ylabel('True labels')
    plt.show()

if __name__ == '__main__':
    main()