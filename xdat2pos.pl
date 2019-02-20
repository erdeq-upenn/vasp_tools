eval '(exit $?0)' && eval 'exec perl -S $0 ${1+"$@"}' && eval 'exec perl -S $0 $argv:q' if 0;
#;-*- Perl -*-

  use Cwd;
  use FindBin qw($Bin);
  use lib "$Bin";

  @ARGV>1 || die "usage:\nxdat2pos.pl <0> <start step> <end step>\nxdat2pos.pl <1> <certain step number>\n";
  if(@ARGV[0]==0&&@ARGV<3){die "usage: xdat2pos.pl <0> <start step> <end step>\n"};
  if(@ARGV > 3) {$quadruple=$ARGV[3];}
  else{$quadruple=0;}
  # Get the length of the XDATCAR file. This is bad but works for now !!!
    open TMP , "XDATCAR" ;
    $nl = 0 ;
    while(<TMP>){$nl++ ;}
    close TMP ;


  if(@ARGV[0]==0){
        $NumStep= @ARGV[2]-@ARGV[1]+1;
        bunchpos($NumStep); 
        makemovie($NumStep,$quadruple);
  }
  if(@ARGV[0]==1){$step=@ARGV[1];onepos($step)};

#make a movie of the selected steps
sub makemovie{
  my ($NumStep, $quadruple)=@_;
  my ( $VTST_BC, $scount, $poscar, $i, $j, $confile, $xyzfile, $movie,$amy);
  $movie="movie.xyz";
  if($quadruple){$movie="movie4.xyz";}
  if(-e $movie){unlink $movie;}
  for($i=0;$i<$NumStep;$i++){
    $scount=$ARGV[1]+$i;
    $poscar="POSCAR".$scount.".out";
    $confile=$poscar.".con";
    $xyzfile=$poscar.".xyz";
    if(!$quadruple){
       $j=`$Bin/vasp2con.pl $poscar; $Bin/con2xyz.pl $confile`;
    }else{
      $VTST_BC=$ENV{'VTST_BC'};
      $ENV{'VTST_BC'}="none";
      $amy=`$Bin/quad.pl $poscar out; $Bin/vasp2con.pl out; mv out.con st4.con`; 
      $ENV{'VTST_BC'}=$VTST_BC; 
      $amy=`$Bin/quad_con.pl st4.con out4.con; $Bin/vasp2con.pl out4.con; $Bin/vasp2con.pl out4;$Bin/vasp2con.pl out4.con; $Bin/vasp2con.pl out4;mv out4.con st4.con; rm -f out out4; $Bin/con2xyz.pl st4.con; rm -f st4.con; mv st4.xyz $xyzfile`; 
    }
    if($i==0){$amy=`cat $xyzfile > $movie`;}
    else{$amy=`cat $xyzfile >> $movie`;}
    unlink $confile, $xyzfile;
  }
}

# Subroutine to get a series of steps from XDATCAR
  sub bunchpos{
   my $NumStep=shift;
   my $scount=0;
 # Set selected steps
    for($scount=0; $scount<$NumStep; $scount++){
        $Step[$scount]=@ARGV[1]+$scount;
        onepos($Step[$scount]);
        }
  }
# End of subroutin bunchpos

