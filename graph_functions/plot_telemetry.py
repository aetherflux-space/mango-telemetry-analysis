import pandas as pd
import matplotlib.pyplot as plt


def plot_atd_summary(coll, telemetry_mnemoic, column_groups, start_time=None, end_time=None, units=None):
    """
    Plot telemetry data in vertical stack of plots based on specified column groups.

    Parameters:
    - coll: MongoDB collection object to retrieve telemetry data.
    - telemetry_mnemoic: The mnemonic string to filter telemetry data.
    - column_groups: A dictionary where keys are group names and values are dictionaries
                     mapping column names to their display names.
    - start_time: Optional start time to limit x-axis (pandas Timestamp).
    - end_time: Optional end time to limit x-axis (pandas Timestamp).

    """

    # Retrieve data from MongoDB and set time as index
    telemetry = coll.find_pandas_all({'mnemonic': telemetry_mnemoic})
    telemetry.set_index('time', inplace=True)

    # Create a figure with subplots
    fig, axes = plt.subplots(nrows=len(column_groups), ncols=1, figsize=(12, 2.5 * len(column_groups)), sharex=True)

    # Iterate over axes and column group. 
    for idx, (ax, (group_name, cols)) in enumerate(zip(axes, column_groups.items())):
        for col, name in cols.items():
            if col in telemetry.columns:
                ax.plot(telemetry.index, telemetry[col], label=name)

        ax.set_title(group_name)
        if not units:
            ax.set_ylabel("Value")
        else:
            ax.set_ylabel(units[idx])
        ax.legend()
        ax.grid(True)

        if start_time:
            for ax in axes:
                ax.set_xlim(left=start_time)
        
        if end_time:
            for ax in axes:
                ax.set_xlim(right=end_time)

    return fig, axes

