<pre style='color:#a9b1d6;background-color:#1a1b26;'>
    &lt;pre style='color:#f2efe8;background-color:#1c1e22;'&gt;
    
    &lt;span style='color:#ffcc80;'&gt;│   │   ├── 
    linear.py&lt;/span&gt;&lt;/pre&gt;
    &lt;pre style='color:#a9b1d6;background-color:#1a1b26;'&gt;
    PLAY REWRTITE
    GOAL:
    I need you to automate AUTOMATIC TESTING for . Its T24, temenos banking 
    website. Release 21 , 26 - old and new browser.
    
    
    Env. is SYT [ closed off system to the net].
    We are the European Excelence Center, KBC owned. I am a Functiona Analyst 
    for local development if Banking apps. You will open the Website, enter 
    usrname pass. go to terminal // cmnd line, and run test
    cases [ JIRA - XRAY - format]. TESTING our stuff before handing it off to 
    UAT. Usually the thing playwright will have to do is COPY-PASTE in to 
    fields, presx F1-F12, click on a
    predetermined place, opennin enquiries, screenshots, REPORT writeup, basic 
    passing to agents. The test and problem right now. we are a closed off 
    systrem. with copilot free work
    license. I am making a case for AI automation. So Copilot Has structured 
    the test, and will have to be prompted to code u. You can send messages to 
    him but not get feedback, it will
    be done by me. We have, playwright + vscode. All of the beh rules will be 
    isntructed. Like name of FIELDS for test. Schemes will be provided for XML, 
    if u have to check output. You
    will have to make PMNTS and test VALIDATION routines, auto fill of fields, 
    max chars, behaviour as descried, Stress tesing, inputing adressof fake 
    client, testing flows, looking ath
    apps and tables for Products , versions, packages, starting stoppigng 
    services. Encoding to base 64 - decoding. MSG rerouting.
    
    
    &amp;gt; **Context:** You are an expert QA Automation Engineer writing 
    Playwright (TypeScript/JavaScript) scripts to automate testing for a Temenos 
    T24 banking environment (Release 21
    and Release 26). I will act as the Functional Analyst providing test cases 
    (in Jira/Xray format), field names, and XML schemas.
    &amp;gt;
    &amp;gt; **Architecture &amp;amp; Coding Standards:**
    &amp;gt; 1. **Page Object Model (POM):** Structure all code using POM. 
    Create separate classes for `LoginPage`, `TerminalCommandPage`, 
    `EnquiryPage`, and specific `ApplicationPages` (e.g.,
    PMNTS).
    &amp;gt; 2. **T24 Quirks:** T24 heavily uses IFRAMES. Ensure        all 
    locators handle frame traversal correctly (e.g., 
    `page.frameLocator('iframe[id=&amp;quot;...&amp;quot;]')`).
    &amp;gt; 3. **Keyboard Actions:** We will frequently use F-keys (F1-F12). 
    Create helper methods for `page.keyboard.press('F3')`, etc.
    &amp;gt; 4. **Resilience:** Use Playwright's built-in auto-waiting. Do not 
    use hard `page.waitForTimeout()` unless strictly necessary for T24 
    rendering quirks. Wait for specific network
    idle states or elements to be visible/enabled.
    &amp;gt; 5. **Screenshots &amp;amp; Reporting:** Integrate automatic 
    screenshots on test failure and at critical verification steps (Xray 
    compliance).
    &amp;gt; 6. **Data handling:** Create helper utilities for Base64 
    encoding/decoding and XML parsing.
    &amp;gt;
    &amp;gt; **First Task:**
    &amp;gt; Write the base Playwright configuration file 
    (`playwright.config.ts`) set up for a closed-network enterprise environment 
    (ignore external CDNs, allow self-signed certs). Then,
    write the `T24LoginPage` class with methods to input username, input 
    password, and submit, and a `TerminalPage` class with a method to enter a 
    command into the T24 command line and
    press Enter.
    
    
    ───────────────────────────────────────────────────────────
    &amp;gt; I literally installed it via our IT, all I know is we have it, its 
    a Script Json parser to Edge -&amp;gt; Website opens - u can tab to the 
only field and paste a command like . ENQ TXN.ENTRY
-&amp;gt; 4 new fields - 2 mandotory. Input FT id then Date in format 20261009 - 
it will open then[ or not and give a no such cust error] the Enquiry, u then 
Read screenshot it. Another,
that is the goal for now : 1. open T24 R21 SYT -&amp;gt; USRNAME FOR  U : 
JF68108A with password AIAI123456 -&amp;gt; COMMAND LINE : 
FT,UBB.OUT.EUR.PMNT.BR. NEW button or quick key. NEW SCREEEN. 40
FIELD page.  INPUT Payer - DEBIT.ACCT.NO from given selection, provided by us. 
Basically fake accts called FIrst Middle LAst. Screen AUTO refreshes since a 
AUTH NEW CONTENT RTN tied
to field will take the number and make sure u are a client , your sector, your 
acct info , the Payer acct info, currency. THen a Currency field- &amp;gt; this 
is end currency. as in the
currency the BENEFICIERY, aka CREDIT.ACCT.NO, A vostro acct will load 
automatically , input EITHER IN debit or credit ammt, not both. Ammont is based 
on the test. U then input
BENEF.NAME and all the fieds. that are mandatory. THEN U WILL TWST THE NEW 
fields or VAL rytn.  U WIILL CLICK VALIDATE, an error ,check or blocker may 
appear. SOME can be overwrtitten
thus a warning some are EB.ATOPPING  errors. Confirm and send -&amp;gt; new 
screen take FT ID created, relogin with new acct -&amp;gt; JF68108B AIAI123456 
-&amp;gt; cmnd line FT,UBB.OUT.EUR.PMNT.BR A [FT ID U COPPIED] -&amp;gt; A for 
Authorize,
S for search, I - input. ok NEW SCREEN WITH FT PMNT- no input screen. Confirm.

Screenshot.

cmnd t24 line -&amp;gt; TS, [with ,] -&amp;gt; new screen -&amp;gt; in the open 
field -&amp;gt; input service . [ALLIENCE.OUT, FT,CBPR.B.PMNT , PRINT OUT, 
UBB.MX.MT].

TS - services abnd bathes.

if u have ti start it  it will be go to field  - dropdown menu -&amp;gt; start 
-&amp;gt; CONFIRM. Services i now on.

UBB.H.TRANSFER.SWFT; MH8.SEPA . H.TRANSFER.TRGT ETC...

open the H table, confirm pmnt is there -&amp;gt; last table before XML  and 
account
ing are triggered.

XML is triggered or not if there is an error there.

screenshot + write/ remember or qhatever FT .

Start again DO OTHER TEST. this 2as an outgoing FT TRns.


OK SOMETIMES U WILL DO INCOMING
&lt;/pre&gt;
</pre>

