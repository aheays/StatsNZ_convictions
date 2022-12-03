from spectr.env import *

import xlrd
book = xlrd.open_workbook('Interview Task 2022.xls')
sheet = book.sheet_by_index(0)
years = [int(t.value) for i,t in enumerate(sheet.row(3)) if i > 0]
offences = [str(sheet.row(i)[0].value) for i in range(4,sheet.nrows-1)]

data = Dataset()
for irow in range(4,sheet.nrows-1):
    row = sheet.row(irow)
    for icell,(year,frequency) in enumerate(zip(years,row[1:])):
        offence = str(row[0].value)
        if icell <= len(years)/2-1:
            region = "Total Regions"
        else:
            region = "Auckland Cluster"
        data.append(
            region=region,
            year=year,
            offence=offence,
            frequency=float(frequency.value),
            normalisation='none',
        )

# data.describe()



## get ex-Auckland region
t_total = data.matches(region="Total Regions")
t_auckland = data.matches(region="Auckland Cluster")
t_auckland,t_total = dataset.get_common(t_auckland,t_total,keys=('year','offence'))
t_ex_auckland = t_auckland.copy()
t_ex_auckland['frequency'] = t_total['frequency'] - t_auckland['frequency']
t_ex_auckland['region'] = "Total Excluding Auckland Cluster"
data.concatenate(t_ex_auckland)    

## normalise offence frequencies to their all-time mean frequency
tdata = data.matches(normalisation='none').copy()
for match_keys,i in tdata.unique_dicts_match('region','offence'):
    tdata['frequency',i] /= np.mean(tdata['frequency',i])
tdata['normalisation'] =  'offence mean over time'
data.concatenate(tdata)

## normalise offense frequencies to the all-time all-offence mean
## frequency
tdata = data.matches(normalisation='none').copy()
for match_keys,i in tdata.unique_dicts_match('region','year'):
    total_offences = tdata.unique_value('frequency',offence='Total Offences',**match_keys)
    tdata['frequency',i] /= total_offences
tdata['normalisation'] = 'total offences'
data.concatenate(tdata)

# normalisation = 'none'
# normalisation = 'offence mean over time'
normalisation = 'total offences'
region = (
    # "Total Regions",
    "Total Excluding Auckland Cluster",
    "Auckland Cluster",
)

fig = qfig(0)
suptitle(f'Data normalisation: {normalisation}')
tdata = data.matches(
    normalisation=normalisation,
    region=region,
)
for iax,(tdict,tdata) in enumerate(tdata.unique_dicts_matches('offence')):
    tdata.plot(
        ax=subplot(iax),
        xkeys='year',
        ykeys='frequency',
        # title=title['offence'],
        zkeys=('region',),
        legend=False,
        plot_ylabel=False,
        plot_xlabel=False,
        markersize=2,
    )
    ax = gca()
    ax.set_ylim(ymin=0)
    ## title
    title = tdict['offence']
    for i,c in enumerate(title):
        if i>30 and c==' ':
            title = title[:i]+'\n'+title[i+1:]
            break
    ax.set_title(title,fontsize=10)
    ## legend
    plotting.suplegend(loc='below')


    # if iax>=2: break            #  DEBUG
        
