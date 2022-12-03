from spectr.env import *

data = dataset.load('../data.psv')

plotting.presetRcParams(
    'article_double_column',
    top=0.80,
    left=0.08,
    wspace=0.25,
)
plotting.set_rcparam({
    'lines.linewidth':2,
})

regions = [
        'Auckland Cluster',
        'Total Excluding Auckland Cluster',
        # 'Total Regions',
]

fig = plt.figure()

ax = subplot()
for iregion,region in enumerate(regions):
    tdata = data.matches(region=region, normalisation='none', offence='Total Offences excluding Traffic and Vehicle',)
    ax.plot(
        tdata['year'],
        tdata['frequency']/1e3,
        label=region,
        linestyle=newlinestyle(iregion),
    )
    ax.set_title('Number of convictions (1000s)')

ax = subplot()
for iregion,region in enumerate(regions):
    tdata = data.matches(region=region, normalisation='population adjusted', offence='Total Offences excluding Traffic and Vehicle',)
    ax.plot(
        tdata['year'],
        tdata['frequency']*1e5,
        label=region,
        linestyle=newlinestyle(iregion),
    )
    ax.set_title('Convictions per 100$\,$000 population')

    ## linear fit
    # i = (tdata['year']>=1980)&(tdata['year']<=1995)
    # p = np.polyfit(tdata['year'][i],tdata['frequency'][i]*1e5,1)
    # ax.plot(
        # tdata['year'],
        # np.polyval(p,tdata['year'],)
        # )



for ax in fig.axes:
    ax.set_ylim(ymin=0)
    ax.set_xlim(data['year'].min(),data['year'].max())
    ax.set_xticks(np.arange(data['year'].min(),data['year'].max()+0.5,5))
    ax.set_xticks(np.arange(data['year'].min(),data['year'].max()+0.5,1),minor=True)
    plotting.rotate_tick_labels(x_or_y='x',rotation=70,ax=ax,horizontalalignment='center')
    ax.grid(True,which='major',axis='x',zorder=-5,color='gray')


ax = fig.axes[-1]
plotting.suplegend(ax=ax,loc='top',frame_on=False)
    
fig.savefig('total_offenses_except_traffic.pdf')
fig.savefig('t.pdf')
    
