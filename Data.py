########################################################
# Author:     Filip Segota
# Course:     Advance CS topics (CSC 310, Spring 2021)
# Assignment: Italy & Covid reporting Assignment in 2020
########################################################

import pandas as pd
from regions import *


class Data:
    def __init__(self):
        self._data = self.read_files()

    def read_files(self):
        reported_cases = pd.read_csv("./Italy_Covid_2020/reported_cases.csv")
        italy_summary_table = pd.read_csv("./Italy_Covid_2020/summary_table.csv")

        return [reported_cases, italy_summary_table]

    def get_region(self):
        return self._data[0]["region"].unique()

    def get_population(self, name):
        found = False
        code = ""
        for k in regions:
            if name.strip() == k:
                code = regions[k]
                found = True
        if found:
            return code
        else:
            return None

    def get_case_number(self, name):
        case_sum = 0
        all_case = self._data[0]
        for index, re in enumerate(all_case["region"]):
            if re == name:
                confirm = all_case["confirm"][index]
                case_sum += confirm
        return case_sum

    def getRegionSummary(self, name):
        s = {}
        df = self._data[1]

        row = df.loc[df["Region"] == name]
        index = df.index[df["Region"] == name][0]
        s["newConfirmed"] = row["New confirmed cases by infection date"][index]
        s["expectedChanges"] = row["Expected change in daily cases"][index]

        return s

    def get_percentage(self, reported_case, region_population):
        re_population = region_population.split(",")
        total_population = ""
        for i in re_population:
            total_population += i
        step1 = int(reported_case) / int(total_population)
        step2 = step1 * 100

        return step2

    def getRegionStats(self, name):
        region_population = self.get_population(name)
        case_number = self.get_case_number(name)
        cal_percentage = self.get_percentage(case_number, region_population)
        summary_table = self.getRegionSummary(name)

        if region_population and case_number and cal_percentage is not None:
            return {
                "region": name,
                "population": regions["Italy"],
                "region_population": region_population,
                "case_number": case_number,
                "newConfirmed": summary_table["newConfirmed"],
                "expectedChanges": summary_table["expectedChanges"],
                "percentage": round(cal_percentage, 1),
            }
        else:
            return None
