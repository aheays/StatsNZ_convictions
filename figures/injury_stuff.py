from spectr.env import *

data = dataset.load('../data.psv')

plotting.presetRcParams(
    'article_double_column',
    top=0.78,
    left=0.11,
    wspace=0.2,
    hspace=0.4,
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

for offence in (
        'Acts Intended To Cause Injury',
        'Abduction, Harassment And Other Offences Against The Person',
        ):
        

    ax = subplot(ncolumns=2)
    for iregion,region in enumerate(regions):
        tdata = data.matches(region=region, normalisation='population adjusted', offence=offence,)
        ax.errorbar(
            tdata['year'],
            tdata['frequency']*1e5,
            tdata['frequency','unc']*1e5,
            # label=region,
            color=newcolor(iregion),
            linestyle=newlinestyle(iregion),
        )
        ax.set_title(tools.paginate_string(offence,40))
        ## for legend
        ax.plot([],[],label=region,
                linestyle=newlinestyle(iregion),
                color=newcolor(iregion))


for ax in fig.axes:
    ax.set_ylim(ymin=0)
    ax.set_xlim(data['year'].min(),data['year'].max())
    ax.set_xticks(np.arange(data['year'].min(),data['year'].max()+0.5,5))
    ax.set_xticks(np.arange(data['year'].min(),data['year'].max()+0.5,1),minor=True)
    ax.xaxis.set_ticklabels(ax.xaxis.get_ticklabels(),fontsize='small')
    plotting.rotate_tick_labels(x_or_y='x',rotation=25,ax=ax,horizontalalignment='center')
    ax.grid(True,which='major',axis='x',zorder=-5,color='gray')


supylabel('Convictions per 100$\,$000 population')
ax = fig.axes[0]
plotting.suplegend(ax=ax,loc='top',frame_on=False)
    
fig.savefig('injury_stuff.pdf')
fig.savefig('t.pdf')
    
