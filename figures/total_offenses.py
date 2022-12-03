from spectr.env import *

data = dataset.load('../data.psv')

plotting.presetRcParams(
    'article_double_column',
    top=0.85,
)
plotting.set_rcparam({
    'lines.linewidth':2,
})

fig = plt.figure()
ax = subplot()
for iregion,region in enumerate([
        # 'Total Regions',
        'Total Excluding Auckland Cluster',
        'Auckland Cluster',
]):
    tdata = data.matches(region=region, normalisation='none', offence='Total Offences',)
    ax.plot(
        tdata['year'],
        tdata['frequency']/1e3,
        label=region,
    )
    ax.set_ylabel('Number of convictions (1000s)')

ax = subplot()
for region in [
        # 'Total Regions',
        'Total Excluding Auckland Cluster',
        'Auckland Cluster',
]:
    tdata = data.matches(region=region, normalisation='population adjusted', offence='Total Offences',)
    ax.plot(
        tdata['year'],
        tdata['frequency']*1e5,
        label=region,)
    ax.set_ylabel('Convictions per 100$\,$000 population')

for ax in fig.axes:
    ax.set_ylim(ymin=0)
    ax.set_xlim(data['year'].min(),data['year'].max())
    ax.set_xticks(np.arange(data['year'].min(),data['year'].max()+0.5,5))
    ax.set_xticks(np.arange(data['year'].min(),data['year'].max()+0.5,1),minor=True)
    plotting.rotate_tick_labels(x_or_y='x',rotation=70,ax=ax,horizontalalignment='center')
    ax.grid(True,which='major',axis='x',zorder=-5,color='gray')


ax = fig.axes[-1]
plotting.suplegend(ax=ax,loc='top',frame_on=False)
    
# fig.savefig('total_offenses.pdf')
fig.savefig('t.pdf')
    
