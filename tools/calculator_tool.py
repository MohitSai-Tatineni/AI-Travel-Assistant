from utils.expense_calculator import Calculator
from typing import List
from langchain.tools import tool

class CalculatorTool:
    def __init__(self):
        self.calculator = Calculator()
        self.calculator_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the calculator tool"""

        @tool
        def estimate_total_hotel_cost(price_per_night: float, total_days: float) -> float:
            """Calculate total hotel cost"""
            # Ensure numeric types
            return self.calculator.multiply(float(price_per_night), float(total_days))

        @tool
        def calculate_total_expense(costs: List[float]) -> float:
            """Calculate total expense of the trip"""
            # Convert all to float in case they come as strings
            numeric_costs = [float(c) for c in costs]
            return self.calculator.calculate_total(*numeric_costs)

        @tool
        def calculate_daily_expense_budget(total_cost: float, days: int) -> float:
            """Calculate daily expense"""
            return self.calculator.calculate_daily_budget(float(total_cost), int(days))

        return [
            estimate_total_hotel_cost,
            calculate_total_expense,
            calculate_daily_expense_budget,
        ]
