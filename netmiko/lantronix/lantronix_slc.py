from netmiko.base_connection import BaseConnection
from typing import Optional
from netmiko.no_enable import NoEnable
from netmiko.no_config import NoConfig


class LantronixSlcSSH(NoEnable, NoConfig, BaseConnection):
    def session_preparation(self) -> None:
        """Prepare the session after the connection has been established."""
        self._test_channel_read(pattern=r">")
        self.set_base_prompt()
        # Clear the read buffer
        self.clear_buffer()

    def set_base_prompt(
        self,
        pri_prompt_terminator: str = ">",
        alt_prompt_terminator: str = ">",
        delay_factor: float = 1.0,
        pattern: Optional[str] = None,
    ) -> str:
        return super().set_base_prompt(
            pri_prompt_terminator=pri_prompt_terminator,
            alt_prompt_terminator=alt_prompt_terminator,
            delay_factor=delay_factor,
            pattern=pattern,
        )

    def save_config(
        self,
        cmd: str = "admin config save current location local",
        confirm: bool = False,
        confirm_response: str = "",
    ) -> str:
        """Saves Config."""
        return super().save_config(cmd=cmd, confirm=confirm, confirm_response=confirm_response)

    def cleanup(self, command: str = "logout") -> None:
        """Gracefully exit the SSH session."""
        # Always try to send final 'exit' (command)
        if self.session_log:
            self.session_log.fin = True
        self.write_channel(command + self.RETURN)
