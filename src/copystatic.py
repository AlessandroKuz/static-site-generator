import logging
import pathlib
import shutil


def copy_files_recursively(src: pathlib.Path | str, dst: pathlib.Path | str, verbose: bool = False) -> None:
    """
    Recursively copy a file or folder, from src to dst.
    :param src: the path of the folder which contents are to be copied from.
    :param dst: the path to the folder which contents are to be copied in.
    :param verbose: whether the operations performed should be logged or not.

    :return: None
    """
    if verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger(__name__)

    logger.info('='*80)
    logger.info(f"Started function; src={src}, dst={dst}")

    if not (isinstance(src, pathlib.Path) or isinstance(src, str)):
        raise TypeError(f"src must be a pathlib.Path or str; instead got: {type(src)}")
    if not (isinstance(dst, pathlib.Path) or isinstance(dst, str)):
        raise TypeError(f"dst must be a pathlib.Path or str; instead got: {type(dst)}")

    if isinstance(src, str):
        src = pathlib.Path(src)
    if isinstance(dst, str):
        dst = pathlib.Path(dst)

    # Check is provided paths exist and are valid
    if not src.exists():
        logger.error(f"src={src} does not exist")
        raise FileNotFoundError(f"{src.resolve()} does not exist")
    if src.is_file():
        logger.error(f"src={src} is not a directory")
        raise NotADirectoryError(f"{src.resolve()} is not a directory")

    # create dst folder if it does not yet exist
    if dst.exists():
        logger.info(f"dst={dst} already exists")
        # wipe the contents of dst to ensure no unexpected behaviour
        logger.info(f"removing files from: {src}")
        shutil.rmtree(dst)
        logger.info(f"dst={dst} contents removed")

    # copy recursively function
    logger.info(f"recreating the destination folder: {dst}")
    dst.mkdir(parents=True, exist_ok=True)
    logger.info(f"copying src={src} to dst={dst}")
    for item in src.iterdir():
        logger.info(f"copying {item} to {dst}")
        if item.is_file():
            logger.info(f"{item} is a file, so just copying it")
            shutil.copy(item, dst)
        else:
            logger.info(f"{item} is a directory, so copying it recursively")
            new_dst = dst / item.name
            copy_files_recursively(item, new_dst)
    logger.info(f"src={src} copied to dst={dst}")
    logger.info("successfully copied all files!")
    logger.info('='*80)
