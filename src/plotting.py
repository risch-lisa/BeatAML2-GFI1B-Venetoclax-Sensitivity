import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_distribution(data: pd.DataFrame, column: str, title: str, save_path: str) -> None:
    """Plot a histogram for a numeric variable."""

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.histplot(data[column], kde=True, ax=ax)

    ax.set_title(title or f"Distribution of {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Count")

    fig.tight_layout()

    fig.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.show()
    plt.close(fig)


def plot_relationship(data: pd.DataFrame, x: str, y: str, save_path: str) -> None:
    """Plot a scatterplot with a trend line"""

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.regplot(
        data=data,
        x=x,
        y=y,
        ax=ax,
        scatter_kws={"alpha": 0.65},
        line_kws={"color": "black"},
    )

    ax.set_title(f"{x} vs. {y}")
    fig.tight_layout()

    fig.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.show()
    plt.close(fig)