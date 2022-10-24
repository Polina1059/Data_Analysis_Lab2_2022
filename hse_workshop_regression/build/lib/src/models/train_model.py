# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from sklearn.model_selection import train_test_split
from src.utils import save_as_pickle
import pandas as pd
from models import catboost_regr_model, linear_svr_model



@click.command()
@click.argument('input_data_filepath', type=click.Path(exists=True))
@click.argument('input_target_filepath', type=click.Path(exists=True))

@click.argument('output_catboost_regr_model_filepath', type=click.Path())
@click.argument('output_linear_svr_model_filepath', type=click.Path())

@click.argument('output_val_data_filepath', type=click.Path())
@click.argument('output_val_target_filepath', type=click.Path())

def main(input_data_filepath, input_target_filepath, output_catboost_regr_model_filepath, output_linear_svr_model_filepath, 
output_val_data_filepath, output_val_target_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    train_data = pd.read_pickle(input_data_filepath)
    train_target = pd.read_pickle(input_target_filepath)

    train_data, val_data, train_target, val_target = train_test_split(train_data, train_target, test_size=0.4, random_state=7)

    print('First model')
    catboost_regr_model.fit(train_data, train_target)
    save_as_pickle(catboost_regr_model, output_catboost_regr_model_filepath)

    print('Second model')
    linear_svr_model.fit(train_data, train_target)
    save_as_pickle(linear_svr_model, output_linear_svr_model_filepath)

    save_as_pickle(val_data, output_val_data_filepath)
    save_as_pickle(val_target, output_val_target_filepath)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
