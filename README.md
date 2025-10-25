# IS601 Midterm Project - Enhanced Calculator

An advanced command-line calculator application built with Python, featuring multiple arithmetic operations, comprehensive history management, undo/redo functionality, and automated testing with CI/CD integration.

## Features

### Core Operations
- **Basic Arithmetic**: Addition, Subtraction, Multiplication, Division
- **Advanced Operations**: Power, Root, Modulus, Integer Division
- **New Operations**: Percentage Calculation, Absolute Difference

### Advanced Features
- **Interactive REPL Interface** with color-coded output
- **History Management** with persistent storage using pandas
- **Undo/Redo Functionality** using the Memento design pattern
- **Observer Pattern** for logging and auto-save functionality
- **Comprehensive Error Handling** with custom exceptions
- **Configuration Management** using environment variables
- **Automated Testing** with 90%+ test coverage
- **CI/CD Pipeline** with GitHub Actions

## Design Patterns Implemented

- **Factory Pattern**: `OperationFactory` for creating operation instances
- **Observer Pattern**: `LoggingObserver` and `AutoSaveObserver` for event handling
- **Memento Pattern**: `CalculatorMemento` for undo/redo functionality
- **Strategy Pattern**: Pluggable operation strategies

## Project Structure

```
project_root/
├── app/
│   ├── __init__.py
│   ├── calculator.py              # Main calculator class
│   ├── calculation.py             # Individual calculation handling
│   ├── calculator_config.py       # Configuration management
│   ├── calculator_memento.py      # Memento pattern implementation
│   ├── calculator_repl.py         # Interactive command-line interface
│   ├── exceptions.py              # Custom exception classes
│   ├── history.py                 # Observer pattern implementations
│   ├── input_validators.py        # Input validation utilities
│   ├── operations.py              # Operation classes and factory
│   └── logger.py                  # Logging configuration
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py         # Calculator and REPL tests
│   ├── test_calculation.py        # Calculation class tests
│   ├── test_operations.py         # Operation tests
│   └── ...                       # Additional test files
├── .env                           # Environment configuration
├── requirements.txt               # Python dependencies
├── main.py                        # Entry point
├── README.md                      # This file
└── .github/
    └── workflows/
        └── python-app.yml         # CI/CD pipeline
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd IS601-Midterm-Project-Calculator
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the project root (or modify the existing one):
   ```env
   # Base Directories
   CALCULATOR_LOG_DIR=test_logs
   CALCULATOR_HISTORY_DIR=test_history

   # History Settings
   CALCULATOR_MAX_HISTORY_SIZE=100
   CALCULATOR_AUTO_SAVE=true

   # Calculation Settings
   CALCULATOR_PRECISION=10
   CALCULATOR_MAX_INPUT_VALUE=1000000
   CALCULATOR_DEFAULT_ENCODING=utf-8
   ```

## Usage

### Running the Calculator

Start the interactive calculator:
```bash
python main.py
```

### Available Commands

#### Arithmetic Operations
- `add` - Addition (a + b)
- `subtract` - Subtraction (a - b)
- `multiply` - Multiplication (a × b)
- `divide` - Division (a ÷ b)
- `power` - Exponentiation (a^b)
- `root` - nth Root (a^(1/b))
- `modulus` - Modulus/Remainder (a % b)
- `int_divide` - Integer Division (a // b)
- `percent` - Percentage ((a/b) × 100)
- `abs_diff` - Absolute Difference (|a - b|)

#### History Management
- `history` - Display calculation history
- `clear` - Clear all history
- `undo` - Undo last calculation
- `redo` - Redo previously undone calculation
- `save` - Manually save history to file
- `load` - Load history from file

#### Utility Commands
- `help` - Show all available commands
- `exit` - Exit the calculator

### Example Usage

```
Welcome to the Python Calculator REPL!
Type 'help' for available commands or 'exit' to quit.

Enter command: add

Enter numbers (or 'cancel' to abort):
First number: 15
Second number: 25

Result: 40

Enter command: percent

Enter numbers (or 'cancel' to abort):
First number: 25
Second number: 100

Result: 25

Enter command: history
Calculation History:
1. Addition(15, 25) = 40
2. PercentageCalculation(25, 100) = 25

Enter command: exit
History saved successfully.
Goodbye!
```

## Testing

### Running Tests

Run all tests:
```bash
pytest
```

Run tests with coverage report:
```bash
pytest --cov=app
```

Run tests with coverage enforcement (90% minimum):
```bash
pytest --cov=app --cov-fail-under=90
```

### Test Coverage

The project maintains 90%+ test coverage across all modules:
- Unit tests for all operation classes
- Integration tests for calculator functionality
- REPL interface testing
- Error handling verification
- Observer pattern testing

## Configuration

The application uses environment variables for configuration:

### Base Directories
- `CALCULATOR_LOG_DIR`: Directory for log files (default: "test_logs")
- `CALCULATOR_HISTORY_DIR`: Directory for history files (default: "test_history")

### History Settings
- `CALCULATOR_MAX_HISTORY_SIZE`: Maximum history entries (default: 100)
- `CALCULATOR_AUTO_SAVE`: Auto-save history on calculations (default: true)

### Calculation Settings
- `CALCULATOR_PRECISION`: Decimal precision (default: 10)
- `CALCULATOR_MAX_INPUT_VALUE`: Maximum input value (default: 1000000)
- `CALCULATOR_DEFAULT_ENCODING`: File encoding (default: "utf-8")

## Continuous Integration

The project includes a GitHub Actions workflow that:
- Runs on every push to main branch
- Runs on every pull request to main branch
- Tests against Python 3.x
- Installs all dependencies
- Runs the full test suite
- Enforces 90% test coverage minimum
- Fails the build if coverage drops below threshold

## Error Handling

The application includes comprehensive error handling:

### Custom Exceptions
- `OperationError`: For calculation and operation failures
- `ValidationError`: For input validation issues

### Validation Features
- Input type validation (numbers only)
- Range validation (configurable limits)
- Division by zero prevention
- Invalid operation detection

## Logging

Comprehensive logging system:
- All calculations logged with timestamps
- Error events recorded
- Configuration changes tracked
- Observer actions logged
- Log files stored in configurable directory

## Data Persistence

### History Storage
- Calculations saved to CSV format using pandas
- Automatic backup on exit
- Manual save/load commands available
- Configurable history size limits

### File Format
CSV files include:
- Operation name
- First operand
- Second operand
- Result
- Timestamp

## Development

### Adding New Operations

1. Create operation class in `app/operations.py`:
   ```python
   class NewOperation(Operation):
       def execute(self, a: Decimal, b: Decimal) -> Decimal:
           # Implementation here
           return result
   ```

2. Register with factory:
   ```python
   OperationFactory.register_operation("new_op", NewOperation)
   ```

3. Add to calculation dictionary in `app/calculation.py`

4. Write comprehensive tests

### Code Quality
- Follow PEP 8 style guidelines
- Use type hints throughout
- Comprehensive docstrings
- Regular code reviews
- Automated testing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Ensure 90%+ test coverage
5. Submit pull request

## License

This project is developed for educational purposes as part of the IS601 course at NJIT.

## Acknowledgments

- Built using Python 3.x
- pandas for data manipulation
- pytest for testing framework
- colorama for terminal colors
- python-dotenv for configuration management
