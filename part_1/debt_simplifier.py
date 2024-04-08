class DebtSimplifier:
    def __init__(self, debts: list):
        self.debts = debts

    def compute_balances(self):
        """Compute the balance of each person in the group."""
        balances = {}
        for debtor, creditor, amount in self.debts:
            balances[debtor] = balances.get(debtor, 0) - float(amount)
            balances[creditor] = balances.get(creditor, 0) + float(amount)
        return balances

    def simplify_debts(self):
        """Simplify the debts in the group. The method returns a list of tuples where each tuple contains the name of the creditor, the name of the debtor, and the amount to be paid from the creditor to the debtor. The amount is the minimum amount required to settle the debt between the creditor and the debtor.


        Returns:
            list: A list of tuples where each tuple contains the name of the creditor, the name of the debtor, and the amount to be paid from the creditor to the debtor.
        """
        simplified_debts = []
        balances = self.compute_balances()
        # Simplify the debts until all balances are zero
        while any(balances.values()):
            # Find the creditor and debtor with the maximum and minimum balances
            debtor = min(balances, key=balances.get)
            creditor = max(balances, key=balances.get)
            # Compute the amount to be paid from the creditor to the debtor
            amount = min(abs(balances[debtor]), balances[creditor])
            # Update the balances
            balances[creditor] -= amount
            balances[debtor] += amount
            # Add the simplified debt to the list
            simplified_debts.append((creditor, debtor, amount))
        return simplified_debts
