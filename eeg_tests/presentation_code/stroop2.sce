scenario = "Choice";
scenario_type = trials; 
response_matching = simple_matching;
no_logfile = false;
active_buttons = 4;
button_codes = 1,2,3,4;
target_button_codes = 1,2,3,4;
#write_codes = true;
pulse_width = 10; 
#default_trial_type = all_correct_responses;
default_trial_type = first_response; 
#default_trial_type = fixed;
default_font_size = 24;
default_background_color = 0, 0, 0;
randomize_trials = true;   

#-------------------------------------------------------
#StroopÛè
#@@³ðL[µ
#  Î=1@@Ô=2@@Â=3@@©=4
#-------------------------------------------------------

begin;

picture {} default;

#TEMPLATE "nazo.tem" randomize


#ITI Setting
$i=1000;  #1000 

#Fix duration
$j=500;
#feedback duration

#font color
$white= "255, 255, 255";
$green= "0, 255, 0";
$red= "255, 0, 0";
$blue= "0, 128, 255";      
$yellow="255, 255, 0"; 


LOOP $k 2;

 trial{

	picture {
		text {
			font_size = 70;
         font_color = "$white";
			system_memory = true;
			caption = " ";};
		x = 0; y = 0; 
    };
   time='0';
   code= "iti" ;
   duration='$j';
   port_code = 0;

	picture {
		text {
			font_size = 70;
         font_color = "$white";
			system_memory = true;
			caption = "+";};
		x = 0; y = 0; 
    };
   time='$j';
   code= "fix" ;
   duration='$i';
   port_code = 100;

	picture {
		text {
			font_size = 80;
         font_color = "$green";
			system_memory = true;
			caption = "VERDE";};
		x = 0; y = 0; 
   };   
   time='$i+$j';
   code= "green" ;
   duration=response;
   port_code = 101;
   target_button= 1;
};


 trial{

	picture {
		text {
			font_size = 70;
         font_color = "$white";
			system_memory = true;
			caption = " ";};
		x = 0; y = 0; 
    };
   time='0';
   code= "iti" ;
   duration='$j';
   port_code = 0;

	picture {
		text {
			font_size = 70;
         font_color = "$white";
			system_memory = true;
			caption = "+";};
		x = 0; y = 0; 
    };
   time='$j';
   code= "fix" ;
   duration='$i';
   port_code = 200;

	picture {
		text {
			font_size = 80;
         font_color = "$red";
			system_memory = true;
			caption = "ROJO";};
		x = 0; y = 0; 
   };   
   time='$i+$j';
   code= "red" ;
   duration=response;
   port_code = 201;
   target_button= 2;
};

 trial{

	picture {
		text {
			font_size = 70;
         font_color = "$white";
			system_memory = true;
			caption = " ";};
		x = 0; y = 0; 
    };
   time='0';
   code= "iti" ;
   duration='$j';
   port_code = 0;

	picture {
		text {
			font_size = 70;
         font_color = "$white";
			system_memory = true;
			caption = "+";};
		x = 0; y = 0; 
    };
   time='$j';
   code= "fix" ;
   duration='$i';
   port_code = 100;

	picture {
		text {
			font_size = 80;
         font_color = "$blue";
			system_memory = true;
			caption = "VERDE";};
		x = 0; y = 0; 
   };   
   time='$i+$j';
   code= "green" ;
   duration=response;
   port_code = 101;
   target_button= 3;
};


 trial{

	picture {
		text {
			font_size = 70;
         font_color = "$white";
			system_memory = true;
			caption = " ";};
		x = 0; y = 0; 
    };
   time='0';
   code= "iti" ;
   duration='$j';
   port_code = 0;

	picture {
		text {
			font_size = 70;
         font_color = "$white";
			system_memory = true;
			caption = "+";};
		x = 0; y = 0; 
    };
   time='$j';
   code= "fix" ;
   duration='$i';
   port_code = 200;

	picture {
		text {
			font_size = 80;
         font_color = "$yellow";
			system_memory = true;
			caption = "ROJO";};
		x = 0; y = 0; 
   };   
   time='$i+$j';
   code= "red" ;
   duration=response;
   port_code = 201;
   target_button= 4;
};

