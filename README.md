# 5. VoP Use Cases

## Business Requirement

The VoP JIRA ticket requires changes to existing functionality, as well as new development in T24, in order to meet the defined UBB business and legal requirements.

The proposed architecture requires T24 to authenticate and communicate with an external node handled by Borica. T24 sends the Verification of Payee request, receives the corresponding response, processes it, and presents the result to the UBB employee in an approved and user-readable format.

The response received from the external service is a string of approximately 1,200 characters. The beginning of the response contains the result of the beneficiary verification, which is interpreted as one of the following statuses:

* **MTCH** – Match
* **CMTC** – Close Match
* **NMTC** – No Match
* **TOUT** – Timeout

According to the documentation provided by UBB, part of the processing must differentiate between customers based on their sector:

* **ЧЛ** – Individual customers
* **ЮЛ** – Corporate customers

The current scope of the change covers **SEPA payment flows**.

Specific checks are required on the beneficiary side. These checks must be linked both to the VoP response and to the outgoing payment message in order to ensure consistency between the beneficiary information verified through VoP and the beneficiary information ultimately used in the outgoing payment.

The same principle must be applied consistently across all outgoing payment applications covered by the JIRA ticket.

The architecture provided by UBB also requires the response time of the external service to be measured and controlled. Response-time handling, including timeout processing, must be performed automatically and without user intervention.

Once the response is received and processed, the employee must be presented with the corresponding VoP result. Different business scenarios must be supported depending on the response received, in accordance with the scenarios defined and approved by UBB.

The implementation is planned in three phases:

* **Phase 1** – Creation of the new tables and applications required for the VoP functionality.
* **Phase 2** – Implementation for outgoing Cross-Border SEPA and Domestic SEPA payment flows.
* **Phase 3** – Implementation of the applicable internal and budgetary payment requirements.

For Phases 2 and 3, new DSFs must also be designed and implemented in T24 in accordance with the applicable business and legal requirements.

All new VoP functionality must be restricted to the applicable payment flows and must not affect existing T24 functionality outside the defined scope.

## Solution

To fulfil the requirements defined in the VoP JIRA ticket, changes are introduced to the affected UPM applications, together with additional functionality in the FT application.

The overall solution includes:

* changes to the relevant **UPM applications**;
* four new fields in the **FT application**;
* approximately three to four new routines;
* three new applications;
* three new DSFs.

For the handling of incoming and outgoing VoP messages, two new applications are to be created:

* **UPM HO** – for Head Office processing;
* **UPM BR** – for Branch processing.

In addition, a dedicated history table is required to store the received VoP responses. Each stored response must be uniquely linked to both the outgoing FT transaction and the corresponding **VOP.ID**, allowing the original VoP request and payment transaction to be traced.

The VoP process starts with the beneficiary information provided by the customer. The customer provides the UBB employee with the beneficiary name and beneficiary account / IBAN. The employee must enter the beneficiary name using the exact spelling provided by the customer and verify the entered information before submitting the VoP request.

Once the information is confirmed, the application sends the request through T24 to an external Java node. The Java node acts as the central communication relay. The request is then forwarded through the external infrastructure to the beneficiary bank. The beneficiary bank performs the verification and returns its response through the same communication path back to T24.

The communication flow is therefore:

**T24 → External Java Node → Borica → Beneficiary Bank**

The response is returned through the same path in the opposite direction.

As the complete returned message can exceed 1,200 characters, the raw technical response is not presented directly to the employee. Instead, the response is post-processed in T24 and converted into a concise, employee-readable result.

The interpreted result is made available through the **RESPONSE.VOP** field.

The supported result values are:

* **MTCH** – Match;
* **CMTC** – Close Match;
* **NMTC** – No Match;
* **TOUT** – Timeout.

This ensures that only the information relevant to the employee's decision is presented, without exposing unnecessary technical details contained in the full external response.

Based on the response received, the user is presented with the corresponding UBB-defined scenario. The exact warning, information message, and permitted user action depend on whether the result is Match, Close Match, No Match, or Timeout.

Once the employee has reviewed the VoP result and made the appropriate decision, the corresponding enquiry opens the relevant FT application.

Information already provided during the VoP process is automatically populated into the FT transaction where applicable. This avoids unnecessary repeated data entry by the employee and ensures that the beneficiary information used in the payment remains consistent with the information previously submitted for VoP verification.

Additional validation logic is introduced as part of the solution.

A new ANC routine will perform checks related to **VOP.ID**. The purpose of this validation is to ensure that the FT transaction is correctly linked to the applicable VoP request and response.

A new validation routine, **VOP.CORP**, will apply the required VoP controls for the relevant corporate customer cases.

A further validation routine will be linked to **VOP.BEN.NAME**. Its purpose is to ensure that the beneficiary name used in the outgoing payment remains consistent with the beneficiary name previously submitted for VoP verification.

The required validations and corresponding errors therefore include:

* **VOP.CORP** – validation of the applicable corporate customer VoP requirements;
* **VOP.ID** – validation of the relationship between the outgoing transaction and the corresponding VoP request;
* **VOP.BEN.NAME** – validation of the beneficiary name against the information used during the VoP verification.

The new rules and validations apply only to the relevant **SEPA payment flows**. They must be implemented with appropriate applicability checks so that existing T24 routines, validations, and payment processing remain unchanged for payment flows outside the VoP scope.
