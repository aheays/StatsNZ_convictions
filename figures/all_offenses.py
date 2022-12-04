from spectr.env import *

data = dataset.load('../data.psv')

plotting.presetRcParams(
    'article_double_column_full_page',
    wspace=0.2,
    hspace=0.5,
    top=0.92,
)
plotting.set_rcparam({
    'lines.linewidth':2,
})

offences = [
    'Total Offences',
    # 'Total Offences excluding Traffic and Vehicle',
    'Traffic And Vehicle Regulatory Offences',
    'Dangerous Or Negligent Acts Endangering Persons',
    'Offences Against Justice Procedures, Government Security And Government Operations',
    'Theft And Related Offences',
    'Acts Intended To Cause Injury',
    'Public Order Offences',
    'Illicit Drug Offences',
    'Fraud, Deception And Related Offences',
    'Unlawful Entry With Intent/Burglary, Break And Enter',
    'Miscellaneous Offences',
    'Property Damage And Environmental Pollution',
    'Prohibited And Regulated Weapons And Explosives Offences',
    'Sexual Assault And Related Offences',
    'Abduction, Harassment And Other Offences Against The Person',
    'Robbery, Extortion And Related Offences',
    'Homicide And Related Offences',
]

offences = [
    offences[:9],
    offences[9:],
    ]

for normalisation,ylabel,renormalisation in (
        ('none','Annual number of convictions (1000s)',1/1000),
        ('population adjusted','Annual convictions per 100$\,$000 population',100000),
):

    for ifig,offencesi in enumerate(offences):

        fig = plt.figure()
        for offence in offencesi:
            ax = subplot(ncolumns=2,nrows=5)
            for iregion,region in enumerate([
                    # 'Total Regions',
                    'Total Excluding Auckland Cluster',
                    'Auckland Cluster',
            ]):
                tdata = data.matches(region=region, normalisation=normalisation, offence=offence,)
                ax.errorbar(
                    tdata['year'],
                    tdata['frequency']*renormalisation,
                    tdata['frequency','unc']*renormalisation,
                    color=newcolor(iregion),
                )
                ax.set_title(
                    tools.paginate_string(offence,50),
                    fontsize='small',
                )
                ## for legend
                ax.plot([],[],label=region,color=newcolor(iregion),)


        for ax in fig.axes:
            ax.set_ylim(ymin=0,ymax=ax.get_ylim()[1])
            ax.set_xlim(data['year'].min(),data['year'].max())
            ax.set_xticks(np.arange(data['year'].min(),data['year'].max()+0.5,5))
            ax.set_xticks(np.arange(data['year'].min(),data['year'].max()+0.5,1),minor=True)
            plotting.rotate_tick_labels(x_or_y='x',rotation=10,ax=ax,horizontalalignment='center')
            ax.grid(True,which='major',axis='x',zorder=-5,color='gray',alpha=0.5),

        plotting.supylabel(ylabel),

        plotting.suplegend(ax=fig.axes[0],loc='top',frame_on=False)
        fig.savefig(f'all_offenses_normalisation_{normalisation}_{ifig}.pdf')

        # break                   #  DEBUG
    # break                       #  DEBUG

fig.savefig('t.pdf')



