import webbrowser as wb


class Tools:
    def write_new_storage(self):
        with open('storage.py','w') as storage:
            storage.write('dbr = {}\ncbr = {}\ndje = []\nret_earn = 0\nni = 0')


t = Tools()


class Journal(Tools):
    def journal_entry(self):
        with open('General_Ledger.csv', 'a') as ledger:
            from storage import dbr, cbr, dje, ret_earn, ni
            self.dbr = dbr
            self.cbr = cbr
            self.dje = dje
            self.ret = ret_earn
            self.ni = ni
            with open('storage.py', 'w') as storage:
                ledger.write("""Date,Debit,Credit,Debit($),Credit($)\n""")
                while True:
                    self.date = str(input('Date?\n'))
                    self.dje.append(self.date)
                    ledger.write(f'{self.date},,,,,\n')
                    while True:
                        self.debit_category = input('Debit Category?\n').lower()
                        self.debit = int(input('Amount?\n'))
                        dbr_check = input('Another Debit y/n?\n').lower()
                        if self.debit_category in self.dbr:
                            self.dbr[f'{self.debit_category}'] = self.dbr[f'{self.debit_category}'] + int(self.debit)
                        else:
                            self.dbr[f'{self.debit_category}'] = self.debit
                        if 'y' in dbr_check:
                            ledger.write(f""",{self.debit_category},,{self.debit},,\n""")
                            pass
                        if 'n' in dbr_check:
                            ledger.write(f""",{self.debit_category},,{self.debit},,\n""")
                            break
                    while True:
                        self.credit_category = input('Credit Category?\n').lower()
                        self.credit = int(input('Amount?\n'))
                        cdr_check = input('Another Credit y/n?\n').lower()
                        if self.credit_category in self.cbr:
                            self.cbr[f'{self.credit_category}'] = self.cbr[f'{self.credit_category}'] + int(self.credit)
                        else:
                            self.cbr[f'{self.credit_category}'] = self.credit
                        if 'y' in cdr_check:
                            ledger.write(f""",,{self.credit_category},,{self.credit},\n""")
                            pass
                        if 'n' in cdr_check:
                            ledger.write(f""",,{self.credit_category},,{self.credit},\n""")
                            break
                    journal_check = input('Another entry y/n?\n').lower()
                    if 'y' in journal_check:
                        ledger.write(f""",,,,,\n""")
                        pass
                    if 'n' in journal_check:
                        ledger.write(f""",,,,,\n""")
                        storage.write(f'dbr = {self.dbr}\n')
                        storage.write(f'cbr = {self.cbr}\n')
                        storage.write(f'dje = {self.dje}\n')
                        storage.write(f'ret_earn = {self.ret}\n')
                        storage.write(f'ni = {self.ni}')
                        storage.close()
                        ledger.close()
                        storage.close()
                        break
        wb.open('General_Ledger.csv')


j = Journal()


class TrialBalance(Tools):
    def compiler(self):
        from storage import dbr, cbr, dje, ret_earn, ni
        self.dbr = dbr
        self.cbr = cbr
        self.dje = dje
        self.ret = ret_earn
        self.ni = ni
        self.tbdbr = self.dbr
        self.tbcbr = self.cbr
        normal_credit_balance = ['payable', 'payables', 'revenue', 'stock', 'earnings', 'accumulated']
        normal_debit_balance = ['receivables', 'receivable', 'cash', 'land', 'equipment', 'building', 'expenses', 'dividends','expense']
        for deb in self.tbdbr:
            for normcbr in normal_credit_balance:
                if deb in normcbr:
                    self.tbdbr[deb] = -1 * self.tbdbr[deb]
                else:
                    pass
        for cre in self.tbcbr:
            for normdbr in normal_debit_balance:
                if cre in normdbr:
                    self.tbcbr[cre] = -1 * self.tbcbr[cre]
                else:
                    pass
        for drb in self.tbdbr.keys():
            for crd in self.tbcbr.keys():
                if drb in crd:
                    if abs(self.tbcbr[crd]) >> abs(self.tbdbr[drb]):
                        pass
                    else:
                        self.tbdbr[drb] = self.tbdbr[drb] + self.tbcbr[crd]
                        self.tbcbr.pop(crd)
                        break
                else:
                    pass
        with open('storage.py','w') as storage:
            storage.write(f'dbr = {self.dbr}\n')
            storage.write(f'cbr = {self.cbr}\n')
            storage.write(f'dje = {self.dje}\n')
            storage.write(f'ret_earn = {self.ret}\n')
            storage.write(f'ni = {self.ni}')
        storage.close()

    def unadjusted_trial_balance(self):
        if sum(self.tbdbr.values()) == sum(self.tbcbr.values()):
            print('Accounts with normal debit balance equal accounts with a normal credit balance!')
        else:
            print('Unadjusted Trial Balance Does Not Work!\nPreparing csv with dbr and cbr amounts!')
            with open('Trial_Balance.csv', 'w') as tb:
                for keys in self.tbdbr:
                    tb.write(keys + ',,' + str(self.tbdbr[keys]) + '\n')
                for keys in self.tbcbr:
                    tb.write(keys + ',,,' + str(self.tbcbr[keys]) + '\n')
                tb.write(f'Totals:,,{sum(self.tbdbr.values())},{sum(self.tbcbr.values())}')
                wb.open('Trial_Balance.csv')

    def adjusting_entries(self):
        adjcheck = input('Adj entries y/n?\n').lower()
        if 'y' in adjcheck:
            print(j.journal_entry())
            print(tr.compiler())
            print(tr.unadjusted_trial_balance())
        else:
            pass


