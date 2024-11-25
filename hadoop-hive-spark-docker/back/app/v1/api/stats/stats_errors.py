class DatabaseConnectionError(RuntimeError):
    message = 'ERROR_DATABASE_CONNECTION'

class DataFrameProcessingError(RuntimeError):
    message = 'ERROR_DATAFRAME_PROCESSING'

class FilterApplicationError(RuntimeError):
    message = 'ERROR_FILTER_APPLICATION'
