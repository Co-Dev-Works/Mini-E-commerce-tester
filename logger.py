import logging
import os
from datetime import datetime

class Logger:
    """Custom logger for test execution"""
    
    @staticmethod
    def get_logger(name=__name__):
        """
        Create and configure logger
        Args:
            name (str): Logger name
        Returns:
            Logger: Configured logger instance
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # File handler
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        fh = logging.FileHandler(f'logs/test_execution_{timestamp}.log')
        fh.setLevel(logging.INFO)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        # Add handlers if not already added
        if not logger.handlers:
            logger.addHandler(fh)
            logger.addHandler(ch)
        
        return logger