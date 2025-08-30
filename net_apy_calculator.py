from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def calculate_net_apy():
    print("=== Lending & Borrowing Strategy Net APY Calculator ===\n")
    
    # Get lending parameters
    print("LENDING PARAMETERS:")
    lending_notional = float(input("Enter lending notional amount: $"))
    lending_apy = float(input("Enter lending APY (%): ")) / 100
    
    # Get borrowing parameters
    print("\nBORROWING PARAMETERS:")
    borrowing_notional = float(input("Enter borrowing notional amount: $"))
    borrowing_apy = float(input("Enter borrowing APY (%): ")) / 100
    
    # Calculate daily rates
    lending_daily_rate = lending_apy / 365
    borrowing_daily_rate = borrowing_apy / 365
    
    # Calculate daily interest
    daily_lending_interest = lending_notional * lending_daily_rate
    daily_borrowing_interest = borrowing_notional * borrowing_daily_rate
    
    # Calculate net daily interest
    net_daily_interest = daily_lending_interest - daily_borrowing_interest
    
    # Calculate net APY (assuming 365 days)
    net_apy = (net_daily_interest * 365) / max(lending_notional, borrowing_notional) * 100
    
    # Display results
    print("\n" + "="*50)
    print("RESULTS:")
    print(f"Lending daily interest: ${daily_lending_interest:.2f}")
    print(f"Borrowing daily interest: ${daily_borrowing_interest:.2f}")
    print(f"Net daily interest: ${net_daily_interest:.2f}")
    print(f"Net APY: {net_apy:.2f}%")
    
    # Strategy assessment
    if net_daily_interest > 0:
        print(f"\n✅ Strategy is profitable - earning ${net_daily_interest:.2f} daily")
    else:
        print(f"\n❌ Strategy is losing money - losing ${abs(net_daily_interest):.2f} daily")

def calculate_net_apy_web(lending_strategies, borrowing_strategies):
    """Web version of the calculator that handles multiple strategies"""
    
    total_lending_notional = 0
    total_lending_daily_interest = 0
    total_borrowing_notional = 0
    total_borrowing_daily_interest = 0
    
    # Process lending strategies
    for strategy in lending_strategies:
        notional = float(strategy['notional'])
        apy = float(strategy['apy']) / 100
        daily_rate = apy / 365
        daily_interest = notional * daily_rate
        
        total_lending_notional += notional
        total_lending_daily_interest += daily_interest
    
    # Process borrowing strategies
    for strategy in borrowing_strategies:
        notional = float(strategy['notional'])
        apy = float(strategy['apy']) / 100
        daily_rate = apy / 365
        daily_interest = notional * daily_rate
        
        total_borrowing_notional += notional
        total_borrowing_daily_interest += daily_interest
    
    # Calculate net daily interest
    net_daily_interest = total_lending_daily_interest - total_borrowing_daily_interest
    
    # Calculate net APY based on total capital deployed
    # If only lending, use lending capital. If only borrowing, use borrowing capital.
    if total_lending_notional > 0 and total_borrowing_notional > 0:
        total_capital = max(total_lending_notional, total_borrowing_notional)
    elif total_lending_notional > 0:
        total_capital = total_lending_notional
    elif total_borrowing_notional > 0:
        total_capital = total_borrowing_notional
    else:
        total_capital = 0
        
    if total_capital > 0:
        net_apy = (net_daily_interest * 365) / total_capital * 100
    else:
        net_apy = 0
    
    # Calculate compounding effects for different time periods
    periods = [7, 30, 365]  # 1 week, 1 month, 1 year
    compounding_results = {}
    
    # Calculate weighted average APY for lending and borrowing
    lending_avg_apy = 0
    borrowing_avg_apy = 0
    
    if total_lending_notional > 0:
        lending_avg_apy = (total_lending_daily_interest * 365) / total_lending_notional
    
    if total_borrowing_notional > 0:
        borrowing_avg_apy = (total_borrowing_daily_interest * 365) / total_borrowing_notional
    
    for days in periods:
        # Calculate lending compounding (interest earned)
        lending_compounded = 0
        if total_lending_notional > 0:
            lending_daily_rate = lending_avg_apy / 365
            # Compound interest formula: P * ((1 + r)^n - 1)
            lending_compounded = total_lending_notional * ((1 + lending_daily_rate) ** days - 1)
        
        # Calculate borrowing compounding (interest owed)
        borrowing_compounded = 0
        if total_borrowing_notional > 0:
            borrowing_daily_rate = borrowing_avg_apy / 365
            # Compound interest formula: P * ((1 + r)^n - 1)
            borrowing_compounded = total_borrowing_notional * ((1 + borrowing_daily_rate) ** days - 1)
        
        # Net compounded result (earnings - costs)
        net_compounded = lending_compounded - borrowing_compounded
        
        compounding_results[f'{days}_days'] = {
            'lending_compounded': round(lending_compounded, 2),
            'borrowing_compounded': round(borrowing_compounded, 2),
            'net_compounded': round(net_compounded, 2),
            'total_value': round(total_capital + net_compounded, 2)
        }
    
    return {
        'total_lending_notional': round(total_lending_notional, 2),
        'total_borrowing_notional': round(total_borrowing_notional, 2),
        'daily_lending_interest': round(total_lending_daily_interest, 2),
        'daily_borrowing_interest': round(total_borrowing_daily_interest, 2),
        'net_daily_interest': round(net_daily_interest, 2),
        'net_apy': round(net_apy, 2),
        'profitable': net_daily_interest > 0,
        'break_even': net_daily_interest == 0,
        'total_capital': round(total_capital, 2),
        'compounding': compounding_results
    }

