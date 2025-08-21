"""Dinstar MTC Routers"""
import time
import re
from typing import Any, Optional
from netmiko.base_connection import BaseConnection, lock_channel
from netmiko.cisco_base_connection import CiscoBaseConnection
from netmiko.exceptions import ReadException, WriteException
from netmiko.netmiko_globals import MAX_BUFFER

class DinstarMtcBase(BaseConnection):

    logged_in = False

    def session_preparation(self) -> None:
        self._test_channel_read(pattern=r"[>\#]")
        self.set_base_prompt()
        self.enable()
        self.clear_buffer()
        self.logged_in = True

        
    def enable(
        self,
        cmd: str = "enable",
        pattern: str = "ssword",
        enable_pattern: Optional[str] = None,
        check_state: bool = True,
        re_flags: int = re.IGNORECASE,
    ) -> str:
        """Enter enable mode."""
        return super().enable(
            cmd=cmd,
            pattern=pattern,
            enable_pattern=enable_pattern,
            check_state=check_state,
            re_flags=re_flags,
        )

    def exit_enable_mode(self, exit_command: str = "exit") -> str:
        return super().exit_enable_mode(exit_command=exit_command)
    
    def check_enable_mode(self, check_string: str = "#") -> bool:
        return super().check_enable_mode(check_string=check_string)
    
    def config_mode(
        self,
        config_command: str = "^config",
        pattern: str = "",
        re_flags: int = 0,
    ) -> str:
        return super().config_mode(
            config_command=config_command, pattern=pattern, re_flags=re_flags
        )
    
    def exit_config_mode(self, exit_config: str = "exit", pattern: str = r"#.*") -> str:
        return super().exit_config_mode(exit_config=exit_config, pattern=pattern)
        
    def check_config_mode(
        self, check_string: str = ")#", pattern: str = "", force_regex: bool = False
    ) -> bool:
        return super().check_config_mode(
            check_string=check_string, pattern=pattern, force_regex=force_regex
        )
    
    def set_base_prompt(
        self,
        pri_prompt_terminator: str = ">",
        alt_prompt_terminator: str = "#",
        delay_factor: float = 1.0,
        pattern: Optional[str] = None,
    ) -> str:
        prompt = super().set_base_prompt(
            pri_prompt_terminator=pri_prompt_terminator,
            alt_prompt_terminator=alt_prompt_terminator,
            delay_factor=delay_factor,
            pattern=pattern,
        )
        prompt = prompt.strip()
        self.base_prompt = prompt
        return self.base_prompt
    
    @lock_channel
    def read_channel(self) -> str:
        """Generic handler that will read all the data from given channel."""
        new_data = self.channel.read_channel()
        if self.ansi_escape_codes:
            new_data = self.strip_ansi_escape_codes(new_data)
        if self.session_log:
            self.session_log.write(new_data)
        return str(new_data)

        if self.disable_lf_normalization is False:
            start = time.time()
            # Data blocks shouldn't end in '\r' (can cause problems with normalize_linefeeds)
            # Only do the extra read if '\n' exists in the output
            # this avoids devices that only use \r.
            while ("\n" in new_data) and (time.time() - start < 4.0):
                time.sleep(0.01)
                new_data += self.channel.read_channel()

        if self.logged_in and new_data:
            print(str(new_data))

        if self.ansi_escape_codes:
            new_data = self.strip_ansi_escape_codes(new_data)
        if self.session_log:
            self.session_log.write(new_data)

        # If data had been previously saved to the buffer, the prepend it to output
        # do post read_channel so session_log/log doesn't record buffered data twice
        if self._read_buffer:
            output = self._read_buffer + new_data
            self._read_buffer = ""
        else:
            output = new_data
        return output
    

class DinstarMtcSSH(DinstarMtcBase):
    pass

class DinstarMtcTelnet(DinstarMtcBase):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.disable_lf_normalization = True
        super().__init__(*args, **kwargs)
        self.ansi_escape_codes = True
        self.disable_lf_normalization = False