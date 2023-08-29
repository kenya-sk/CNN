import hydra

from annotator.config import load_annotator_config
from annotator.constants import ANNOTATOR_CONFIG_NAME, CONFIG_DIR
from annotator.density_annotator import DensityAnnotator
from annotator.logger import logger


def main() -> None:
    """Run DensityAnnotator according to the settings defined in the config file."""
    cfg = load_annotator_config(CONFIG_DIR / ANNOTATOR_CONFIG_NAME)
    logger.info(f"Loaded config: {cfg}")
    annotator = DensityAnnotator(cfg)
    annotator.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception(e)
