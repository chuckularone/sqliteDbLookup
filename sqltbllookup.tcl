######################################################################
# Name:		sqltbllookup.tcl
# Purpose:	someaht akin to hcitbllookup
#
# UPoC type:	plain old tcl proc meant to be called elsewhere
# 
# Args: 	
#

#               
package require sqlite

proc sqltbllookup { tableName keyVal { sqlDBPath /path/to/database/clTables.db } { debug 0 } } {

# sqlite DBCMD /path/to/database/clTables.db;
sqlite DBCMD $sqlDBPath

if { $debug } { echo "key: $keyVal" } 
set query "select val from $tableName where name=\'$keyVal\'"
if { $debug } { echo "query: $query" } 
set rslts ""
set pfFlag  [ catch { DBCMD eval $query } rslts ] 
if { $pfFlag == "0" } {
   if { $debug } { echo "results: $rslts" } 
   return $rslts
} else {
   if { $debug } { echo "default" } 
   echo "sql error: $rslts"
   return ""
}

return ""
}
