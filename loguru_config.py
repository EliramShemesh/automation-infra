from loguru import logger
import sys

# Remove the default Loguru handler (stderr)
logger.remove()

logger.add(sys.stdout, level="DEBUG", colorize=True)
