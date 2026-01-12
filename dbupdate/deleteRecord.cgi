#!/usr/bin/perl -w

use strict;
use warnings;
use CGI qw/:standard/;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use lib "/usr/local/cchs/perllib";
use BIF::sqlDo;
use BIF::bifFile;

my $dbLoc = bifFile::slurp("dbLoc.dat");
my $q = CGI->new;

my $colName = $q->param('colName');
my $dbName  = $q->param('dbName');
my $tblName = $q->param('tblName');
my $guidKey = $q->param('guidKey');

print $q->header;
print $q->start_html(
        -title   => 'Record Deleted',
        -author  => 'cmckenna@christianacare.org',
        -style   => {'src' => 'http://inet/InterfaceDIET/standard.css'},
    );

my $guidVal = sqlDo::getVal( "$dbLoc/userGuids.db", "guidTbl", $guidKey );
print $q->h2("colName: $colName");
print $q->h2("dbName: $dbName");
print $q->h2("tblName: $tblName");
print $q->h2("User Logged: $guidVal");
print $q->h2("guidKey: $guidKey");
print $q->br();

my $dumpVals = sqlDo::deleteItem("$dbLoc/$dbName", $tblName, $colName);
print $dumpVals;
print br();
print br();
print $q->a( {-href=>"http://qted/cgi-bin/dbupdate/tableList.cgi?dbName=$dbName&tblName=$tblName&guidKey=$guidKey"}, "Back to editing");
print br();
print $q->a( {-href=>"http://qted/cgi-bin/dbupdate/chooseDb.cgi?guidKey=$guidKey"}, "Top");

print $q->end_html;

# Log edit. 
my @dtg = bifFile::nowTime();
my $logPath = "$dbLoc/logs/";
my $logFile = "$dbName.$dtg[0].log";
bifFile::logWrite("$logPath$logFile", $dumpVals, $guidVal);

exit 0;
