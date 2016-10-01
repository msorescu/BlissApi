import boto
from boto.dynamodb2.table import Table
from dynamodb_config_store import DynamoDBConfigStore
import boto.swf
import boto.ec2


DEFAULT_REGION_NAME = 'us-west-2'


def get_region(region_name=DEFAULT_REGION_NAME, resource_name='swf'):
    aws_region = None

    if resource_name == 'swf':
        regions = boto.swf.regions()
    elif resource_name == 'ec2':
        regions = boto.ec2.regions()

    for reg in regions:
        if reg.name == region_name:
            aws_region = reg
            break

    return aws_region


class ConfigBase(object):
    TABLE_NAME = 'config'

    def __init__(self, store):
        self.store_name = store

        try:
            connection = boto.dynamodb2.connect_to_region(DEFAULT_REGION_NAME)
            # Instantiate the store
            self.store = DynamoDBConfigStore(
                connection,
                ConfigBase.TABLE_NAME,
                self.store_name,
                config_store='TimeBasedConfigStore',
                config_store_kwargs={'update_interval': 60})
        except Exception as ex:
            msg1 = ex.message + 'Failed to instantiate config store'
            raise Exception(msg1)


class Config(ConfigBase):
    STORE_NAME = 'media_bliss'
    region=None

    def __init__(self):
        ConfigBase.__init__(self, store=self.STORE_NAME)
        self.region = get_region()

    @property
    def log_level(self):
        return self.store.config.common['log_level']

    @property
    def default_region_name(self):
        return DEFAULT_REGION_NAME
