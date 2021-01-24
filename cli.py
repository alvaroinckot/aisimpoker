import click
from scripts.main_multithread import process_poker_logs
from scripts.xgboost_classifier import fit


@click.group()
def ml():
    pass


@ml.command()
def process():
    """Command on ML"""
    process_poker_logs()


@ml.command()
def xgboost():
    """Command on ML"""
    fit()


cli = click.CommandCollection(sources=[ml])

if __name__ == '__main__':
    cli()
