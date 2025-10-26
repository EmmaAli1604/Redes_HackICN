import numpy as np
import pandas as pd
from scipy import sparse

class Generator:

    def __init__(self, df):
        self.df = df.copy()
        