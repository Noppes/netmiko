"""Calix Axos SSH Driver for Netmiko"""

from typing import Any, Optional
import time

from netmiko.cisco_base_connection import CiscoSSHConnection
from netmiko.exceptions import NetmikoTimeoutException


class CalixAxosBase(CiscoSSHConnection):

    def session_preparation(self) -> Any:
        """Prepare the session after the connection has been established."""
        self.ansi_escape_codes = True
        self._test_channel_read(pattern=r"#")
        self.set_base_prompt()
        self.enable()
        self.set_terminal_width(command="terminal width 511", pattern="terminal")
        self.disable_paging()

    def special_login_handler(self, delay_factor: float = 1.0) -> None:
        """
        Calix presents with the following on login:

        login as:
        Password: ****
        """
        new_data = ""
        time.sleep(0.1)
        start = time.time()
        login_timeout = 20
        while time.time() - start < login_timeout:
            output = self.read_channel() if not new_data else new_data
            new_data = ""
            if output:
                if "login as:" in output:
                    assert isinstance(self.username, str)
                    self.write_channel(self.username + self.RETURN)
                elif "Password:" in output:
                    assert isinstance(self.password, str)
                    self.write_channel(self.password + self.RETURN)
                    break
                time.sleep(0.1)
            else:
                # No new data...sleep longer
                time.sleep(0.5)
                new_data = self.read_channel()
                # If still no data, send an <enter>
                if not new_data:
                    self.write_channel(self.RETURN)
        else:  # no-break
            msg = """
Login process failed to Calix B6 device. Unable to login in {login_timeout} seconds.
"""
            raise NetmikoTimeoutException(msg)

    def check_enable_mode(self, check_string: str = "#") -> bool:
        """Check if in enable mode. Return boolean."""
        return True

    def set_base_prompt(
        self,
        pri_prompt_terminator: str = "#",
        alt_prompt_terminator: str = None,
        delay_factor: float = 1.0,
        pattern: Optional[str] = None,
    ) -> str:
        return super().set_base_prompt(
            pri_prompt_terminator=pri_prompt_terminator,
            alt_prompt_terminator=alt_prompt_terminator,
            delay_factor=delay_factor,
            pattern=pattern,
        )

    def config_mode(
        self,
        config_command: str = "configure",
        pattern: str = "",
        re_flags: int = 0,
    ) -> str:
        return super().config_mode(
            config_command=config_command, pattern=pattern, re_flags=re_flags
        )

    def save_config(
        self,
        cmd: str = "copy running-config startup-config",
        confirm: bool = False,
        confirm_response: str = "",
    ) -> str:
        return super().save_config(
            cmd=cmd, confirm=confirm, confirm_response=confirm_response
        )


class CalixAxosSSH(CalixAxosBase):
    pass


class CalixAxosTelnet(CalixAxosBase):
    pass
