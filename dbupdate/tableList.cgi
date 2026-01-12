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
my $dbName  = $q->param('dbName');
my $tblName = $q->param('tblName');
my $guidKey = $q->param('guidKey');

my $JSCRIPT=<<THEEND;
function toggleMe(a){
  var e=document.getElementById(a);
  if(!e)return true;
  if(e.style.display=="none"){
    e.style.display="block"
  } else {
    e.style.display="none"
  }
  return true;
}
THEEND
# Header
print $q->header;
print $q->start_html(
        -title   => 'Table editing/viewing',
        -author  => 'cmckenna@christianacare.org',
        -style   => {'src' => 'http://inet/InterfaceDIET/standard.css'},
        -script=>$JSCRIPT);                       
# Body
my $guidVal = sqlDo::getVal( "$dbLoc/userGuids.db", "guidTbl", $guidKey );
if ($guidVal) {
	print "\n\n";
	print $q->h2 ("$guidVal is being logged as editing.");
	print $q->h2 ("Click button to toggle view of - $tblName");
	# Set up table start
	print "<input type=\"button\" class=\"button\" onclick=\"return toggleMe('para1')\" value=\"Show/Hide Table\">";
	print "<div id=\"para1\" style=\"display:none\">";
	print "<table border=\"1\" cellpadding=\"5\">\n";
	print "<tr><td>Name</td><td>Val</td><td>Comment</td></tr> \n"; 
	# Build table
	my @dumpit = sqlDo::returnThree("$dbLoc/$dbName", $tblName);
	my @valList, my $line, my $item;
	foreach $line (@dumpit) {
		@valList = split /\|/, $line;
		print "<tr><td>@valList[0]</td><td>@valList[1]</td><td>@valList[2]</td></tr> \n"; 
	}	
	print "</table>\n";
	print "</div>";
	print "\n\n";
	# Horizontal Line
	print hr();
	print $q->h1("Delete");
	print $q->h2("Enter item name to be removed from table");
	print $q->start_form(
	   -action=>'http://qted/cgi-bin/dbupdate/deleteRecord.cgi',
	   -method=>'POST',
	);
	print "<table><tr><td>Name</td></tr><tr><td>";
		print $q->textfield(
		    -name      => 'colName',
		    -value     => '',
		    -size      => 20,
		    -maxlength => 50,
		);
	    print $q->hidden(
	        -name      => 'dbName',
	        -default   => $dbName,
	    );
	    print $q->hidden(
	        -name      => 'tblName',
	        -default   => $tblName,
	    );
	    print $q->hidden(
	        -name      => 'guidKey',
	        -default   => $guidKey,
	    );
	print "</td></tr><tr><td>";
	    
	print $q->br();
	print $q->br();
	
	print $q->submit(
	   -type=>'submit',
	   -name=>'Delete Record',
	);
	
	print "</td></tr></table>";
	print $q->end_form;
	
	print hr();
	print $q->h1("Add");
	print $q->h2("Values to be ADDED to table");
	print $q->start_form(
	   -action=>'http://qted/cgi-bin/dbupdate/addRecord.cgi',
	   -method=>'POST',
	);
	print "<table><tr><td>Name</td><td>Value</td><td>Comment</td></tr><tr><td>";
		print $q->textfield(
		    -name      => 'colName',
		    -value     => '',   
		    -size      => 20,
		    -maxlength => 35,
		);
	print "</td><td>";
		print $q->textfield(
		    -name      => 'colVal',
		    -value     => '',
		    -size      => 10,
		    -maxlength => 30,
		);
	print "</td><td>";
		print $q->textfield(
		    -name      => 'colComm',
		    -value     => '',
		    -size      => 35,
		    -maxlength => 100,
		);
	    print $q->hidden(
	        -name      => 'dbName',
	        -default   => $dbName,
	    );
	    print $q->hidden(
	        -name      => 'tblName',
	        -default   => $tblName,
	    );
	    print $q->hidden(
	       -name      => 'guidKey',
	       -default   => $guidKey,
	    );
	print "</td></tr><tr><td>";
	print $q->br();
	print $q->br();
	print $q->submit(
	   -type=>'submit',
	   -name=>'Add Record',
	);
	print "</td><td>&nbsp;</td><td>&nbsp;</td></tr></table>";
	print $q->end_form;
	
	print hr();
	print $q->h1("Modify");
	print $q->h2("Enter Name and Value to be modified.");
	print $q->start_form(
	   -action=>'http://qted/cgi-bin/dbupdate/modRecord.cgi',
	   -method=>'POST',
	);
	print "<table><tr><td>Name</td><td>Value</td><td>Comment</td></tr><tr><td>";
		print $q->textfield(
		    -name      => 'colName',
		    -value     => '',   
		    -size      => 20,
		    -maxlength => 35,
		);
	print "</td><td>";
		print $q->textfield(
		    -name      => 'colVal',
		    -value     => '',
		    -size      => 10,
		    -maxlength => 30,
		);
	print "</td><td>";
		print $q->textfield(
		    -name      => 'colComm',
		    -value     => '',
		    -size      => 35,
		    -maxlength => 100,
		);
	    print $q->hidden(
	        -name      => 'dbName',
	        -default   => $dbName,
	    );
	    print $q->hidden(
	        -name      => 'tblName',
	        -default   => $tblName,
	    );
	    print $q->hidden(
	        -name      => 'guidKey',
	        -default   => $guidKey,
	    );
	print "</td></tr><tr><td>";
	print $q->br();
	print $q->br();
	print $q->submit(
	   -type=>'submit',
	   -name=>'Add Record',
	);
	print "</td><td>&nbsp;</td><td>&nbsp;</td></tr></table>";
	print $q->end_form;
} else {
print $q->h1("You are not authorized to edit $tblName.");
}
print br();
print br();
print $q->a( {-href=>"http://qted/cgi-bin/dbupdate/chooseDb.cgi?guidKey=$guidKey"}, "Top");
print end_html;

