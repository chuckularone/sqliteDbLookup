######################################################################
# Name:         xltpSqLiteReturnVal
# Purpose:      Returns a value from a SQLite table
# UPoC type:    xltp
# Args:         database(site) tableName getValueForName
# Notes:        All data is presented through special variables.  The initial
#               upvar in this proc provides access to the required variables.
#
#               This proc style only works when called from a code fragment
#               within an XLT.
#

proc xltpSqLiteReturnVal {} {
    upvar xlateId       xlateId         \
          xlateInList   xlateInList     \
          xlateInTypes  xlateInTypes    \
          xlateInVals   xlateInVals     \
          xlateOutList  xlateOutList    \
          xlateOutTypes xlateOutTypes   \
          xlateOutVals  xlateOutVals

set dbName  [lindex $xlateInVals 0]
set dbTable [lindex $xlateInVals 1]
set dbVal   [lindex $xlateInVals 2]

if { [ string length $dbName ] = 0 } {
      set xlateOutVals [ list "no Name" ERR ] 
   } else {
      package require sqlite
      set dbName "/sitesdevl/sqlite/$dbName"
      sqlite DBCMD $dbName;           # open database

      set query {select val from $dbTable where name='$dbVal'}
      set rslts [DBCMD eval $query]

      set out "$rslts"
      set xlateOutVals [ list "$out" OK ] 
   }

   # function end 

}


