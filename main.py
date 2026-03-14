from src import normalization
from src.utils import read_xlsx
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filename="app.log",
    filemode="w",
)

df = read_xlsx("./data/dummy.xlsx")
df = normalization.normalization(df)
df.to_excel("./dist/output.xlsx", index=False)
