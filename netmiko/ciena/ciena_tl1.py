"""Ciena TL1 support."""

from typing import Optional, Any
import time
from netmiko.no_enable import NoEnable
from netmiko.no_config import NoConfig
from netmiko.base_connection import BaseConnection
from netmiko.ssh_auth import SSHClient_noauth
from netmiko.exceptions import NetmikoAuthenticationException

from paramiko import SSHClient


class CienaTl1Base(NoEnable, NoConfig, BaseConnection):
    """
    Ciena TL1 support.

    Implements methods for interacting Ciena devices.

    """

    def __init__(self, *args: Any, **kwargs: Any):
        kwargs["default_enter"] = ";"
        super().__init__(*args, **kwargs)

    def set_base_prompt(
        self,
        pri_prompt_terminator: str = "<",
        alt_prompt_terminator: str = "",
        delay_factor: float = 1.0,
        pattern: Optional[str] = None,
    ) -> str:
        return super().set_base_prompt(
            pri_prompt_terminator=pri_prompt_terminator,
            alt_prompt_terminator=alt_prompt_terminator,
            delay_factor=delay_factor,
            pattern=pattern,
        )

    def session_preparation(self) -> None:
        self._test_channel_read()
        self.set_base_prompt()

    def _login_handler(self, delay_factor: float = 1.0) -> str:
        delay_factor = self.select_delay_factor(delay_factor)
        i = 0
        time.sleep(delay_factor * 1.5)
        output = ""
        while i <= 12:
            output = self.read_channel()
            if output:
                self.write_channel(f'ACT-USER::"{self.username}":1::"{self.password}":')
                break
            else:
                time.sleep(delay_factor * 1.5)
            i += 1
        time.sleep(delay_factor * 1.0)
        output = self.read_channel()
        if "DENY" in output:
            self.disconnect()
            raise NetmikoAuthenticationException(f"Login failed: {self.host}")
        return output


class CienaTl1SSH(CienaTl1Base):
    def _get_ssh_client_instance(self) -> SSHClient:
        return SSHClient_noauth()

    def special_login_handler(self, delay_factor: float = 1.0) -> None:
        self._login_handler(delay_factor=delay_factor)


class CienaTl1Telnet(CienaTl1Base):
    def telnet_login(
        self,
        pri_prompt_terminator: str = r"#\s*$",
        alt_prompt_terminator: str = r">\s*$",
        username_pattern: str = r"(?:user:|username|login|user name)",
        pwd_pattern: str = r"assword",
        delay_factor: float = 1.0,
        max_loops: int = 20,
    ) -> str:
        return self._login_handler(delay_factor=delay_factor)
