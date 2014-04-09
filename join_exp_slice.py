import os
import glob

def join_exp_slice( filenames , modelnames ):
    """
    Do a concatenation of multiple time-slice CMIP type nc files using CDO, and do a smart naming of the output (give the correct year-range in the output file name) and remove the mess (input files). Should be made more general.
    """ 

    for mod in modelnames:
       modfilesall = [ filename for filename in filenames if filename.split( '_' )[2] == mod ]
       ensmembersall = [ modfile.split('_')[4] for modfile in modfilesall ]
       uniq_ensmems = sorted( set( ensmembersall ) )
       
       for ensmem in uniq_ensmems:
               modfiles = [ modfilename for modfilename in modfilesall if 
                            modfilename.split( '_' )[4] == ensmem ]

	       start_dates = [ int( cfile.split( '_' )[5].split('-')[0]) 
		               for cfile in modfiles ]
	       end_dates = [ int( cfile.split( '_' )[5].split('-')[1].split('.')[0] )
		             for cfile in modfiles ]

	       start_date = min( start_dates)
	       end_date = max( end_dates )

	       varname = modfiles[0].split('_')[0]
	       realm = modfiles[0].split('_')[1]
	       ensmember = modfiles[0].split('_')[4]
	       exp = modfiles[0].split('_')[3]

	       print 
	       print mod, ensmem, start_date , end_date, len( modfiles)
	       if len( modfiles ) > 1:
		  print "joining... "
                  infiles = ' '.join( modfiles )
		  catstring = 'cdo cat ' + infiles + ' ' + varname + '_' + realm + '_'+ mod + '_' + exp + '_' + ensmember + '_' + str(start_date ) + '-' + str( end_date ) + '.nc'			
		  os.system( catstring )
		  for cfile in modfiles:
		      delstr = 'rm ' + cfile
		      os.system( delstr ) 


def match_exp( filenames , modelnames, rcpname='rcp45' ):
    """
    Do a concatenation of multiple time-slice CMIP type nc files using CDO, and do a smart naming of the output (give the correct year-range in the output file name) and remove the mess (input files). Should be made more general.
    """

    for mod in modelnames:
       print "cmipdata.match_exp: Model ", mod 
       modfilesall = [ filename for filename in filenames if filename.split( '_' )[2] == mod ]

       modfiles_historical = [ filename for filename in modfilesall if filename.split( '_' )[3] == 'historical' ]
       ensmembers_hist = [ modfile.split('_')[4] for modfile in modfiles_historical ]
       uniq_ensmems_hist = sorted( set( ensmembers_hist ) )

       modfiles_rcp = [ filename for filename in modfilesall if filename.split( '_' )[3] == rcpname ]
       ensmembers_rcp = [ modfile.split('_')[4] for modfile in modfiles_rcp ]
       uniq_ensmems_rcp = sorted( set( ensmembers_rcp ) )

       for ensmem in uniq_ensmems_hist:
               modfiles = [ modfilename for modfilename in modfilesall if
                            modfilename.split( '_' )[4] == ensmem ]

               if any( ensmem in s for s in uniq_ensmems_rcp):
                   print "Historical - RCP match for: ", ensmem
               else:
                   print " NO match for: ", ensmem, "...deleting"
                   for cfile in modfiles:
                       delstr = 'rm ' + cfile
                       os.system(delstr)
       print 
