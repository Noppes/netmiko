import time
from typing import Optional
from netmiko.no_enable import NoEnable
from netmiko.no_config import NoConfig
from netmiko.cisco_base_connection import CiscoSSHConnection


class AccedianSSH(NoEnable, NoConfig, CiscoSSHConnection):
    
    def session_preparation(self) -> None:
        self.ansi_escape_codes = True
        self._test_channel_read(pattern=r"[:#]")
        self.set_base_prompt()
        
    def establish_connection(self, width: int = 511, height: int = 800) -> None:
        """Establish SSH connection to the network device"""
        super().establish_connection(width=width, height=height)

    def set_base_prompt(
        self,
        pri_prompt_terminator: str = ":",
        alt_prompt_terminator: str = "#",
        delay_factor: float = 2.0,
        pattern: Optional[str] = None,
    ) -> str:
        """Sets self.base_prompt: used as delimiter for stripping of trailing prompt in output."""
        super().set_base_prompt(
            pri_prompt_terminator=pri_prompt_terminator,
            alt_prompt_terminator=alt_prompt_terminator,
            delay_factor=delay_factor,
            pattern=pattern,
        )
        return self.base_prompt

    def save_config(self, cmd: str = "", confirm: bool = False, confirm_response: str = "") -> str:
        """Not Implemented"""
        raise NotImplementedError
