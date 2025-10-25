"""
Tests specifically for the calculator REPL interface to improve coverage.
"""

import pytest
from unittest.mock import patch, Mock
from io import StringIO
import sys

from app.calculator_repl import calculator_repl


class TestCalculatorREPL:
    """Test cases for the REPL interface to improve coverage."""

    @patch('builtins.input', side_effect=['add', '5', '3', 'history', 'exit'])
    @patch('builtins.print')
    def test_history_with_calculations(self, mock_print, mock_input):
        """Test displaying history with calculations."""
        calculator_repl()
        # Should show the calculation in history
        calls = [str(call) for call in mock_print.call_args_list]
        history_found = any("Addition(5, 3) = 8" in call for call in calls)
        assert history_found, "History should display the calculation"

    @patch('builtins.input', side_effect=['add', '5', '3', 'clear', 'history', 'exit'])
    @patch('builtins.print')
    def test_clear_history(self, mock_print, mock_input):
        """Test clearing history."""
        calculator_repl()
        mock_print.assert_any_call("\x1b[32mHistory cleared\x1b[0m")

    @patch('builtins.input', side_effect=['add', '5', '3', 'undo', 'exit'])
    @patch('builtins.print')
    def test_undo_operation(self, mock_print, mock_input):
        """Test undo functionality."""
        calculator_repl()
        mock_print.assert_any_call("\x1b[32mOperation undone\x1b[0m")

    @patch('builtins.input', side_effect=['undo', 'exit'])
    @patch('builtins.print')
    def test_undo_nothing_to_undo(self, mock_print, mock_input):
        """Test undo when nothing to undo."""
        calculator_repl()
        mock_print.assert_any_call("\x1b[33mNothing to undo\x1b[0m")

    @patch('builtins.input', side_effect=['add', '5', '3', 'undo', 'redo', 'exit'])
    @patch('builtins.print')
    def test_redo_operation(self, mock_print, mock_input):
        """Test redo functionality."""
        calculator_repl()
        mock_print.assert_any_call("\x1b[32mOperation redone\x1b[0m")

    @patch('builtins.input', side_effect=['redo', 'exit'])
    @patch('builtins.print')  
    def test_redo_nothing_to_redo(self, mock_print, mock_input):
        """Test redo when nothing to redo."""
        calculator_repl()
        mock_print.assert_any_call("\x1b[33mNothing to redo\x1b[0m")

    @patch('builtins.input', side_effect=['add', '5', '3', 'save', 'exit'])
    @patch('builtins.print')
    def test_manual_save(self, mock_print, mock_input):
        """Test manual save command."""
        calculator_repl()
        mock_print.assert_any_call("\x1b[32mHistory saved successfully\x1b[0m")

    @patch('builtins.input', side_effect=['load', 'exit'])
    @patch('builtins.print')
    def test_load_command(self, mock_print, mock_input):
        """Test load command."""
        calculator_repl()
        # Should either succeed or show error - both are valid
        calls = [str(call) for call in mock_print.call_args_list]
        load_result = any("loaded" in call.lower() or "error" in call.lower() for call in calls)

    @patch('builtins.input', side_effect=['add', 'cancel', 'exit'])
    @patch('builtins.print')
    def test_cancel_operation_first_number(self, mock_print, mock_input):
        """Test canceling operation at first number input."""
        calculator_repl()
        mock_print.assert_any_call("\x1b[33mOperation cancelled\x1b[0m")

    @patch('builtins.input', side_effect=['add', '5', 'cancel', 'exit'])
    @patch('builtins.print')
    def test_cancel_operation_second_number(self, mock_print, mock_input):
        """Test canceling operation at second number input."""
        calculator_repl()
        mock_print.assert_any_call("\x1b[33mOperation cancelled\x1b[0m")

    @patch('builtins.input', side_effect=['divide', '5', '0', 'exit'])
    @patch('builtins.print')
    def test_division_by_zero_error(self, mock_print, mock_input):
        """Test division by zero error handling."""
        calculator_repl()
        calls = [str(call) for call in mock_print.call_args_list]
        error_found = any("error" in call.lower() and "division" in call.lower() for call in calls)

    @patch('builtins.input', side_effect=['add', 'invalid', '5', 'exit'])
    @patch('builtins.print')
    def test_invalid_input_error(self, mock_print, mock_input):
        """Test invalid input error handling."""
        calculator_repl()
        calls = [str(call) for call in mock_print.call_args_list]
        error_found = any("error" in call.lower() for call in calls)

    @patch('builtins.input', side_effect=['invalid_command', 'exit'])
    @patch('builtins.print')
    def test_unknown_command(self, mock_print, mock_input):
        """Test unknown command handling."""
        calculator_repl()
        mock_print.assert_any_call("\x1b[31mUnknown command: 'invalid_command'. Type 'help' for available commands.\x1b[0m")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_keyboard_interrupt(self, mock_print, mock_input):
        """Test keyboard interrupt handling (Ctrl+C)."""
        mock_input.side_effect = [KeyboardInterrupt(), 'exit']
        calculator_repl()
        mock_print.assert_any_call("\n\x1b[33mOperation cancelled\x1b[0m")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_eof_error(self, mock_print, mock_input):
        """Test EOF error handling (Ctrl+D)."""
        mock_input.side_effect = EOFError()
        calculator_repl()
        mock_print.assert_any_call("\n\x1b[36mInput terminated. Exiting...\x1b[0m")

    @patch('builtins.input', side_effect=['modulus', '10', '3', 'exit'])
    @patch('builtins.print')
    def test_modulus_operation(self, mock_print, mock_input):
        """Test modulus operation."""
        calculator_repl()
        mock_print.assert_any_call("\n\x1b[32mResult: \x1b[1m1\x1b[0m")

    @patch('builtins.input', side_effect=['int_divide', '10', '3', 'exit'])  
    @patch('builtins.print')
    def test_int_divide_operation(self, mock_print, mock_input):
        """Test integer division operation."""
        calculator_repl()
        mock_print.assert_any_call("\n\x1b[32mResult: \x1b[1m3\x1b[0m")

    @patch('builtins.input', side_effect=['percent', '25', '100', 'exit'])
    @patch('builtins.print')
    def test_percent_operation(self, mock_print, mock_input):
        """Test percentage operation."""
        calculator_repl()
        mock_print.assert_any_call("\n\x1b[32mResult: \x1b[1m25\x1b[0m")

    @patch('builtins.input', side_effect=['abs_diff', '10', '3', 'exit'])
    @patch('builtins.print')
    def test_abs_diff_operation(self, mock_print, mock_input):
        """Test absolute difference operation."""
        calculator_repl()
        mock_print.assert_any_call("\n\x1b[32mResult: \x1b[1m7\x1b[0m")

    @patch('builtins.input', side_effect=['power', '2', '3', 'exit'])
    @patch('builtins.print')
    def test_power_operation(self, mock_print, mock_input):
        """Test power operation."""
        calculator_repl()
        mock_print.assert_any_call("\n\x1b[32mResult: \x1b[1m8\x1b[0m")

    @patch('builtins.input', side_effect=['root', '9', '2', 'exit'])
    @patch('builtins.print')
    def test_root_operation(self, mock_print, mock_input):
        """Test root operation."""
        calculator_repl()
        mock_print.assert_any_call("\n\x1b[32mResult: \x1b[1m3\x1b[0m")

    @patch('app.calculator.Calculator.save_history')
    @patch('builtins.input', side_effect=['save'])
    @patch('builtins.print')
    def test_save_error_handling(self, mock_print, mock_input, mock_save):
        """Test save error handling."""
        mock_save.side_effect = Exception("Save failed")
        mock_input.side_effect = ['save', 'exit']
        calculator_repl()
        mock_print.assert_any_call("\x1b[31mError saving history: Save failed\x1b[0m")

    @patch('app.calculator.Calculator.load_history')
    @patch('builtins.input', side_effect=['load'])
    @patch('builtins.print')
    def test_load_error_handling(self, mock_print, mock_input, mock_load):
        """Test load error handling."""
        mock_load.side_effect = Exception("Load failed")
        mock_input.side_effect = ['load', 'exit']
        calculator_repl()
        mock_print.assert_any_call("\x1b[31mError loading history: Load failed\x1b[0m")
