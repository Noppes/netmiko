from netmiko.cisco_base_connection import CiscoBaseConnection


class CiscoIseBase(CiscoBaseConnection):

    def session_preparation(self) -> None:
        """Prepare the session after the connection has been established."""

        data = self.read_until_pattern(
            pattern=r"Enter session number to resume or press <Enter> to start a new one:|>|#"
        )

        if "resume" in data:
            self.write_channel(f"{self.RETURN}")
            data = self.read_until_pattern(pattern=r">|#")

        self.disable_paging()
        self.set_base_prompt()

    def save_config(
        self,
        cmd: str = "write memory",
        confirm: bool = False,
        confirm_response: str = "",
    ) -> str:
        """Copies the running configuration to the startup configuration."""
        return super().save_config(
            cmd=cmd, confirm=confirm, confirm_response=confirm_response
        )


class CiscoIseSSH(CiscoIseBase):
    """Cisco ISE SSH driver."""

    pass


class CiscoIseTelnet(CiscoIseBase):
    """Cisco ISE Telnet driver."""

    pass