# Subroutine to get one step from XDATCAR
  sub onepos{
    my ($step)=@_;
    # Get information about, number and types of atoms, box lengths ets.
    # from the POSCAR file and write out to the output POSCAR file
    open POS , "POSCAR" or die " NO POSCAR IN THIS DIRECTORY \n";
    $outfile="POSCAR".$step.".out";
    open(OUT,">$outfile");

    for($i=0; $i<8; $i++){
      $pos = <POS> ; print OUT $pos ;
      chomp($pos) ; $pos=~s/^\s+//g ; @pos=split /\s+/,$pos ;
      if($i == 0){
        @elements = split /\s+/ , $pos ;
        $nel = @elements ;
      }

#      if($i == 5){
#        @not[0..$nel-1] = @pos[0..$nel-1] ;
#        while($not[$k] != undef){$natoms+=$not[$k++] ;} 
#      }
#    }

      if($i == 5){
        if($pos[0]=~ /^\d+$/){
          @not[0..$nel-1] = @pos[0..$nel-1] ;
            while($not[$k] != undef){$natoms+=$not[$k++] ;}   # Calculate the number of atoms
        ;}
        else{
          $atomtypeflag= 1; #check for vasp5 style POSCAR
          @elements = split /\s+/ , $pos ;
          $nel = @elements ;
        }
      }
      if($i == 6){
        if($atomtypeflag== 1){
          @not[0..$nel-1] = @pos[0..$nel-1] ;
          while($not[$k] != undef){$natoms+=$not[$k++] ;}   # Calculate the number of atoms
        ;}
      }
    }

    $pos = undef ;
    for($i=0; $i<$natoms; $i++){$pos .= <POS> ;}
    close POS ;
    @pos = split /\n/ , $pos ;

  # Get the right step from the XDATCAR
    open XDAT , "XDATCAR" or die " NO XDATCAR IN THIS DIRECTORY \n";
    $a = $step;
    if($atomtypeflag== 1){
      $st = 5+($natoms+1)*($a-1) ;}
    else{
      $st = 6+($natoms+1)*($a-1) ;}
    $fn = $st+$natoms ;  

    die "THE SEARCH IS OUT OF BOUNDS\n" if($st > $nl || $fn > $nl) ;

    for($i=0; $i<$st-1; $i++){$in = <XDAT> ;}
    $in = <XDAT> ;
    $j = 0 ; 
    for($i=$st+1; $i<=$fn; $i++){
      $in = <XDAT> ;
      if($in == undef){print $i," hallo\n" ;}
      chomp($in) ; $in=~s/^\s+//g ; @in=split /\s+/,$in ;
      $p = $pos[$j] ;
      $j++ ;
      chomp($p) ; $p=~s/^\s+//g ; @p=split /\s+/,$p ;
      printf OUT "%15.10f %15.10f %15.10f %5s %5s %5s \n",$in[0],$in[1],$in[2],$p[3],$p[4],$p[5] ;
#    $IN = <STDIN> ;
    }
  close OUT ;
  close XDAT ;
# End of subroutin onepos
  }


## Assign a type (element) to each atom.
#
#  $n = 0 ;
#  $j = 0 ;
#  for($i=1; $i<=$natoms; $i++){ 
#    $j++ ;
#    if($j <= $not[$n]){$type[$i-1] = $elements[$n] ;}
#    else{$n++ ; $type[$i-1] = $elements[$n] ; $j = 1 ;}  
##    print $i,"  ",$j,"  ",$type[$i-1];
##    $IN = <STDIN> ;
#  }
# 
## Read the XDAT file and make .xyz files
#
#  for($i=0; $i<5; $i++){$line = <XDAT> ; }                # Jump over the first few lines
#  $n=0 ;  
#  open MOV, ">movie.xyz" ;
#  while($line = <XDAT>){
#    chomp($line) ;
#    print MOV $natoms,"\n" ;
#    $f = $forces[$n] ; chomp($f) ; $f=~s/^\s+//g ; @f=split /\s+/,$f ;
#    $e = $energy[$n] ; chomp($e) ; $e=~s/^\s+//g ; @e=split /\s+/,$e ;
#    print MOV "FORCE:  $f[4]  ...  ENERGY:  $e[6]","\n" ;
#    for($i=0; $i<$natoms; $i++){
#      $line = <XDAT> ;
#      chomp($line) ; $line=~s/^\s+//g ; @line=split /\s+/,$line ;
##  Transform from direct coordinates to cart. coordinates.
#      $x = $line[0] ; $y = $line[1] ; $z = $line[2] ;
#      $xt=$x*$sidex[0]+$y*$sidey[0]+$z*$sidez[0];
#      $yt=$x*$sidex[1]+$y*$sidey[1]+$z*$sidez[1];
#      $zt=$x*$sidex[2]+$y*$sidey[2]+$z*$sidez[2];
#      $x=$latt*$xt; $y=$latt*$yt; $z=$latt*$zt;
#      printf MOV "%2s %18.13f %18.13f %18.13f \n",$type[$i],$x,$y,$z ;  
#    }
#    $n++ ;
#  }
