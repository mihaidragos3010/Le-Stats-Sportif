import os
import time
import logging
from logging.handlers import RotatingFileHandler


# The class that builds a logger set on global time with a specific format.
class Loggin:
    def __init__(self, dir_path: str):

        self.removeBeforeLoggerDirectoryAndMakeNewOne(dir_path)
                                                 
        self.logger = logging.getLogger("website logger")
        self.logger.setLevel(logging.INFO)
        
        handler = RotatingFileHandler(f'{dir_path}/webserver.log', maxBytes=10000, backupCount=10)
        formatter = self.UTCFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        self.logger.addHandler(handler)

    # The logger is sent through this function.
    def get(self):
        return self.logger
    
    # Create a logger directory and delete everything that was previously in it.
    def removeBeforeLoggerDirectoryAndMakeNewOne(self, dir_path: str):
        try:
            if os.path.exists(dir_path):
                files = os.listdir(dir_path)
                for file_name in files:
                    file_path = os.path.join(dir_path, file_name)
                    os.remove(file_path)   

        except OSError as e:
            print(f"Error: {e}")

        finally:
            os.makedirs(dir_path, exist_ok=True)

    # A specific format for the date is constructed and set based on the global date.
    class UTCFormatter(logging.Formatter):
        converter = time.gmtime
        def formatTime(self, record, datefmt=None):
            return time.strftime('%Y-%m-%d %H:%M:%S', self.converter(record.created))
        

