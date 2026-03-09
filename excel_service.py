import pandas as pd
import os


def create_excel(pdf_links, folder):

    names = [link.split("/")[-1] for link in pdf_links]

    df = pd.DataFrame({
        "PDF Name": names,
        "PDF URL": pdf_links
    })

    folder_name = os.path.basename(folder)

    excel_path = os.path.join(folder, f"{folder_name}.xlsx")

    df.to_excel(excel_path, index=False)

    return excel_path