#----------------

 trial{

	picture {
		text {
			font_size = 70;
         font_color = "$white";
			system_memory = true;
			caption = " ";};
		x = 0; y = 0; 
    };
   time='0';
   code= "iti" ;
   duration='$j';
   port_code = 0;

	picture {
		text {
			font_size = 70;
         font_color = "$white";
			system_memory = true;
			caption = "+";};
		x = 0; y = 0; 
    };
   time='$j';
   code= "fix" ;
   duration='$i';
   port_code = 100;

	picture {
		text {
			font_size = 80;
         font_color = "$green";
			system_memory = true;
			caption = "VERDE";};
		x = 0; y = 0; 
   };   
   time='$i+$j';
   code= "green" ;
   duration=response;
   port_code = 101;
   target_button= 1;
};


 trial{

	picture {
		text {
			font_size = 70;
         font_color = "$white";
			system_memory = true;
			caption = " ";};
		x = 0; y = 0; 
    };
   time='0';
   code= "iti" ;
   duration='$j';
   port_code = 0;

	picture {
		text {
			font_size = 70;
         font_color = "$white";
			system_memory = true;
			caption = "+";};
		x = 0; y = 0; 
    };
   time='$j';
   code= "fix" ;
   duration='$i';
   port_code = 200;

	picture {
		text {
			font_size = 80;
         font_color = "$red";
			system_memory = true;
			caption = "ROJO";};
		x = 0; y = 0; 
   };   
   time='$i+$j';
   code= "red" ;
   duration=response;
   port_code = 201;
   target_button= 2;
};

 trial{

	picture {
		text {
			font_size = 70;
         font_color = "$white";
			system_memory = true;
			caption = " ";};
		x = 0; y = 0; 
    };
   time='0';
   code= "iti" ;
   duration='$j';
   port_code = 0;

	picture {
		text {
			font_size = 70;
         font_color = "$white";
			system_memory = true;
			caption = "+";};
		x = 0; y = 0; 
    };
   time='$j';
   code= "fix" ;
   duration='$i';
   port_code = 100;

	picture {
		text {
			font_size = 80;
         font_color = "$blue";
			system_memory = true;
			caption = "VERDE";};
		x = 0; y = 0; 
   };   
   time='$i+$j';
   code= "green" ;
   duration=response;
   port_code = 101;
   target_button= 3;
};


 trial{

	picture {
		text {
			font_size = 70;
         font_color = "$white";
			system_memory = true;
			caption = " ";};
		x = 0; y = 0; 
    };
   time='0';
   code= "iti" ;
   duration='$j';
   port_code = 0;

	picture {
		text {
			font_size = 70;
         font_color = "$white";
			system_memory = true;
			caption = "+";};
		x = 0; y = 0; 
    };
   time='$j';
   code= "fix" ;
   duration='$i';
   port_code = 200;

	picture {
		text {
			font_size = 80;
         font_color = "$yellow";
			system_memory = true;
			caption = "ROJO";};
		x = 0; y = 0; 
   };   
   time='$i+$j';
   code= "red" ;
   duration=response;
   port_code = 201;
   target_button= 4;
};
  
#----------------

 trial{

	picture {
		text {
			font_size = 70;
         font_color = "$white";
			system_memory = true;
			caption = " ";};
		x = 0; y = 0; 
    };
   time='0';
   code= "iti" ;
   duration='$j';
   port_code = 0;

	picture {
		text {
			font_size = 70;
         font_color = "$white";
			system_memory = true;
			caption = "+";};
		x = 0; y = 0; 
    };
   time='$j';
   code= "fix" ;
   duration='$i';
   port_code = 100;

	picture {
		text {
			font_size = 80;
         font_color = "$green";
			system_memory = true;
			caption = "VERDE";};
		x = 0; y = 0; 
   };   
   time='$i+$j';
   code= "green" ;
   duration=response;
   port_code = 101;
   target_button= 1;
};


 trial{

	picture {
		text {
			font_size = 70;
         font_color = "$white";
			system_memory = true;
			caption = " ";};
		x = 0; y = 0; 
    };
   time='0';
   code= "iti" ;
   duration='$j';
   port_code = 0;

	picture {
		text {
			font_size = 70;
         font_color = "$white";
			system_memory = true;
			caption = "+";};
		x = 0; y = 0; 
    };
   time='$j';
   code= "fix" ;
   duration='$i';
   port_code = 200;

	picture {
		text {
			font_size = 80;
         font_color = "$red";
			system_memory = true;
			caption = "ROJO";};
		x = 0; y = 0; 
   };   
   time='$i+$j';
   code= "red" ;
   duration=response;
   port_code = 201;
   target_button= 2;
};

 trial{

	picture {
		text {
			font_size = 70;
         font_color = "$white";
			system_memory = true;
			caption = " ";};
		x = 0; y = 0; 
    };
   time='0';
   code= "iti" ;
   duration='$j';
   port_code = 0;

	picture {
		text {
			font_size = 70;
         font_color = "$white";
			system_memory = true;
			caption = "+";};
		x = 0; y = 0; 
    };
   time='$j';
   code= "fix" ;
   duration='$i';
   port_code = 100;

	picture {
		text {
			font_size = 80;
         font_color = "$blue";
			system_memory = true;
			caption = "VERDE";};
		x = 0; y = 0; 
   };   
   time='$i+$j';
   code= "green" ;
   duration=response;
   port_code = 101;
   target_button= 3;
};


 trial{

	picture {
		text {
			font_size = 70;
         font_color = "$white";
			system_memory = true;
			caption = " ";};
		x = 0; y = 0; 
    };
   time='0';
   code= "iti" ;
   duration='$j';
   port_code = 0;

	picture {
		text {
			font_size = 70;
         font_color = "$white";
			system_memory = true;
			caption = "+";};
		x = 0; y = 0; 
    };
   time='$j';
   code= "fix" ;
   duration='$i';
   port_code = 200;

	picture {
		text {
			font_size = 80;
         font_color = "$yellow";
			system_memory = true;
			caption = "ROJO";};
		x = 0; y = 0; 
   };   
   time='$i+$j';
   code= "red" ;
   duration=response;
   port_code = 201;
   target_button= 4;
};
  
ENDLOOP;