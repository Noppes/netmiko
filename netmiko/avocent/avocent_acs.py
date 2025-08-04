import time
from netmiko.base_connection import BaseConnection
from netmiko.no_enable import NoEnable


class AvocentACSSSH(NoEnable, BaseConnection):

    def session_preparation(self) -> None:
        """Prepare the session after the connection has been established."""
        self._test_channel_read()
        self.enter_cli_mode()
        self.set_base_prompt()
        self.disable_paging()

    def enter_cli_mode(self) -> None:
        self.write_channel(self.RETURN)
        delay_factor = self.select_delay_factor(delay_factor=0)
        time.sleep(0.1 * delay_factor)
        self.write_channel("cli" + self.RETURN)
        self.read_until_pattern(pattern=r"[>#]", read_timeout=10)
