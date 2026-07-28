import sqlite3
import pandas as pd

conn=sqlite3.connect("db/nifty100.db")

peer=pd.read_sql("SELECT * FROM peer_percentiles",conn)

writer=pd.ExcelWriter(
    "output/peer_comparison.xlsx",
    engine="openpyxl"
)

for grp in peer.peer_group_name.dropna().unique():

    temp=peer[peer.peer_group_name==grp]

    temp.to_excel(
        writer,
        sheet_name=str(grp)[:31],
        index=False
    )

writer.close()

conn.close()

print("peer_comparison.xlsx created.")