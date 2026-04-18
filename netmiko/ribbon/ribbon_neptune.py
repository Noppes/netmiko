import time

from netmiko.no_enable import NoEnable
from netmiko.base_connection import BaseConnection


class RibbonNeptuneBase(NoEnable, BaseConnection):
    def session_preparation(self) -> None:
        self._test_channel_read()
        self.set_base_prompt()
        self.set_terminal_width(command="set cli screen-width 511")
        self.disable_paging(command="set cli screen-length 0")
        # Clear the read buffer
        time.sleep(0.3 * self.global_delay_factor)
        self.clear_buffer()

    def commit(self) -> str:
        return self._send_command_str(command_string="commit")

    def config_mode(
        self,
        config_command: str = "configure",
        pattern: str = "#",
        re_flags: int = 0,
    ) -> str:
        return super().config_mode(
            config_command=config_command, pattern=pattern, re_flags=re_flags
        )

    def check_config_mode(
        self,
        check_string: str = "#",
        pattern: str = "",
        force_regex: bool = False,
    ) -> bool:
        return super().check_config_mode(
            check_string=check_string, pattern=pattern, force_regex=force_regex
        )

    def exit_config_mode(self, exit_config: str = "exit", pattern: str = "#") -> str:
        return super().exit_config_mode(exit_config=exit_config, pattern=pattern)


class RibbonNeptuneSSH(RibbonNeptuneBase):
    pass
