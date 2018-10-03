''' 
dict for regions, currently defined by lat(e/w) lon(s/n) borders.
llcrnrlon=12.2,llcrnrlat=67.6,urcrnrlon=13.2,urcrnrlat=67.9
Ultimately, a shape file would be preferred.
'''
regions_dict = {"Global":           {
                                    "llcrnrlon":-180,
                                    "llcrnrlat":-90,
                                    "urcrnrlon":180,
                                    "urcrnrlat":90
                                    },
                "ARCMFC":          {
                                    "boundinglat":50,
                                    },
                "Moskenes":         {
                                    "llcrnrlon":12.,
                                    "llcrnrlat":67.5,
                                    #"urcrnrlon":13.5,
                                    "urcrnrlon":14,
                                    #"urcrnrlat":68},
                                    "urcrnrlat":68.5
                                    },
                }
