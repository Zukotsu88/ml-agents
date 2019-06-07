import logging

from mlagents.trainers.trainer import UnityTrainerException
from mlagents.trainers.components.reward_signals.gail.signal import GAILSignal
from mlagents.trainers.components.reward_signals.extrinsic.signal import ExtrinsicSignal
from mlagents.trainers.components.reward_signals.curiosity.signal import CuriositySignal
from mlagents.trainers.policy import Policy

logger = logging.getLogger("mlagents.trainers")


NAME_TO_CLASS = {
    "extrinsic": ExtrinsicSignal,
    "gail": GAILSignal,
    "curiosity": CuriositySignal,
}


def create_reward_signal(policy: Policy, name, config_entry):
    """
    Creates a reward signal class based on the name and config entry provided as a dict. 
    :param policy: The policy class which the 
    :param name: The name of the reward signal
    :param config_entry: The config entries for that reward signal
    :return: The reward signal class instantiated 
    """
    rcls = NAME_TO_CLASS.get(name)
    if not rcls:
        raise UnityTrainerException("Unknown reward signal type {0}".format(name))
    rcls.check_config(config_entry)
    try:
        class_inst = rcls(policy, **config_entry)
    except TypeError:
        raise UnityTrainerException(
            "Unknown parameters given for reward signal {0}".format(name)
        )
    return class_inst