tr = TrialBalance()


class FinancialStatements(Tools):
    def income_statement(self):
        from storage import dbr, cbr, dje, ret_earn, ni
        self.dbr = dbr
        self.cbr = cbr
        self.dje = dje
        self.ret = ret_earn
        self.ni = ni
        revenue = {}
        revenue_cat = ['revenue', 'revenues']
        expense = {}
        expense_cat = ['expense', 'expenses']
        for creds in self.cbr.keys():
            for revenues_cats in revenue_cat:
                if revenues_cats in creds:
                    revenue[creds] = self.cbr[creds]
                    break
        for debs in self.dbr.keys():
            for expenses_cats in expense_cat:
                if expenses_cats in debs:
                    expense[debs] = self.dbr[debs]
                    break
        with open('Income_Statement.csv','w') as income_statement:
            income_statement.write(f'\nIncome Statement for year ended {self.dje[-1]} \n\n\nRevenues\n')
            for revenues in revenue:
                income_statement.write(revenues + ',,' + str(revenue[revenues]) + '\n')
            income_statement.write('Revenue Total:,,, ' + f'{sum(revenue.values())}\n' + '\nExpenses\n')
            for expenses in expense:
                income_statement.write(expenses + ',,' + str(expense[expenses]) + '\n')
            income_statement.write('Expense Total:,,, ' + f'{sum(expense.values())}\n' + '\n')
            self.ni = sum(revenue.values()) - sum(expense.values())
            income_statement.write(f'Net Income (loss):,,, {self.ni}')
            with open('storage.py', 'w') as storage:
                storage.write(f'dbr = {self.dbr}\n')
                storage.write(f'cbr = {self.cbr}\n')
                storage.write(f'dje = {self.dje}\n')
                storage.write(f'ret_earn = 0\n')
                storage.write(f'ni = {self.ni}')
            storage.close()
            wb.open('Income_Statement.csv')

    def statement_of_retained_earnings(self):
        from storage import dbr, cbr, dje, ret_earn, ni
        self.dbr = dbr
        self.cbr = cbr
        self.dje = dje
        self.ret = ret_earn
        self.ni = ni
        dvdnds = {}
        dvd = ['dividends', 'dividend']
        with open('Statement_of_Ret_Earnings.csv','w') as ret_earn_stat:
            ret_earn_stat.write(f'\nStatement of Retained Earnings for year ended {self.dje[-1]}\n\n'
                                f'Beginning Retained Earnings:,,{self.ret}\n'
                                f'Add: Net Income,, {self.ni}\n')
            for div in self.dbr:
                for i in dvd:
                    if i in div:
                        dvdnds[div] = self.dbr[div]
            ret_earn_stat.write(f'Less: Dividends,\n')
            for d in dvdnds:
                ret_earn_stat.write(str(d) + ',,' + str(dvdnds[d]) + '\n')
            self.ret = (int(self.ret) + int(self.ni)) - sum(dvdnds.values())
            ret_earn_stat.write(f'Ending Retained Earnings:,{self.ret}')
            with open('storage.py', 'w') as storage:
                storage.write(f'dbr = {self.dbr}\n')
                storage.write(f'cbr = {self.cbr}\n')
                storage.write(f'dje = {self.dje}\n')
                storage.write(f'ret_earn = {self.ret}\n')
                storage.write(f'ni = {self.ni}')
            storage.close()
            wb.open('Statement_of_Ret_Earnings.csv')

    def balance_sheet(self):
        from storage import ret_earn, dbr, cbr, dje
        asset = {}
        asset_cat = ['cash', 'equipment', 'land', 'receivable', 'building', 'deposit', 'accumulated','prepaid']
        liability = {}
        liability_cat = ['payable', 'liabilities']
        se = {}
        se_cat = ['earnings', 'common stock', 'preferred stock', 'capital']
        self.dbr = dbr
        self.cbr = cbr
        self.dje = dje
        self.ret_earn = ret_earn
        for debs in self.dbr:
            for cats in asset_cat:
                if debs in cats:
                    asset[debs] = self.dbr[debs]
        for creds in self.cbr:
            for catz in liability_cat:
                if catz in creds:
                    liability[creds] = self.cbr[creds]
        for see in self.cbr:
            for catc in se_cat:
                if catc in see:
                    se[see] = self.cbr[see]
        se['Retained Earnings'] = self.ret_earn
        with open('Balance_Sheet.csv','w') as sheet:
            sheet.write(f'\nBalance Sheet for {input("Company name? ")} corporation for period ended {self.dje[-1]}:\n\n'
                        f'Assets:\n')
            for assets in asset:
                sheet.write(str(assets) + ',,' + str(asset[assets]) + '\n')
            sheet.write(f'Total Assets:,,, {sum(asset.values())}\n')
            sheet.write('\nLiabilities:\n')
            for liabilities in liability:
                sheet.write(str(liabilities) + ',,' + str(liability[liabilities]) + '\n')
                sheet.write(f'Total Liabilities:,,, {sum(liability.values())}\n')
            sheet.write("""\nShareholder's Equity:\n""")
            for she in se:
                sheet.write(str(she) + ',,' + str(se[she]) + '\n')
            sheet.write(f'Total Shareholder Equity:,,, {sum(se.values())}\n'
                        f'Total Shareholder Equity and Liabilities:,,,{sum(liability.values()) + sum(se.values())}')
            wb.open('Balance_Sheet.csv')

    def statement_of_cash_flows(self):
        from storage import dbr, cbr, dje, ret_earn, ni
        self.dbr = dbr
        self.cbr = cbr
        self.dje = dje
        self.ret = ret_earn
        self.ni = ni
        receipts = {'Cash Received from Customers': 0}
        paid = {'Cash Paid for inventory': 0, 'Cash Paid for Operating Expenses': 0, 'Cash Paid for Taxes': 0}
        investing = {'Cash Paid for Equipment': 0, 'Cash Received on Sale of Equipment': 0}
        financing = {'Cash Received from Issuing Stock': 0, 'Cash Paid for Dividends': 0, 'Cash Paid on Long-Term Notes': 0}
        for a in self.cbr:
            if 'revenue' in a:
                receipts['Cash Received from Customers'] = int(self.cbr[a]) + receipts['Cash Received from Customers']
            if 'accounts payable' in a:
                paid['Cash Paid for inventory'] = int(paid['Cash Paid for inventory']) - int(self.cbr[a])
            if 'notes payable' in a:
                financing['Cash Paid on Long-Term Notes'] = int(financing['Cash Paid on Long-Term Notes']) - int(self.cbr[a])
            if 'taxes payable' in a:
                paid['Cash Paid for Taxes'] = int(paid['Cash Paid for Taxes']) - int(self.cbr[a])
            if 'payable' in a:
                paid['Cash Paid for Operating Expenses'] = int(paid['Cash Paid for Operating Expenses']) - int(self.cbr[a])
            if 'stock' in a:
                financing['Cash Received from Issuing Stock'] = int(financing['Cash Received from Issuing Stock']) + int(self.cbr[a])
        for b in self.dbr:
            if 'tax expense' in b:
                paid['Cash Paid for Taxes'] = int(self.dbr[b]) + int(paid['Cash Paid for Taxes'])
            if 'receivable' in b:
                receipts['Cash Received from Customers'] = int(receipts['Cash Received from Customers']) - int(self.dbr[b])
            if 'cost of goods sold' in b:
                paid['Cash Paid for inventory'] = int(paid['Cash Paid for inventory']) + int(self.dbr[b])
            if 'inventory' in b:
                paid['Cash Paid for inventory'] = int(paid['Cash Paid for inventory']) + int(self.dbr[b])
            if 'expense' in b:
                paid['Cash Paid for Operating Expenses'] = int(paid['Cash Paid for Operating Expenses']) + int(self.dbr[b])
            if 'dividends' in b:
                financing['Cash Paid for Dividends'] = int(financing['Cash Paid for Dividends']) - int(self.dbr[b])
            if 'gain on sale of equipment' in b:
                investing['Cash Received on Sale of Equipment'] = int(investing['Cash Received on Sale of Equipment']) + int(self.dbr[b])
            if 'equipment' in b:
                investing['Cash Paid for Equipment'] = int(investing['Cash Paid for Equipment']) - int(self.dbr[b])
        with open('Cash_Flows_Statement.csv', 'w') as cash:
            cash.write(f'\nConsolidated Statement of Cash Flows for Period Ended {self.dje[-1]}:\n\n')
            cash.write('Operating Revenues\n')
            for c in receipts:
                cash.write(f'{c} ,, {receipts[c]}\n')
            cash.write('Operating Expenses\n')
            for d in paid:
                cash.write(f'{d},,{paid[d]}\n')
            cash.write(f'Cash gained Provided (used) by Operating Activities:,,,{int(receipts["Cash Received from Customers"]) - sum(paid.values())}\n\n')
            cash.write('Investing Cash Flows:\n')
            for f in investing:
                cash.write(f'{f},,{investing[f]}\n')
            cash.write(f'Total Cash Provided (used) by Investing Activities:,,,{sum(investing.values())}\n\n')
            cash.write('Financing Cash Flows:\n')
            for i in financing:
                cash.write(f'{i},,{financing[i]}\n')
            cash.write(f'Total Cash Provided (used) by Financing Activities:,,,{sum(financing.values())}\n\n')
            cash.write(f'Total Change in Cash:,,,{(int(receipts["Cash Received from Customers"]) - sum(paid.values())) + sum(investing.values()) + sum(financing.values())}')
            wb.open('Cash_Flows_Statement.csv')


