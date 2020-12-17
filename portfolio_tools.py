import xlrd

class BalanceExcelTool:

    def __init__(self, path):
        excel_workbook = xlrd.open_workbook(path)
        self.worksheet = excel_workbook.sheet_by_index(0)
    
    def getTotalDeposits(self):
        self.totalDeposit = 0
        for row in range(self.worksheet.nrows):
            if self.worksheet.cell_value(row,2) == 'Talletus':
                #get value and remove + and € signs
                deposit = self.worksheet.cell_value(row, 4)[1:-2]
                self.totalDeposit += float(deposit)
        return self.totalDeposit
