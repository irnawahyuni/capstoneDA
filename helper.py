import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from io import BytesIO
import base64

def load_telco():
    # Read data
    telco = pd.read_csv('data/telcochurn.csv')
    
    # Adjust dtypes
    catcol = telco.select_dtypes('object').columns
    telco[catcol] = telco[catcol].apply(lambda x: x.astype('category'))
    
    # Tenure Months to grouping categories
    def grouping_tenure(telco) :
        if telco["tenure_months"] <= 12 :
            return "< 1 Year"
        elif (telco["tenure_months"] > 12) & (telco["tenure_months"] <=24 ):
            return "1-2 Year"
        elif (telco["tenure_months"] >24 ) & (telco["tenure_months"] <= 48) :
            return "2-4 Year"
        elif (telco["tenure_months"] >48) & (telco["tenure_months"] <=60) :
            return "4-5 Year"
        else:
            return "> 5 Year"

    telco["tenure_group"] = telco.apply(lambda telco: grouping_tenure(telco), axis = 1) 

    # Adjust category order
    tenure_group = ["< 1 Year", "1-2 Year", "2-4 Year", "4-5 Year", "> 5 Year"]
    telco["tenure_group"] = pd.Categorical(telco["tenure_group"], categories = tenure_group, ordered=True)
    
    return(telco)

def table_churn(data):
    table = pd.crosstab(
        data['churn_label'],
        columns = 'percent',
        normalize = True
    )*100

    return(table)

def plot_phone(data):
    
    # ---- Phone Service Customer
    _df=pd.crosstab(index=data['phone_service'], 
                columns=data['churn_label']
                )
            
    #_df
    ax = _df.plot(kind = 'barh', color=['#53a4b1','#c34454'], figsize = (8,6))

    # Plot Configuration
    #ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    plt.legend(['Retain', 'Churn'],fancybox=True,shadow=True)
    plt.axes().get_yaxis().set_label_text('')
    plt.title('Phone Service Customer')
    
    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png', transparent=True)
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_internet(data):

    # ---- Internet Service Customer
    _df2=pd.crosstab(index=data['internet_service'], 
                columns=data['churn_label'],
                normalize=True
            )*100
            
    _df2
    ax = _df2.plot(kind = 'barh', color=['#53a4b1','#c34454'], figsize = (8,6))

    # Plot Configuration
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    plt.legend(['Retain', 'Churn'],fancybox=True,shadow=True)
    plt.axes().get_yaxis().set_label_text('')
    plt.title('Internet Service Customer')

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_tenure_churn(data):
    
    # ---- Churn Rate by Tenure Group
    _df3=pd.crosstab(index=data['tenure_group'], 
                columns=data['churn_label'],
                normalize=True
            )*100
            

    ax = _df3.plot(kind = 'bar', color=['#53a4b1','#c34454'], figsize=(8, 6))

    # Plot Configuration
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.axes().get_xaxis().set_label_text('')
    plt.xticks(rotation = 360)
    plt.legend(['Retain', 'Churn'],fancybox=True,shadow=True)
    plt.title('Churn Rate by Tenure Group')

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_tenure_cltv(data):

    # ---- Average Lifetime Value by Tenure
    _df4=pd.crosstab(index=data['tenure_months'], 
                columns=data['churn_label'],
                values=data['cltv'],
                aggfunc='mean'
            )
            
    _df4

    ax = _df4.plot(color=['#333333','#b3b3b3'], figsize=(8, 6),style = '.--')

    # Plot Configuration
    plt.axes().get_xaxis().set_label_text('Tenure (in Months)')
    plt.title('Average Lifetime Value by Tenure')
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
    plt.xticks(rotation = 360)
    plt.legend(['Retain', 'Churn'],fancybox=True,shadow=True)

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_contract(data):

    # ---- count total churn by contract
    _df=pd.crosstab(index=data['contract'], 
                columns=data['churn_label'],

            )
            
  #  _df

    ax = _df.plot(kind = 'barh', color=['#53a4b1','#c34454'], figsize = (8,6))

    # Plot Configuration
    #ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    plt.legend(['Retain', 'Churn'],fancybox=True,shadow=True)
    plt.axes().get_xaxis().set_label_text('total customer')
    plt.axes().get_yaxis().set_label_text('contract')
    plt.title('Churn rate distribution by contract')
    
    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png', transparent=True)
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_contract_inetservices(data):

    # ---- count churn for each phone_service
    _df6=pd.crosstab(index=data['contract'], 
                columns=[data['churn_label'],data['internet_service']]
            )
            
  #  _df

    ax =_df6['Yes'].plot(kind='barh',stacked=True,figsize = (8,6)) 

    # Plot Configuration
    plt.axes().get_xaxis().set_label_text('total customer churn')
    plt.axes().get_yaxis().set_label_text('contract')
    plt.title('Churned Distribution by Internet Service vs Contract')
    
    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png', transparent=True)
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)