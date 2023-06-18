import hydra
from annotator.constants import ANNOTATOR_CONFIG_NAME, CONFIG_DIR
from annotator.density_annotator import DensityAnnotator
from annotator.logger import logger
from omegaconf import DictConfig


@hydra.main(
    version_base="1.1", config_path=str(CONFIG_DIR), config_name=ANNOTATOR_CONFIG_NAME
)
def main(cfg: DictConfig) -> None:
    """
    Run DensityAnnotator according to the settings defined in the config file.

    :param cfg: config that loaded by @hydra.main()
    :return: None
    """
    annotator = DensityAnnotator(cfg)
    annotator.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception(e)
