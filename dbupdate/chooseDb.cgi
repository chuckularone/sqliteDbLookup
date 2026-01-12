#!/usr/bin/perl -w
use strict;
use warnings;
use CGI qw/:standard/;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use lib "/usr/local/cchs/perllib";
use BIF::sqlDo;

##############################################
# Extract list of databases from dblist file #
#
my @dblist;
open FILE, "./dblist" or die "Couldn't open: $!";
while (<FILE>) {
	chomp $_;
	push @dblist, $_;
}
close FILE;

#    
# New instance and headers for CGI.
#
my $q = CGI->new;
my $guidKey = $q->param('guidKey');

print $q->header;
print $q->start_html(
        -title   => 'Listing of table: $tblName',
        -author  => 'cmckenna@christianacare.org',
        -style   => {'src' => 'http://inet/InterfaceDIET/standard.css'},
    );

#
# Begin output to screen to select database
#
my $guidVal = sqlDo::getVal( "userGuids.db", "guidTbl", $guidKey );
if ($guidVal) {
	print "\n\n";
	print $q->h2 ("$guidVal is being logged as editing.");
	print $q->h2("Select DB");
	print $q->hr();
	
	print $q->start_form(
	   -action=>'./chooseTable.cgi',
	   -method=>'POST',
	);
	
	#
	# List of database names in pull down box
	#
	print $q->popup_menu(
	      -name => 'dbName',
	      -values => [ @dblist ],
	);
    print $q->hidden(
	      -name      => 'guidKey',
	      -default   => $guidKey,
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
print $q->end_html;

exit 0;
