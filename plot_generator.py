import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def generate_plot(df, chart_type, x_col=None, y_col=None):
    if chart_type in ["pairplot", "clustermap", "jointplot"]:
        # Special plot types with their own figures
        if chart_type == "pairplot":
            plot = sns.pairplot(df.select_dtypes(include='number'))
            return plot.fig  # .fig returns the matplotlib Figure

        elif chart_type == "clustermap":
            corr = df.select_dtypes(include='number').corr()
            plot = sns.clustermap(corr, cmap="viridis", annot=True)
            return plot.fig  # .fig for Clustermap

        elif chart_type == "jointplot":
            if x_col and y_col:
                plot = sns.jointplot(data=df, x=x_col, y=y_col, kind="scatter")
                return plot.fig  # .fig for Jointplot
            else:
                return None

    else:
        # Regular matplotlib-based plots
        fig, ax = plt.subplots(figsize=(10, 5))

        try:
            if chart_type == "scatterplot":
                sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
            elif chart_type == "lineplot":
                sns.lineplot(data=df, x=x_col, y=y_col, ax=ax)
            elif chart_type == "barplot":
                sns.barplot(data=df, x=x_col, y=y_col, ax=ax)
            elif chart_type == "countplot":
                sns.countplot(data=df, x=x_col, ax=ax)
            elif chart_type == "boxplot":
                sns.boxplot(data=df, x=x_col, y=y_col, ax=ax)
            elif chart_type == "violinplot":
                sns.violinplot(data=df, x=x_col, y=y_col, ax=ax)
            elif chart_type == "stripplot":
                sns.stripplot(data=df, x=x_col, y=y_col, ax=ax)
            elif chart_type == "swarmplot":
                sns.swarmplot(data=df, x=x_col, y=y_col, ax=ax)
            elif chart_type == "histplot":
                sns.histplot(data=df[x_col], bins=20, ax=ax)
            elif chart_type == "kdeplot":
                sns.kdeplot(data=df[x_col], fill=True, ax=ax)
            elif chart_type == "heatmap":
                corr = df.select_dtypes(include='number').corr()
                sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
            elif chart_type == "rugplot":
                sns.rugplot(data=df[x_col], ax=ax)
            else:
                return None

            ax.set_title(f"{chart_type} of {x_col} and {y_col}" if y_col else f"{chart_type} of {x_col}")
            ax.tick_params(axis='x', rotation=45)
            fig.tight_layout()
            return fig

        except Exception as e:
            print(f"[Plot Generation Error] {e}")
            return None
