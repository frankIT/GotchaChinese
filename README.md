
About
=====
Basically a dumb SIP client which ring someone up repeatedly like the chinese water torture.  
It's been coded as a joke to annoy one of my mates that didn't want to give me back the money I've borrowed him for a dinner out.  
Well, I got the money back after 1 day (and several hundreds of rings), spending just about 3 euros in picked up calls :)


How it works
------------
The client executes an infinite loop making a call to the specified number and waits 6 seconds to hangup. That's just enought to make a single ring.  
It waits for a random number (from 60 to 180) of seconds between each loop/ring, so it's hard to pick up the call.  
If the call gets picked up 10 times, the loop interval get multiplied by 2, so 60 to 180 becomes 120 to 360.  
So the more rings the reciver is able to catch, the more harder becomes to pick them up.  
A counter keep track of how many times the random interval get increased, and the client keeps on increase the interval on every (10*counter) calls that got picked up.


How to use
----------
First of all you need a SIP account with any of the many providers around.  
Then you have to install the [sipsimple SDK](https://sipsimpleclient.org/) on your system. Rely on their official docs for that.  
You can than configure the credentials of your SIP account globally with the sip-settings tool.  
The script has been coded for a single use case without parametrization in mind, so to set the phone number you have to replace "victim_number" in the source file.  
Same thing if you wanna tweak timings and behaviour, you should manually change the vars in the source just before the loop statement.


Notes
-----
The client uses the [sipsimple SDK](https://sipsimpleclient.org/), and has been written for python 2.7
