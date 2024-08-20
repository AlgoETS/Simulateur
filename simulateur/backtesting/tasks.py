from celery import shared_task
from .models import Strategy, StockBacktest, StrategyOutput
import subprocess
import os
import concurrent.futures

@shared_task
def run_strategy(strategy_id, stock_id):
    try:
        strategy = Strategy.objects.get(id=strategy_id)
        stock = StockBacktest.objects.get(id=stock_id)

        # Create the command for running the strategy script
        command = ['python3', strategy.script_path]

        # Add parameters from the strategy
        for key, value in strategy.parameters.items():
            command.extend([f"--{key}", str(value)])

        # Add stock-specific data
        command.extend([f"--ticker", stock.ticker])

        # Run the command in multiple threads (if needed)
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(subprocess.run, command, check=True, capture_output=True, text=True) for _ in range(4)]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()

                # Save the output as a StrategyOutput
                output = StrategyOutput.objects.create(
                    strategy=strategy,
                    ticker=stock.ticker,
                    output_type='chart',
                    file_path=f"path/to/save/output/{strategy.name}_{stock.ticker}_output.html"
                )

        return {"status": "success", "output": output.file_path}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@shared_task
def run_batch_backtesting(strategy_name, instruments):
    # Dynamically import the strategy based on the name
    strategy = globals().get(strategy_name)
    if not strategy:
        return {"status": "failed", "error": f"Strategy {strategy_name} not found"}

    # Run the backtests using the provided script
    outputs = run_backtests_strategies(instruments, [strategy_name])

    # Process the output (save results, generate charts, etc.)
    # Implement your logic to save outputs as StrategyOutput models

    return {"status": "success", "outputs": outputs}
