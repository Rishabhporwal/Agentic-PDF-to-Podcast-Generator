"""
Logging Configuration

Provides centralized logging for the entire application with:
- Console output (INFO level)
- File output (DEBUG level)
- Structured formatting with timestamps
"""

import logging
import os
from pathlib import Path
from datetime import datetime


def setup_logger(name: str, log_dir: str = "logs") -> logging.Logger:
    """
    Set up a logger with both console and file handlers.

    Args:
        name: Logger name (usually __name__ of the module)
        log_dir: Directory to store log files

    Returns:
        Configured logger instance
    """
    # Create logs directory
    Path(log_dir).mkdir(exist_ok=True)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Avoid duplicate handlers if logger already configured
    if logger.handlers:
        return logger

    # Console handler (INFO and above)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)

    # File handler (DEBUG and above)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"podcast_generation_{timestamp}.log")
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.info(f"Logger initialized. Logs saved to: {log_file}")

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get or create a logger for the given module.

    Args:
        name: Logger name (usually __name__ of the module)

    Returns:
        Logger instance
    """
    return setup_logger(name)
