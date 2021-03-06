.. _tutorial:

Tutorial
========

Exploring basic rules
---------------------

Let's try exploring the `/agreements` endpoint:

.. include:: tutorial/agreements-listing-0.http
   :code:

Just invoking it reveals an empty set.

Agreement is transferred from the tender system by an automated process.


.. index:: Agreements

Creating agreement
------------------

Let's say that we have conducted tender and it has ``complete`` status. When the tender is completed, agreement (that has been created in the tender system) is transferred to the agreement system **automatically**.

*Brokers (eMalls) can't create agreements in the agreement system.*

Getting agreement
-----------------

Agreement in the tender system

.. include:: tutorial/example_agreement.http
   :code:

*Agreement id is the same in both tender and agreement system.*

Let's access the URL of the created object inside agreement system:

.. include:: tutorial/agreement-view.http
   :code:

Getting access
--------------

In order to get rights for future agreement editing, you need to use this view ``PATCH: /agreements/{id}/credentials?acc_token={tender_token}`` with the API key of the eMall (broker), where tender was generated.

In the ``PATCH: /agreements/{id}/credentials?acc_token={tender_token}``:

* ``id`` stands for agreement id,

* ``tender_token`` is tender's token (is used for agreement token generation).

Response will contain ``access.token`` for the agreement that can be used for further agreement modification.

.. include:: tutorial/agreement-credentials.http
   :code:

Let's view agreements.

.. include:: tutorial/agreements-listing-1.http
   :code:


We do see the internal `id` of a agreement (that can be used to construct full URL by prepending `http://api-sandbox.openprocurement.org/api/0/agreements/`) and its `dateModified` datestamp.


Modifying agreement
-------------------


**Essential agreement terms** can be modified by the submission of a new `change` object to the `Agreement.changes` container. `Change` can be one of this types :ref:`ChangeTaxRate`, :ref:`ChangeItemPriceVariation`, :ref:`ChangePartyWithdrawal` or :ref:`ChangeThirdParty`

All `changes` are processed by the endpoint `/agreement/{id}/changes`.

Submitting a change
~~~~~~~~~~~~~~~~~~~

Let's add new `change` to the agreement:

.. include:: tutorial/add-agreement-change.http
   :code:

Note that you should provide value in ``rationaleType`` field. This field is required.

You can view the `change`:

.. include:: tutorial/view-agreement-change.http
   :code:

`Change` can be modified while it is in the ``pending`` status:

.. include:: tutorial/patch-agreement-change.http
   :code:

Uploading change document
~~~~~~~~~~~~~~~~~~~~~~~~~

Document can be added only while `change` is in the ``pending`` status.

Document has to be added in two stages:

* you should upload document

.. include:: tutorial/add-agreement-change-document.http
   :code:

* you should set document properties ``"documentOf": "change"`` and ``"relatedItem": "{change.id}"`` in order to bind the uploaded document to the `change`:

.. include:: tutorial/set-document-of-change.http
   :code:

Updating agreement properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now you can update agreement properties which belong to the change.

.. include:: tutorial/add-agreement-change-modification.http
   :code:


Agreement preview
~~~~~~~~~~~~~~~~~

Also, while `change` is in the ``pending`` status, you can see agreement as `change` would be applied.
You need to use this view ``GET: /agreements/{id}/preview?acc_token={agreement_token}``.

.. include:: tutorial/agreement_preview.http
   :code:

As you can see, `value.amount` on `contracts` `unitPrices` are changed due `modification` is applied. So if this `modification` is what you need, you can apply `change`.

Applying the change
~~~~~~~~~~~~~~~~~~~

`Change` can be applied by switching to the ``active`` status.

In order to apply ``active`` status `dateSigned` field must be set.

After this `change` can't be modified anymore.

.. include:: tutorial/apply-agreement-change.http
   :code:

`dateSigned` field validation:

* for the first agreement `change` date should be after `agreement.dateSigned`;

* for all next `change` objects date should be after the previous `change.dateSigned`.

You can view all changes:

.. include:: tutorial/view-all-agreement-changes.http
   :code:

All changes are also listed on the agreement view.

.. include:: tutorial/view-agreement.http
   :code:

Uploading documentation
-----------------------

Procuring entity can upload PDF files into the created agreement. Uploading should
follow the `upload` rules.

.. include:: tutorial/upload-agreement-document.http
   :code:

`201 Created` response code and `Location` header confirm document creation.
We can additionally query the `documents` collection API endpoint to confirm the
action:

.. include:: tutorial/agreement-documents.http
   :code:

And again we can confirm that there are two documents uploaded.

.. include:: tutorial/upload-agreement-document-2.http
   :code:

In case we made an error, we can reupload the document over the older version:

.. include:: tutorial/upload-agreement-document-3.http
   :code:

And we can see that it is overriding the original version:

.. include:: tutorial/get-agreement-document-3.http
   :code:


.. index:: Enquiries, Question, Answer


Completing agreement
--------------------

Agreement can be completed by switching to ``terminated`` status.
Let's perform these actions in single request:

.. include:: tutorial/agreement-termination.http
   :code:

If agreement is unsuccessful reasons for termination ``terminationDetails`` should be specified.

Any future modification to the agreement are not allowed.
