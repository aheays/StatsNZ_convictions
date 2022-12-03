from spectr.env import *

import xlrd
book = xlrd.open_workbook('Interview Task 2022.xls')
sheet = book.sheet_by_index(0)
years = [int(t.value) for i,t in enumerate(sheet.row(3)) if i > 0]

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
            normalisation='none',)

## add total offences neglecting traffic
tdata0,tdata1 = dataset.get_common(
    data.matches(offence='Total Offences'),
    data.matches(offence='Traffic And Vehicle Regulatory Offences'),
    keys=('year','region','normalisation')
)
tdata0['offence'] = 'Total Offences excluding Traffic and Vehicle'
tdata0['frequency'] -= tdata1['frequency']
data.concatenate(tdata0)

## resort offences according to reducing frequency in Total Regions
offences = data.unique('offence')
frequency = []
for offence in offences:
    i = data.match(offence=offence,region="Total Regions",normalisation='none')
    frequency.append(data['frequency',i].sum())
i = np.argsort(frequency)
offences = offences[i[::-1]]

## estimate uncertainites as a Poisson process
data['frequency','unc'] = 2*np.sqrt(data['frequency'])

# data.describe()

## load population data
data['population'] = np.nan

# ## regional populations
# tdata = sheet_to_dict('DPE389701_20221203_021116_0_mod.csv',comment='#')
# for region0,region1 in (
        # ("Auckland Region","Auckland Cluster"),
        # ("New Zealand","Total Regions"),
        # ):
    # for year,population in zip(tdata['year'],tdata[region0]):
        # i = data.match(year=year,region=region1)
        # data['population',i] = population

# ## territorial authorities population
# tdata = sheet_to_dict('DPE389801_20221203_024200_39_mod.csv',comment='#')
# for region0,region1 in (
        # ("Auckland","Auckland Cluster"),
        # ("New Zealand","Total Regions"),
        # ):
    # for year,population in zip(tdata['year'],tdata[region0]):
        # i = data.match(year=year,region=region1)
        # data['population',i] = population

## defacto national population https://figure.nz/chart/MFMkVhvbhuVFbiWr
tdata = Dataset()
tdata.load('./Population_Estimated_population_by_year_ended_June_19372022_mod.csv')
tdata.limit_to_match({'Measure':'Estimated population','Unit':'Total',})
for year,population in zip(tdata['Year ended June'],tdata['Value']):
    i = data.match(year=year,region="Total Regions")
    data['population',i] = population

## get ex-Auckland region
t_total = data.matches(region="Total Regions")
t_auckland = data.matches(region="Auckland Cluster")
t_auckland,t_total = dataset.get_common(t_auckland,t_total,keys=('year','offence'))
t_ex_auckland = t_auckland.copy()
for key in ('frequency','population',):
    t_ex_auckland[key] = t_total[key] - t_auckland[key]
t_ex_auckland['region'] = "Total Excluding Auckland Cluster"
data.concatenate(t_ex_auckland)    

## normalise offence frequencies to their all-time mean frequency
tdata = data.matches(normalisation='none').copy()
for match_keys,i in tdata.unique_dicts_match('region','offence'):
    tdata['frequency',i] /= np.mean(tdata['frequency',i])
    tdata['frequency','unc',i] /= np.mean(tdata['frequency','unc',i])
tdata['normalisation'] =  'offence mean over time'
data.concatenate(tdata)

## normalise offense frequencies to the all-time all-offence mean
## frequency
tdata = data.matches(normalisation='none').copy()
for match_keys,i in tdata.unique_dicts_match('region','year'):
    total_offences = tdata.unique_value('frequency',offence='Total Offences',**match_keys)
    tdata['frequency',i] /= total_offences
    tdata['frequency','unc',i] /= total_offences
tdata['normalisation'] = 'total offences'
data.concatenate(tdata)

## normalise offense frequencies to population
tdata = data.matches(normalisation='none').copy()
for match_keys,i in tdata.unique_dicts_match('region'):
    tdata['frequency',i] /= tdata['population',i]
    tdata['frequency','unc',i] /= tdata['population',i]
tdata['normalisation'] = 'population'
data.concatenate(tdata)

# ## normalise offense frequencies to national population, total offence
# ## for Auckland
# tdata = data.matches(normalisation='none').copy()
# for region in tdata.unique('region'):
#     for year in tdata.unique('year'):
#         i = tdata.match(year=year,region=region)
#         if region == "Total Regions":
#             normalisation = tdata.unique_value('population',year=year,region="Total Regions",offence='Total Offences')
#         else:
#             normalisation = (tdata.unique_value('population',year=year,region="Total Regions",offence='Total Offences')
#                              * tdata.unique_value('frequency',year=year,region=region,offence='Total Offences')
#                              / tdata.unique_value('frequency',year=year,region="Total Regions",offence='Total Offences') )
#         tdata['frequency',i] /= normalisation
#         tdata['frequency','unc',i] /= normalisation
# tdata['normalisation'] = 'population adjusted'
# data.concatenate(tdata)

## normalise offense frequencies to national population, total offence
## for Auckland
tdata = data.matches(normalisation='none').copy()
for region in tdata.unique('region'):
    for year in tdata.unique('year'):
        i = tdata.match(year=year,region=region)
        normalisation = tdata.unique_value(
            'population',
            year=year,
            region="Total Regions",
            offence='Total Offences')
        if region == 'Auckland Cluster':
            normalisation *= 0.19
        elif region == "Total Excluding Auckland Cluster":
            normalisation *= 1-0.19
        tdata['frequency',i] /= normalisation
        tdata['frequency','unc',i] /= normalisation
tdata['normalisation'] = 'population adjusted'
data.concatenate(tdata)

normalisation = (
    'none',
    # 'offence mean over time',
    # 'total offences',
    # 'population',
    'population adjusted',
    )

region = (
    "Total Regions",
    "Total Excluding Auckland Cluster",
    "Auckland Cluster",
)

for ifig,normalisationi in enumerate(normalisation):
    fig = qfig(ifig)

    suptitle(f'Data normalisation: {normalisationi}')
    for iax,offence in enumerate(offences):
        tdata = data.matches(
            normalisation=normalisationi,
            region=region,
            offence=offence,
        )

        tdata.plot(
            ax=subplot(iax),
            xkeys='year',
            ykeys='frequency',
            # title=title['offence'],
            zkeys=('region',),
            # legend=False,
            legend=(iax==0),
            plot_ylabel=False,
            plot_xlabel=False,
            markersize=2,
        )
        ax = gca()
        ax.set_ylim(ymin=0)
        ## title
        title = offence
        for i,c in enumerate(title):
            if i>30 and c==' ':
                title = title[:i]+'\n'+title[i+1:]
                break
        ax.set_title(title,fontsize=10)
        ## legend
        # plotting.suplegend(loc='below')

        # ax.set_xlim(1997,2013)      #  DEBUG
        # if iax>=2: break            #  DEBUG

## plot population
qfig(3)
t0,t1 = dataset.get_common(
    data.matches(region='Total Regions',normalisation='none',offence='Total Offences'),
    data.matches(region="Auckland Cluster",normalisation='none',offence='Total Offences'),
    keys='year')
plot(t0['year'],t1['frequency']/t0['frequency'])
print( np.mean(t1['frequency']/t0['frequency']))

# ylim(ymin=0)

    # "Total Regions",
    # "Total Excluding Auckland Cluster",
    # "Auckland Cluster",