f = FinancialStatements()


class ErrorReporting:
    def create_report(self):
        error = str(input('What was overstated and by how much?\n'))
        error_date = str(input('When did it happen?\n'))
        with open('Error_Reporting.csv', 'a') as report:
            report.write(f'\nError Report for {error_date}'
                         f'\nWhat happened?'
                         f'\n{error}')


e = ErrorReporting()


class Menu(FinancialStatements, TrialBalance, Journal, Tools, ErrorReporting):
    def __init__(self):
        while True:
            mcheck = input('What will you do today?'
                           '\n'
                           '\njournal = journal entries'
                           '\ncheck = check to see if accounts balance (trial balance)'
                           '\nadj = adjusting entries'
                           '\nni = income statement | ret = statement of ret. earnings  | bal = balance sheet | cash = cash flows sheet'
                           '\nwri = write new storage <--- MUST DO THIS COMMAND FIRST IF FIRST TIME LOADING PROGRAM'
                           '\nerror = error reporting sheet'
                           '\nexit = exit'
                           '\n'
                           ).lower()
            if 'journal' in mcheck:
                print(j.journal_entry())
                print(tr.compiler())
            if 'check' in mcheck:
                print(tr.compiler())
                print(tr.unadjusted_trial_balance())
            if 'adj' in mcheck:
                print(tr.adjusting_entries())
            if 'ni' in mcheck:
                print(f.income_statement())
            if 'ret' in mcheck:
                print(f.statement_of_retained_earnings())
            if 'bal' in mcheck:
                print(f.balance_sheet())
            if 'cash' in mcheck:
                print(f.statement_of_cash_flows())
            if 'error' in mcheck:
                print(e.create_report())
            if 'wri' in mcheck:
                print(t.write_new_storage())
            if 'exit' in mcheck:
                input('Press Enter to Exit')
                break


m = Menu()