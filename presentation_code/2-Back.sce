#-- scenario file --#

response_matching = simple_matching;
default_font_size = 48;
active_buttons = 1;
button_codes = 1;
stimulus_properties = letter, string, is_target, string;
event_code_delimiter = ",";

begin;

array {
   text { caption = "A"; description = "A"; } A;
   text { caption = "B"; description = "B"; };
   text { caption = "C"; description = "C"; };
   text { caption = "D"; description = "D"; };
   text { caption = "E"; description = "E"; };
} letters;

trial {
   trial_duration = 2000;
   all_responses = false;

   stimulus_event {
      picture {
         text A;
         x = 0; y = 0;
      } pic;
      time = 0;
      duration = 500;
   } event1;
} main_trial;

begin_pcl;

sub
   int random_exclude( int first, int last, int exclude )
begin
   int rval = random( first, last - 1 );
   if (rval >= exclude) then
      rval = rval + 1
   end;
   return rval
end;

int stimulus_count = 100;
array<int> is_target[stimulus_count];
loop int i = 1 until i > stimulus_count / 4 begin
   is_target[i] = 1;
   i = i + 1
end;
is_target.shuffle();
loop until is_target[1] == 0 && is_target[2] == 0 begin
   is_target.shuffle()
   end;

loop
   int i = 1;
   int last = 0;
   int two_back = 0;
until
   i > stimulus_count
begin
   int index;
   string target_string = ",no";
   if (is_target[i] == 1) then
      index = two_back;
      target_string = ",yes"
   else
      index = random_exclude( 1, letters.count(), two_back )
   end;
   pic.set_part( 1, letters[index] );
   event1.set_event_code( letters[index].description() + target_string );
   main_trial.present();
   two_back = last;
   last = index;
   i = i + 1
   end