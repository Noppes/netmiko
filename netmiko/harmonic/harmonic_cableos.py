from netmiko.base_connection import BaseConnection
from netmiko.no_enable import NoEnable


class HarmonicCableOsBase(BaseConnection, NoEnable):
    """
    Implements methods for communicating with Westermo devices.
    """

    def session_preparation(self) -> None:
        """
        Prepare the session after the connection has been established.

        Set the base prompt for interaction ('#').
        """
        self._test_channel_read()
        self.set_base_prompt()
        self.disable_paging(command="paginate false")

    def check_config_mode(
        self, check_string: str = ")#", pattern: str = r"[>#]", force_regex: bool = False
    ) -> bool:
        """
        Checks if the device is in configuration mode or not.
        """
        return super().check_config_mode(check_string=check_string, pattern=pattern)

    def config_mode(
        self, config_command: str = "config", pattern: str = r"#", re_flags: int = 0
    ) -> str:
        return super().config_mode(
            config_command=config_command, pattern=pattern, re_flags=re_flags
        )

    def exit_config_mode(
        self, exit_config: str = "exit configuration-mode", pattern: str = "#"
    ) -> str:
        return super().exit_config_mode(exit_config=exit_config, pattern=pattern)

    def commit(self, cmd: str = "commit", read_timeout: float = 120.0) -> str:
        if not self.check_config_mode():
            raise ValueError("Must be in configuration mode to commit.")
        self.write_channel(self.normalize_cmd(cmd))
        output = self.read_until_pattern(pattern=r"\)#", read_timeout=read_timeout)
        return output

    def save_config(
        self,
        cmd: str = "write",
        confirm: bool = False,
        confirm_response: str = "",
    ) -> str:
        return super().save_config(cmd=cmd, confirm=confirm, confirm_response=confirm_response)


class HarmonicCableOsSSH(HarmonicCableOsBase):
    pass
