import click
from ml.utils import (
    train_application_classification_transformer_model,
    train_traffic_classification_transformer_model,
)

@click.command()
@click.option(
    "-d",
    "--data_path",
    help="Training data directory path containing parquet files",
    required=True,
)
@click.option("-m", "--model_path", help="Output model path", required=True)
@click.option(
    "-t",
    "--task",
    help='Classification task. Options: "app" or "traffic"',
    required=True,
)
def main(data_path, model_path, task):
    if task == "app":
        train_application_classification_transformer_model(data_path, model_path)
    elif task == "traffic":
        train_traffic_classification_transformer_model(data_path, model_path)
    else:
        click.echo("Unsupported task specified. Use 'app' or 'traffic'.", err=True)
        exit(1)

if __name__ == "__main__":
    main()