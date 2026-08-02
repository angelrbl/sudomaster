import plotext as plt
import pandas as pd

def plot_execution_time(df: pd.DataFrame) -> None:
    if df.empty:
        return

    grouped_df = df.groupby("difficulty", observed=True)["execution_time"].mean()

    difficulty_list = grouped_df.index.tolist()
    execution_time_list = grouped_df.values.tolist()

    plt.clear_figure()

    plt.theme("clear")

    plt.bar(difficulty_list, execution_time_list, color="green")

    plt.title("Average execution time by difficulty.")
    plt.xlabel("Difficulty")
    plt.ylabel("Time (s)")

    plt.plotsize(60, 12)

    plt.show()

def plot_backtracks(df: pd.DataFrame) -> None:
    if df.empty:
        return

    grouped_df = df.groupby("difficulty", observed=True)["backtracks"].mean()

    difficulty_list = grouped_df.index.tolist()
    execution_time_list = grouped_df.values.tolist()

    plt.clear_figure()

    plt.theme("clear")

    plt.bar(difficulty_list, execution_time_list, color="green")

    plt.title("Average backtracks by difficulty.")
    plt.xlabel("Difficulty")
    plt.ylabel("Backtracks")

    plt.plotsize(60, 12)

    plt.show()

def plot_scatter_backtracks_vs_time(df: pd.DataFrame) -> None:
    if df.empty:
        return

    x = df["backtracks"].tolist()
    y = df["execution_time"].tolist()

    plt.clear_figure()
    plt.theme("clear")
    
    plt.scatter(x, y, color="green")
    
    plt.title("Backtracks vs Execution Time")
    plt.xlabel("Backtracks")
    plt.ylabel("Time (s)")
    plt.plotsize(60, 12)
    plt.show()

def plot_time_distribution(df: pd.DataFrame, bins: int = 10) -> None:
    if df.empty:
        return

    values = df["execution_time"].tolist()

    plt.clear_figure()
    plt.theme("clear")
    
    plt.hist(values, bins=bins, color="green")
    
    plt.title("Execution Time Distribution")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency")
    plt.plotsize(60, 12)
    plt.show()

def render_benchmark_charts(df: pd.DataFrame) -> None:
    print("\n")

    plot_execution_time(df=df)
    print("\n")
    plot_backtracks(df=df)

    print("\n")