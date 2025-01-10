import csv
from enum import Enum
import matplotlib.pyplot as plt
import numpy as np


class ContinueNewChoices(Enum):
    C = "CONTINUE"
    N = "NEW"


class DecayCalculator:
    def __init__(
        self,
        start_year=1836,
        end_year=1936,
        continue_or_new: ContinueNewChoices = ContinueNewChoices.N,
        output_file="decay_data.csv",
    ):
        self.start_year = start_year
        self.end_year = end_year
        self.output_file = output_file
        self.year_value_pairs: list[tuple[int, float]] = []
        self.initial_value = None
        self.slope = None

        if continue_or_new == ContinueNewChoices.C:
            self._load_existing_data()
        else:
            # Create a new file and write the header
            with open(self.output_file, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Year", "Value"])

    def _load_existing_data(self):
        """Loads existing data points from the output file."""
        try:
            with open(self.output_file, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header
                self.year_value_pairs = [(int(row[0]), float(row[1])) for row in reader]
                if self.year_value_pairs:
                    self.initial_value = self.year_value_pairs[0][1]
                    self.slope = -self.initial_value / (self.end_year - self.start_year)
            print(
                f"Loaded {len(self.year_value_pairs)} data points from {self.output_file}."
            )
        except FileNotFoundError:
            print(f"No existing file found. Starting fresh.")
        except Exception as e:
            print(f"Error loading file: {e}. Starting fresh.")

    def calculate_value(self, year):
        """Calculates the expected value for a given year based on linear decay."""
        if self.slope is None:
            raise ValueError("Initial value and slope must be set before calculations.")
        return self.initial_value + self.slope * (year - self.start_year)

    def add_data_point(self, year: int, value: float) -> None:
        """Adds a new data point, logs it to a file, and determines if adjustment is needed."""
        if not (self.start_year <= year <= self.end_year):
            raise ValueError(
                f"Year must be between {self.start_year} and {self.end_year}."
            )

        # Set initial value and slope if not already set
        if self.initial_value is None:
            self.initial_value = value
            self.slope = -self.initial_value / (self.end_year - self.start_year)
            print(
                f"Initial value set to {self.initial_value}. Calculated slope is {self.slope:.4f}."
            )

        # Save the data point
        self.year_value_pairs.append((year, value))
        with open(self.output_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([year, value])

        # Calculate the expected value and give feedback
        expected_value = self.calculate_value(year)
        print(
            f"Year: {year}, Provided Value: {value}, Expected Value: {expected_value:.4f}"
        )

        if value < expected_value:
            print("Recommendation: Amortize decay.")
        elif value > expected_value:
            print("Recommendation: Speed up decay.")
        else:
            print("Recommendation: Decay is on track.")

        # Show the updated plot
        self.plot_decay()

    def plot_decay(self):
        """Plots the expected decay and the provided data points."""
        if self.slope is None:
            print("Cannot plot decay function until initial value is set.")
            return

        years = np.linspace(self.start_year, self.end_year, 100)
        expected_values = [self.calculate_value(year) for year in years]

        plt.figure(figsize=(10, 6))
        plt.plot(
            years, expected_values, label="Expected Decay", color="blue", linestyle="--"
        )
        if self.year_value_pairs:
            data_years, data_values = zip(*self.year_value_pairs)
            plt.scatter(
                data_years, data_values, color="red", label="Provided Values", zorder=5
            )

        plt.title("Decay Function and Data Points")
        plt.xlabel("Year")
        plt.ylabel("Value")
        plt.legend()
        plt.grid()
        plt.show()


# Example Usage
if __name__ == "__main__":
    continue_or_new_input = (
        input("Do you want to CONTINUE previous calculations or start NEW? (C/N): ")
        .strip()
        .upper()
    )
    continue_or_new_choice = (
        ContinueNewChoices.C if continue_or_new_input == "C" else ContinueNewChoices.N
    )

    decay_calculator = DecayCalculator(
        start_year=1836, end_year=1936, continue_or_new=continue_or_new_choice
    )

    while True:
        try:
            user_input = input(
                "Enter year and value (e.g., '1850, 0.8') or 'exit' to quit: "
            ).strip()
            if user_input.lower() == "exit":
                break
            year, value = map(float, user_input.split(","))
            decay_calculator.add_data_point(int(year), value)
        except ValueError as e:
            print(f"Invalid input: {e}")
