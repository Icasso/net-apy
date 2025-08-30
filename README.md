# Net APY Calculator

A Python tool for calculating net APY (Annual Percentage Yield) from lending and borrowing strategies in DeFi.

## Features

- **Net APY Calculation**: Compute overall returns from multiple lending/borrowing positions
- **Multi-Strategy Support**: Handle multiple lending and borrowing strategies simultaneously
- **Compounding Analysis**: View returns over different time periods (7, 30, 365 days)
- **Target APY Calculator**: Determine required APY for specific daily earnings
- **Web Interface**: Clean Flask-based web app for easy calculations
- **CLI Mode**: Command-line interface for quick calculations

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Web Application

```bash
python run_web_app.py
```

Open browser to `http://localhost:8080`

### Command Line

```bash
python net_apy_calculator.py
```

## API Endpoints

- `POST /calculate` - Calculate net APY from lending/borrowing strategies
- `POST /calculate-target-apy` - Calculate target APY for desired daily earnings

## Input Format

### Lending/Borrowing Strategies
```json
{
  "lending_strategies": [
    {"notional": 10000, "apy": 8.5},
    {"notional": 5000, "apy": 12.0}
  ],
  "borrowing_strategies": [
    {"notional": 3000, "apy": 5.2}
  ]
}
```

### Target APY Calculator
```json
{
  "daily_earning": 50,
  "notional": 10000
}
```

## Output

Returns comprehensive results including:
- Total lending/borrowing amounts
- Daily interest calculations
- Net APY percentage
- Profitability assessment
- Compounding effects over time
- Target APY requirements

## Sample Request/Response

### Calculate Net APY

**Request:**
```json
{
  "lending_strategies": [
    {"notional": 10000, "apy": 8.5},
    {"notional": 5000, "apy": 12.0}
  ],
  "borrowing_strategies": [
    {"notional": 3000, "apy": 5.2}
  ]
}
```

**Response:**
```json
{
  "success": true,
  "total_lending_notional": 15000.0,
  "total_borrowing_notional": 3000.0,
  "daily_lending_interest": 5.21,
  "daily_borrowing_interest": 0.43,
  "net_daily_interest": 4.78,
  "net_apy": 11.63,
  "profitable": true,
  "break_even": false,
  "total_capital": 15000.0,
  "compounding": {
    "7_days": {
      "lending_compounded": 36.47,
      "borrowing_compounded": 3.01,
      "net_compounded": 33.46,
      "total_value": 15033.46
    },
    "30_days": {
      "lending_compounded": 156.30,
      "borrowing_compounded": 12.90,
      "net_compounded": 143.40,
      "total_value": 15143.40
    },
    "365_days": {
      "lending_compounded": 1901.37,
      "borrowing_compounded": 156.95,
      "net_compounded": 1744.42,
      "total_value": 16744.42
    }
  }
}
```

### Calculate Target APY

**Request:**
```json
{
  "daily_earning": 50,
  "notional": 10000
}
```

**Response:**
```json
{
  "success": true,
  "target_apy": 18.25,
  "daily_earning": 50.0,
  "notional": 10000.0,
  "annual_earning": 18250.0
}
```

## Dependencies

- Flask 2.3.3
- Werkzeug 2.3.7

## License

MIT
