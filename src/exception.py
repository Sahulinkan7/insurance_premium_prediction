
import os,sys

class CustomException(Exception):
    def __init__(self,error_message : str ,error_details : sys):
        self.error_message = self.get_error_message(error_message=error_message,error_details=error_details)
        self.error_details = error_details
        
    def get_error_message(self,error_message:str,error_details:sys):
        _,__,exc_tb = error_details.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        
        error_message = f"""
        Error occurred in file {file_name},
        line number {exc_tb.tb_lineno},
        error message is '{str(error_message)}'
        """
        
        return error_message
        
    def __str__(self):
        return self.error_message