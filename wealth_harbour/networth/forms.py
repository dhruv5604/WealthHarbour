# forms.py
from django import forms

class InterestForm(forms.Form):
    cashRate = forms.FloatField(label='Cash Rate')
    reRate = forms.FloatField(label='Real Estate Rate')
    iaRate = forms.FloatField(label='Investment Account Rate')
    otherRate = forms.FloatField(label='Other Rate')
    slRate = forms.FloatField(label='Student Loan Rate')
    mdRate = forms.FloatField(label='Mortgage Debt Rate')
    plRate = forms.FloatField(label='Credit Card/Personal Loan Rate')
    otherRateL = forms.FloatField(label='Other Liabilities Rate')
    yearLib = forms.IntegerField(label='Year of Liabilities')
