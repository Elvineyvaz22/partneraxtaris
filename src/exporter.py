import pandas as pd


def export_excel(df: pd.DataFrame, output_path: str) -> None:
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='All Results', index=False)
        df[df['grade'].str.startswith('A')].to_excel(writer, sheet_name='A Grade', index=False)
        df[df['grade'].str.startswith('B')].to_excel(writer, sheet_name='B Grade', index=False)
        df[df['grade'] == 'Reject'].to_excel(writer, sheet_name='Reject', index=False)
