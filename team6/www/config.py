import os
import datetime
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
	SECRET_KEY = 'TrustyPathces'
	permanent_session_lifetime = datetime.timedelta(seconds=10)
	
class DevelopmentConfig(BaseConfig):
	DEBUG = True
	
config = {
	'development': DevelopmentConfig,
	'default': DevelopmentConfig
}
