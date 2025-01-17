import os
import random
from pathlib import Path
from typing import List

import cv2
from tqdm import tqdm

from annotator.config import SamplerConfig, load_config
from annotator.constants import (
    CONFIG_DIR,
    DATA_DIR,
    IMAGE_EXTENTION,
    SAMPLER_CONFIG_NAME,
)
from annotator.exceptions import LoadVideoFrameError, SamplingTypeError
from annotator.logger import logger
from annotator.utils import get_full_path_list, load_video, save_image


def get_sampled_frame_number(total_frame_number: int, sample_rate: int) -> List:
    """Sample frame numbers randomly according to the sample rate.

    Args:
        total_frame_number (int): total frame number of target video
        sample_rate (int): sampling rate for frame

    Returns:
        List: list of random sampled frame number
    """
    frame_number_list = []

    # sample target frame number
    for start_idx in range(1, total_frame_number, sample_rate):
        end_idx = start_idx + sample_rate - 1
        if end_idx > total_frame_number:
            end_idx = total_frame_number - 1

        sampled_frame_number = random.randint(start_idx, end_idx)
        frame_number_list.append(sampled_frame_number)

    return frame_number_list


def get_frame_number_list(
    total_frame_number: int, sampling_type: str, sample_rate: int
) -> List[int]:
    """Get a list of frames with two sampling methods: "random" or "fixed".

    Args:
        total_frame_number (int): total frame number of target video
        sampling_type (str): sampling type "random" or "fixed"
        sample_rate (int): sampling rate for frame

    Returns:
        List: list of sampled frame number
    """
    if sampling_type == "random":
        frame_number_list = get_sampled_frame_number(total_frame_number, sample_rate)
    elif sampling_type == "fixed":
        frame_number_list = [
            i for i in range(total_frame_number) if i % sample_rate == 0
        ]
    else:
        message = f'sampling_type="{sampling_type}" is not defined.'
        logger.error(message)
        raise SamplingTypeError(message)

    return frame_number_list


def frame_sampler(
    input_video_list: List[Path],
    save_frame_dirc: Path,
    sampling_type: str,
    sample_rate: int,
) -> None:
    """Load the video and save the sampled frames as image data.

    Args:
        input_video_list (List[Path]): list of input video path
        save_frame_dirc (str): save sampled frame path
        sampling_type (str): sampling type "random" or "fixed"
        sample_rate (int): sampling rate for frame
    """
    for video_path in input_video_list:
        file_name = os.path.splitext(os.path.basename(video_path))[0]
        video = load_video(video_path)
        total_frame_number = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        # create save frame directory
        current_save_dirc = f"{save_frame_dirc}/{file_name}"
        os.makedirs(current_save_dirc, exist_ok=True)

        # get sample target frame number list
        frame_number_list = get_frame_number_list(
            total_frame_number, sampling_type, sample_rate
        )

        for frame_number in tqdm(frame_number_list):
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            # load current frame
            ret, frame = video.read()
            if ret:
                save_file_name = Path(
                    f"{current_save_dirc}/{frame_number}{IMAGE_EXTENTION}"
                )
                save_image(save_file_name, frame)
            else:
                message = f"Frame number={frame_number} cannot load."
                logger.error(message)
                raise LoadVideoFrameError(message)


def main() -> None:
    """Run frame sampler according to the settings defined in the config file.

    Args:
        cfg (DictConfig): config that loaded by @hydra.main()
    """
    cfg = load_config(CONFIG_DIR / SAMPLER_CONFIG_NAME, SamplerConfig)
    logger.info(f"Loaded config: {cfg}")
    input_video_list = get_full_path_list(DATA_DIR, cfg.path.input_video_list)
    save_frame_dirc = DATA_DIR / cfg.path.save_frame_dirc

    # execute frame sampler
    frame_sampler(input_video_list, save_frame_dirc, cfg.sampling_type, cfg.sample_rate)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception(e)
