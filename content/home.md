title: TeamKiwi
tags: interesting
owner: admin

#Members
* Jacob Stinson *(Team Leader ABC)* - [Email](stinsonj2@mymail.nku.edu)
     * Always Be Coding (and/or Communicating)
* Garrett Foister - [Email](foisterg1@mymail.nku.edu)
* Nick Peace - [Email](peacen1@mymail.nku.edu)
* Ryan Massey - [Email](masseyr2@mymail.nku.edu)
* Diana Coronado - [Email](coronadod1@mymail.nku.edu)

###Rules
* No surprises.
* Don’t show your emotions to your colleagues
* Don’t contact your boss’ boss directly
* Don’t give that which is holy to the dogs (Matt 7:6)
* People lie; write and confirm.
* Be serious about your and other’s work. No joke in your writings 
when you submit to others.

##Features
###Jacob Stinson
* API: use page as template (saveas)
* Example: SERVER/saveas/page_name/new_page_name 
* Unit test: 
    * New page should not have the same name as old page
    * New page should contain the same markdown as old page
* Demonstration1: ngrok/saveas/kiwi/new_kiwi
    * Description:
         * Click "save as" when editing
         * Enter a name for the copied page
         * Click Save
###Nick Peace
* API: User creation
* Example: POST to SERVER/register/
* Unit test: 
    * New user should have new unique name
    * New user should be able to log in using /login/
* Demonstration1: ngrok/register/
    * Description:
         * Click 'register' at the top of page
         * Enter a new username and password
         * Submit form and log in as new user
###Diana Coronado
* API: image upload
* Example: SERVER/picture/page/url
* Unit test: 
    * Image should be included in wiki page
    * Image directory should exist and contain the image file
* Demonstration1: ngrok/picture/kiwi/image.png
    * Description:
         * Click "upload picture"
         * enter the desired image URL
         * Click Save
###Ryan Massey
* API: User profile page
* Example: SERVER/user/username
* Unit test: 
    * User page should be unique to the user
    * User page should not be editable by other users
* Demonstration1: ngrok/user/stinsonj2
    * Description:
         * Login to wiki
         * Click on "profile"
         * View or edit profile page
###Garrett Foister
* API: Save page as markdown / PDF
* Example: SERVER/export/type/page
* Unit test: 
    * page should exist
    * page should download in the correct file format to user's system
* Demonstration1: ngrok/export/pdf/kiwi
    * Description:
         * Go to any wiki page
         * Click "export"
         * Select file type and submit
##Schedule:
* **Meetings:**
      - Two remote meetings per week via Discord on Wednesday and Thursday evenings. If an in person meeting is needed, it will occur on a Thursday. 

* **A Stage**
      - Deadline Date: October 10th

      - Milestones:

           - Create GitHub repository and ensure all members have access-- COMPLETED

           - All Team Members successfully clone Github Repo with project contents and installed the appropriate tools. Complete by 9/26.

           - Complete Test Case Generation. Complete by 10/1.

           - Complete DocTest Cases. Complete by 10/3.

      - Progress (individual): 
           Write your first name next to the item when complete
           - Repo cloned
           - Tools installed
           - 

      - Progress (group): Team leader will sign off on items as they are completed
           - Test case generation
           - Complete DocTest Cases
           - 

* **B Stage**
      - Deadline Date: October 29th
      - **Task assignments:**
           - Part 1 - Plan, Rules, and Retrospect 
                - Jacob Stinson

           - Part 2 - Wiki Software Design
	        - 2.1 - Diana
	        - 2.2 - Jacob
	        - 2.3 
		     * 1 - Ryan
		     * 2 - Nick
		     * 3 - Garrett
		
      - Part 3 -  Feature proposals

        - Save page as (copy page as new name) - Jacob
		- Export as HTML/Markdown file - Garrett
		- user creation - Nick
		- user profile page - Ryan
		- upload pictures - Diana

     - Schedule
          * Complete needed stage B documentation - October 29th
          * Begin research and gathering tools needed for feature implementation - November 1st
          * First sprint for feature implementation begins - November 2nd
          * First sprint review - November 15th
          * Final sprint and testing begins - November 16th
          * Final sprint review - November 22nd

      
* **C Stage**
      - Deadline Date: TBD
           - Details to be added soon

### Relevant Links
* [Github](https://github.com/jrstinson/TeamKiwi)
* [JetBrains](https://account.jetbrains.com/licenses) - for PyCharm
* [Mythical Man Month](https://nku.instructure.com/courses/20805/modules/items/760933)
