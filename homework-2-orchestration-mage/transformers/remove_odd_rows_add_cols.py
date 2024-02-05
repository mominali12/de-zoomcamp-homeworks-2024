import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
   # Specify your transformation logic here
    data.columns = (data.columns
                .str.replace('(?<=[a-z])(?=[A-Z])', '_', regex=True)
                .str.lower()
             )
    
    data['lpep_pickup_date'] =  pd.to_datetime(data['lpep_pickup_datetime']).dt.date ### As per the question asked in homework

    #using differnt approach to convert to human readable date format
    # data['lpep_pickup_date'] =  data['lpep_pickup_datetime'].dt.strftime('%Y-%m-%d') ### As per usage here

    
    data = data[(data['passenger_count'] > 0)]
    data = data[(data['trip_distance'] > 0)]

    print(data.shape)
    print(data['vendor_id'].unique())
    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    assert 'vendor_id' in output.columns, 'vendor id column is missing'
    assert len(output[(output['passenger_count'] == 0)]) == 0, 'data contains trips with zero passengers'
    assert len(output[(output['trip_distance'] == 0)]) == 0, 'data contains trips with zero distance'
