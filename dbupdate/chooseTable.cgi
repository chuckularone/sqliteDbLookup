#!/usr/bin/perl -w
use strict;
use warnings;
use CGI qw/:standard/;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use lib "/usr/local/cchs/perllib";
use BIF::sqlDo;

my $q = CGI->new;
my $dbName  = $q->param('dbName');
my $guidKey = $q->param('guidKey');

print $q->header;
print $q->start_html(
        -title   => 'Listing of table: $tblName',
        -author  => 'cmckenna@christianacare.org',
        -style   => {'src' => 'http://inet/InterfaceDIET/standard.css'},
    );

my $guidVal = sqlDo::getVal( "userGuids.db", "guidTbl", $guidKey );
if ($guidVal) {
	print "\n\n";
	print $q->h2 ("$guidVal is being logged as editing.");
    my @dumpVals = sqlDo::dumpDbTables($dbName);
	print $q->h2("Select Table");
	print $q->hr();
	
	print $q->start_form(
	   -action=>'http://qted/cgi-bin/dbupdate/tableList.cgi',
	   -method=>'POST',
	);
	
	
	print $q->hidden(
	      -name => 'dbName',
	      -default => [ $dbName ],
	);
	
	print $q->hidden(
	      -name      => 'guidKey',
	      -default   => $guidKey,
	);
	
	print $q->popup_menu(
	       -name => 'tblName',
	       -values =>\@dumpVals,
	 );
	
	
	print $q->br();
	print $q->br();
	
	print $q->submit(
	   -type=>'submit',
	   -name=>'Select table',
	);
	
	
	
	
	print $q->end_form;
	
} else {
    print $q->h2("Table selection unauthorized");
}

print br();
print br();
print $q->a( {-href=>"http://qted/cgi-bin/dbupdate/chooseDb.cgi?guidKey=$guidKey"}, "Top");
print $q->end_html;

exit 0;
