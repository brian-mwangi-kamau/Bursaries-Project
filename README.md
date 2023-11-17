## The NG-CDF Bursaries Program

The program herein is a digital system that could be used by the __National Government Constituencies Development Fund__(_NG-CDF_) in Kenya to facilitate the collection of applications and the disbursement of bursary funds.

Utilizing this digital system, students across primary, secondary, and tertiary institutions can efficiently submit their applications, eliminating the need for printed papers and thereby saving valuable time and resources.

__Note:__ *This particular system has been tailored for one constituency - Ndaragwa, in Nyandarua County*

The process of application involves the following:

### 1: Filling in the application with the following details:
   - The student's name
   - The name of their school
   - Their gender
   - Their school admission number
   - Their class, form, or year of study
   - Their constituency and location of residence
   - Their, or parent's phone number
   - Their, or parent's Identification number
   - And an optional email address where they can receive updates on the status of their application.

### 2: Submitting the application.

Upon submission, the application data will be saved in a database before being processed in step [3 below](#3-application-processing). This will ensure the efficient storage of application data, for future reference.

### 3: Application processing

The ID number provided in the application will queried against a secure database _provided by the **IEBC**_, which contains the names and Identification numbers of voters along with their constituency/s and location/s of residence.

Applications whose ID numbers and locations match with the data in the **IEBC** database will be marked as qualified, and will be automatically uploaded to Google Spreadsheets, accessible by the bursary administrator of that particular constituency.

On the other hand, applications whose ID numbers will either be found to be from a different location and constituency from what indicated on the application, or won't be found on the IEBC database, will be marked as disqualified, and will be sent to an email address operated by the constituency's bursary administrator. They can then use the phone number or email address provided in the application to contact the applicant for manual verification of eligibility.

### 4: Bursary funds disbursement

The office will then process the applications, by downloading the data in the spreadsheets into their local environment, for future reference.



## Advantages of this digital system over the traditional application method:

__1:__ This method, if used, would save time and use of resources like application forms for applicants when applying.

__2:__ It would also ease the process of reviewing, sorting applications and disbursing funds by the NG-CDF staff. Currently, applications are reviewed manually, a process which takes time, and isn't very effective, since some forms get misplaced leading to some applicants missing out.

__3:__ This method would also ensure the credibility of the process, by making sure that beneficiaries of bursary funds are people from their respective constituencies.

__4__: This system offers a secure repository for application data, ensuring the safe storage of information. In contrast to traditional methods susceptible to misplacement, flooding, or fire damage, our digital solution guarantees the integrity and accessibility of vital application records.

## Conclusion:
#### For this system to be applicable, there would be a need to develop slightly different versions of the program for each of the 290 constituencies in Kenya.

#### Upon completion of this project I was happy with the achievement, and look forward to developing more software solutions to solve real-world problems in the future.

## Important links:
The __web application__ is accessible through the following __[URL](https://bursaries.pythonanywhere.com)__ .

*__Disclaimer__: This web application is neither owned, nor operated by the government of Kenya. In any case you wish to submit an application for testing purposes, do so while using dummy data.*