def calculate_target_apy(daily_earning, notional):
    """Calculate the target APY needed to achieve a specific daily earning"""
    if notional <= 0:
        return None
    
    # Daily earning = notional * (APY / 365)
    # Therefore: APY = (daily_earning * 365) / notional
    target_apy = (daily_earning * 365) / notional * 100
    
    return {
        'target_apy': round(target_apy, 4),
        'daily_earning': round(daily_earning, 2),
        'notional': round(notional, 2),
        'annual_earning': round(daily_earning * 365, 2)
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        
        lending_strategies = data.get('lending_strategies', [])
        borrowing_strategies = data.get('borrowing_strategies', [])
        
        # Validate that we have at least one strategy
        if not lending_strategies and not borrowing_strategies:
            return jsonify({'success': False, 'error': 'Please add at least one lending or borrowing strategy'})
        
        # Handle case where only one type of strategy exists
        if not lending_strategies:
            lending_strategies = []
        if not borrowing_strategies:
            borrowing_strategies = []
        
        results = calculate_net_apy_web(lending_strategies, borrowing_strategies)
        return jsonify({'success': True, **results})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/calculate-target-apy', methods=['POST'])
def calculate_target_apy_endpoint():
    try:
        data = request.get_json()
        
        daily_earning = float(data.get('daily_earning', 0))
        notional = float(data.get('notional', 0))
        
        if daily_earning <= 0:
            return jsonify({'success': False, 'error': 'Daily earning must be greater than 0'})
        
        if notional <= 0:
            return jsonify({'success': False, 'error': 'Notional amount must be greater than 0'})
        
        results = calculate_target_apy(daily_earning, notional)
        return jsonify({'success': True, **results})
        
    except ValueError:
        return jsonify({'success': False, 'error': 'Please enter valid numbers'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def run_web_app():
    """Run the Flask web application"""
    print("Starting Net APY Calculator Web App...")
    print("Open your browser and go to: http://localhost:8080")
    app.run(debug=True, host='0.0.0.0', port=8080)

if __name__ == "__main__":
    try:
        calculate_net_apy()
    except ValueError:
        print("Error: Please enter valid numbers")
    except KeyboardInterrupt:
        print("\n\nCalculator stopped by user")